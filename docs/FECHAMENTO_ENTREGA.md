# Fechamento técnico da atividade - 25/11/2026

E1–E5 e o desafio adicional foram executados e conferidos no repositório coletivo. Operador das execuções finais: Rafael, com Codex, preservando os cenários de Juan, a implementação de Leonardo/Samara e a documentação inicial de Felipe.

| Evidência | Resultado | Execução oficial |
|---|---|---|
| E1 | CI na main: três jobs verdes | [E1](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45707223436) |
| E2 | PR #8: três falhas esperadas em Testes de código | [E2](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728001528) |
| E3 | PR #9: drift em 4/12, DVC e portão aprovados | [E3](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728255899) |
| E4 | PR #10: precisão 0,6568 rejeitada; campeão preservado | [E4](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728387236) |
| E5 | v1.0.0: CI, build, smoke e publicação aprovados | [E5](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728416630) |

Os PRs #8 e #10 foram fechados sem merge, com branches preservadas. O PR #9 só foi integrado depois dos checks aprovados e da comprovação E1–E5, para executar o bônus.

## Bônus

CT: [BONUS_CT](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728991546). O robô publicou apenas `models/champion/model.joblib` e `models/champion/metrics.json` no commit `0c9b4c195d7cc4a32b7575bf8233b0001cfe3995`, criou a tag `v1.1.0` e chamou o CD por `workflow_dispatch` como `github-actions[bot]`: [BONUS_CD](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45729083218). A tag e o CD apontam para o mesmo commit.

`PROMOCAO_AUTOMATICA` foi ligada temporariamente e restaurada para `false`, com confirmação pela API em `evidencias/bonus_estado_final.json`. A main já estava sem proteção; nenhuma proteção foi removida. O pipeline original não precisou de alteração.

## Imagens e integridade

[Pacote público](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/pkgs/container/mlops-estabilidade-rede-grupo). As versões `1.0.0` e `1.1.0` foram baixadas com configurações Docker separadas e `auths` vazio, sem login, e passaram no smoke de `/health` e `/predict`. Logs, digests e resultados estão em `evidencias/`. Os contêineres de verificação foram parados ao final.

Fonte, CSV de treino e holdout foram preservados byte a byte. O campeão inicial permanece em `v1.0.0`; a única substituição do campeão foi a promoção autorizada pelo CT. Não houve nova seleção, mudança de sementes, limiares ou partições. Os resultados de E3/E4 e a limitação de reutilização da avaliação documentada por Juan permanecem registrados.

## Documentação e entrega

`ADAPTACAO.md`, `ENTREGA_D2L.txt`, `EVIDENCIAS.json` e os registros foram atualizados. O material está preparado para um único envio ao D2L; nenhum envio ao portal foi realizado. Autoria: [CONTRIBUICOES.md](CONTRIBUICOES.md). A equipe final confirmada por Rafael tem cinco integrantes (Rafael, Leonardo, Samara, Juan e Felipe), todos com commits próprios comprovados. Victor ficou apenas no planejamento histórico. A exclusividade do dataset entre grupos depende da confirmação da disciplina.

Para reproduzir os cenários históricos E2–E4, crie a branch a partir de `v1.0.0`. A main já contém o lote E3 e o campeão promovido; aplicar novamente o cenário 4 nela não representa o estado inicial das evidências.
