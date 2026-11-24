# Etapa 1 — Rafael: planejamento e coordenação

**Responsável:** Rafael (`RafaellLobo`). **Registro:** 24/11/2026. **Prazo da atividade:** 25/11/2026.

## 1. Estado e limites desta entrega

Rafael definiu o protocolo técnico abaixo para orientar a execução das etapas 2–4. Ele está **pronto para revisão do grupo**; não há registro de aceite dos outros cinco integrantes. Felipe é o revisor proposto desta etapa.

Esta entrega cobre preparação, verificação de elegibilidade, decisões documentadas e organização da integração. **Não executa a adaptação atribuída aos colegas**: os CSVs ativos, código, parâmetros, campeão e workflows continuam no baseline original. Não foram treinados modelos, geradas partições ou medidas métricas do modelo elétrico nesta etapa.

| Item | Evidência/estado |
|---|---|
| Repositório coletivo público, próprio e sem fork | [mlops-estabilidade-rede-grupo](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo) |
| Origem consultada | [Projeto da disciplina](https://github.com/wesleyasantos/ci_cd_ct_mlops), commit `371c2dfe8882aab238f2ec2f7796915eedc5aa0f` |
| Primeiro CI antes da adaptação | [45421009801](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/actions/runs/45421009801): ruff e testes Python 3.11/3.12 aprovados no commit `26b0cf09488ec2ebd4c75b7e7ea230a74c8e7e14` |
| Actions | Escrita de conteúdo e permissão de abrir PRs confirmadas |
| Promoção automática | `PROMOCAO_AUTOMATICA=false`; bônus somente depois das evidências obrigatórias |
| Papéis | [ETAPAS_GRUPO.md](../ETAPAS_GRUPO.md): seis responsáveis e revisores propostos |
| Convites | Samara, Juan, Victor e Felipe: convites de escrita enviados, aguardando aceite na consulta de 24/11; Leonardo: convite adiado por orientação de Rafael |
| Salvaguarda individual | Separada; suas execuções, métricas e pacote não serão apresentados como evidências coletivas |

O CI acima prova o funcionamento **do projeto original**, não E1 da adaptação coletiva. Os itens dependentes de trabalho futuro permanecem abertos no final deste documento.

## 2. Problema, usuário e custo do erro

**Problema:** classificar o estado de uma rede elétrica simulada de quatro nós como estável ou instável, para apoiar a triagem de cenários por pesquisadores/engenheiros. É uma demonstração acadêmica de MLOps, sem operação de rede real.

**Positiva:** `instavel=1`, a partir de `stabf="unstable"`; `stable` vira `0`. O objetivo principal é reduzir **falsos negativos**, que deixariam uma instabilidade sem investigação. Falsos positivos representam investigações desnecessárias e precisam ser limitados por uma trava de precisão.

Essa prioridade é uma decisão didática de Rafael. Não há levantamento de custo financeiro, validação de risco operacional ou requisito de segurança elétrica que justifique transformar esses limiares em garantia de produção.

## 3. Fonte elegível e inspeção realizada

[Electrical Grid Stability Simulated Data — UCI](https://archive.ics.uci.edu/dataset/471/electrical+grid+stability+simulated+data), Vadim Arzamasov (2018), DOI [10.24432/C5PG66](https://doi.org/10.24432/C5PG66), licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). A atribuição ao autor e à fonte deve acompanhar os dados derivados.

Arquivo oficial: `Data_for_UCI_named.csv`. Inspeção feita sobre o download oficial, separadamente do clone; detalhes em [verificacao_fonte_uci.json](verificacao_fonte_uci.json).

| Verificação realizada | Resultado |
|---|---|
| Linhas / atributos numéricos candidatos a entrada | 10.000 / 12 — atende aos mínimos 500 / 8 |
| Classes originais | 3.620 `stable`; 6.380 `unstable` |
| Nulos / números não finitos / duplicatas de atributos | 0 / 0 / 0 |
| Sinal de `stab` e rótulo `stabf` | Nenhuma inconsistência encontrada |
| Balanço de potência | `abs(p1+p2+p3+p4) < 1e-8` em todas as linhas inspecionadas |
| SHA-256 do CSV original | `7afc3154fed9cd65258b3403b60381fe6b0d832bf817a1ea4866395d05a84a83` |
| Natureza | Dados simulados; sem registros de pessoas no domínio descrito pela fonte |

O hash se refere aos **bytes originais**, antes de normalizar finais de linha. Leonardo deverá baixar a fonte, conferir sua integridade e registrar a proveniência da versão efetivamente usada pelo grupo. A API da UCI não trouxe um campo de licença; CC BY 4.0 foi conferida na página oficial.

A conferência anterior dos labs disponíveis encontrou Iris/Wine nas Aulas 05/06 e Breast Cancer na Aula 07. **Ainda é necessário confirmar com a turma/professor que esta base não pertence a outro lab indisponível ou a outro grupo.** A elegibilidade dimensional não resolve essa restrição da disciplina.

## 4. Contrato de dados e protocolo fixado por Rafael

### Esquema a implementar

Ordem das entradas: `tau1,tau2,tau3,tau4,p1,p2,p3,p4,g1,g2,g3,g4`. Alvo derivado: `instavel`, inteiro em `{0,1}`. Os CSVs derivados devem conter as 12 entradas nessa ordem, seguidas pelo alvo.

- `tau1..tau4`: tempos de reação, faixa da fonte `[0.5,10]`.
- `p2..p4`: consumo negativo, faixa `[-2,-0.5]`; `p1`: produção positiva, faixa compatível `[1.5,6]`; exigir balanço com tolerância numérica `1e-8`.
- `g1..g4`: coeficientes de elasticidade, faixa `[0.05,1]`.
- Rejeitar tipos não numéricos, nulos, infinitos e rótulos inválidos. As faixas são do domínio simulado e devem ser verificadas tanto na ingestão quanto no contrato da API.
- `p1` é derivada das potências dos consumidores. Será preservada como atributo físico do esquema, mas não deve ser apresentada como informação independente adicional.
- Excluir `stab` e `stabf` das entradas do modelo. `stab` determina o rótulo e seu uso como preditor produz vazamento; `stabf` serve somente ao mapeamento do alvo.

### Partições e sementes a implementar por Leonardo

1. Preservar a ordem do CSV oficial e separar por `train_test_split`, estratificando pelo alvo, com `random_state=7`: **6.000 treino e 4.000 restantes**.
2. Separar os 4.000 restantes em **2.000 holdout fixo e 2.000 reserva**, também com estratificação e `random_state=7`.
3. Não gerar lotes no início da adaptação; `data/raw/lotes/` permanece sem CSVs até a produção de E3/E4.
4. Verificar disjunção por identidade dos atributos entre treino, holdout e reserva. Manter rastreabilidade da linha de origem; nome de arquivo diferente não prova amostra diferente.
5. Fonte de novos lotes: somente a reserva. Cada lote terá divisão estratificada fixa em **50% treino / 50% avaliação**, `random_state=7`, conforme o desenho do DVC existente.
6. Controlar consumo da reserva para não reutilizar o mesmo registro em lotes distintos. Não regenerar splits ou trocar sementes para obter resultados melhores.

A ordem das chamadas deve ser explícita para reproduzir as mesmas identidades (não basta registrar a semente):

```python
resto, treino = train_test_split(df, test_size=6000, stratify=df["instavel"], random_state=7)
reserva, holdout = train_test_split(
    resto, test_size=2000, stratify=resto["instavel"], random_state=7
)
```

Aplicar `reset_index(drop=True)` somente após registrar a associação à linha original. Esse exemplo especifica o protocolo; as divisões ainda serão implementadas por Leonardo.

Estes números são **o protocolo definido**, não partições já produzidas ou verificadas neste clone. O holdout não participa de treino, escolha de algoritmo, transformações aprendidas ou seleção de hiperparâmetros.

### Validação de modelo a implementar por Samara

- Pré-processamento aprendido deve ser ajustado somente no treino, dentro do pipeline.
- Se houver seleção de parâmetros, usar um split interno estratificado **80/20 da base de treino**, `random_state=42`: 4.800/1.200 no protocolo acima. Samara deve declarar candidatos, versões e ordem de desempate antes das execuções.
- Critério: maior recall da positiva entre os candidatos com precisão >=0,90; desempate por precisão e, depois, pela ordem dos candidatos previamente registrada.
- Não escolher aqui o algoritmo ou seus hiperparâmetros em nome de Samara. A regressão logística é a referência existente; mudanças devem ser justificadas por avaliação interna, com tentativas e falhas registradas.
- Fixar o vencedor antes de abrir a avaliação no holdout; treinar o campeão inicial na base de treino completa, respeitando a sequência de compatibilização com a API.
- Se o contrato não for atingido, registrar a falha. Não ajustar parâmetros ou limites olhando o holdout. Qualquer revisão de protocolo precisa de justificativa e registro anterior à nova avaliação.

## 5. Contrato de qualidade e evidências a produzir

Definição a implementar: `CLASSE_INSTAVEL=1`; recall da positiva **>=0,92**; precisão da positiva **>=0,90**; tolerância de regressão de recall do candidato frente ao campeão **0,0**, medidos no **mesmo conjunto**. Piso separado de sanidade do campeão no holdout: 0,80, conforme o mecanismo existente, sem substituir os pisos de promoção.

Essas metas priorizam sensibilidade e limitam alertas falsos. Por exemplo, prever sempre `instavel` teria recall 1,0 e precisão 0,638 na fonte inspecionada: falharia no contrato de precisão. Isso é uma conta sobre a prevalência da fonte, **não uma execução ou métrica de modelo treinado pelo grupo**.

Drift proposto para Juan: KS por atributo, `p<0,01`, gatilho em **pelo menos 2 dos 12 atributos**. Um lote selecionado por maior elasticidade média pode demonstrar mudança de distribuição preservando os rótulos originais. Drift não é prova de piora e não garante que o retreino será aprovado. Limiares de seleção, tamanho e origem do lote devem ser declarados antes de avaliar o portão.

O portão compara campeão e candidato no holdout fixo somado às metades de avaliação dos lotes, mantendo essas linhas fora do treino. A reutilização dessa referência em sucessivas decisões limita a independência da avaliação; produção exigiria teste final separado e renovação controlada.

| Evidência | Produção | Condição de aceite |
|---|---|---|
| E1 | Victor, após integração | Três jobs CI verdes na main **adaptada** |
| E2 | Victor | PR de falha controlada no step esperado; fechar sem merge |
| E3 | Juan, com conferência de Victor | Lote válido, drift demonstrado e portão realmente aprovado |
| E4 | Juan, com conferência de Victor | Recall/precisão insuficientes, CT falhando no portão e campeão preservado |
| E5 | Victor | Tag de commit aprovado, CD verde, imagem pública do grupo e smoke após pull sem credenciais |
| Bônus | Felipe, revisão de Rafael | CT promove, cria tag e dispara CD por conta própria; vantagens/riscos documentados |

As evidências acima continuam **pendentes**. Não usar execuções ou imagens do repositório individual como se fossem do coletivo. Manter `PROMOCAO_AUTOMATICA=false` até o momento acordado de demonstrar o bônus.

## 6. Coordenação concreta da integração das etapas 2–4

**Branch conjunta:** `codex/integracao-estabilidade-rede`, preparada por Rafael a partir da main com este planejamento. Ela é um ponto de partida, não uma adaptação concluída.

| Passagem | Responsável | O que repassar | Conferência de Rafael |
|---|---|---|---|
| Dados → modelo/API | Leonardo | Fonte/hash, script, esquema, splits, testes de dados e sementes | Protocolo respeitado e ausência de sobreposição |
| Modelo → operação | Samara | Pipeline, nomes das métricas, parâmetros, testes e validação interna | Positiva correta, ausência de uso do teste na seleção |
| Operação → campeão | Juan | API, smoke, drift, cinco cenários e novo teste de API | Contrato de 12 entradas e consumidores compatíveis |
| Campeão → PR conjunto | Samara e Rafael | Campeão inicial, DVC e CI local integral | Métricas reais, autores preservados, nenhum requisito pendente escondido |
| Main adaptada → evidências | Victor e Juan | E1 primeiro; depois E2–E5 | Links do coletivo, falhas intencionais isoladas |
| Relatório → entrega | Felipe, revisão de Rafael | Até duas páginas, seis contribuições, uso de IA, E1–E5 e pacote | Coerência com código e execuções reais |

Cada autor trabalha com sua própria identidade. Enquanto dados/modelo/API estiverem incompatíveis, as mudanças ficam locais. Para passar trabalho ao colega, usar sessão conjunta ou commits exportados como patches, preservando os autores originais. Não publicar cabeças de branch quebradas apenas para transmitir trabalho.

Com o conjunto integrado, executar `python demo/local.py ci` e `python demo/local.py ct`. Publicar a branch conjunta e abrir PR para main somente depois de interpretar os resultados e cumprir os critérios. Rafael revisa conflitos e os checks desse PR; sua execução depende da entrega dos colegas. Não reescrever autoria, não fazer force push e não integrar E2/E4 na main.

### O que Rafael já entregou e o que depende de terceiros

- [x] Repositório e baseline original com três jobs aprovados.
- [x] Papéis, dependências e critérios distribuídos em seis etapas.
- [x] Inspeção oficial da fonte e protocolo técnico registrados.
- [x] Convites de escrita enviados para as quatro contas confirmadas; convite de Leonardo explicitamente adiado.
- [x] Roteiro de integração preparado; branch conjunta disponibilizada ao concluir este PR.
- [ ] Felipe revisar esta etapa; registrar eventuais discordâncias e o aceite coletivo sem presumir consenso.
- [ ] Equipe confirmar elegibilidade perante os demais labs/grupos.
- [ ] Convidados aceitarem acesso; Rafael enviar o convite de Leonardo quando o perfil for confirmado.
- [ ] Receber, revisar e integrar o código efetivamente produzido nas etapas 2–4.
- [ ] Rafael revisar o relatório de Felipe e acompanhar a confirmação de envio ao D2L.

Pendências de revisão, convites e integração futura não são execução concluída nem aprovação já dada pelos colegas. Não é necessário avançar nas tarefas deles para fechar os artefatos de planejamento de Rafael.

## 7. Contribuição e uso de IA

Rafael é o responsável pela preparação e por este planejamento. O Codex foi usado, a pedido de Rafael, para consultar o estado do GitHub, inspecionar a fonte pública, redigir o protocolo e organizar a integração. Os colegas ainda não tiveram suas contribuições de implementação registradas nesta etapa. O relatório final de Felipe deve declarar este uso de IA e os demais usos efetivamente ocorridos.
