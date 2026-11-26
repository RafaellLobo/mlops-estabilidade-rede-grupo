# Etapa 2 - dados e contrato de Leonardo

**Implementação integrada. Registro complementar preparado por Rafael com Codex em 25/11/2026**, a partir dos commits reais de Leonardo. Não representa um documento escrito por Leonardo nem atribui a ele as verificações posteriores.

Leonardo (`le0zinn1316`, autor Git `LeonardoSecco`) publicou nove commits, de `c97b822` a `0b9f972`, no PR #4: fonte UCI com proveniência, FEATURES/ALVO, ingestão, partições, validações físicas e testes. O PR original teve falhas de integração; seus commits foram preservados pelo PR #6, que também incorporou as correções seguintes e os CSVs regenerados por Felipe em `e3dfe49`.

A fonte contém 10.000 registros, 12 entradas e classes derivadas de stabf; stab/stabf ficam fora das entradas. As divisões fixas são 6.000 treino, 2.000 holdout e 2.000 reserva, estratificadas com semente 7. Validações cobrem esquema, tipos, nulos, infinitos, faixas e balanço de potência. O SHA-256 da fonte está no planejamento e no relatório de integridade final.

Rafael executou no conjunto integrado o validador e 13 testes de dados aprovados, além das demais camadas (43 testes no total). O CI oficial E1 e os CIs de E3/CD também validaram essas camadas em Python 3.11 e 3.12. A fonte e os CSVs originais permanecem idênticos aos da v1.0.0; a verificação de bytes está em `docs/evidencias/integridade_final.json`.

Evidências: [PR #4](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/pull/4), [integração #6](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/pull/6), [E1](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45707223436). O uso de IA de Leonardo não foi declarado nos materiais consultados; não foi presumido. Os resultados locais originais e as correções de outras pessoas permanecem com suas autorias reais.
