# Protocolo técnico dos dados e da avaliação

Decisões originais de Rafael, registradas em 24/11/2026, preservadas como referência metodológica. O texto abaixo descreve o protocolo definido antes da implementação, incluindo suas restrições e limites; os resultados efetivamente obtidos estão em [EVIDENCIAS.json](EVIDENCIAS.json) e os responsáveis em [CONTRIBUICOES.md](CONTRIBUICOES.md). A organização interna de tarefas foi retirada desta documentação.

## 1. Problema, usuário e custo do erro

**Problema:** classificar o estado de uma rede elétrica simulada de quatro nós como estável ou instável, para apoiar a triagem de cenários por pesquisadores/engenheiros. É uma demonstração acadêmica de MLOps, sem operação de rede real.

**Positiva:** `instavel=1`, a partir de `stabf="unstable"`; `stable` vira `0`. O objetivo principal é reduzir **falsos negativos**, que deixariam uma instabilidade sem investigação. Falsos positivos representam investigações desnecessárias e precisam ser limitados por uma trava de precisão.

Essa prioridade é uma decisão didática de Rafael. Não há levantamento de custo financeiro, validação de risco operacional ou requisito de segurança elétrica que justifique transformar esses limiares em garantia de produção.

## 2. Fonte elegível e inspeção realizada

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

## 3. Contrato de dados e protocolo fixado por Rafael

### Esquema de entrada

Ordem das entradas: `tau1,tau2,tau3,tau4,p1,p2,p3,p4,g1,g2,g3,g4`. Alvo derivado: `instavel`, inteiro em `{0,1}`. Os CSVs derivados devem conter as 12 entradas nessa ordem, seguidas pelo alvo.

- `tau1..tau4`: tempos de reação, faixa da fonte `[0.5,10]`.
- `p2..p4`: consumo negativo, faixa `[-2,-0.5]`; `p1`: produção positiva, faixa compatível `[1.5,6]`; exigir balanço com tolerância numérica `1e-8`.
- `g1..g4`: coeficientes de elasticidade, faixa `[0.05,1]`.
- Rejeitar tipos não numéricos, nulos, infinitos e rótulos inválidos. As faixas são do domínio simulado e devem ser verificadas tanto na ingestão quanto no contrato da API.
- `p1` é derivada das potências dos consumidores. Será preservada como atributo físico do esquema, mas não deve ser apresentada como informação independente adicional.
- Excluir `stab` e `stabf` das entradas do modelo. `stab` determina o rótulo e seu uso como preditor produz vazamento; `stabf` serve somente ao mapeamento do alvo.

### Partições e sementes

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

### Validação interna do modelo

- Pré-processamento aprendido deve ser ajustado somente no treino, dentro do pipeline.
- Se houver seleção de parâmetros, usar um split interno estratificado **80/20 da base de treino**, `random_state=42`: 4.800/1.200 no protocolo acima. Samara deve declarar candidatos, versões e ordem de desempate antes das execuções.
- Critério: maior recall da positiva entre os candidatos com precisão >=0,90; desempate por precisão e, depois, pela ordem dos candidatos previamente registrada.
- Não escolher aqui o algoritmo ou seus hiperparâmetros em nome de Samara. A regressão logística é a referência existente; mudanças devem ser justificadas por avaliação interna, com tentativas e falhas registradas.
- Fixar o vencedor antes de abrir a avaliação no holdout; treinar o campeão inicial na base de treino completa, respeitando a sequência de compatibilização com a API.
- Se o contrato não for atingido, registrar a falha. Não ajustar parâmetros ou limites olhando o holdout. Qualquer revisão de protocolo precisa de justificativa e registro anterior à nova avaliação.

## 4. Contrato de qualidade e avaliação

Definição a implementar: `CLASSE_INSTAVEL=1`; recall da positiva **>=0,92**; precisão da positiva **>=0,90**; tolerância de regressão de recall do candidato frente ao campeão **0,0**, medidos no **mesmo conjunto**. Piso separado de sanidade do campeão no holdout: 0,80, conforme o mecanismo existente, sem substituir os pisos de promoção.

Essas metas priorizam sensibilidade e limitam alertas falsos. Por exemplo, prever sempre `instavel` teria recall 1,0 e precisão 0,638 na fonte inspecionada: falharia no contrato de precisão. Isso é uma conta sobre a prevalência da fonte, **não uma execução ou métrica de modelo treinado pelo grupo**.

Drift proposto para Juan: KS por atributo, `p<0,01`, gatilho em **pelo menos 2 dos 12 atributos**. Um lote selecionado por maior elasticidade média pode demonstrar mudança de distribuição preservando os rótulos originais. Drift não é prova de piora e não garante que o retreino será aprovado. Limiares de seleção, tamanho e origem do lote devem ser declarados antes de avaliar o portão.

O portão compara campeão e candidato no holdout fixo somado às metades de avaliação dos lotes, mantendo essas linhas fora do treino. A reutilização dessa referência em sucessivas decisões limita a independência da avaliação; produção exigiria teste final separado e renovação controlada.
