"""Testes de modelo: limiares, baseline e comportamento (ML Test Score, Breck et al., 2017)."""

import json

import numpy as np
import pytest
from sklearn.dummy import DummyClassifier

from mlops_demo import config
from mlops_demo.evaluate import avaliar, calcular_metricas
from mlops_demo.features import separar_xy
from mlops_demo.train import treinar

pytestmark = pytest.mark.modelo


def test_campeao_versionado_foi_certificado_pelo_portao():
    """O metrics.json do campeão registra o que o portão mediu ao aprová-lo e cumpre o contrato."""
    with open(config.METRICAS_CAMPEAO, encoding="utf-8") as arquivo:
        declaradas = json.load(arquivo)
    assert declaradas["recall_instavel"] >= config.RECALL_MINIMO, declaradas
    assert declaradas["precisao_instavel"] >= config.PRECISAO_MINIMA, declaradas


def test_campeao_versionado_nao_colapsou_na_base_de_referencia(campeao, base_holdout):
    """Sanidade: o artefato carrega, prevê e não perdeu o básico no holdout fixo.

    O contrato de 0,90 é medido pelo portão, no conjunto de avaliação da época da promoção.
    Depois que o modelo se adapta a dados novos, o holdout antigo pode cair um pouco.
    Por isso o piso aqui é menor.
    """
    metricas = avaliar(campeao, base_holdout)
    assert metricas["recall_instavel"] >= config.PISO_SANIDADE, metricas
    assert metricas["precisao_instavel"] >= config.PISO_SANIDADE, metricas


def test_treino_com_o_codigo_e_params_atuais_cumpre_o_contrato(modelo_atual, base_holdout):
    """Se alguém mexer no código ou no params.yaml, o CI treina de novo e confere os limiares."""
    metricas = avaliar(modelo_atual, base_holdout)
    assert metricas["recall_instavel"] >= config.RECALL_MINIMO, metricas
    assert metricas["precisao_instavel"] >= config.PRECISAO_MINIMA, metricas


def test_modelo_supera_o_baseline_ingenuo(modelo_atual, base_treino, base_holdout):
    X_tr, y_tr = separar_xy(base_treino)
    X_te, y_te = separar_xy(base_holdout)
    baseline = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    nota_baseline = calcular_metricas(y_te, baseline.predict(X_te))["acuracia"]
    nota_modelo = calcular_metricas(y_te, modelo_atual.predict(X_te))["acuracia"]
    assert nota_modelo > nota_baseline + 0.1


def test_treino_e_deterministico(base_treino, params, xy_holdout):
    X_te, _ = xy_holdout
    a = treinar(base_treino, params).predict_proba(X_te)
    b = treinar(base_treino, params).predict_proba(X_te)
    assert np.allclose(a, b)


def test_modelo_consegue_memorizar_um_lote_pequeno(base_treino, params):
    """Teste clássico de sanidade: se nem um lote pequeno é aprendido, há um bug no pipeline.

    Com o HistGradientBoosting, cada folha exige pelo menos 20 amostras (padrão do
    scikit-learn); por isso o lote tem 100 linhas, e não 40.
    """
    pequeno = base_treino.sample(100, random_state=0)
    modelo = treinar(pequeno, params)
    X, y = separar_xy(pequeno)
    assert (modelo.predict(X) == y).mean() >= 0.95


def test_probabilidades_sao_validas(modelo_atual, xy_holdout):
    X_te, _ = xy_holdout
    probas = modelo_atual.predict_proba(X_te)
    assert np.all((probas >= 0) & (probas <= 1))
    assert np.allclose(probas.sum(axis=1), 1.0)


def test_invariancia_a_ruido_minimo(modelo_atual, xy_holdout):
    """Teste de comportamento: ruído de 0,01% nos atributos quase nunca muda a previsão."""
    X_te, _ = xy_holdout
    rng = np.random.default_rng(0)
    ruidoso = X_te * (1 + rng.normal(0, 1e-4, X_te.shape))
    mudou = (modelo_atual.predict(X_te) != modelo_atual.predict(ruidoso)).mean()
    assert mudou <= 0.02


def test_direcional_tempos_e_elasticidades_maiores_nao_reduzem_a_instabilidade(
    modelo_atual, xy_holdout
):
    """Novo (Etapa 3), teste direcional do domínio.

    Na base de TREINO, tau1..tau4 e g1..g4 têm correlação de Spearman positiva com instavel
    (de 0,20 a 0,24); as potências p1..p4 ficam perto de zero. Aumentar em 10% os tempos de
    reação e as elasticidades não pode reduzir a probabilidade média de instabilidade.
    As potências não são alteradas, para preservar o balanço p1 + p2 + p3 + p4 = 0.
    """
    X_te, _ = xy_holdout
    coluna = list(modelo_atual.classes_).index(config.CLASSE_INSTAVEL)
    maior = X_te.copy()
    for c in ["tau1", "tau2", "tau3", "tau4", "g1", "g2", "g3", "g4"]:
        maior[c] = maior[c] * 1.10
    antes = modelo_atual.predict_proba(X_te)[:, coluna].mean()
    depois = modelo_atual.predict_proba(maior)[:, coluna].mean()
    assert depois >= antes
