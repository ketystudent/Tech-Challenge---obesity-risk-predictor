# Resumo de Resultados

## EDA

- Registros originais: 2.111
- Registros apos remocao de duplicatas: 2.087
- Duplicatas identificadas: 24
- Valores ausentes: 0
- Classes do alvo: 7
- Distribuicao do alvo relativamente equilibrada.

Distribuicao do alvo apos limpeza:

| Classe | Registros | Percentual |
|---|---:|---:|
| `Obesity_Type_I` | 351 | 16.82% |
| `Obesity_Type_III` | 324 | 15.52% |
| `Obesity_Type_II` | 297 | 14.23% |
| `Overweight_Level_II` | 290 | 13.90% |
| `Normal_Weight` | 282 | 13.51% |
| `Overweight_Level_I` | 276 | 13.22% |
| `Insufficient_Weight` | 267 | 12.79% |

## Modelo Final

O modelo final escolhido foi `RandomForestClassifier`, pois apresentou melhor equilibrio entre desempenho em validacao cruzada e resultado no teste.

Metricas finais:

| Metrica | Valor |
|---|---:|
| Acurácia | 0.8445 |
| Precisão macro | 0.8429 |
| Revocação macro | 0.8408 |
| F1 macro | 0.8410 |

## Otimização

A otimização com `RandomizedSearchCV` encontrou um `RandomForest` otimizado com F1 macro de 0.9749 no teste. Como esse valor ficou abaixo do modelo final atual, o modelo otimizado foi mantido apenas como artefato comparativo.

## Redundancia e Leakage Conceitual

Foram avaliados cenarios para medir impacto das variaveis redundantes:

- Modelo completo: F1 macro medio 0.9868.
- Sem atributos derivados redundantes: F1 macro médio 0.9627.
- Modelo preventivo/comportamental sem `Weight`: F1 macro medio 0.8791.

Conclusão: o cenário preventivo permanece acima de 75% e foi adotado como modelo publicado. Ele é mais adequado ao objetivo de analisar tendências sem peso, altura ou IMC, mas não representa previsão longitudinal nem diagnóstico.

## Artefatos

- Modelo final: `models/final_pipeline.joblib`
- Encoder: `models/label_encoder.joblib`
- Metricas: `models/metrics.json`
- Relatorios: `reports/model_results/`
- Figuras: `reports/figures/`
