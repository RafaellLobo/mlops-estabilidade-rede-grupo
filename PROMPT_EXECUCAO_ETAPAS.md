# Prompt operacional — execução e fechamento das seis etapas

## 1. Como o integrante deve acionar a IA

Abra o clone **atualizado** de `RafaellLobo/mlops-estabilidade-rede-grupo` na ferramenta de IA. Este arquivo é o roteiro de trabalho; ele não executa comandos sozinho nem concede acesso ao GitHub. A IA precisa de ferramentas, autenticação e permissões. Instruções de sessão, regras de segurança e autorizações do usuário continuam valendo.

`AGENTS.md` aponta para este guia no Codex. `CLAUDE.md` importa o mesmo arquivo de entrada no Claude Code. Se a ferramenta não carregar essas instruções, anexe este Markdown ou mande lê-lo explicitamente. Não é possível garantir a leitura automática em qualquer chat de IA.

Os arquivos de entrada precisam existir na branch aberta. Se você está numa branch antiga que ainda não os contém, não descarte seu trabalho nem mude de base às cegas: anexe este Markdown, use sua versão na main pelo GitHub ou peça à IA que leia `git show origin/main:PROMPT_EXECUCAO_ETAPAS.md` depois de atualizar as referências. Esse comando só lê o arquivo remoto conhecido e não altera a árvore de trabalho.

**Frase completa recomendada** — troque nome, conta e etapa:

> Sou Samara, minha conta é Samysruiz. Leia PROMPT_EXECUCAO_ETAPAS.md, ETAPAS_GRUPO.md e docs/PLANEJAMENTO.md. Execute e finalize a etapa 3 atribuída a mim: confira o estado atual, reaproveite o trabalho existente, faça somente as correções necessárias, execute as verificações, registre os resultados, faça os commits com minha identidade e publique o PR. Acompanhe os checks e registre as URLs reais. Respeite as dependências e não declare conclusão enquanto faltar um critério. Não integre na main nem publique imagem fora da autorização da minha etapa.

Com as instruções do projeto carregadas e a identidade inequívoca, uma frase curta como **“Execute e finalize a terceira etapa que foi designada a mim”** deve ser interpretada pelo roteiro abaixo. Se publicação, merge, tag ou configuração ainda não estiverem autorizados pelas instruções do usuário/sessão, prepare tudo até ficar revisável e peça somente a autorização que faltar. Nunca contorne a sandbox.

### Identificação

| Etapa | Pessoa | Conta conhecida | Registro da etapa |
|---|---|---|---|
| 1 | Rafael | `RafaellLobo` | `docs/PLANEJAMENTO.md` |
| 2 | Leonardo | `le0zinn1316` | `docs/ETAPA2_LEONARDO.md` |
| 3 | Samara | `Samysruiz` | `docs/ETAPA3_SAMARA.md` |
| 4 | Juan | `juanguatierri-wq` | `docs/ETAPA4_JUAN.md` |
| 5 | Victor | `VictorHugo-syss` | `docs/ETAPA5_VICTOR.md` |
| 6 | Felipe | `fclivati` foi a conta informada; `felipebpkedu` aparece em commits | `docs/ETAPA6_FELIPE.md` |

Felipe deve confirmar sua conta atual; não presumir que duas contas pertencem à mesma pessoa. Comparar pessoa declarada, conta autenticada e autoria Git antes de escrever commits. Se houver divergência sem explicação/autorização, pedir a identificação correta. Nunca fabricar autoria, configurar outra pessoa para gerar commits ou atribuir ao colega testes executados por você.

## 2. Instrução central à IA

Você é responsável por **executar o trabalho da pessoa que o acionou**, não apenas sugerir um plano. Trabalhe até entregar os artefatos, verificações, PR e evidências exigidos pela etapa, dentro das autorizações disponíveis. Responda em português brasileiro e sem emojis.

Antes de alterar arquivos:

1. Leia este guia, `ETAPAS_GRUPO.md`, `docs/PLANEJAMENTO.md`, o registro da etapa e os workflows reais em `.github/workflows/`.
2. Confira remoto, branch, alterações locais, PRs, commits e runs recentes. A documentação pode estar desatualizada: estado atual do código e Actions são a evidência principal.
3. Preserve trabalho local não registrado e contribuições dos colegas. Não executar reset, rebase, force push, exclusão ou sobrescrita de resultados para conseguir uma árvore limpa.
4. Confirme identidade e ferramentas. Com GitHub CLI, use `gh auth status`, `gh api user --jq .login`, `git config --local user.name` e `git config --local user.email`; não exponha tokens, segredos ou emails em relatórios públicos.
5. Examine branches existentes antes de escolher a base. Não refaça a implementação de uma etapa já publicada nem volte a uma branch antiga que perderia correções dos colegas.
6. Apresente brevemente arquivos que pretende tocar, dependências e verificações. Continue a execução autorizada; não pare somente no plano.

**Limites:** este roteiro não autoriza ações fora da etapa, mudanças globais no computador, instalação indiscriminada de dependências, treino longo, nova busca de modelos, mudanças de holdout/limiares, publicação de dados sensíveis ou envio de mensagens aos colegas. Reutilize o ambiente do projeto. Instalações necessárias, autenticação e elevação de acesso obedecem às permissões da sessão.

### Fotografia de partida, não estado permanente

Na conferência de **25/11/2026**, a main estava em `ccc84c2`, ainda no baseline original. A branch **`integracao-etapas-2-4`**, em `e3dfe49`, reunia dados regenerados, modelo, API e cenários. O PR #4 de Leonardo era anterior à integração e tinha falhas de lint/dados. Existiam registros locais de Samara/Juan, mas faltavam E1–E5 oficiais, tag, CD, `dvc.lock` e `ADAPTACAO.md`.

As branches `codex/integracao-estabilidade-rede` e as individuais não devem ser consideradas mais novas só pelo nome. A IA deve atualizar essa avaliação pelos SHAs/ancestralidade. **Não restaurar a main antiga sobre a implementação existente.** Esta fotografia não é uma ordem para refazer commits nem uma certificação de que algo permanece pendente hoje.

### Protocolo científico obrigatório

- Preservar fonte/licença e SHA-256; 12 entradas elétricas e alvo `instavel`, positiva `1`; excluir `stab`/`stabf` das entradas.
- Preservar treino/holdout/reserva e sementes definidos no planejamento. Não ajustar modelos com base no holdout nem mudar divisões/limiares para obter verde.
- Preservar recall mínimo 0,92, precisão mínima 0,90 e comparação com campeão no mesmo conjunto, salvo decisão de protocolo explicitamente autorizada e documentada.
- Distinguir resultados medidos agora, registros históricos dos colegas e hipóteses. Não copiar métricas esperadas para arquivos de resultado.
- Não repetir seleção de parâmetros porque uma métrica de teste desagradou. Revisão metodológica exige decisão explícita, justificativa e registro das limitações. Manter no relatório as tentativas e a reutilização de avaliação já reconhecidas por Juan.
- Não sobrescrever campeão histórico, fonte ou resultados importantes sem autorização. Versionamento anterior e tags devem permanecer rastreáveis.

## 3. Fluxo comum de desenvolvimento e PR

### Base e autoria

- Repositório de trabalho: **`RafaellLobo/mlops-estabilidade-rede-grupo`**. Não modificar a salvaguarda individual nem usar seus links como evidências coletivas.
- Para finalizar etapas 2–4, preferir a implementação conjunta mais recente após conferir seu conteúdo. Se `integracao-etapas-2-4` ainda for a branch ativa, criar a branch de finalização a partir dela e abrir PR **para ela**. Registrar o SHA base. Se a main já incorporou a adaptação, partir da main atual.
- Usar branch própria, por exemplo `samara/finalizacao-etapa-3`. Reaproveitar PR existente quando ele corresponder ao mesmo trabalho; não criar duplicatas.
- Se os commits próprios já estão na integração, não os reaplicar nem criar um commit cosmético para “marcar presença”. Revisão técnica, correção necessária e registro de resultados reais são contribuições válidas; identificar quem fez cada ação.
- Com vários participantes, conferir a base novamente antes de integrar. Não substituir uma branch compartilhada por um snapshot local antigo. Resolver divergências de forma revisável, preservando autores.

### Verificações locais

Com o ambiente correto e versões compatíveis, executar os comandos aplicáveis e registrar saída/código de retorno:

```text
python -m mlops_demo.data validar
python demo/local.py ci
python demo/local.py ct
git diff --check
```

O CI local cobre lint, formatação e testes de código/dados/modelo/API. O CT local executa DVC e portão e só deve ser chamado quando relevante à etapa e autorizado; ele faz um treino curto do projeto. Em Windows, ativar a `.venv` para que o `python` usado pelo DVC seja o mesmo. Sem ativação, chamar um executável isolado na frente não corrige automaticamente o PATH do processo filho.

Não instalar pacotes no ambiente global. Não executar todos os experimentos da equipe em cada etapa. Para mudança somente documental, verificar links, JSON, formatação relevante e diff; não treinar modelo sem necessidade.

O formato dos exemplos Python dentro de Markdown também pode ser verificado pelo Ruff atual. Não ignorar uma falha documental como se o CI inteiro tivesse passado.

### Publicação e acompanhamento

Após as verificações locais pertinentes passarem, revisar o diff, adicionar somente arquivos da tarefa, criar commits com autoria real, enviar a branch e criar/atualizar o PR para a base correta. Corpo do PR deve conter: mudança, dependências, comandos executados, resultados, limitações e ligação com a etapa. Preferir `--body-file` para descrições multilinha.

```text
gh pr create --base BASE_VALIDADA --head SUA_BRANCH --title "Etapa N: resumo" --body-file CAMINHO_DO_CORPO
gh pr checks NUMERO_DO_PR --watch --interval 10
```

Esses são modelos: preencher valores reais, sem executar placeholders. Ferramentas equivalentes por conector/interface também podem ser usadas. Se faltarem acesso ou permissões, entregar o diff/registro concreto e explicar a ação exata que o usuário deve realizar; não alegar que o PR foi criado.

Ler o log do **step que falhou**. Corrigir somente causas dentro do escopo e repetir a verificação pertinente. Não renomear uma falha de instalação/integração como E2 ou E4. Não aceitar `skipped`, `cancelled` ou `action_required` como aprovação do critério solicitado.

**Exceção deliberada de E2/E4:** antes de publicar a branch de evidência, confirmar localmente a falha esperada. O vermelho intencional é o resultado a demonstrar nesse experimento, com PR claramente identificado e sem merge. Essa exceção não libera o envio de uma adaptação incompleta como se fosse cenário controlado.

**Merge de etapas 2–4:** direcionar correções à integração; Rafael coordena o PR conjunto para main depois que o conjunto estiver validado. A IA de um participante não deve integrar código quebrado na main nem assumir que abrir PR é autorização de merge. Se merge estiver autorizado para sua função, conferir checks e SHA atual antes de fazê-lo.

## 4. Gatilhos reais: PR não executa tudo automaticamente

| Pipeline | Gatilho observado no projeto | O que precisa comprovar |
|---|---|---|
| CI | Push na main e qualquer PR; também reutilizado pelo CD | Ruff e testes Python 3.11/3.12; para E1, main já adaptada |
| CT | PR/push na main que altere lotes ou `params.yaml`; agenda e disparo manual | Por evento, retreino apenas com drift; execução manual/agendada retreina mesmo sem drift |
| CD | Push de tag `v*.*.*` ou disparo manual | CI reutilizado, build, smoke e publicação |

Reabrir os YAMLs atuais para confirmar esses gatilhos antes de agir. PR de documentação pode rodar só CI. CT pode ficar verde pulando o portão: isso **não é E3**. Um CD manual pode ajudar a validar a imagem, mas a evidência E5 deve estar associada à tag de versão solicitada pelo enunciado.

No bônus, a tag criada com `GITHUB_TOKEN` não dispara outro workflow pelo push; o CT existente chama explicitamente o CD por `workflow_dispatch`. Comprovar essa chamada e seu autor, sem apresentar um disparo manual do integrante como automação do CT.

## 5. Etapa 1 — IA de Rafael

**Escopo:** preparação, decisões registradas, acessos e coordenação da integração. Preservar `docs/PLANEJAMENTO.md` e as pendências reais de revisão coletiva.

1. Conferir os PRs e a integração mais recente, preservando o trabalho existente de Leonardo/Samara/Juan.
2. Coordenar a conciliação com a main, inclusive divergências documentais, sem rebase/force push. Não integrar isoladamente o PR #4 antigo se houver uma integração mais completa.
3. Conferir que o conjunto tem dados elétricos, código/modelo/API compatíveis, testes novos por camada e CI local completo. Solicitar revisão de protocolo quando houver dúvida material, sem inventar aceite de Felipe ou do grupo.
4. Abrir/conferir o PR conjunto integração → main e acompanhar os checks. Se o usuário autorizou esse merge, integrar apenas com checks pertinentes aprovados e SHA conferido.
5. Registrar commit integrado, PR e CI da main adaptada, repassando a referência para Victor/Juan. E1 poderá ser registrada por Victor a partir dessa execução válida.

**Concluída:** preparação rastreável e integração coordenada realmente efetuada, ou escopo documental explicitamente entregue com integração ainda pendente. Usar estados separados; não dizer que a entrega coletiva está pronta só porque o planejamento está publicado.

## 6. Etapa 2 — IA de Leonardo

**Escopo:** `data/source/`, CSVs de base, contrato de entrada em `config.py`, ingestão/divisão/validação em `data.py` e `tests/test_dados.py`. Respeitar partes de drift/API já feitas por Juan no mesmo arquivo.

1. Conferir se o commit de regeneração das bases já está na integração; reaproveitar, sem sobrescrever trabalho de Felipe ou reverter à branch antiga de Leonardo.
2. Verificar licença/atribuição e hash dos bytes originais; se o Git alterar finais de linha, corrigir a preservação de forma explícita, sem trocar o hash esperado para esconder divergência.
3. Conferir esquema, 6.000/2.000/2.000 conforme protocolo, mapeamento de classes, reserva exclusiva, identidades e ausência de sobreposição. Lotes iniciais sem CSV antes das evidências; não apagar lotes históricos já publicados posteriormente.
4. Validar tipos, nulos, infinitos, faixas e balanço físico; manter pelo menos um novo teste específico de dados. Conferir que a reserva é reproduzível e não depende de amostras de teste usadas como treino.
5. Executar validador e testes no conjunto integrado. Corrigir os problemas de sua etapa que permanecerem; o CI antigo do PR #4 não certifica nem condena automaticamente a integração mais recente.
6. Registrar verificações atuais, ambiente e limites em `docs/ETAPA2_LEONARDO.md`; abrir/atualizar PR para a base correta e acompanhar checks. Se outro PR substituiu o #4, registrar a relação e fechar o antigo sem merge somente com autorização.

**Concluída:** dados/contrato/testes conferidos, mudanças necessárias revisáveis, PR validado e integração registrada. Se só os testes isolados passaram, registrar **validação parcial**, não conclusão do pipeline.

## 7. Etapa 3 — IA de Samara

**Escopo:** `features.py`, `train.py`, `evaluate.py`, `gate.py`, `selecao.py`, `params.yaml`, testes de código/modelo, campeão e dependências do DVC. Não desfazer a API, o drift ou a fixação de versão já feita por Juan.

1. Ler `docs/ETAPA3_SAMARA.md` e o JSON da seleção; conferir o vencedor e as versões atuais. Reaproveitar seleção/campeão existentes se íntegros; não repetir buscas olhando o holdout.
2. Conferir positiva `1`, nomes das métricas e consumidores. Verificar novos testes de código/modelo, comportamento direcional justificado e compatibilidade do artefato com o ambiente do CI/Docker.
3. Corrigir somente pendências reais. Se o documento ainda disser que a API está antiga ou que a versão não está fixada, confrontar com a integração atual e atualizar o registro histórico sem apagar como o trabalho foi realizado.
4. Executar as verificações pertinentes no conjunto integrado. Se necessário para reproduzir o pipeline, executar o treino curto do DVC, conferir o portão e gerar/versionar `dvc.lock`; coordenar o arquivo com Juan e não versionar candidato/relatórios ignorados como se fossem campeão.
5. Não substituir o campeão apenas para um teste passar. Se for necessário recriá-lo, demonstrar incompatibilidade/necessidade e respeitar a autorização e o protocolo. Preservar os valores históricos e registrar a avaliação realmente executada.
6. Atualizar `docs/ETAPA3_SAMARA.md` com resultados atuais e limites, commits e PR da finalização. Criar/atualizar PR para a integração vigente, acompanhar o CI completo e registrar URL/SHA.

**Concluída:** modelo e métricas compatíveis no conjunto, testes exigidos aprovados, artefato rastreável, pipeline DVC reproduzido quando necessário e PR validado. A publicação de E3/E4/CD não pertence a esta etapa; se essas evidências estiverem pendentes, registrá-las sem assumir que sua ausência invalida toda a implementação de Samara.

## 8. Etapa 4 — IA de Juan

**Escopo:** drift/lotes, monitor, API de 12 entradas, smoke, testes de API e cinco cenários, preservando o contrato de Leonardo e o modelo de Samara.

1. Partir da integração atual e ler `docs/ETAPA4_JUAN.md`; reaproveitar as correções existentes. Conferir faixas/validação de API, mensagens, positiva, probabilidade e novo teste específico da camada.
2. Conferir fonte/reserva dos lotes, ausência de sobreposição e preservação dos rótulos. Não produzir contrafactuais com rótulo falso nem reaproveitar o mesmo registro em lotes independentes para inflar evidência.
3. Verificar os cinco cenários na versão atual dos parâmetros. Gerar experimentos somente em branches/cópias separadas e registrar que são falhas intencionais. Não corromper a main ou o campeão para obter vermelho.
4. Validar CI local e, nos cenários pertinentes, CT/portão. Registrar falhas e a limitação de avaliação já observada. Resultado local não deve ganhar uma URL inventada de Actions.
5. Abrir/atualizar PR operacional para a integração e acompanhar checks. Se E1 da main adaptada ainda não existir, registrar **implementação validada, evidências oficiais pendentes de E1**; não chamar a etapa inteira de concluída.
6. Depois de E1, executar E3/E4 no Actions por PRs distintos. Se Victor já as executou corretamente com os seus cenários, conferir/reutilizar os runs válidos e registrar quem executou; não repetir só para trocar o autor.

**E3:** lote com drift efetivo, DVC executado, portão aprovado com tabela campeão/candidato. **E4:** candidato reprovado por recall/precisão, falha no step do portão, hash/commit do campeão preservado. Falha de download/instalação não conta. Fechar PR de falha sem merge, preservando branch/execução.

**Concluída:** implementação validada e evidências E3/E4 oficiais registradas. Se a sequência impedir a segunda passagem agora, documentar a dependência e os artefatos prontos para Victor; não executar tarefas dos outros fingindo que eram suas nem prometer que o passo foi feito.

## 9. Etapa 5 — IA de Victor

**Escopo:** CI/CD, fechamento e consolidação das evidências E1–E5 e imagem pública. Trabalho real de integração operacional e registro de evidências deve produzir contribuição própria, sem imitar commits dos colegas.

1. Exigir main adaptada ou PR conjunto pronto para revisão do coordenador. Se ainda faltar integração, entregar diagnóstico/PR concreto do problema e registrar dependência de Rafael; não fabricar E1 com o baseline.
2. Conferir o CI da **main elétrica**: três jobs aprovados, SHA e data. Registrar E1.
3. Produzir E2 em branch/PR de cenário controlado depois do baseline adaptado aprovado; verificar step e teste esperados. Fechar sem merge após capturar a execução.
4. Conferir com os registros de Juan se E3/E4 já existem. Se não, pode produzir as execuções oficiais usando os cenários implementados por ele, registrando Victor como executor e preservando a autoria do código de Juan. Seguir os critérios da seção anterior, sem ajustar contratos/holdout para conseguir o resultado.
5. Confirmar tag adequada de um commit válido da main; não sobrescrever tag existente. Com publicação autorizada, criar/enviar a tag, acompanhar o CD e conferir seus três jobs CI mais o job de build/smoke/publicação.
6. Conferir URL do pacote do grupo e visibilidade Public; testar pull sem credenciais e smoke da imagem publicada. Se apenas o proprietário puder alterar o pacote, fornecer o link e a configuração exata; não declarar público antes de comprovar.
7. Criar/atualizar `docs/ETAPA5_VICTOR.md` e `docs/EVIDENCIAS.json` com valores reais. Documentação por PR também deve ter checks acompanhados. Não instalar ferramentas globais nem alterar workflows sem causa demonstrada.

**Concluída:** E1–E5 oficiais verificadas, tag e imagem vinculadas ao commit correto, pacote público e consumo testado. Os runs podem ser de etapas/operadores diferentes; registrar essa origem corretamente. Falta de um desses itens impede declarar a etapa 5 encerrada.

## 10. Etapa 6 — IA de Felipe

**Escopo:** relatório, documentação final, autoria, eventual bônus e texto para D2L. Confirmar a conta real de Felipe antes dos commits, sem reatribuir os anteriores.

1. Auditar E1–E5 e o estado final da main; conferir cada URL, SHA, job e step. Usar o registro de Victor, sem tratar sua existência como garantia automática.
2. Atualizar `README.md` para o problema elétrico e os comandos/versões reais. Não deixar descrições de Breast Cancer como se fossem o produto atual; preservar atribuição ao projeto original.
3. Criar `ADAPTACAO.md` na raiz, até duas páginas na apresentação final, cobrindo os seis itens do enunciado: problema/fonte/licença/tamanho; contrato; mudanças por arquivo; E1–E5; limites/monitoramento; contribuições e IA.
4. Relacionar contribuições reais dos seis a commits/PRs. Não inventar uma contribuição de Victor ou outro integrante se ela ainda não existir; identificar essa pendência para a própria pessoa resolver.
5. Preservar a limitação de reuso da avaliação relatada por Juan, diferenças de ambiente e tentativas reprovadas relevantes. Não transformar sucesso do portão em segurança operacional comprovada.
6. Produzir `docs/ETAPA6_FELIPE.md` e `ENTREGA_D2L.txt` com repositório público, cinco URLs oficiais e página/print do pacote. Enquanto faltar evidência, manter rascunho explicitamente incompleto, sem placeholders apresentados como entrega final.
7. Publicar o PR documental, acompanhar o CI e solicitar/reunir a revisão de Rafael. Merge e envio ao D2L dependem das autorizações correspondentes. Preparar o arquivo não significa que o D2L recebeu a atividade.

### Bônus opcional, quando autorizado

Depois das evidências obrigatórias, com Rafael/coordenador ciente, conferir permissões do Actions e condição da main sem proteção. Alterar `PROMOCAO_AUTOMATICA` para `true` somente no momento autorizado. Não remover regras de proteção nem ampliar permissões sem autorização explícita.

Usar candidato/lote previamente validados no protocolo. O **CT** deve aprovar o portão, promover, criar a tag seguinte e chamar o CD. Comprovar:

- Run de CT e steps de promoção/tag aprovados.
- Commit do robô alterando os artefatos corretos, com histórico anterior preservado.
- Tag apontando para o campeão promovido.
- CD sobre esse mesmo commit/tag, disparado pelo workflow, com CI/build/smoke/publicação aprovados.
- Imagem pública testada, riscos/vantagens e estado final da variável registrados.

Não simular esse fluxo criando manualmente a tag e disparando o CD como usuário. Se reprovar, registrar e investigar; não manipular o campeão, os limiares ou o holdout. Não atribuir o bônus da salvaguarda ao coletivo.

**Concluída:** relatório consistente, seis contribuições comprovadas, E1–E5 e pacote verificados, PR validado, arquivo de entrega pronto e revisão/aceite claramente registrados. Bônus só pode ser declarado se executado e comprovado; não é condição para os pontos obrigatórios.

## 11. Registro obrigatório de cada IA

Atualizar o registro da própria etapa, mantendo histórico relevante e usando um estado claro: `em_execucao`, `validada_localmente`, `pr_em_revisao`, `integrada`, `evidencias_pendentes` ou `concluida`. Não misturar “código escrito”, “CI verde”, “modelo promovido” e “entrega enviada”.

Incluir, com dados reais:

| Campo | Conteúdo obrigatório |
|---|---|
| Pessoa / conta / executor | Integrante real e uso de IA |
| Base | Branch e SHA dos quais o trabalho partiu |
| Mudanças | Arquivos e motivo, preservando o que já estava pronto |
| Ambiente | Python e dependências relevantes, com divergências apontadas |
| Verificações | Comando, resultado, contagens e limitações; distinguir local de Actions |
| GitHub | Commits, PR, branch de destino e runs com conclusão/steps |
| Evidências | Quais E1–E5/bônus foram comprovadas, por quem, em qual commit |
| Pendências | Dependência, responsável e próxima ação concreta |

Em `docs/EVIDENCIAS.json`, Victor/Felipe devem consolidar para cada E1–E5: URL do run, workflow, evento, branch, SHA, conclusão, jobs/steps esperados, PR/tag e executor. Registrar hash do campeão antes/depois em E4; em E5, imagem, tag, digest e teste de consumo. Não criar esse índice com valores fictícios apenas para preencher o formato.

### Resposta final que a IA deve dar ao integrante

Informar: estado real da etapa; o que mudou e por quê; arquivos; comandos e resultados; commits/PR/runs; evidências obtidas; dependências pendentes e próxima pessoa da sequência. Se algo ficou impedido por acesso, dependência ou decisão científica, explicar exatamente o que falta, sem alegar conclusão.

**Regra de encerramento:** não pare depois de escrever código ou abrir o PR quando ainda houver trabalho autorizado de validação/acompanhamento. Também não ultrapasse sua etapa, invente resultados ou repita ações irreversíveis para forçar a conclusão. Um bloqueio externo real deve deixar uma entrega concreta, rastreável e retomável.

## 12. Referências de carregamento das instruções

O roteiro acima é uma instrução do projeto, não configuração executável de segurança. As ferramentas podem deixar de carregar instruções por versão, escopo, modo gerenciado ou configuração. Para conferir o mecanismo: [Codex — AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) e [Claude Code — instruções de projeto](https://code.claude.com/docs/en/memory). No Claude Code, o pequeno `CLAUDE.md` usa o import `@AGENTS.md` para compartilhar a orientação sem duplicar o roteiro.

O carregamento e a adesão de cada IA devem ser conferidos pelo integrante. Em caso de dúvida, usar a frase completa da seção 1 e pedir que a IA confirme os arquivos que leu antes de agir.
