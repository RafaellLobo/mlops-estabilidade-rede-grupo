"""Ingestão, divisão e validação dos dados de estabilidade de rede.

Comandos:
    python -m mlops_demo.data base      # baixa/verifica a fonte e gera treino/holdout
    python -m mlops_demo.data preparar  # combina base + lotes em data/processed/
    python -m mlops_demo.data validar   # valida todos os CSVs de data/raw/
"""

import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from mlops_demo import config

SEMENTE_DADOS = 7
N_TREINO_BASE = 6000
N_HOLDOUT_BASE = 2000
N_RESERVA_BASE = 2000
COLUNA_ROTULO_ORIGINAL = "stabf"
COLUNA_SCORE_ORIGINAL = "stab"


def baixar_fonte_uci(destino: Path = config.FONTE_UCI) -> Path:
    """Baixa o CSV oficial da UCI, preservando os bytes para conferência do SHA-256."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    zip_destino = destino.parent / "electrical-grid-stability-uci.zip"
    requisicao = urllib.request.Request(
        config.URL_FONTE_UCI,
        headers={"User-Agent": "mlops-estabilidade-rede-grupo/1.0"},
    )
    with urllib.request.urlopen(requisicao, timeout=60) as resposta:
        zip_destino.write_bytes(resposta.read())

    with zipfile.ZipFile(zip_destino) as arquivo_zip:
        candidatos = [
            nome for nome in arquivo_zip.namelist()
            if Path(nome).name == destino.name
        ]
        if len(candidatos) != 1:
            raise ValueError(
                "O pacote UCI deve conter exatamente um arquivo "
                f"{destino.name}; encontrados: {candidatos}"
            )
        destino.write_bytes(arquivo_zip.read(candidatos[0]))
    zip_destino.unlink(missing_ok=True)
    return destino


def verificar_hash_fonte(caminho: Path = config.FONTE_UCI) -> str:
    """Confere o SHA-256 do CSV original, antes de qualquer transformação."""
    if not caminho.is_file():
        raise FileNotFoundError(f"Fonte UCI não encontrada: {caminho}")
    digest = hashlib.sha256(caminho.read_bytes()).hexdigest()
    if digest != config.SHA256_FONTE_UCI:
        raise ValueError(
            "SHA-256 da fonte UCI divergente: "
            f"esperado {config.SHA256_FONTE_UCI}, obtido {digest}"
        )
    return digest


def carregar_dataset_completo() -> pd.DataFrame:
    """Lê a fonte oficial e retorna 12 atributos + alvo instavel (0/1)."""
    if not config.FONTE_UCI.exists():
        baixar_fonte_uci()
    verificar_hash_fonte()

    original = pd.read_csv(config.FONTE_UCI)
    if list(original.columns) != config.COLUNAS_ORIGINAIS:
        raise ValueError(
            "Colunas inesperadas na fonte UCI: "
            f"{list(original.columns)}"
        )

    rotulos = original[COLUNA_ROTULO_ORIGINAL].map(
        {"stable": config.CLASSE_ESTAVEL, "unstable": config.CLASSE_INSTAVEL}
    )
    if rotulos.isna().any():
        raise ValueError("A fonte contém rótulos stabf diferentes de stable/unstable.")

    score = pd.to_numeric(original[COLUNA_SCORE_ORIGINAL], errors="coerce")
    sinal_inconsistente = (
        ((score > 0) & (rotulos != config.CLASSE_INSTAVEL))
        | ((score < 0) & (rotulos != config.CLASSE_ESTAVEL))
    )
    if sinal_inconsistente.any():
        raise ValueError(
            f"{int(sinal_inconsistente.sum())} rótulos discordam do sinal de stab."
        )

    dados = original[config.FEATURES].apply(pd.to_numeric, errors="coerce")
    dados[config.ALVO] = rotulos.astype("int64")
    problemas = validar_dataframe(dados)
    if problemas:
        raise ValueError("Fonte UCI inválida: " + "; ".join(problemas))
    return dados


def dividir_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Gera treino (6.000), holdout (2.000) e reserva (2.000), estratificados."""
    df = carregar_dataset_completo()

    # A primeira saída é o restante (4.000); a segunda, treino (6.000).
    resto, base_treino = train_test_split(
        df,
        test_size=N_TREINO_BASE,
        stratify=df[config.ALVO],
        random_state=SEMENTE_DADOS,
    )
    # Do restante, separar holdout fixo (2.000) e reserva (2.000).
    reserva, base_holdout = train_test_split(
        resto,
        test_size=N_HOLDOUT_BASE,
        stratify=resto[config.ALVO],
        random_state=SEMENTE_DADOS,
    )

    conjuntos = [base_treino, base_holdout, reserva]
    if [len(parte) for parte in conjuntos] != [
        N_TREINO_BASE, N_HOLDOUT_BASE, N_RESERVA_BASE
    ]:
        raise AssertionError("Tamanhos das partições diferem do protocolo definido.")

    chaves = [
        set(map(tuple, parte[config.FEATURES].to_numpy()))
        for parte in conjuntos
    ]
    if not (
        chaves[0].isdisjoint(chaves[1])
        and chaves[0].isdisjoint(chaves[2])
        and chaves[1].isdisjoint(chaves[2])
    ):
        raise AssertionError("Há registros repetidos entre treino, holdout e reserva.")

    return tuple(
        parte.reset_index(drop=True).copy()
        for parte in conjuntos
    )


def criar_base() -> None:
    """Gera os CSVs de treino e holdout; a reserva fica disponível para lotes."""
    if not config.FONTE_UCI.exists():
        baixar_fonte_uci()
    digest = verificar_hash_fonte()
    base_treino, base_holdout, reserva = dividir_dataset()

    config.DADOS_BRUTOS.mkdir(parents=True, exist_ok=True)
    config.DADOS_LOTES.mkdir(parents=True, exist_ok=True)
    base_treino.to_csv(config.BASE_TREINO, index=False)
    base_holdout.to_csv(config.BASE_HOLDOUT, index=False)

    print(f"SHA-256 UCI: {digest}")
    print(
        f"base_treino: {len(base_treino)} | "
        f"base_holdout: {len(base_holdout)} | reserva: {len(reserva)}"
    )
    print("A reserva é mantida em memória e será usada apenas para gerar lotes.")


def aplicar_drift(df: pd.DataFrame, fator: float) -> pd.DataFrame:
    """Aplica uma transformação multiplicativa aos atributos, preservando o alvo."""
    saida = df.copy()
    for coluna in config.FEATURES:
        saida[coluna] = saida[coluna] * fator
    return saida


def gerar_lote(nome: str, n: int = 120, fator_drift: float = 1.0, semente: int = 1) -> str:
    """Gera lote a partir da reserva, sem reutilizar linhas em lotes anteriores."""
    _, _, reserva = dividir_dataset()
    usados = set()
    for caminho_existente in listar_lotes():
        lote_existente = pd.read_csv(caminho_existente)
        usados.update(map(tuple, lote_existente[config.FEATURES].to_numpy()))

    disponiveis = reserva[
        ~reserva[config.FEATURES].apply(tuple, axis=1).isin(usados)
    ]
    if disponiveis.empty:
        raise ValueError("A reserva já foi consumida; não há registros disponíveis.")
    lote = disponiveis.sample(
        n=min(n, len(disponiveis)), random_state=semente
    ).reset_index(drop=True)
    if fator_drift != 1.0:
        lote = aplicar_drift(lote, fator_drift)
    problemas = validar_dataframe(lote)
    if problemas:
        raise ValueError(
            "O lote gerado viola o contrato físico: " + "; ".join(problemas)
        )
    config.DADOS_LOTES.mkdir(parents=True, exist_ok=True)
    caminho = config.DADOS_LOTES / f"{nome}.csv"
    if caminho.exists():
        raise FileExistsError(f"O lote {nome} já existe; não será sobrescrito.")
    lote.to_csv(caminho, index=False)
    return str(caminho)


def validar_dataframe(df: pd.DataFrame) -> list[str]:
    """Valida ordem, tipos, nulos, finitude, rótulos e regras físicas do domínio."""
    problemas = []
    esperadas = [*config.FEATURES, config.ALVO]
    if list(df.columns) != esperadas:
        faltando = sorted(set(esperadas) - set(df.columns))
        extras = sorted(set(df.columns) - set(esperadas))
        return [
            "esquema diferente do esperado "
            f"(faltando={faltando}, extras={extras}, ordem={list(df.columns)})"
        ]

    nulos = int(df.isna().sum().sum())
    if nulos:
        problemas.append(f"{nulos} valores nulos")

    numericos = df[esperadas].apply(pd.to_numeric, errors="coerce")
    if numericos.isna().sum().sum() > nulos:
        problemas.append("valores não numéricos")
    if not np.isfinite(numericos.to_numpy(dtype=float)).all():
        problemas.append("valores infinitos ou não finitos")

    if not df[config.ALVO].isin([config.CLASSE_ESTAVEL, config.CLASSE_INSTAVEL]).all():
        problemas.append("alvo com valores fora de {0, 1}")

    for coluna, (minimo, maximo) in config.FAIXAS_FEATURES.items():
        if coluna not in df:
            continue
        valores = pd.to_numeric(df[coluna], errors="coerce")
        if valores.notna().any() and (
            (valores < minimo).any() or (valores > maximo).any()
        ):
            problemas.append(
                f"{coluna} fora da faixa física [{minimo}, {maximo}]"
            )

    if all(coluna in df for coluna in config.COLUNAS_POTENCIA):
        potencias = df[config.COLUNAS_POTENCIA].apply(
            pd.to_numeric, errors="coerce"
        )
        if potencias.notna().all().all():
            desequilibrio = (
                potencias["p1"] - potencias[["p2", "p3", "p4"]].sum(axis=1).abs()
            ).abs()
            if (desequilibrio > config.TOLERANCIA_BALANCO_POTENCIA).any():
                problemas.append("balanço de potência inválido: p1 != abs(p2 + p3 + p4)")

    return problemas


def listar_lotes() -> list[Path]:
    """Retorna os CSVs de lotes novos em ordem alfabética."""
    if not config.DADOS_LOTES.exists():
        return []
    return sorted(config.DADOS_LOTES.glob("*.csv"))


def preparar() -> None:
    """Combina treino e avaliação; metade de cada lote fica fora do treino."""
    treino = [pd.read_csv(config.BASE_TREINO)]
    avaliacao = [pd.read_csv(config.BASE_HOLDOUT)]
    for caminho in listar_lotes():
        lote = pd.read_csv(caminho)
        problemas = validar_dataframe(lote)
        if problemas:
            raise ValueError(f"{caminho.name}: {'; '.join(problemas)}")
        metade_treino, metade_aval = train_test_split(
            lote,
            test_size=0.5,
            stratify=lote[config.ALVO],
            random_state=SEMENTE_DADOS,
        )
        treino.append(metade_treino)
        avaliacao.append(metade_aval)
    config.DADOS_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    pd.concat(treino, ignore_index=True).to_csv(config.TREINO_PROCESSADO, index=False)
    pd.concat(avaliacao, ignore_index=True).to_csv(
        config.AVALIACAO_PROCESSADA, index=False
    )
    print(f"lotes usados: {len(listar_lotes())}")
    print(
        f"treino: {sum(len(t) for t in treino)} linhas | "
        f"avaliação: {sum(len(a) for a in avaliacao)} linhas"
    )


def validar_tudo() -> int:
    """Valida todos os CSVs de data/raw/; 0 = todos válidos."""
    arquivos = [config.BASE_TREINO, config.BASE_HOLDOUT, *listar_lotes()]
    codigo = 0
    for caminho in arquivos:
        if not caminho.is_file():
            print(f"{caminho.name}: FALHOU: arquivo ausente")
            codigo = 1
            continue
        problemas = validar_dataframe(pd.read_csv(caminho))
        status = "OK" if not problemas else "FALHOU: " + "; ".join(problemas)
        print(f"{caminho.name}: {status}")
        codigo |= 1 if problemas else 0
    return codigo


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "base":
        criar_base()
    elif comando == "preparar":
        preparar()
    elif comando == "validar":
        sys.exit(validar_tudo())
    else:
        print(__doc__)
        sys.exit(2)
