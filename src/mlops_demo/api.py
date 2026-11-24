"""API de inferência para classificação da estabilidade da rede elétrica."""

import json
import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from mlops_demo import __version__, config

CAMINHO_MODELO = Path(os.environ.get("MODEL_PATH", config.MODELO_CAMPEAO))
CAMINHO_METRICAS = CAMINHO_MODELO.with_name("metrics.json")

app = FastAPI(title="Estabilidade de rede elétrica (CI/CD/CT)", version=__version__)
_modelo = joblib.load(CAMINHO_MODELO)


class EntradaRede(BaseModel):
    """Os 12 atributos da rede, na mesma ordem do treino."""

    atributos: list[float] = Field(
        min_length=len(config.FEATURES),
        max_length=len(config.FEATURES),
    )

    @field_validator("atributos")
    @classmethod
    def validar_atributos(cls, valores: list[float]) -> list[float]:
        entrada = dict(zip(config.FEATURES, valores, strict=True))

        for nome, valor in entrada.items():
            minimo, maximo = config.FAIXAS_FEATURES[nome]

            if not minimo <= valor <= maximo:
                raise ValueError(f"{nome} fora da faixa física permitida")

        balanco = sum(entrada[nome] for nome in config.COLUNAS_POTENCIA)

        if abs(balanco) > config.TOLERANCIA_BALANCO_POTENCIA:
            raise ValueError("Balanço de potência inválido")

        return valores


class Predicao(BaseModel):
    classe: str
    probabilidade_instavel: float
    versao_codigo: str


@app.get("/health")
def saude() -> dict:
    metricas = {}
    if CAMINHO_METRICAS.exists():
        metricas = json.loads(CAMINHO_METRICAS.read_text(encoding="utf-8"))
    return {"status": "ok", "versao_codigo": __version__, "metricas_do_campeao": metricas}


@app.post("/predict", response_model=Predicao)
def prever(rede: EntradaRede) -> Predicao:
    entrada = pd.DataFrame([rede.atributos], columns=config.FEATURES)
    previsto = int(_modelo.predict(entrada)[0])

    coluna = list(_modelo.classes_).index(config.CLASSE_INSTAVEL)
    p_instavel = float(_modelo.predict_proba(entrada)[0][coluna])

    return Predicao(
        classe="instavel" if previsto == config.CLASSE_INSTAVEL else "estavel",
        probabilidade_instavel=round(p_instavel, 4),
        versao_codigo=__version__,
    )
