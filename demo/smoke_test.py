"""Teste de fumaça da API de estabilidade da rede elétrica."""

import csv
import json
import sys
import urllib.request
from pathlib import Path

URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
HOLDOUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "base_holdout.csv"

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


def chamar(caminho: str, corpo: dict | None = None) -> dict:
    dados = json.dumps(corpo).encode() if corpo is not None else None
    requisicao = urllib.request.Request(
        URL + caminho, data=dados, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(requisicao, timeout=10) as resposta:
        return json.loads(resposta.read())


saude = chamar("/health")
assert saude["status"] == "ok", saude
print("health ok | versão:", saude["versao_codigo"])

with open(HOLDOUT, encoding="utf-8") as arquivo:
    linha = next(csv.DictReader(arquivo))

atributos = [float(linha[nome]) for nome in FEATURES]

predicao = chamar("/predict", {"atributos": atributos})

assert predicao["classe"] in {"instavel", "estavel"}, predicao
assert 0.0 <= predicao["probabilidade_instavel"] <= 1.0, predicao

print("predict ok |", predicao)
