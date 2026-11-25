# Etapa 5: CI/CD e consolidação de E1 a E5

**Estado: `evidencias_pendentes`.** Nenhuma evidência E1 a E5 foi produzida no GitHub até este registro. O que existe é a
validação local abaixo, que **não vale como evidência oficial**.

## Responsabilidade e executor

| Campo | Conteúdo |
|---|---|
| Etapa atribuída a | Victor (conta conhecida `VictorHugo-syss`) |
| Etapa assumida por | Felipe, que informou ter assumido a etapa 5 além da 6 |
| Contribuição de Victor | nenhum commit, PR ou execução no repositório até 25/11/2026 (conferido em `git log` e nas refs de PR) |
| Uso de IA | Claude, a pedido de Felipe, para preparar este registro e a validação local. A IA não tem acesso autenticado ao GitHub e não executou nada no Actions |

Se Victor ou outra pessoa executar algum passo, registrar o executor real em `docs/EVIDENCIAS.json`. A autoria do código de
Juan, Samara e Leonardo não muda.

## Base

`main` em `330fcf8` (merge do PR #6), com as etapas 2 a 4 já integradas. Refs conferidas: PRs #1 a #6 estão todos na `main`
e **não existe nenhuma tag**. O pacote do grupo no GHCR ainda não foi conferido. Os workflows e o `Dockerfile` estão idênticos
ao baseline original e não precisam de alteração.

## Ambiente da validação local

Linux, Python 3.12.3, scikit-learn 1.7.2, DVC 3.67.1. O registro de Rafael usou Windows com Python 3.11.9. O CI do GitHub
usa Python 3.11 e 3.12.

## Verificações locais (25/11/2026)

| Verificação | Resultado |
|---|---|
| SHA-256 de `base_treino.csv`, `base_holdout.csv` e `model.joblib` | iguais aos de `docs/INTEGRACAO_ETAPAS_2_4.md` (`2de25aab…`, `aea4479c…`, `dde5ee49…`) |
| `python demo/local.py ci` | 7 de 7 passos: lint, formatação, validação dos dados e 43 testes |
| Cenário 1 (E2) | lint passa; **Testes de código** falha (3 testes); os demais testes passam |
| Cenário 4 (E3), CT | drift em 4 de 12 atributos; DVC executado; candidato com recall 0,9668 e precisão 0,9452 (2.200 amostras); **portão aprovado**; campeão inalterado até a promoção |
| Cenários 4 e 5 (E4), CT | candidato com recall 1,0 e precisão 0,6568; regra de precisão **FALHOU**; portão **reprovado**; hash do campeão igual antes e depois |
| API real (uvicorn) | `/health`, `/predict` e HTTP 422 para balanço de potência inválido; `demo/smoke_test.py` ok |
| Docker | não validado (indisponível no ambiente); o CD fará o build |

Os números de E3 e E4 reproduzem os de `docs/ETAPA4_JUAN.md`. As verificações de Rafael (43 testes e campeão inalterado)
foram confirmadas de forma independente.

## Gatilhos reais (conferidos nos YAMLs)

| Workflow | Dispara | Observação |
|---|---|---|
| CI | push na `main` e todo PR | também reutilizado pelo CD |
| CT | PR ou push na `main` que altere `data/raw/lotes/**` ou `params.yaml`; agenda; manual | por evento, só retreina com drift; o passo de promoção **não roda em PR** |
| CD | push de tag `v*.*.*` ou manual | CI reutilizado, build, smoke e publicação |

Um CT verde que pulou o treino e o portão **não é E3**.

## Roteiro para produzir E1 a E5

Pré-requisitos: acesso de escrita com a conta que fará o push; Actions habilitado; em Settings > Actions > General,
**Read and write permissions**. Merges com **Create a merge commit**.

### E1: CI na `main` adaptada

Em Actions > CI, filtre `branch: main` e `event: push` e abra a execução do commit `330fcf8` (ou do commit de merge mais
recente). Confira os três jobs verdes (`Lint e formatação (ruff)`, `Testes (Python 3.11)`, `Testes (Python 3.12)`) e anote a
URL, o SHA e a data. Se não houver execução verde, investigue o step que falhou, sem mudar testes nem limiares.

### E2: falha controlada

```bash
git switch main && git pull --ff-only
git switch -c e2-falha-controlada
python demo/cenarios.py aplicar 1
git add -A && git commit -m "cenario 1: remove g4 das entradas (falha controlada)"
git push -u origin e2-falha-controlada
```

Abra o PR. Esperado: **Testes de código** vermelho e lint verde. Registre a URL, **feche sem merge** e preserve a branch.

### E3: drift, retreino e portão aprovado

```bash
git switch main && git pull --ff-only
git switch -c e3-drift-aprovado
python demo/cenarios.py aplicar 4
git add -A && git commit -m "cenario 4: lote com drift (elasticidade)"
git push -u origin e3-drift-aprovado
```

No PR, o CI deve ficar verde e o CT deve **executar** o drift, o DVC e o portão (não pode estar `skipped`). Registre o
Summary (4 de 12 atributos esperados e a tabela campeão x candidato). Só chame de aprovado se o portão aprovar. O fluxo de
promoção por PR só aparece se o lote for integrado na `main` no modo com revisão; isso é uma decisão do grupo.

### E4: portão reprovado

```bash
git switch main && git pull --ff-only
git switch -c e4-portao-reprova
python demo/cenarios.py aplicar 4
python demo/cenarios.py aplicar 5
git add -A && git commit -m "cenarios 4 e 5: treinamento insuficiente (falha controlada no portao)"
git push -u origin e4-portao-reprova
```

Esperado: step **Portão de qualidade** vermelho (precisão ~0,657). Comprove que o campeão não mudou:

```bash
git rev-parse origin/main:models/champion/model.joblib
git rev-parse origin/e4-portao-reprova:models/champion/model.joblib
```

Os dois devem ser iguais (SHA-256 esperado `dde5ee49…fd34d`). **Feche sem merge.** Nenhuma tag aponta para essas branches.

### E5: tag, CD e pacote público

```bash
git switch main && git pull --ff-only
git tag -a v1.0.0 -m "primeira entrega coletiva"
git push origin v1.0.0
```

Use um commit da `main` com CI verde e não reutilize a tag da salvaguarda individual. Em Actions > CD, confira o CI
reutilizado, o build, o smoke no container e a publicação. Depois, em Packages > o pacote > Package settings > Change
visibility > **Public** (se exigir o proprietário, pedir ao Rafael). Teste sem credenciais (o nome é em minúsculas):

```bash
docker logout ghcr.io
docker pull ghcr.io/rafaellobo/mlops-estabilidade-rede-grupo:1.0.0
docker run -d -p 8000:8000 ghcr.io/rafaellobo/mlops-estabilidade-rede-grupo:1.0.0
python demo/smoke_test.py http://localhost:8000
```

Anote a tag, o digest da imagem e o resultado do smoke.

## Pendências

| Item | Responsável | Próxima ação |
|---|---|---|
| E1 a E5 | quem tiver acesso autenticado (Felipe, Victor ou Juan) | executar o roteiro acima e registrar em `docs/EVIDENCIAS.json` |
| Pacote público | proprietário do repositório, se exigir | mudar a visibilidade e testar o pull sem login |
| Contribuição de Victor | Victor | registrar o que de fato executar; nada é creditado sem commit, PR ou execução |
