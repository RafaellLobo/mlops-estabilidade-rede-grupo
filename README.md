# Estabilidade de rede elétrica: CI/CD/CT para ML

> **Fechamento técnico:** E1–E5 e bônus comprovados; [evidências](docs/FECHAMENTO_ENTREGA.md), [contribuições](docs/CONTRIBUICOES.md) e [texto para D2L](ENTREGA_D2L.txt). Imagens públicas `1.0.0`/`1.1.0` com pull anônimo e smoke aprovados. Campeão atual promovido pelo robô na `v1.1.0`: recall 0,9668 e precisão 0,9452 em 2.200 linhas; os números do campeão inicial abaixo são históricos. Promoção automática restaurada para `false`.

**Equipe da entrega:** Rafael, Leonardo, Samara, Juan e Felipe. Todos possuem commits próprios comprovados em [docs/CONTRIBUICOES.md](docs/CONTRIBUICOES.md). [Relatório em PDF de duas páginas](ADAPTACAO.pdf).

Projeto de demonstração de MLOps que mostra como um modelo de machine learning é testado, retreinado e entregue de forma
automática. Usa **GitHub Actions**, **pytest**, **ruff**, **DVC**, **FastAPI**, **Docker** e **GitHub Container Registry**.

O modelo classifica o estado de uma **rede elétrica simulada de quatro nós** como *estável* ou *instável*, para apoiar a
triagem de cenários. A classe de interesse é a **instável** (`instavel = 1`): deixar passar uma instabilidade (falso
negativo) é o erro mais caro, então medimos **recall** e **precisão** dessa classe. É uma demonstração acadêmica com dados
simulados, sem operação de rede real.

Adaptado do projeto de demonstração da disciplina, que classificava tumores de mama (Breast Cancer, scikit-learn) e serviu
de modelo para a estrutura de CI/CD/CT.

> Relatório de adaptação (até duas páginas): [ADAPTACAO.md](ADAPTACAO.md). Metodologia: [docs/PROTOCOLO.md](docs/PROTOCOLO.md). Evidências oficiais: [docs/EVIDENCIAS.json](docs/EVIDENCIAS.json). Autoria e uso de IA: [docs/CONTRIBUICOES.md](docs/CONTRIBUICOES.md).

## Dados

Fonte: *Electrical Grid Stability Simulated Data* (Arzamasov, 2018), UCI Machine Learning Repository,
[DOI 10.24432/C5PG66](https://doi.org/10.24432/C5PG66), licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
O arquivo original fica em `data/source/` (SHA-256 conferido na carga). São 10.000 simulações, divididas em
**6.000 de treino**, **2.000 de holdout** e **2.000 de reserva** (a reserva só gera lotes novos e não é gravada em disco).

Os 12 atributos de entrada são:

| Grupo | Atributos | Faixa física |
|---|---|---|
| Tempo de reação dos participantes | `tau1` a `tau4` | 0,5 a 10 |
| Potência (produção > 0, consumo < 0) | `p1` (produtor), `p2` a `p4` (consumidores) | `p1` 1,5 a 6; `p2` a `p4` -2 a -0,5 |
| Elasticidade do preço | `g1` a `g4` | 0,05 a 1 |

A potência é um sistema fechado: **`p1 + p2 + p3 + p4 = 0`** (tolerância 1e-8). As colunas `stab` e `stabf` da fonte são
alvos e **nunca** entram como atributo. O alvo é `instavel` (`stabf = "unstable"` vira `1`).

## O que cada letra faz neste projeto

| Letra | Workflow | Quando dispara | O que faz |
|---|---|---|---|
| **CI** | `.github/workflows/ci.yml` | push na `main` e todo Pull Request | lint, validação dos dados, testes de código, dados, modelo e API (Python 3.11 e 3.12) |
| **CT** | `.github/workflows/ct.yml` | agenda semanal e execução manual (sempre retreinam); lote novo ou `params.yaml` alterado (retreinam só se houver drift) | detecta drift, retreina com DVC, aplica o portão de qualidade e propõe o novo campeão em um PR (ou, no modo automático, publica direto e cria a tag) |
| **CD** | `.github/workflows/cd.yml` | tag `v*.*.*` | roda o CI, constrói a imagem Docker, faz o teste de fumaça e publica no `ghcr.io` |

## Estrutura

```
.github/workflows/     ci.yml, ct.yml, cd.yml
src/mlops_demo/        config, data, features, selecao, evaluate, train, gate, monitor, api
tests/                 test_codigo, test_dados, test_modelo, test_api
data/source/           arquivo original da UCI e atribuição
data/raw/              base_treino.csv, base_holdout.csv e lotes/ (lotes novos chegam aqui)
models/champion/       o modelo em produção (versionado no Git)
params.yaml            hiperparâmetros e candidatos da seleção interna
dvc.yaml               pipeline: preparar e treinar
Dockerfile             imagem da API com o modelo campeão
demo/                  cenários de prática, gerador de lotes, teste de fumaça e execução local
docs/                  protocolo, integração, registros técnicos e índice de evidências
```

## Contrato de qualidade

Definido em `src/mlops_demo/config.py` e aplicado pelo portão (`gate.py`):

- recall da classe instável **>= 0,92**;
- precisão da classe instável **>= 0,90** (sem ela, um modelo que chuta tudo como instável teria recall 1,0);
- o candidato não pode ter recall menor que o do campeão, medido **no mesmo conjunto**;
- gatilho de drift: teste KS com p < 0,01 em pelo menos **2 dos 12** atributos.

O campeão inicial da `v1.0.0` foi um `HistGradientBoostingClassifier`, escolhido por seleção interna 80/20 só da base de treino. No holdout de 2.000 linhas: recall 0,9632 e precisão 0,9505. O campeão atual, promovido pelo CT na `v1.1.0`, tem recall 0,9668 e precisão 0,9452 na avaliação ampliada de 2.200 linhas (`models/champion/metrics.json`). Os conjuntos são diferentes; os números não constituem uma comparação direta de ganho.

## API

`GET /health` devolve o estado e as métricas do campeão. `POST /predict` recebe os 12 atributos, **nesta ordem**
(`tau1..tau4`, `p1..p4`, `g1..g4`):

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"atributos": [5, 5, 5, 5, 3, -1, -1, -1, 0.5, 0.5, 0.5, 0.5]}'
```

```json
{"classe": "instavel", "probabilidade_instavel": 1.0, "versao_codigo": "0.1.0"}
```

A API responde **HTTP 422** para entrada fisicamente impossível: quantidade diferente de 12 valores, valor fora da faixa
física ou balanço de potência diferente de zero.

---

# Passo a passo

## Parte 1. Rodar na sua máquina (sem GitHub)

Pré-requisitos: Python 3.11 (o mesmo do Docker e do CT; o projeto aceita 3.10 ou superior) e Git. Docker é opcional.

**1. Crie e ative o ambiente virtual.**

```bash
python -m venv .venv
source .venv/Scripts/activate        # Git Bash no Windows
# PowerShell:  .venv\Scripts\Activate.ps1
# Linux e macOS: source .venv/bin/activate
```

**2. Instale o projeto.**

```bash
pip install -e ".[dev,ct]"
```

**3. Confira os dados.** As bases de `data/raw/` já vêm no repositório. Para regenerá-las a partir da fonte:

```bash
python -m mlops_demo.data base
```

**4. Rode o CI inteiro.** Deve terminar com os sete passos `[ok]`.

```bash
python demo/local.py ci
```

**5. Rode o CT inteiro** (drift, retreino com DVC e portão de qualidade, sem abrir PR).

```bash
python demo/local.py ct
```

Sem lote novo em `data/raw/lotes/`, o monitor não encontra drift para comparar. Use os cenários da Parte 3.

**6. Suba a API e teste.**

```bash
uvicorn mlops_demo.api:app --reload
# em outro terminal, com o ambiente ativo:
python demo/smoke_test.py http://localhost:8000
```

**7. (Opcional) Construa a imagem Docker.**

```bash
docker build -t mlops-demo .
docker run -p 8000:8000 mlops-demo
```

> O `dvc repro` usa o `python` do PATH. Se o ambiente virtual não estiver ativo, ele falha com
> `No module named 'mlops_demo'`.

## Parte 2. Colocar o projeto no GitHub

Este repositório já está em `RafaellLobo/mlops-estabilidade-rede-grupo`. Para repetir em outro repositório:

**1. Crie o repositório.** Público e **vazio** (sem README). Repositório público tem Actions gratuito.

**2. Configure o Git somente nesta pasta** (sem `--global`) e envie o projeto.

```bash
git init
git config --local user.name  "Seu Nome"
git config --local user.email "seu-email@exemplo.com"
git config --local core.autocrlf false
git add -A
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git commit -m "projeto inicial"
git push -u origin main
```

**3. Confirme o primeiro CI.** Na aba **Actions**, o CI roda sozinho e deve ficar verde nos três jobs
(`Lint e formatação (ruff)`, `Testes (Python 3.11)` e `Testes (Python 3.12)`).

**4. Libere o CT para abrir Pull Requests.** Em **Settings > Actions > General > Workflow permissions**, selecione
**Read and write permissions** e marque **Allow GitHub Actions to create and approve pull requests**. Sem isso o CT cria
a branch `ct/novo-campeao`, mas não abre o PR.

**5. Escolha como o CT promove um modelo novo.** Em **Settings > Secrets and variables > Actions > Variables**, crie a
variável `PROMOCAO_AUTOMATICA`:

| Valor | Modo | O que o CT faz quando o portão aprova |
|---|---|---|
| `false` (padrão) | com revisão | abre um Pull Request e uma pessoa decide |
| `true` | automático | publica na `main`, cria a tag da versão e dispara o CD, sem ninguém |

Sem a variável, vale o modo com revisão. **Com `true`, a `main` não pode exigir Pull Request**, porque o CT grava nela
direto.

**6. (Opcional) Proteja a `main`.** Em **Settings > Branches**, exija Pull Request e os três checks do CI. A regra é
incompatível com o modo automático.

## Parte 3. Prática com cinco cenários

Para reproduzir E2–E4, parta da tag `v1.0.0`: a main já recebeu o lote e o campeão do bônus. Cada cenário muda uma coisa no projeto. **Antes de rodar, tente prever** o que vai falhar e em qual etapa.
Troque `N` pelo número do cenário.

```bash
git switch main && git pull
git switch -c cenario-N v1.0.0
python demo/cenarios.py aplicar N
git add -A
git commit -m "cenario N"
git push -u origin cenario-N
```

Abra o Pull Request e acompanhe a aba **Checks**. Ao terminar, feche o PR **sem fazer merge** e volte:

```bash
git switch main
# Preserve a branch para rastreabilidade da evidencia.
```

| N | O que muda | O que você deve observar |
|---|---|---|
| 1 | remove `g4` das entradas do modelo | CI vermelho em **Testes de código** (3 testes falham) |
| 2 | 5 nulos em `tau1` e 3 valores negativos em `tau2` na base de treino | CI vermelho em **Validar os dados brutos**, antes do treino |
| 3 | `max_iter: 1` no `params.yaml` | CI vermelho em **Testes de modelo** (o contrato não é cumprido) |
| 4 | lote de 400 registros de maior elasticidade (`g1..g4`) e peso 1,5 na classe instável | CI verde. O drift aparece no **CT** (4 de 12 atributos) |
| 5 | `max_iter: 1`, aplicado **depois do 4** | CT com **portão reprovado**: recall 1,0, mas precisão 0,657 (< 0,90). O campeão não muda |

Para listar os cenários: `python demo/cenarios.py listar`.

> Os cenários 3 e 5 fazem a mesma alteração no `params.yaml`. O que muda é onde ela é percebida: no 3, pelos testes de
> modelo do CI; no 5, pelo portão do CT, sobre o lote do cenário 4.

### Cenário 4: o treinamento contínuo

O lote novo é feito de registros reais da reserva com maior elasticidade média: os atributos e rótulos ficam intactos,
só a distribuição muda. O CI continua verde, porque os dados são válidos. Quem reage é o **CT**.

1. No PR do cenário 4, abra o workflow **CT** e o **Summary** do run: relatório de drift e tabela do portão
   (campeão x candidato).
2. Se o portão aprovar e você fizer merge na `main`, o CT roda de novo e abre o PR
   **"ct: novo modelo campeão aprovado no portão de qualidade"**.
3. O CI desse PR aparece como **Action required**, porque o PR foi aberto pelo `GITHUB_TOKEN`. Abra o PR e clique em
   **Approve and run workflows**.
4. Revise o PR (só `models/champion/` muda) e faça o merge. O CT propõe, uma pessoa decide.

### Cenário 4, modo automático

Com `PROMOCAO_AUTOMATICA = true` e a `main` sem exigência de Pull Request, o CT publica o campeão aprovado na `main`, cria a
tag da nova versão e dispara o CD. Passos:

1. Confirme **Read and write permissions** em Settings > Actions > General e que a `main` não exige Pull Request.
2. Troque a variável `PROMOCAO_AUTOMATICA` para `true`.
3. Na `main` atualizada: `python demo/cenarios.py aplicar 4`, depois `git add -A`, commit e `git push origin main`.
4. Acompanhe a aba **Actions**: o **CT** detecta o drift, retreina, o portão aprova, o robô commita
   **"ct: promove novo modelo campeão (portão aprovado)"** e cria a tag; o **CD** constrói, testa e publica a imagem.

Se o portão reprovar, nada é publicado e o modelo anterior continua em produção. Se o campeão não mudar, não há versão nova.
A cada novo campeão a versão sobe um nível (`v1.0.0`, `v1.1.0`, ...). Para voltar ao modo com revisão, troque a variável
para `false`.

### Entrega (CD): tag e imagem

Com a `main` verde, crie uma tag de versão:

```bash
git switch main && git pull
git tag v1.0.0
git push origin v1.0.0
```

O **CD** roda o CI, constrói a imagem, faz o teste de fumaça no container e só então publica no `ghcr.io`. Depois, em
**Packages**, abra o pacote e mude a visibilidade para **Public** (Package settings > Change visibility). O nome da imagem
é sempre em minúsculas:

```bash
docker run -p 8000:8000 ghcr.io/rafaelllobo/mlops-estabilidade-rede-grupo:1.0.0
python demo/smoke_test.py http://localhost:8000
```

## Comandos úteis

| Comando | Para que serve |
|---|---|
| `python -m mlops_demo.data base` | regenera `base_treino.csv` e `base_holdout.csv` a partir da fonte UCI |
| `python -m mlops_demo.data validar` | valida esquema, faixas físicas e balanço de potência dos CSVs de `data/raw/` |
| `python -m mlops_demo.selecao` | seleção interna 80/20 entre os candidatos do `params.yaml` |
| `python -m mlops_demo.monitor` | compara os lotes novos com a base (teste KS) e diz se o gatilho dispara |
| `dvc repro` | roda `preparar` e `treinar`, refazendo só o que mudou |
| `python -m mlops_demo.gate` | compara candidato e campeão. Sai com código 1 se reprovar |
| `python -m mlops_demo.gate --promover` | copia o candidato para `models/champion/` |
| `python demo/cenarios.py listar` | lista os cenários de prática |
| `python demo/gerar_lote.py lote_02 --drift 0.25 --n 120` | gera um lote novo da reserva (`--drift` é a fração de maior elasticidade) |

## Se algo der errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Jobs falham em 2 segundos, sem passos | conta do GitHub com problema de cobrança | corrija em Settings > Billing e reexecute |
| CI falha em "Validar os dados brutos" com colunas `mean radius...` | CSVs antigos (Breast Cancer) em `data/raw/` | `python -m mlops_demo.data base` e commite os dois CSVs |
| CT passa, mas não há PR | permissão do passo 4 da Parte 2 desligada | ligue a permissão e rode o CT de novo (Actions > CT > Run workflow) |
| CI do PR do campeão em "Action required" | PR aberto pelo `GITHUB_TOKEN` | clique em **Approve and run workflows** |
| Modo automático: falha ao enviar para a `main` | a `main` exige Pull Request | desligue a proteção |
| Modo automático ligado, mas o CT abriu um PR | variável com outro nome ou valor diferente de `true`, ou execução fora da `main` | confira o nome, o valor e a aba Variables |
| `dvc repro` falha com "No module named" | ambiente virtual inativo | ative o ambiente e rode de novo |
| `dvc repro` falha com "is git-ignored" | `dvc.lock` no `.gitignore` | não ignore o `dvc.lock` |
| Números do modelo diferentes dos documentados | versão do scikit-learn diferente | o `pyproject.toml` fixa `scikit-learn==1.7.2` |
| Cenário não aplica ("trecho não encontrado") | a mudança já foi aplicada nesta branch | volte à `main` e crie outra branch |
| `docker pull` pede login | pacote ainda privado | mude a visibilidade para Public em Package settings |

## Limites e observações

- Os dados são **simulados** (UCI) e pequenos, e ficam no Git. Em um projeto real, use `dvc add` com um *remote*.
- Os limiares de recall e precisão são metas didáticas, não garantia de segurança elétrica nem requisito operacional.
- O lote de drift seleciona registros de maior elasticidade média; é uma mudança de distribuição simulada, não um evento real.
- O `GITHUB_TOKEN` padrão basta aqui. Em produção, o PR de promoção costuma usar um *GitHub App* ou token dedicado.
