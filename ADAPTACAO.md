# Adaptação: CI/CD/CT para estabilidade de rede elétrica

Repositório do grupo: <https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo>. Projeto original: classificador
de tumores de mama (Breast Cancer). **Rascunho: evidências E1 a E5 pendentes (seção 4).**

## 1. Problema, fonte, licença e tamanho

Classificar uma rede elétrica simulada de quatro nós como **estável (0)** ou **instável (1)**, para triagem de cenários
(demonstração acadêmica, sem operação real). O erro mais caro é o falso negativo, então a classe positiva é `instavel = 1`.
Fonte: *Electrical Grid Stability Simulated Data* (Arzamasov, 2018), UCI, [DOI 10.24432/C5PG66](https://doi.org/10.24432/C5PG66),
**CC BY 4.0**, SHA-256 conferido. São 10.000 simulações e 12 atributos (`tau1..4`, `p1..4`, `g1..4`): 6.000 de treino,
2.000 de holdout e 2.000 de reserva (para lotes). `stab` e `stabf` nunca entram como entrada.

## 2. Contrato e justificativa

Recall da classe instável >= 0,92 (menos falsos negativos); precisão >= 0,90 (evita aprovar quem chuta tudo como instável);
recall do candidato não menor que o do campeão no mesmo conjunto; drift quando o KS (p < 0,01) acusa 2 ou mais dos 12 atributos. A API exige 12 entradas, faixa física e `p1+p2+p3+p4 = 0`, e responde HTTP 422 caso contrário.

## 3. Mudanças por arquivo

| Arquivo | Mudança |
|---|---|
| `data/source/`, `data.py`, `config.py` | fonte UCI com atribuição e hash; esquema, faixas físicas, partições e validação |
| `data/raw/*.csv` | bases regeneradas da fonte UCI (ainda eram as do Breast Cancer) |
| `features.py`, `selecao.py`, `evaluate.py`, `gate.py`, `params.yaml` | seleção 80/20 sem o holdout; métricas e portão para `instavel=1` |
| `models/champion/` | HistGradientBoosting: recall 0,9632 e precisão 0,9505 no holdout |
| `api.py`, `monitor.py`, `demo/*` | API de 12 entradas, drift por lotes reais da reserva, cinco cenários, smoke test |
| `tests/`, `pyproject.toml`, `dvc.lock` | quatro camadas com teste novo; `scikit-learn==1.7.2`; workflows e `Dockerfile` inalterados |

## 4. Evidências E1–E5

Estado: **PENDENTE** até a execução no GitHub; só URLs reais (índice em `docs/EVIDENCIAS.json`).

| | O que prova | Link |
|---|---|---|
| E1 | `main` adaptada com os três jobs do CI verdes | PENDENTE |
| E2 | CI vermelho controlado em PR (cenário 1, passo "Testes de código") | PENDENTE |
| E3 | drift, retreino e portão aprovado no CT | PENDENTE |
| E4 | portão reprovado, campeão inalterado (SHA-256 antes e depois) | PENDENTE |
| E5 | tag, CD verde e imagem pública em `ghcr.io` | PENDENTE |

A reprodução local (fora do Actions, sem valor de evidência) está em `docs/ETAPA5_VICTOR.md`.

## 5. Limites e monitoramento

Dados simulados e limiares didáticos: as métricas não valem para uma rede real. Parte dos dados de avaliação foi reutilizada
nos experimentos de CT (`docs/ETAPA4_JUAN.md`), sem mudar os critérios do portão. O PR #4 original de Leonardo tinha falhas de
lint e foi superado pela integração (`docs/INTEGRACAO_ETAPAS_2_4.md`). Rafael verificou em Windows (Python 3.11.9) e esta
reprodução foi em Linux (Python 3.12.3), com scikit-learn 1.7.2 nos dois. Monitoramento: drift (KS) por lote e portão antes
de promover; promoção automática desligada (`PROMOCAO_AUTOMATICA = false`).

## 6. Contribuições e uso de IA

Hashes em `github.com/RafaellLobo/mlops-estabilidade-rede-grupo/commit/`. Quem só recebeu uma tarefa não é creditado.

- **Rafael** (IA: Codex): `e511087`, `1085b5f`, `c332430`, `978e408`, `011ee02`; PRs #1, #2, #3, #5 e #6.
- **Leonardo** (IA: não declarada): `c97b822` a `0b9f972`, 9 commits (PR #4).
- **Samara** (IA: Claude): `5c75f8f`, `8046737`, `0c59578`, `b28bb5c`.
- **Juan** (IA: ChatGPT): `34d811b`, `0fc1d6f`.
- **Victor** (IA: PENDENTE): PENDENTE, sem commit, PR ou execução; a etapa 5 foi assumida por Felipe.
- **Felipe** (IA: Claude): `e3dfe49`; README, ADAPTACAO e registros das etapas 5 e 6.
