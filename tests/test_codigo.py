"""Testes de código: funções e pipeline se comportam como o contrato diz."""

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from mlops_demo import config
from mlops_demo.evaluate import calcular_metricas
from mlops_demo.features import construir_classificador, construir_pipeline, separar_xy
from mlops_demo.gate import decidir
from mlops_demo.selecao import escolher

pytestmark = pytest.mark.codigo


def test_separar_xy_devolve_12_atributos_e_alvo(base_treino):
    X, y = separar_xy(base_treino)
    assert X.shape == (len(base_treino), 12)
    assert len(y) == len(base_treino)


def test_separar_xy_impoe_a_ordem_das_colunas(base_treino):
    embaralhado = base_treino[list(reversed(base_treino.columns))]
    X, _ = separar_xy(embaralhado)
    assert list(X.columns) == config.FEATURES


def test_separar_xy_falha_quando_falta_coluna(base_treino):
    sem_coluna = base_treino.drop(columns=["tau1"])
    with pytest.raises(ValueError, match="Colunas ausentes"):
        separar_xy(sem_coluna)


def test_separar_xy_nao_altera_o_dataframe_original(base_treino):
    antes = base_treino.copy()
    separar_xy(base_treino)
    pd.testing.assert_frame_equal(base_treino, antes)


def test_separar_xy_nunca_usa_stab_nem_stabf_como_entrada(base_treino):
    """Novo (Etapa 3): `stab` determina o rótulo; se estiver no CSV, não pode virar atributo."""
    com_vazamento = base_treino.assign(stab=0.01, stabf="unstable")
    X, _ = separar_xy(com_vazamento)
    assert "stab" not in X.columns and "stabf" not in X.columns
    assert list(X.columns) == config.FEATURES


def test_pipeline_tem_padronizacao_e_classificador(params):
    pipeline = construir_pipeline(params)
    assert isinstance(pipeline, Pipeline)
    assert [nome for nome, _ in pipeline.steps] == ["padronizar", "classificador"]


def test_tipo_de_modelo_desconhecido_falha_com_mensagem_clara():
    with pytest.raises(ValueError, match="Tipo de modelo desconhecido"):
        construir_classificador({"tipo": "inexistente"}, 42)


def test_metricas_usam_a_classe_instavel_como_positiva():
    # modelo que chuta tudo como instável (1): recall 1.0 e precisão = proporção real de instáveis
    y_real = [1, 1, 0, 0]
    metricas = calcular_metricas(y_real, [1, 1, 1, 1])
    assert config.CLASSE_INSTAVEL == 1
    assert metricas["recall_instavel"] == 1.0
    assert metricas["precisao_instavel"] == pytest.approx(0.5)


# --- seleção interna: o critério declarado é aplicado como escrito ---------------------------


def _resultado(ordem, recall, precisao):
    return {
        "ordem": ordem,
        "candidato": {"tipo": f"c{ordem}"},
        "metricas": {"recall_instavel": recall, "precisao_instavel": precisao},
    }


def test_selecao_ignora_candidato_com_precisao_abaixo_do_minimo():
    vencedor = escolher([_resultado(1, 0.99, 0.80), _resultado(2, 0.93, 0.91)])
    assert vencedor["ordem"] == 2


def test_selecao_desempata_pela_precisao_e_depois_pela_ordem():
    assert escolher([_resultado(1, 0.95, 0.91), _resultado(2, 0.95, 0.93)])["ordem"] == 2
    assert escolher([_resultado(1, 0.95, 0.93), _resultado(2, 0.95, 0.93)])["ordem"] == 1


def test_selecao_sem_candidato_elegivel_devolve_none():
    assert escolher([_resultado(1, 0.99, 0.50)]) is None


# --- o próprio portão de qualidade precisa ser testado ---------------------------------------


def _metricas(recall, precisao):
    return {"recall_instavel": recall, "precisao_instavel": precisao, "n_amostras": 100}


def test_gate_aprova_candidato_melhor_e_dentro_dos_limiares():
    assert decidir(_metricas(0.97, 0.95), _metricas(0.95, 0.95))["aprovado"]


def test_gate_reprova_recall_abaixo_do_limiar():
    assert not decidir(_metricas(0.85, 0.99), _metricas(0.80, 0.99))["aprovado"]


def test_gate_reprova_precisao_abaixo_do_limiar():
    # recall perfeito não compensa uma precisão ruim
    assert not decidir(_metricas(1.0, 0.70), _metricas(0.95, 0.95))["aprovado"]


def test_gate_reprova_candidato_pior_que_o_campeao():
    assert not decidir(_metricas(0.93, 0.95), _metricas(0.97, 0.95))["aprovado"]
