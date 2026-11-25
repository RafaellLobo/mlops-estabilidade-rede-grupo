"""Testes de contrato da API de estabilidade da rede elétrica."""

import pytest
from fastapi.testclient import TestClient

from mlops_demo import config
from mlops_demo.api import app

pytestmark = pytest.mark.api

cliente = TestClient(app)


def test_health_responde_ok():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_predict_devolve_o_formato_combinado(base_holdout):
    rede = base_holdout[config.FEATURES].iloc[0].tolist()
    resposta = cliente.post("/predict", json={"atributos": rede})

    assert resposta.status_code == 200

    corpo = resposta.json()
    assert set(corpo) == {
        "classe",
        "probabilidade_instavel",
        "versao_codigo",
    }
    assert corpo["classe"] in {"instavel", "estavel"}
    assert 0.0 <= corpo["probabilidade_instavel"] <= 1.0


def test_predict_rejeita_quantidade_errada_de_atributos():
    resposta = cliente.post("/predict", json={"atributos": [1.0, 2.0]})
    assert resposta.status_code == 422


def test_predict_concorda_com_campeao(base_holdout, campeao):
    X = base_holdout[config.FEATURES]
    coluna = list(campeao.classes_).index(config.CLASSE_INSTAVEL)
    probabilidades = campeao.predict_proba(X)[:, coluna]

    indices = [
        int(probabilidades.argmax()),
        int(probabilidades.argmin()),
    ]

    for indice in indices:
        entrada = X.iloc[[indice]]
        previsto = int(campeao.predict(entrada)[0])
        esperado = "instavel" if previsto == config.CLASSE_INSTAVEL else "estavel"

        resposta = cliente.post(
            "/predict",
            json={"atributos": X.iloc[indice].tolist()},
        )

        assert resposta.status_code == 200
        assert resposta.json()["classe"] == esperado


def test_predict_rejeita_balanco_de_potencia_invalido():
    atributos = [
        5.0,
        5.0,
        5.0,
        5.0,
        4.0,
        -1.0,
        -1.0,
        -1.0,
        0.5,
        0.5,
        0.5,
        0.5,
    ]

    resposta = cliente.post("/predict", json={"atributos": atributos})

    assert resposta.status_code == 422


def test_predict_rejeita_tempo_de_reacao_invalido(base_holdout):
    atributos = base_holdout[config.FEATURES].iloc[0].tolist()
    atributos[config.FEATURES.index("tau1")] = -1.0

    resposta = cliente.post("/predict", json={"atributos": atributos})

    assert resposta.status_code == 422
