# Etapa 3 — Samara: modelo, métricas, portão e campeão

**Atualização de fechamento (25/11/2026):** E1–E5 e bônus comprovados por Rafael com Codex. Consulte [FECHAMENTO_ENTREGA.md](FECHAMENTO_ENTREGA.md) e [EVIDENCIAS.json](EVIDENCIAS.json). O registro abaixo preserva o trabalho e as condições históricas da etapa; pendências técnicas antigas foram superadas pelas execuções finais. A equipe final tem Rafael, Leonardo, Samara, Juan e Felipe, todos com commits comprovados; Victor pertence somente ao planejamento histórico. As autorias estão em [CONTRIBUICOES.md](CONTRIBUICOES.md).

## Registro histórico da etapa

**Responsável:** Samara (`Samysruiz`). **Revisor proposto:** Juan. **Base:** branch `leonardo/etapa-2-dados` (commit `8651435`).

## O que mudou

| Arquivo | Mudança |
|---|---|
| `src/mlops_demo/features.py` | Pipeline aceita três tipos de classificador declarados no `params.yaml`; `separar_xy` usa só as 12 entradas (`stab`/`stabf` nunca entram). |
| `src/mlops_demo/evaluate.py` | Classe positiva `instavel=1`; métricas `recall_instavel` e `precisao_instavel`. |
| `src/mlops_demo/gate.py` | Mesmas regras do contrato com os novos nomes: recall ≥ 0,92, precisão ≥ 0,90, recall do candidato ≥ campeão no mesmo conjunto. |
| `src/mlops_demo/selecao.py` (novo) | Seleção interna 80/20 só da base de treino (`random_state=42`); registra todos os candidatos. |
| `params.yaml` | Candidatos e critério declarados antes da execução; bloco `modelo` = vencedor. |
| `dvc.yaml` | `config.py` passa a ser dependência do estágio `treinar` (limiares e esquema invalidam o pipeline). |
| `tests/test_codigo.py`, `tests/test_modelo.py` | Adaptados ao novo domínio; novos testes listados abaixo. |
| `models/champion/` | Campeão inicial treinado na base de treino completa. |

## Seleção interna (holdout não utilizado)

Critério declarado: maior recall da classe instável entre os candidatos com precisão ≥ 0,90; desempate pela precisão e pela ordem. Validação interna: 4.800 treino / 1.200 validação.

| Ordem | Candidato | Recall instável | Precisão instável | Acurácia |
|---|---|---|---|---|
| 1 | Regressão logística (C=1, balanced) | 0,7898 | 0,8582 | 0,7825 |
| 2 | Random forest (300 árvores, balanced) | 0,9648 | 0,8968 | 0,9067 |
| 3 | HistGradientBoosting (300 iterações, lr 0,1) | **0,9687** | 0,9322 | 0,9350 |

A regressão logística, referência original, e o random forest não atingem a precisão mínima de 0,90 neste ambiente. Vencedor: HistGradientBoosting. Registro completo em `docs/selecao_modelo_etapa3.json`.

Sensibilidade à versão: numa execução preliminar com scikit-learn 1.9.1 (Python 3.11.18), o vencedor foi o mesmo, mas o random forest teve precisão de 0,9408 e seria elegível. A escolha do vencedor não mudou entre as versões; a elegibilidade do random forest mudou.

## Campeão inicial (holdout fixo, 2.000 linhas, avaliado uma vez após fixar o modelo)

Recall instável **0,9632**; precisão instável **0,9505**; 2.000 amostras (valores completos em `models/champion/metrics.json`). Cumpre o contrato (recall ≥ 0,92; precisão ≥ 0,90).

## Testes novos

- Código: `stab`/`stabf` nunca entram como atributo; tipo de modelo inválido falha com mensagem clara; o critério de seleção é aplicado como declarado (três testes).
- Modelo: teste direcional — aumentar 10% `tau1..tau4` e `g1..g4` não reduz a probabilidade média de instabilidade (na base de treino, esses atributos têm Spearman de 0,20 a 0,24 com `instavel`).
- Adaptado: o teste de memorização usa 100 linhas, porque o HistGradientBoosting exige 20 amostras por folha.

## Ambiente e verificações

Execução oficial desta etapa no computador de Samara (Windows): Python 3.10.11, scikit-learn 1.7.2, numpy 2.2.6, pytest 9.2.0. Executado: `python -m mlops_demo.data base` (6.000 / 2.000 / 2.000), `python -m mlops_demo.selecao`, `python -m mlops_demo.train --campeao` e `pytest -m "codigo or modelo"` (24 aprovados). Lint verificado com ruff na preparação. O projeto não fixa a versão do scikit-learn: o CI e o Docker podem instalar outra versão e os números podem variar; fixar a versão é decisão do grupo.

## Pendências fora desta etapa

- **API (Juan):** `api.py`, `tests/test_api.py` e `demo/smoke_test.py` ainda usam `CLASSE_MALIGNA` e os campos antigos; dois testes de API falham até a adaptação dele.
- **Dados (Leonardo):** ver parecer de revisão da Etapa 2.
- **DVC:** `dvc.lock` ainda não gerado; depende de `dvc repro` com o pipeline integrado.

## Uso de IA

Código, testes e este registro foram preparados com auxílio do Claude, a pedido de Samara, que revisou e fez os commits com a própria conta.
