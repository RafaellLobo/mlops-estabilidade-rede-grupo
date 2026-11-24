"""Testes de dados: esquema, integridade física e separação das partições."""

import pandas as pd
import pytest

from mlops_demo import config
from mlops_demo.data import dividir_dataset, validar_dataframe

pytestmark = pytest.mark.dados


@pytest.fixture
def particoes():
    return dividir_dataset()


@pytest.fixture
def base_treino(particoes):
    return particoes[0]


@pytest.fixture
def base_holdout(particoes):
    return particoes[1]


def test_hash_sha256_da_fonte_original():
    assert verificar_hash_fonte() == config.SHA256_FONTE_UCI


def test_fonte_gera_particoes_com_tamanhos_do_protocolo(particoes):
    treino, holdout, reserva = particoes
    assert (len(treino), len(holdout), len(reserva)) == (6000, 2000, 2000)


def test_particoes_nao_tem_registros_sobrepostos(particoes):
    chaves = [
        set(map(tuple, parte[config.FEATURES].to_numpy()))
        for parte in particoes
    ]
    assert chaves[0].isdisjoint(chaves[1])
    assert chaves[0].isdisjoint(chaves[2])
    assert chaves[1].isdisjoint(chaves[2])


def test_particoes_contem_as_duas_classes(particoes):
    for parte in particoes:
        assert set(parte[config.ALVO].unique()) == {
            config.CLASSE_ESTAVEL, config.CLASSE_INSTAVEL
        }


def test_fonte_nao_expoe_colunas_de_vazamento(base_treino):
    assert list(base_treino.columns) == [*config.FEATURES, config.ALVO]
    assert "stab" not in base_treino.columns
    assert "stabf" not in base_treino.columns


def test_validador_aceita_dados_fisicamente_validos(base_treino):
    assert validar_dataframe(base_treino) == []


def test_validador_detecta_nulos_e_valores_nao_finitos(base_treino):
    corrompido = base_treino.copy()
    corrompido.loc[0, "tau1"] = None
    corrompido.loc[1, "g1"] = float("inf")
    problemas = validar_dataframe(corrompido)
    assert any("nulos" in p for p in problemas)
    assert any("não finitos" in p for p in problemas)


def test_validador_detecta_valor_nao_numerico(base_treino):
    corrompido = base_treino.copy()
    corrompido["tau1"] = corrompido["tau1"].astype(object)
    corrompido.loc[0, "tau1"] = "invalido"
    assert any("não numéricos" in p for p in validar_dataframe(corrompido))


def test_validador_detecta_esquema_diferente(base_treino):
    assert validar_dataframe(base_treino.drop(columns=["tau1"]))


def test_validador_aceita_potencia_negativa_de_consumidores(base_treino):
    assert (base_treino[["p2", "p3", "p4"]] < 0).all().all()
    assert validar_dataframe(base_treino) == []


def test_validador_rejeita_balanco_de_potencia_invalido(base_treino):
    corrompido = base_treino.copy()
    corrompido.loc[0, "p1"] += 0.1
    problemas = validar_dataframe(corrompido)
    assert any("balanço de potência inválido" in p for p in problemas)


def test_validador_rejeita_atributo_fora_da_faixa_fisica(base_treino):
    corrompido = base_treino.copy()
    corrompido.loc[0, "tau1"] = 20.0
    problemas = validar_dataframe(corrompido)
    assert any("tau1 fora da faixa física" in p for p in problemas)


def test_validador_rejeita_rotulo_invalido(base_treino):
    corrompido = base_treino.copy()
    corrompido.loc[0, config.ALVO] = 2
    problemas = validar_dataframe(corrompido)
    assert any("alvo" in p for p in problemas)
