# Etapa 4 — Juan: drift, API e cenários

**Atualização de fechamento (25/11/2026):** E1–E5 e bônus comprovados por Rafael com Codex. Consulte [FECHAMENTO_ENTREGA.md](FECHAMENTO_ENTREGA.md) e [EVIDENCIAS.json](EVIDENCIAS.json). O registro abaixo preserva o trabalho e as condições históricas da etapa; pendências técnicas antigas foram superadas pelas execuções finais. A equipe final tem Rafael, Leonardo, Samara, Juan e Felipe, todos com commits comprovados; Victor pertence somente ao planejamento histórico. As autorias estão em [CONTRIBUICOES.md](CONTRIBUICOES.md).

## Registro histórico da etapa

## Alterações realizadas

- Adaptação da API para o domínio de estabilidade da rede elétrica, utilizando os 12 atributos do dataset.

- Validação dos valores de entrada e do balanço de potência.

- Adaptação dos testes de contrato da API e do smoke test.

- Geração de lotes com drift a partir de registros reais da reserva do dataset, sem alteração artificial dos atributos ou das classes.

- Adaptação do monitor de drift e dos cenários de demonstração.

- Fixação da versão do scikit-learn em 1.7.2 para garantir compatibilidade com o campeão treinado na etapa 3.

- Correções de lint e formatação durante a integração.

## Detecção de drift

O drift foi simulado selecionando registros com maior elasticidade média, considerando os atributos g1, g2, g3 e g4.

O monitor utiliza o teste de Kolmogorov-Smirnov, com p-valor inferior a 0,01. O retreinamento é disparado quando pelo menos dois atributos apresentam drift.

No lote final de 400 registros, os quatro atributos de elasticidade apresentaram drift.

## Experimentos de retreinamento

Inicialmente, foram testados lotes de 120 e 400 registros com os hiperparâmetros originais. Nos dois casos, o candidato atingiu os limites mínimos de recall e precisão, mas não superou o recall do campeão.

Foi realizada uma seleção adicional utilizando exclusivamente a base de treinamento, com divisão estratificada de 80/20 e semente 42.

| Peso da classe instável | Recall | Precisão |
|---|---:|---:|
| 1,00 | 96,87% | 93,22% |
| 1,25 | 97,39% | 93,37% |
| 1,50 | 97,52% | 93,38% |
| 2,00 | 97,39% | 92,56% |

O peso 1,50 foi selecionado por apresentar o maior recall entre os candidatos que atingiram a precisão mínima de 90%.

Parte dos dados de avaliação foi reutilizada nos experimentos de CT, o que representa uma limitação metodológica. Os critérios do portão permaneceram inalterados.

## E3 — Aprovação local

- Lote: 400 registros.

- Fator de seleção por elasticidade: 0,25.

- Semente: 1.

- Atributos com drift: 4 de 12.

- Iterações: 300.

- Peso da classe instável: 1,5.

- Recall do candidato: 96,68%.

- Precisão do candidato: 94,52%.

- Recall do campeão: 96,47%.

- Resultado: aprovado pelo portão de qualidade.

## E4 — Reprovação local

Inicialmente, foi testado um peso de 50 para a classe instável. O candidato ainda foi aprovado, com precisão de 90,08%.

Para simular uma falha controlada, o número de iterações foi reduzido de 300 para 1, mantendo o lote e o peso utilizados na E3.

- Recall do candidato: 100%.

- Precisão do candidato: 65,68%.

- Resultado: reprovado pelo portão de qualidade.

O hash SHA256 do modelo campeão permaneceu inalterado antes e depois dos testes:

`dde5ee499363c5fbca7f1b5943345570e775fb2f0ef2c13bf8a17999626fd34d`

## Reprodução dos cenários

O cenário 4 gera o lote de 400 registros e aplica o peso de 1,5 para a classe instável.

O cenário 5 deve ser aplicado após o cenário 4 para reproduzir a falha controlada, reduzindo o treinamento para uma única iteração.

Os parâmetros originais do campeão foram restaurados após os experimentos.

## Validação final

Comando executado: `python demo/local.py ci`.

- Lint e formatação: aprovados.

- Validação dos dados: aprovada.

- Testes de código: 15 aprovados.

- Testes de dados: 13 aprovados.

- Testes de modelo: 9 aprovados.

- Testes da API: 6 aprovados.

Total: 43 testes aprovados.

As evidências E3 e E4 foram validadas localmente. As execuções oficiais no GitHub Actions ainda dependem da integração do grupo e da conclusão da E1.

## Uso de IA

O ChatGPT foi utilizado como auxílio na adaptação do código, identificação de problemas, planejamento dos experimentos, interpretação dos resultados e elaboração desta documentação. As alterações e os testes foram realizados e conferidos pelo responsável pela etapa.
