# Adaptação: CI/CD/CT para estabilidade de rede elétrica

Repositório: [mlops-estabilidade-rede-grupo](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo). Adaptado do [projeto da disciplina](https://github.com/wesleyasantos/ci_cd_ct_mlops). Evidências oficiais verificadas em 25/11/2026; índice detalhado: [docs/EVIDENCIAS.json](docs/EVIDENCIAS.json).

## 1. Problema e dados

Classificar uma rede elétrica simulada de quatro nós como estável (0) ou instável (1), para triagem acadêmica de cenários. Fonte: Electrical Grid Stability Simulated Data, Arzamasov (2018), UCI, [DOI 10.24432/C5PG66](https://doi.org/10.24432/C5PG66), CC BY 4.0. São 10.000 linhas e 12 entradas numéricas (`tau1..4`, `p1..4`, `g1..4`); 6.000 treino, 2.000 holdout e 2.000 reserva, estratificados com semente 7. A fonte tem hash conferido; `stab` e `stabf` não entram no modelo. `p1` é derivada das demais potências. Nenhum dado pessoal real é usado.

## 2. Contrato e justificativa

Positiva `instavel=1`; o erro mais caro é o falso negativo. Recall mínimo 0,92 e precisão mínima 0,90 limitam perdas de instabilidade e alertas indiscriminados. O recall do candidato não pode ser inferior ao do campeão no mesmo conjunto. Drift: KS com p < 0,01 em pelo menos 2/12 entradas. A API valida 12 valores, faixas físicas e balanço de potência com tolerância 1e-8. Os limiares são didáticos, sem garantia operacional.

## 3. Mudanças por arquivo

- `data/source/`, `data.py`, `config.py` e CSVs: fonte/licença/hash, esquema, classes, partições e validações físicas.
- `features.py`, `selecao.py`, `evaluate.py`, `gate.py`, `params.yaml`: seleção interna 80/20 no treino, HistGradientBoosting, métricas e portão para a classe instável.
- `api.py`, `monitor.py`, `demo/*`: contrato elétrico, lotes reais da reserva, drift e cinco cenários adaptados.
- `tests/*`: quatro camadas e testes novos do domínio; 43 testes. `pyproject.toml`: scikit-learn 1.7.2; `dvc.yaml`/`dvc.lock`: dependências e reprodução. Workflows e Dockerfile originais preservados.
- `models/champion/`: inicial com recall 0,9632 e precisão 0,9505 no holdout; promoção pelo CT na v1.1.0 com 0,9668/0,9452 na avaliação ampliada de 2.200 linhas. São conjuntos diferentes; esses valores não são uma comparação direta de ganho.

## 4. Cinco evidências oficiais

| Evidência | Resultado | Actions |
|---|---|---|
| E1 | CI na main: três jobs verdes | [E1](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45707223436) |
| E2 | PR #8: três falhas esperadas em Testes de código | [E2](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728001528) |
| E3 | PR #9: drift em 4/12, DVC e portão aprovados | [E3](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728255899) |
| E4 | PR #10: precisão 0,6568 rejeitada; campeão preservado | [E4](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728387236) |
| E5 | v1.0.0: CI, build, smoke e publicação aprovados | [E5](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728416630) |

As falhas E2/E4 são intencionais; seus PRs foram fechados sem merge. [Pacote público](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/pkgs/container/mlops-estabilidade-rede-grupo): `ghcr.io/rafaelllobo/mlops-estabilidade-rede-grupo`, tags `1.0.0` e `1.1.0`, ambas com pull anônimo e smoke aprovados; digests/logs em `docs/evidencias/`.

## 5. Limites, monitoramento e desafio adicional

Dados simulados e avaliação reutilizada nos experimentos de CT limitam a generalização; o portão não detecta todos os erros ou vazamentos. Preservamos as tentativas e limitações de Juan. Em produção, monitoraríamos drift, qualidade com rótulos, recall/precisão por período, latência e falhas da API, com revisão independente e rollback.

Bônus comprovado: [CT automático](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45728991546) promoveu o campeão, criou `v1.1.0` e disparou o [CD como robô](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45729083218). Vantagens: rastreabilidade e menor intervenção. Riscos: main sem revisão obrigatória e propagação de erros não cobertos pelo contrato. A variável foi restaurada para `false`; histórico e v1.0.0 permitem recuperar a versão anterior. A exclusividade do dataset entre grupos depende da confirmação da disciplina.

## 6. Contribuições e IA

Rafael (Codex): planejamento, protocolo, integração e fechamento oficial; PRs #1–#3, #5–#6 e #8–#10. Leonardo: nove commits de dados (`c97b822`–`0b9f972`), PR #4; IA não declarada. Samara (Claude): modelo, seleção, métricas, testes e campeão (`5c75f8f`, `8046737`, `0c59578`, `b28bb5c`). Juan (ChatGPT): API, drift, cenários e compatibilidade (`34d811b`, `0fc1d6f`). Felipe (Claude): bases, README, relatório e registros (`e3dfe49`, `77e9321`), PR #7. A equipe final confirmada por Rafael é formada pelos cinco acima; Felipe assumiu também a etapa 5. Detalhes e autorias em [docs/CONTRIBUICOES.md](docs/CONTRIBUICOES.md). As IAs auxiliaram código, análise, testes e redação; não substituem as contribuições humanas registradas.
