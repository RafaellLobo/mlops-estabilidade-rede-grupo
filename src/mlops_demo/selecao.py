"""Seleção interna do modelo (Etapa 3), sem usar o holdout.

Uso:
    python -m mlops_demo.selecao      # avalia os candidatos do params.yaml e grava o relatório

Protocolo (docs/PLANEJAMENTO.md, seção 4): split estratificado 80/20 SOMENTE da base de treino,
com a semente declarada em params.yaml. Critério: maior recall da classe instável entre os
candidatos com precisão >= PRECISAO_MINIMA; desempate pela precisão e depois pela ordem
declarada. O resultado registra todos os candidatos, inclusive os que falharam.
"""

import json
import platform

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split

from mlops_demo import config
from mlops_demo.evaluate import calcular_metricas
from mlops_demo.features import construir_pipeline, separar_xy

RELATORIO_SELECAO = config.RAIZ / "docs" / "selecao_modelo_etapa3.json"


def escolher(resultados: list[dict]) -> dict | None:
    """Aplica o critério declarado. Devolve o vencedor ou None se nenhum cumpre a precisão."""
    elegiveis = [
        r for r in resultados if r["metricas"]["precisao_instavel"] >= config.PRECISAO_MINIMA
    ]
    if not elegiveis:
        return None
    return sorted(
        elegiveis,
        key=lambda r: (
            -r["metricas"]["recall_instavel"],
            -r["metricas"]["precisao_instavel"],
            r["ordem"],
        ),
    )[0]


def executar() -> dict:
    params = config.carregar_params()
    selecao = params["selecao"]
    base = pd.read_csv(config.BASE_TREINO)
    treino, validacao = train_test_split(
        base,
        test_size=selecao["proporcao_validacao"],
        stratify=base[config.ALVO],
        random_state=selecao["semente"],
    )
    X_tr, y_tr = separar_xy(treino)
    X_va, y_va = separar_xy(validacao)

    resultados = []
    for ordem, candidato in enumerate(selecao["candidatos"], start=1):
        modelo = construir_pipeline(params, candidato).fit(X_tr, y_tr)
        metricas = calcular_metricas(y_va, modelo.predict(X_va))
        resultados.append({"ordem": ordem, "candidato": candidato, "metricas": metricas})
        print(f"{ordem}. {candidato['tipo']}: {json.dumps(metricas)}")

    vencedor = escolher(resultados)
    relatorio = {
        "protocolo": "split interno estratificado da base de treino; holdout não utilizado",
        "n_treino_interno": int(len(treino)),
        "n_validacao_interna": int(len(validacao)),
        "semente": selecao["semente"],
        "criterio": (
            "maior recall_instavel entre candidatos com precisao_instavel >= "
            f"{config.PRECISAO_MINIMA}; desempate por precisão e pela ordem declarada"
        ),
        "candidatos": resultados,
        "vencedor": vencedor,
        "cumpre_recall_minimo": bool(
            vencedor and vencedor["metricas"]["recall_instavel"] >= config.RECALL_MINIMO
        ),
        "ambiente": {
            "python": platform.python_version(),
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
        },
    }
    RELATORIO_SELECAO.parent.mkdir(parents=True, exist_ok=True)
    with open(RELATORIO_SELECAO, "w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
    print("vencedor:", vencedor["candidato"]["tipo"] if vencedor else "nenhum")
    return relatorio


if __name__ == "__main__":
    executar()
