# Atividade CI/CD/CT — divisão em seis etapas

**Equipe:** Rafael, Leonardo, Samara, Juan, Victor e Felipe.  
**Prazo do enunciado:** 25/11/2026.  
**Repositório coletivo:** https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo  
**Pasta local de preparação:** `C:\mlops-estabilidade-rede-grupo`.

## 1. Situação inicial e separação da salvaguarda

Este repositório contém o **projeto original da disciplina e este planejamento**. Ainda não é a entrega adaptada do grupo. A equipe precisa implementar, validar e produzir suas próprias evidências.

- Origem: https://github.com/wesleyasantos/ci_cd_ct_mlops.
- Commit consultado na origem: `371c2dfe8882aab238f2ec2f7796915eedc5aa0f`.
- Histórico próprio, repositório público, sem fork.
- Primeiro CI do projeto original: https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45421009801.
- Actions com escrita e permissão de criar PRs; `PROMOCAO_AUTOMATICA=false` inicialmente.
- O `README.md` e os dados ainda descrevem o problema original. Serão substituídos durante a adaptação.

A salvaguarda individual de Rafael permanece em **outro repositório e outra pasta**. Não deve receber os commits desta execução coletiva. Links, métricas e imagens da salvaguarda não valem como evidências de execução do grupo. A equipe pode consultar referências anteriores, declarando o uso, mas deve realizar e registrar suas próprias contribuições.

### Acesso dos integrantes

| Integrante | GitHub | Situação inicial |
|---|---|---|
| Rafael | `RafaellLobo` | Proprietário do repositório |
| Leonardo | A confirmar | Convite pendente; Rafael enviará posteriormente |
| Samara | `Samysruiz` | Convite de escrita enviado; verificar aceite |
| Juan | `juanguatierri-wq` | Convite de escrita enviado; verificar aceite |
| Victor | `VictorHugo-syss` | Convite de escrita enviado; verificar aceite |
| Felipe | `fclivati` | Convite de escrita enviado; verificar aceite |

Cada pessoa deve aceitar seu convite, configurar o Git **com a própria identidade** e realizar commits de trabalho real. Não criar commits em nome de outro integrante. A preparação inicial e este guia foram feitos por Rafael com auxílio do Codex; isso não representa contribuição já realizada pelos outros cinco participantes.

## 2. Visão geral das seis etapas

| Etapa | Responsável | Entrega principal | Dependências |
|---|---|---|---|
| 1 | **Rafael** | Base do GitHub, acordo de domínio/contrato e coordenação da integração | Primeiro CI original verde |
| 2 | **Leonardo** | Dados reproduzíveis, esquema, validação e testes de dados | Decisões da etapa 1 |
| 3 | **Samara** | Modelo, métricas, portão, testes de código/modelo e campeão inicial | Dados e contrato da etapa 2; fechamento com etapa 4 |
| 4 | **Juan** | Drift, API, smoke test, cenários e preparação de E3/E4 | Dados/modelo; E3/E4 executadas depois de E1 |
| 5 | **Victor** | CI coletivo, E1–E5 consolidadas e imagem pública do grupo | Adaptação integrada das etapas 2–4 |
| 6 | **Felipe** | Relatório, contribuição dos seis, desafio opcional e pacote de entrega | Cinco evidências obrigatórias verificadas |

**Revisões sugeridas:** Felipe revisa a etapa 1; Samara a etapa 2; Juan a etapa 3; Victor a etapa 4; Felipe a etapa 5; Rafael a etapa 6. O responsável implementa; o revisor confere evidências e limitações.

### Dependência importante: etapas não equivalem a seis PRs independentes

Dados, configuração, modelo, testes e API estão acoplados no projeto original. Trocar os CSVs isoladamente quebra o restante do contrato. Portanto:

1. A `main` começa no baseline original aprovado.
2. As etapas 2, 3 e 4 formam **uma adaptação integrada**, com commits próprios de seus responsáveis. Rafael coordena essa integração; Samara gera o campeão depois que os contratos finais estiverem compatíveis.
3. Durante o desenvolvimento local, executar `python demo/local.py ci` a cada etapa e registrar os resultados. Falhas por dependências ainda não adaptadas significam que o trabalho permanece local e não está pronto para publicação.
4. Para trabalhar sequencialmente sem publicar código quebrado, os autores podem repassar seus commits como patches Git ou trabalhar numa sessão conjunta. A integração deve preservar os autores originais, sem reescrever autoria ou fazer force push. O colega seguinte parte do trabalho anterior.
5. Publicar a branch conjunta e abrir o PR **somente quando o CI local completo passar**. Não integrar versões parciais quebradas na `main`.
6. Depois de E1, produzir as falhas intencionais E2/E4 em branches específicas, identificadas como evidência e fechadas sem merge.

Não é necessário concluir toda a etapa 4 para começar a etapa 3. Entretanto, a aprovação final do pacote das etapas 2–4 exige todas as camadas compatíveis. As evidências de CT da etapa 4 têm uma segunda passagem após Victor registrar E1.

## 3. Etapa 1 — Rafael: preparação e decisões do projeto

**Objetivo:** garantir que todos trabalhem no repositório correto e no mesmo protocolo.

### O que fazer

- Conferir o CI original verde e registrar sua URL antes de adaptar código.
- Confirmar os acessos; enviar posteriormente o convite de Leonardo.
- Discutir e registrar o problema, usuário do modelo, classe positiva, erro mais caro, métrica e limiares. Não tratar a proposta abaixo como decisão já aceita por todos.
- Registrar fonte/licença, divisões, sementes e critérios de comparação antes de avaliar no holdout.
- Coordenar a branch conjunta das etapas 2–4, preservando as contribuições de cada autor.
- Registrar decisões e limites em uma seção de planejamento do `README.md` ou em `docs/PLANEJAMENTO.md`.

### Proposta técnica inicial para discussão

Usar **Electrical Grid Stability Simulated Data**, de Vadim Arzamasov (2018), UCI, DOI https://doi.org/10.24432/C5PG66, licença **CC BY 4.0**. São 10.000 simulações e 12 atributos numéricos. Fonte: https://archive.ics.uci.edu/dataset/471/electrical+grid+stability+simulated+data.

- Problema: triagem de cenários estáveis/instáveis de uma rede elétrica simulada; uso acadêmico por pesquisadores/engenheiros.
- Positiva: `instavel=1`; `stable=0`. Falso negativo é o erro mais caro na proposta, por deixar uma instabilidade sem investigação.
- Entradas: `tau1..tau4`, `p1..p4`, `g1..g4`, nessa ordem. **Excluir `stab` e `stabf` das entradas**: `stab` determina o rótulo; `stabf` fornece a classe.
- Proposta de divisão estratificada: 6.000 treino, 2.000 holdout fixo, 2.000 reserva; semente 7.
- Proposta de contrato: recall positivo >=0,92, precisão >=0,90 e recall do candidato não inferior ao campeão **no mesmo conjunto**. Justificar como metas didáticas, sem afirmar segurança operacional comprovada.
- Confirmar que a base não foi usada em outros labs ou atribuída a outro grupo. Nos materiais locais conferidos anteriormente apareceram Iris, Wine e Breast Cancer; isso não confirma o conteúdo de materiais não disponíveis.

**Arquivos:** planejamento, referências no `README.md` e este guia se a equipe aprovar ajustes de responsabilidades.

**Critério de conclusão:** decisões aceitas e registradas, baseline verde, papéis conhecidos e acessos resolvidos ou explicitamente pendentes.

## 4. Etapa 2 — Leonardo: dados e contrato de entrada

**Objetivo:** entregar dados reproduzíveis, sem vazamento e compatíveis com o domínio escolhido.

### O que fazer

1. Obter a fonte oficial, atribuir licença e registrar hash do arquivo original. Preservar seus bytes se o hash for calculado sobre o download original.
2. Implementar a leitura/transformação reproduzível; remover `load_breast_cancer` das funções de geração e divisão.
3. Definir os atributos e o alvo em conjunto com Rafael; atualizar `config.py` e todos os consumidores com os demais responsáveis.
4. Gerar `base_treino.csv` e `base_holdout.csv` sem sobreposição; separar reserva exclusiva para lotes. Na adaptação inicial, manter `data/raw/lotes/` sem CSVs.
5. Implementar validação de ordem/esquema, tipos, nulos, infinitos, rótulos e regras físicas. Na proposta elétrica, consumidores `p2..p4` negativos são válidos; verificar balanço de potência em vez de proibir todo negativo.
6. Acrescentar **pelo menos um teste novo de dados** específico do domínio, além de adaptar os existentes. Sugestões: balanço de potência, exclusão de `stab` ou disjunção das três partições.

**Arquivos principais:** `data/raw/base_treino.csv`, `data/raw/base_holdout.csv`, fonte/proveniência em `data/source/`, `src/mlops_demo/data.py`, contrato em `src/mlops_demo/config.py` e `tests/test_dados.py`.

**Verificações:** fonte/licença/hash; número de linhas/atributos; contagens por classe; duplicatas e sobreposição; `python -m mlops_demo.data validar`; testes de dados; CI local completo com registro das dependências pendentes.

**Entregar para Samara/Juan:** fonte e script, nomes/ordem dos atributos, mapeamento das classes, partições e sementes fixadas, regras do validador e resultados reais das verificações. Não modificar posteriormente o holdout para melhorar métricas.

## 5. Etapa 3 — Samara: modelo, métricas e campeão

**Objetivo:** treinar e avaliar um modelo coerente com o contrato sem escolher parâmetros no teste.

### O que fazer

1. Adaptar `features.py` e `train.py`; manter ou substituir a regressão logística com justificativa. Preservar o nome do pacote `mlops_demo`.
2. Manter hiperparâmetros/semente no `params.yaml`; registrar versões das dependências usadas por ambiente local, Actions e Docker.
3. Se houver seleção de parâmetros, usar somente validação interna do treino. Fixar candidatos e critério; registrar tentativas e falhas. Não buscar configurações sucessivamente olhando o holdout.
4. Adaptar métricas, `pos_label` e nomes de campos no `evaluate.py`; atualizar `gate.py` e seus consumidores em conjunto com Juan.
5. Garantir que candidato e campeão sejam comparados no mesmo conjunto, com os dois pisos do contrato e a regra de não regressão de recall.
6. Adaptar `tests/test_codigo.py` e `tests/test_modelo.py`, adicionando **um teste novo por camada**. Exemplos: impedir entrada do indicador `stab`; conferir o mapeamento da positiva; comportamento direcional justificado pelo domínio.
7. Revisar com Juan as dependências do `dvc.yaml`, para invalidar o pipeline quando código/configuração relevante mudar. Versionar `dvc.lock`.
8. **Depois de Juan fechar API/cenários**, gerar o campeão inicial com `python -m mlops_demo.train --campeao`. Isso treina na base de treino; não incorporar holdout ao ajuste.

**Arquivos principais:** `src/mlops_demo/features.py`, `train.py`, `evaluate.py`, `gate.py`, `params.yaml`, testes de código/modelo, `models/champion/` e dependências pertinentes no DVC/ambiente.

**Verificações:** testes de código/modelo, baseline ingênuo, probabilidades, repetibilidade no ambiente, métricas medidas e CI completo após integrar a etapa 4. Registrar limitações entre plataformas; não prometer determinismo universal.

**Critério de conclusão:** código e parâmetros rastreáveis, métricas honestas, campeão compatível com a API e pacote conjunto das etapas 2–4 apto a passar o CI antes do push.

## 6. Etapa 4 — Juan: drift, API e cenários de CT

**Objetivo:** completar a adaptação operacional e preparar os casos de aprovação/reprovação do CT.

### Primeira passagem: implementação

1. Adaptar `aplicar_drift`, geração de lotes e `monitor.py`; definir atributos monitorados e `MIN_FEATURES_DRIFT` para o novo esquema.
2. Na proposta elétrica, selecionar casos da reserva com maior elasticidade média é uma opção de mudança de distribuição que preserva medições/rótulos. Não multiplicar atributos arbitrariamente mantendo rótulos como se fossem verdade física comprovada.
3. Garantir que lotes não reutilizem amostras de treino/holdout nem repitam registros já enviados em outro lote. Dividir cada lote em treino/avaliação com protocolo fixo.
4. Adaptar `api.py`: quantidade/ordem dos atributos, campos de resposta, classe positiva e validação das entradas. Para a proposta elétrica, são 12 entradas, não 30.
5. Atualizar `demo/smoke_test.py` e `tests/test_api.py`; acrescentar **pelo menos um teste novo de API** específico, como rejeitar estado fisicamente impossível com HTTP 422.
6. Reescrever os cenários 1–5 em `demo/cenarios.py`: perda de atributo, dados inválidos, configuração ruim, drift e desequilíbrio de recall/precisão.
7. Entregar os contratos finais a Samara para gerar o campeão. Rafael coordena o CI integral antes de publicar a adaptação conjunta.

**Arquivos principais:** `src/mlops_demo/data.py` (parte de lotes/drift, coordenada com Leonardo), `monitor.py`, `api.py`, `demo/gerar_lote.py`, `smoke_test.py`, `cenarios.py` e `tests/test_api.py`.

### Segunda passagem: evidências de CT, depois de E1

- **E3:** abrir PR com lote válido e drift, executar o CT e registrar Summary com drift e tabela do portão. Só chamar de aprovado se o portão realmente aprovar.
- **E4:** criar outra branch/PR que faça o portão reprovar por recall/precisão insuficiente. Demonstrar que a falha é no portão e que o campeão não mudou, registrando hash/commit antes e depois.
- Não enfraquecer limiares, alterar holdout ou esconder tentativas para obter verde. Se o candidato perder para o campeão, registrar a reprovação e discutir o próximo passo com o grupo.
- Entregar URLs e resultados para Victor/Felipe. Fechar PRs de falhas sem merge; nenhuma tag de entrega deve apontar para uma falha controlada.

**Critério de conclusão:** API e smoke adaptados, novo teste de API, cinco cenários funcionais, E3/E4 verificadas no repositório do grupo com seus resultados reais.

## 7. Etapa 5 — Victor: CI, CD e consolidação de E1–E5

**Objetivo:** provar que a adaptação coletiva funciona no GitHub e que a imagem é pública e executável.

### O que fazer

1. Após o CI local conjunto passar, revisar o PR de adaptação e integrar à `main` com seus checks aprovados. Registrar **E1: os três jobs verdes** na main adaptada; o primeiro CI do projeto original não substitui E1.
2. Criar branch/PR de **E2**, aplicando um cenário adaptado de falha controlada. Conferir o step que falhou; erro de instalação/rede não substitui a falha planejada. Fechar sem merge após registrar a execução.
3. Conferir com Juan **E3 e E4**, seus Summaries, métricas e preservação do campeão na reprovação.
4. Sobre commit aprovado da main, criar a tag da primeira entrega coletiva, por exemplo `v1.0.0`. Essa tag pertence a este repositório; não reaproveitar a tag/evidência da salvaguarda.
5. Acompanhar **E5: CD verde**, incluindo CI reutilizado, build, smoke no container e publicação no GHCR.
6. Tornar o pacote do grupo público em Packages e confirmar o pull sem credenciais, seguido do smoke test. Se a permissão de pacote exigir o proprietário, solicitar que Rafael execute essa configuração.
7. Entregar para Felipe as cinco URLs, PRs, commit/tag e página do pacote. Não produzir números ou prints sem execução correspondente.

**Arquivos principais:** `.github/workflows/ci.yml`, `ct.yml`, `cd.yml`, `Dockerfile`, `demo/smoke_test.py` e registro de evidências em `docs/`. Alterar workflows somente se houver necessidade demonstrada; não fazer mudanças cosméticas para gerar commits.

### Mapa de evidências

| Evidência | Responsável pela produção | Quem consolida | Estado inicial |
|---|---|---|---|
| E1 — main adaptada com três jobs CI verdes | Victor, após integração conjunta | Felipe | Pendente |
| E2 — CI vermelho controlado em PR | Victor | Felipe | Pendente |
| E3 — drift e portão aprovado | Juan | Victor/Felipe | Pendente |
| E4 — portão reprovado, campeão inalterado | Juan | Victor/Felipe | Pendente |
| E5 — tag, CD e imagem pública | Victor | Felipe | Pendente |
| Bônus — CT promove, cria tag e dispara CD | Felipe, com revisão de Rafael | Felipe | Pendente; opcional |

**Critério de conclusão:** E1–E5 verificáveis, imagem pública do grupo funcionando e referência precisa entre commits, tag e execuções.

## 8. Etapa 6 — Felipe: relatório, bônus e entrega final

**Objetivo:** entregar uma síntese fiel ao que o grupo implementou e executou.

### O que fazer

1. Finalizar `README.md` para o novo problema, com ambiente, contrato da API e reprodução compatíveis com o código.
2. Criar `ADAPTACAO.md` na raiz, com **no máximo duas páginas**, cobrindo: problema/fonte/licença/tamanho; contrato e justificativa; mudanças por arquivo; URLs E1–E5; limites/monitoramento; contribuições dos seis e uso de IA.
3. Registrar a contribuição de cada integrante com links para commits/PRs. O uso do Codex na preparação e demais usos de IA devem ser declarados. Não atribuir execução a quem apenas recebeu uma tarefa.
4. Conferir os links logado e, quando aplicável, sem login. Verificar que todos apontam ao repositório/pacote do grupo.
5. Preparar o texto de envio ao D2L com repositório, cinco execuções e página/print do pacote. A equipe define uma única pessoa para o envio; não presumir que criar esse arquivo já envia a atividade.

### Desafio opcional, depois de E1–E5

- Com revisão de Rafael, definir `PROMOCAO_AUTOMATICA=true` e conferir a condição da main sem proteção exigida pela demonstração. Até lá, manter `false`.
- Usar um candidato/lote validado para que o próprio CT aprove o portão, atualize o campeão, crie a próxima tag e dispare o CD. Não criar manualmente a tag/CD e chamar isso de automação do CT.
- Comprovar autoria do commit do robô, tag apontando para o campeão promovido e CD disparado pelo workflow. Validar a imagem publicada.
- Explicar benefícios (rapidez e rastreabilidade) e riscos (main sem proteção, ausência de revisão humana, limites das métricas e necessidade de rollback/aprovação em produção).
- Registrar falhas/tentativas e o estado final da variável. A realização do bônus do repositório individual não conclui o bônus deste repositório coletivo.

**Arquivos principais:** `README.md`, `ADAPTACAO.md`, evidências em `docs/` e texto final de entrega. Evidências do bônus também devem ser próprias do grupo.

**Critério de conclusão:** relatório dentro do limite, seis contribuições reais rastreáveis, E1–E5 válidas e pacote público; bônus documentado se executado; envio ao D2L confirmado pela pessoa responsável.

## 9. Fluxo mínimo de trabalho e encerramento

Cada pessoa clona **o repositório coletivo** e usa sua conta:

```powershell
git clone https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo.git
cd mlops-estabilidade-rede-grupo
git config --local user.name "SEU NOME"
git config --local user.email "SEU EMAIL VERIFICADO OU NOREPLY DO GITHUB"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,ct]"
python demo/local.py ci
```

Use um Python compatível com as dependências adotadas pela equipe; a proposta é Python 3.11 para coincidir com Docker/CT. Não compartilhar `.venv`, tokens, senhas ou arquivos `.env`. Se a ativação do PowerShell for bloqueada, é possível chamar `.\.venv\Scripts\python.exe` diretamente, sem alterar globalmente a política do computador.

Para mudanças publicáveis e já validadas:

```powershell
git switch main
git pull --ff-only
git switch -c etapa-N-seu-nome
# implementar e executar as verificações da etapa
python demo/local.py ci
# revisar git diff; adicionar somente os arquivos da tarefa
git add CAMINHOS_DOS_ARQUIVOS
git commit -m "tipo: descreve a contribuicao real"
git push -u origin etapa-N-seu-nome
# abrir PR com mudança, validações e limitações
```

Esse roteiro se aplica quando o conjunto já passa no CI. Para as etapas 2–4 acopladas, usar a integração local conjunta descrita no início; não publicar os estados incompletos. E2/E4 são exceções intencionais, com branch/PR de evidência e falha identificada.

### Checklist de entrega coletiva

- [ ] Decisões do grupo registradas antes da avaliação final.
- [ ] Dados elegíveis, licença atribuída e partições sem vazamento.
- [ ] Quatro camadas de testes adaptadas e um novo teste específico por camada.
- [ ] Campeão, DVC, API e cinco cenários adaptados.
- [ ] E1–E5 produzidas neste repositório; pacote do grupo público e testado.
- [ ] Rafael, Leonardo, Samara, Juan, Victor e Felipe com contribuições reais no histórico.
- [ ] `ADAPTACAO.md` final, até duas páginas, com uso de IA declarado.
- [ ] Desafio opcional documentado, se realizado pelo grupo.
- [ ] Um único envio da equipe confirmado no D2L até o prazo.

**Este arquivo é um plano de execução, não uma declaração de conclusão das etapas.** Atualizar os estados somente após conferir as entregas e suas evidências.
