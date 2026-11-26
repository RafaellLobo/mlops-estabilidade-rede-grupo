## Portão de qualidade: REPROVADO

| Modelo | Recall instável | Precisão instável | Amostras |
|---|---|---|---|
| campeao | 0.965 | 0.950 | 2200 |
| candidato | 1.000 | 0.657 | 2200 |

| Regra | Resultado | Valor |
|---|---|---|
| recall instável do candidato >= 0.92 | passou | 1.0 |
| precisão instável do candidato >= 0.90 | FALHOU | 0.6568 |
| recall instável do candidato >= recall do campeão (mesmo conjunto) | passou | 1.0000 x 0.9647 |
