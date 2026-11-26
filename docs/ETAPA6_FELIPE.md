# Etapa 6: relatório, documentação final, bônus e entrega

**Atualização de fechamento (25/11/2026):** E1–E5 e bônus comprovados por Rafael com Codex. Consulte [FECHAMENTO_ENTREGA.md](FECHAMENTO_ENTREGA.md) e [EVIDENCIAS.json](EVIDENCIAS.json). O registro abaixo preserva o trabalho e as condições históricas da etapa; pendências técnicas antigas foram superadas pelas execuções finais. A equipe final tem Rafael, Leonardo, Samara, Juan e Felipe, todos com commits comprovados; Victor pertence somente ao planejamento histórico. As autorias estão em [CONTRIBUICOES.md](CONTRIBUICOES.md).

## Registro histórico da etapa

**Estado: `validada_localmente`** para a documentação; o PR ainda não foi aberto e as evidências estão `evidencias_pendentes`.
A entrega **não está pronta**: faltam E1 a E5 e o pacote público (ver `docs/ETAPA5_VICTOR.md`).

## Responsável, conta e uso de IA

| Campo | Conteúdo |
|---|---|
| Pessoa | Felipe, que também assumiu a etapa 5 |
| Conta GitHub | **a confirmar.** O planejamento cita `fclivati`, os commits antigos citam `felipebpkedu` e Felipe informou `felipebioparkedu`. Não se presume que sejam a mesma pessoa; a conta autenticada deve ser confirmada antes do push |
| Autoria Git dos novos commits | `Felipe <felipebioparkedu@gmail.com>`, informada por Felipe. O commit `e3dfe49` (bases regeneradas) já está na `main` com essa autoria |
| Uso de IA | Claude, a pedido de Felipe, na análise do repositório, na validação local e na redação. Sem acesso autenticado ao GitHub |

## Base e mudanças

Base: `main` em `330fcf8`. Arquivos desta etapa: `README.md` (reescrito para o problema elétrico, com atribuição ao projeto
original), `ADAPTACAO.md` (duas páginas), `docs/ETAPA5_VICTOR.md`, este registro, `docs/EVIDENCIAS.json`,
`ENTREGA_D2L.txt` (rascunho) e uma nota em `docs/PLANEJAMENTO.md` sobre a reatribuição da etapa 5. Nenhum código, workflow,
parâmetro, holdout ou limiar foi alterado.

## Auditoria do estado real (25/11/2026)

| Item | Situação verificada |
|---|---|
| PRs #1 a #6 | todos na `main` (cabeças são ancestrais da `main`) |
| Tags | nenhuma no remoto |
| Execuções do Actions | **não consultadas**: a API pública estava com limite de requisições e não há credencial. Nenhum run foi confirmado ou negado |
| Pacote no GHCR | não conferido |
| README anterior | descrevia o projeto original; substituído |
| Contribuição de Victor | nenhuma no histórico |
| Contribuição de Leonardo na etapa 2 | existe, mas não há `docs/ETAPA2_LEONARDO.md`; cabe a ele registrar |

## Verificações locais deste registro

`python demo/local.py ci` (7 de 7, 43 testes), `git diff --check`, validade do JSON, e `ADAPTACAO.md` renderizado em duas
páginas. Os testes locais de E2, E3 e E4 estão em `docs/ETAPA5_VICTOR.md`.

## Bônus: promoção automática (só depois de E1 a E5)

Pré-condições, todas a confirmar com Rafael: E1 a E5 comprovadas; a `main` aceita push direto do `github-actions[bot]` (sem exigir
Pull Request); Settings > Actions > General com Read and write permissions. **Não remover proteções nem ampliar permissões sem
autorização explícita.**

1. Em Settings > Secrets and variables > Actions > Variables, crie ou edite `PROMOCAO_AUTOMATICA = true` e registre o momento.
2. Na `main` atualizada: `python demo/cenarios.py aplicar 4`, commit e push direto na `main`. O lote e o candidato são os já
   validados em E3.
3. Acompanhe o **CT**: drift, DVC, portão aprovado, `Publicar o novo campeão na main` e `Criar a tag da nova versão e disparar o CD`.
4. Comprove, com URLs reais: o commit do robô `ct: promove novo modelo campeão (portão aprovado)` alterando só
   `models/champion/`; a tag seguinte (`v1.1.0`, se `v1.0.0` do E5 existir) apontando para esse commit; o run do **CD** com
   evento `workflow_dispatch` e autor `github-actions[bot]`, disparado pelo passo `gh workflow run` do CT; CI, build, smoke e
   publicação aprovados; e o pull da imagem sem login com smoke.
5. Volte `PROMOCAO_AUTOMATICA` para `false` e registre o estado final.

Observações: o CT só cria tag se o campeão realmente mudar; se o portão reprovar, nada é publicado. Não crie a tag nem dispare
o CD manualmente e chame isso de automação. Se falhar, registre e investigue, sem mudar campeão, limiares ou holdout. O bônus
da salvaguarda individual não conta. Riscos a registrar: `main` sem proteção, nenhuma revisão humana, métricas limitadas e
necessidade de rollback.

## Pendências

| Item | Responsável | Próxima ação |
|---|---|---|
| Confirmar a conta GitHub | Felipe | dizer qual conta usará e conferir `gh auth status` ou o login no navegador |
| Abrir o PR documental | Felipe | `git push -u origin felipe/etapas-5-6-entrega` e abrir PR para a `main` |
| Revisão | Rafael | revisar e aprovar o PR |
| E1 a E5 e pacote | ver etapa 5 | executar no GitHub e preencher `docs/EVIDENCIAS.json` |
| `ADAPTACAO.md` e `ENTREGA_D2L.txt` | Felipe | trocar `PENDENTE` por URLs reais ao final |
| Envio ao D2L | uma pessoa definida pelo grupo | enviar; **este arquivo não envia nada** |
