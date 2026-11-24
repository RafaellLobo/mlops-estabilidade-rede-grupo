"""Testes de dados: esquema, integridade física e separação das partições."""

import pandas as pd
import pytest

from mlops_demo import config
from mlops_demo.data import (
    dividir_dataset,
    listar_lotes,
    validar_dataframe,
)

pytestmark = pytest.mark.dados


def _arquivos_de_dados():
    return [config.BASE_TREINO, config.BASE_HOLDOUT, *listar_lotes()]


@pytest.mark.parametrize("caminho", _arquivos_de_dados(), ids=lambda c: c.name)
def test_arquivo_respeita_esquema_e_regras_fisicas(caminho):
    problemas = validar_dataframe(pd.read_csv(caminho))
    assert problemas == [], f"{caminho.name}: {problemas}"


def test_particoes_tem_tamanhos_do_protocolo():
    treino, holdout, reserva = dividir_dataset()
    assert (len(treino), len(holdout), len(reserva)) == (6000, 2000, 2000)


def test_particoes_nao_tem_registros_sobrepostos():
    treino, holdout, reserva = dividir_dataset()
    chaves = [
        set(map(tuple, parte[config.FEATURES].to_numpy()))
        for parte in (treino, holdout, reserva)
    ]
    assert chaves[0].isdisjoint(chaves[1])
    assert chaves[0].isdisjoint(chaves[2])
    assert chaves[1].isdisjoint(chaves[2])


def test_treino_e_holdout_contem_as_duas_classes(base_treino, base_holdout):
    assert set(base_treino[config.ALVO].unique()) == {0, 1}
    assert set(base_holdout[config.ALVO].unique()) == {0, 1}


def test_validador_detecta_nulos_e_valores_nao_finitos(base_treino):
    corrompido = base_treino.copy()
    corrompido.loc[0, "tau1"] = None
    corrompido.loc[1, "g1"] = float("inf")
    problemas = validar_dataframe(corrompido)
    assert any("nulos" in p for p in problemas)
    assert any("não finitos" in p for p in problemas)


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
