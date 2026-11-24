"""Gera lotes de estabilidade da rede elétrica a partir da reserva.

Exemplos:
    python demo/gerar_lote.py lote_01
    python demo/gerar_lote.py lote_02 --drift 0.25 --n 120
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mlops_demo.data import gerar_lote  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    ap.add_argument("nome", help="nome do arquivo, sem extensão")
    ap.add_argument("--n", type=int, default=120, help="quantidade de registros")
    ap.add_argument(
        "--drift",
        type=float,
        default=1.0,
        help="fração de candidatos com maior elasticidade (1.0 = sem seleção)",
    )
    ap.add_argument("--semente", type=int, default=1)

    args = ap.parse_args()

    print("criado:", gerar_lote(args.nome, args.n, args.drift, args.semente))
