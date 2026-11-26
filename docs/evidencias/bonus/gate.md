## Portão de qualidade: APROVADO: o candidato pode virar campeão

| Modelo | Recall instável | Precisão instável | Amostras |
|---|---|---|---|
| campeao | 0.965 | 0.950 | 2200 |
| candidato | 0.967 | 0.945 | 2200 |

| Regra | Resultado | Valor |
|---|---|---|
| recall instável do candidato >= 0.92 | passou | 0.9668 |
| precisão instável do candidato >= 0.90 | passou | 0.9452 |
| recall instável do candidato >= recall do campeão (mesmo conjunto) | passou | 0.9668 x 0.9647 |
