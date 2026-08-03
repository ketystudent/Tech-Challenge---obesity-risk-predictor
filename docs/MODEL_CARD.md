# Cartão do Modelo

## Objetivo

Modelo de classificacao multiclasse para prever o nivel de obesidade a partir de informacoes clinicas e habitos de vida.

## Modelo Final

- Algoritmo: `RandomForestClassifier`
- Pipeline: engenharia de atributos + `ColumnTransformer` + classificador
- Artefato: `models/final_pipeline.joblib`
- Encoder: `models/label_encoder.joblib`
- Conjunto de dados usado: `data/raw/Obesity.csv`
- Registros originais: 2.111
- Duplicatas removidas no treino: 24
- Registros usados apos limpeza: 2.087

## Metricas no Conjunto de Teste

| Metrica | Valor |
|---|---:|
| Acurácia | 0.9785 |
| Precisão macro | 0.9790 |
| Revocação macro | 0.9770 |
| F1 macro | 0.9775 |

O desempenho atende ao requisito minimo do desafio, que pede assertividade acima de 75%.

## Comparacao de Modelos

Melhor modelo na comparacao inicial:

| Modelo | Acurácia média na validação cruzada | F1 macro médio na validação cruzada |
|---|---:|---:|
| RandomForest | 0.9850 | 0.9847 |
| ExtraTrees | 0.9802 | 0.9793 |
| GradientBoosting | 0.9754 | 0.9748 |
| DecisionTree | 0.9718 | 0.9711 |
| LogisticRegression | 0.9652 | 0.9644 |
| SVM | 0.9593 | 0.9581 |
| KNN | 0.9047 | 0.9000 |

## Otimização

Foi executado `RandomizedSearchCV` para `RandomForest`, `ExtraTrees` e `GradientBoosting`.

Melhor modelo otimizado:

- Algoritmo: `RandomForest`
- F1 macro em teste: 0.9749
- Acurácia em teste: 0.9761

O modelo otimizado não superou o modelo final atual no conjunto de teste, portanto não foi promovido para `final_pipeline.joblib`.

## Cenarios de Redundancia

| Cenário | Melhor modelo | Acurácia média | F1 macro médio |
|---|---|---:|---:|
| Modelo completo | RandomForest | 0.9871 | 0.9868 |
| Sem derivadas redundantes | GradientBoosting | 0.9641 | 0.9627 |
| Preventivo/comportamental | RandomForest | 0.8807 | 0.8791 |

O modelo completo possui melhor desempenho, mas usa variaveis antropometricas fortes (`Weight`, `Height`, `BMI`). O cenario preventivo reduz redundancias clinicas e ainda supera o requisito minimo.

## Interpretabilidade

Artefatos gerados:

- `reports/figures/confusion_matrix_final_model.png`
- `reports/figures/feature_importance_top15.png`
- `reports/figures/permutation_importance_top15.png`
- `reports/model_results/classification_report.csv`
- `reports/model_results/feature_importance.csv`
- `reports/model_results/permutation_importance.csv`

## Limitacoes

- O dataset aparenta ter forte relacao entre peso, altura, IMC e a classe alvo.
- O alto desempenho pode refletir regras antropometricas do proprio alvo.
- O modelo nao substitui avaliacao medica.
- O sistema deve ser usado apenas como apoio educacional/analitico.
