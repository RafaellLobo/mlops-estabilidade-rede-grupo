"""Pré-processamento e construção do pipeline de modelo."""

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from mlops_demo.config import ALVO, FEATURES

TIPOS_SUPORTADOS = ("regressao_logistica", "random_forest", "hist_gradient_boosting")


def separar_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separa atributos e alvo, garantindo as colunas esperadas e a ordem.

    Colunas extras (por exemplo, `stab` ou `stabf` da fonte UCI) nunca entram no modelo:
    só as 12 colunas de FEATURES são usadas como entrada.
    """
    faltando = [c for c in FEATURES + [ALVO] if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes: {faltando}")
    X = df[FEATURES[:-1]].copy()
    y = df[ALVO].astype(int)
    return X, y


def construir_classificador(modelo: dict, semente: int):
    """Cria o classificador descrito em um bloco de configuração (params.yaml)."""
    tipo = modelo.get("tipo", "regressao_logistica")
    if tipo == "regressao_logistica":
        return LogisticRegression(
            C=modelo["C"],
            max_iter=modelo["max_iter"],
            class_weight=modelo["class_weight"],
            random_state=semente,
        )
    if tipo == "random_forest":
        return RandomForestClassifier(
            n_estimators=modelo["n_estimators"],
            max_depth=modelo["max_depth"],
            min_samples_leaf=modelo["min_samples_leaf"],
            class_weight=modelo["class_weight"],
            random_state=semente,
            n_jobs=1,
        )
    if tipo == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(
            max_iter=modelo["max_iter"],
            learning_rate=modelo["learning_rate"],
            max_leaf_nodes=modelo["max_leaf_nodes"],
            class_weight=modelo["class_weight"],
            early_stopping=False,
            random_state=semente,
        )
    raise ValueError(f"Tipo de modelo desconhecido: {tipo!r}. Use um de {TIPOS_SUPORTADOS}.")


def construir_pipeline(params: dict, modelo: dict | None = None) -> Pipeline:
    """Pipeline de treino: padronização + classificador.

    A padronização é ajustada só nos dados de treino de cada ajuste (dentro do pipeline).
    Para árvores ela não muda o resultado, mas mantém o mesmo contrato de etapas.
    """
    return Pipeline(
        [
            ("padronizar", StandardScaler()),
            (
                "classificador",
                construir_classificador(modelo or params["modelo"], params["semente"]),
            ),
        ]
    )
