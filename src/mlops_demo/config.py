"""Configuração central do projeto: caminhos, esquema e limiares de qualidade."""

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]

# Dados de origem, brutos e processados
DADOS_FONTE = RAIZ / "data" / "source"
FONTE_UCI = DADOS_FONTE / "Data_for_UCI_named.csv"
DADOS_BRUTOS = RAIZ / "data" / "raw"
DADOS_LOTES = DADOS_BRUTOS / "lotes"
DADOS_PROCESSADOS = RAIZ / "data" / "processed"
BASE_TREINO = DADOS_BRUTOS / "base_treino.csv"
BASE_HOLDOUT = DADOS_BRUTOS / "base_holdout.csv"
TREINO_PROCESSADO = DADOS_PROCESSADOS / "treino.csv"
AVALIACAO_PROCESSADA = DADOS_PROCESSADOS / "avaliacao.csv"

# Fonte UCI — Electrical Grid Stability Simulated Data
URL_FONTE_UCI = (
    "https://archive.ics.uci.edu/static/public/471/electrical+grid+stability+simulated+data.zip"
)
SHA256_FONTE_UCI = "7afc3154fed9cd65258b3403b60381fe6b0d832bf817a1ea4866395d05a84a83"
COLUNAS_ORIGINAIS = [
    "tau1",
    "tau2",
    "tau3",
    "tau4",
    "p1",
    "p2",
    "p3",
    "p4",
    "g1",
    "g2",
    "g3",
    "g4",
    "stab",
    "stabf",
]

# Esquema público do projeto: 12 atributos numéricos e alvo binário.
FEATURES = [
    "tau1",
    "tau2",
    "tau3",
    "tau4",
    "p1",
    "p2",
    "p3",
    "p4",
    "g1",
    "g2",
    "g3",
    "g4",
]
ALVO = "instavel"
CLASSE_ESTAVEL = 0
CLASSE_INSTAVEL = 1
COLUNAS_POTENCIA = ["p1", "p2", "p3", "p4"]
TOLERANCIA_BALANCO_POTENCIA = 1e-8

# Faixas físicas do domínio simulado (UCI).
FAIXAS_FEATURES = {
    "tau1": (0.5, 10.0),
    "tau2": (0.5, 10.0),
    "tau3": (0.5, 10.0),
    "tau4": (0.5, 10.0),
    "p1": (1.5, 6.0),
    "p2": (-2.0, -0.5),
    "p3": (-2.0, -0.5),
    "p4": (-2.0, -0.5),
    "g1": (0.05, 1.0),
    "g2": (0.05, 1.0),
    "g3": (0.05, 1.0),
    "g4": (0.05, 1.0),
}

# Modelos e relatórios
MODELO_CAMPEAO = RAIZ / "models" / "champion" / "model.joblib"
METRICAS_CAMPEAO = RAIZ / "models" / "champion" / "metrics.json"
MODELO_CANDIDATO = RAIZ / "models" / "candidate" / "model.joblib"
METRICAS_CANDIDATO = RAIZ / "reports" / "candidate_metrics.json"
RELATORIO_GATE = RAIZ / "reports" / "gate.json"
RESUMO_GATE = RAIZ / "reports" / "gate.md"
RELATORIO_DRIFT = RAIZ / "reports" / "drift.md"
PARAMS = RAIZ / "params.yaml"

# Limiares de qualidade do contrato. Alterações exigem revisão em PR.
RECALL_MINIMO = 0.92
PRECISAO_MINIMA = 0.90
TOLERANCIA_CAMPEAO = 0.0
PISO_SANIDADE = 0.80
LIMITE_DRIFT_P = 0.01
MIN_FEATURES_DRIFT = 2


def carregar_params() -> dict:
    """Lê o params.yaml (hiperparâmetros e semente)."""
    with open(PARAMS, encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)
