# Integração das etapas 2 a 4 — 25/11/2026

Rafael realizou a integração e as verificações abaixo com auxílio do Codex. Os commits existentes de Leonardo, Samara, Juan e da branch de integração foram preservados com suas autorias. Este registro não atribui a eles as verificações executadas por Rafael.

## Escopo e histórico

O PR #4 de Leonardo isoladamente continha falhas de lint e dados ainda incompatíveis com a adaptação. A branch `integracao-etapas-2-4` já continha seus commits e as correções das etapas seguintes, incluindo os CSVs elétricos. A integração usa esse conjunto, sem ignorar checks vermelhos ou fabricar um resultado para o PR antigo.

A preparação documental foi publicada pelo [PR #5](https://github.com/RafaellLobo/mlops-estabilidade-rede-grupo/pull/5), com CI aprovado. O protocolo metodológico preservado está em [PROTOCOLO.md](PROTOCOLO.md); os resultados finais estão em [EVIDENCIAS.json](EVIDENCIAS.json).

Commits verificados como ancestrais da integração:

- Leonardo: `0b9f972551e2d0fa5c60e624752a8f9fbbdb6912`.
- Samara: `b28bb5c7f2bc34305adb209fa7c09a4ee0855ba3`.
- Juan: `0fc1d6ffde3263fab16ef422bfe37b1f631f9956`.
- Integracao anterior: `e3dfe49bd15de151ec08bda291dfc50a9bae5575`.

## Verificações locais realizadas

Ambiente isolado do grupo: Windows, Python 3.11.9, scikit-learn 1.7.2, NumPy 2.4.6, pandas 3.1.1 e DVC 3.67.1. Foi usada a versão de scikit-learn já fixada no projeto para compatibilidade com o campeão; nenhuma dependência global foi alterada.

- `python demo/local.py ci`: aprovado; Ruff check, formatação (29 arquivos), validação dos dois CSVs e 43 testes: 15 de código, 13 de dados, 9 de modelo e 6 de API.
- `python demo/local.py ct`: aprovado; monitor, `dvc repro` e portão de qualidade.
- O monitor não encontrou lotes novos. A reprodução local foi executada explicitamente pelo script local, sem comprovar o gatilho de drift E3.
- Candidato e campeão obtiveram recall instável 0,963166144200627 e precisão instável 0,9505027068832174 no mesmo conjunto de avaliação de 2.000 linhas. O portão aprovou os limites e a comparação sem tolerância adicional.
- Foram preservados os hashes dos CSVs de treino/holdout e do campeão antes/depois do CI/CT. Não houve promoção, nova seleção de hiperparâmetros nem alteração de sementes, divisões ou limiares.
- `dvc.lock` foi gerado pelo DVC, para rastrear esta reprodução; não foi preenchido manualmente.
- Foi observado um aviso de depreciação de Starlette/FastAPI sobre o TestClient com httpx. Não houve falha de teste e não foram alteradas dependências para silenciar o aviso.

SHA-256 dos arquivos preservados:

- `data/raw/base_treino.csv`: `2de25aab6f56d85156b5532f38f8f13218acf04ddf25afee1b91f5b5c2dab1d4`.
- `data/raw/base_holdout.csv`: `aea4479c8ca988442217d3d7c6570cabaad13a24b53d3fd57583948a30713034`.
- `models/champion/model.joblib`: `dde5ee499363c5fbca7f1b5943345570e775fb2f0ef2c13bf8a17999626fd34d`.

## Limites e próximo trabalho

Esta integração torna a implementação elétrica disponível em conjunto. Não certifica o fechamento das seis etapas. As evidências oficiais de E1–E5, a publicação pública da imagem e o bônus precisam ser conferidos pelos responsáveis nas execuções reais do GitHub Actions. Um CT verde com treino/portão pulados não comprova E3. O CT local acima não substitui E3/E4 e não apaga as tentativas e limitações históricas registradas em [ETAPA4_JUAN.md](ETAPA4_JUAN.md).

Victor deve registrar os cenários oficiais e o CD na etapa 5. Felipe deve concluir a documentação adaptada e a entrega na etapa 6; o corpo do README herdado ainda precisa ser atualizado. Cada integrante deve conferir e complementar o registro de sua etapa, inclusive o documento da etapa 2 de Leonardo, sem refazer o que já existe.

O repositório individual de salvaguarda não foi usado como evidência coletiva nem modificado por esta integração.
