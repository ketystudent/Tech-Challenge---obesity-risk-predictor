# Cartão do Modelo

## Objetivo

Modelo multiclasse para estimar tendências associadas aos níveis de obesidade a partir de informações pessoais, histórico familiar e hábitos de vida.

## Modelo Final

- Algoritmo: `RandomForestClassifier`
- Pipeline: engenharia de atributos + `ColumnTransformer` + classificador
- Finalidade: tendência preventiva/comportamental
- Variáveis excluídas: peso, altura, IMC, classe de IMC e classe de peso
- Artefato: `models/final_pipeline.joblib`
- Encoder: `models/label_encoder.joblib`
- Conjunto de dados usado: `data/raw/Obesity.csv`
- Registros originais: 2.111
- Duplicatas removidas no treino: 24
- Registros usados apos limpeza: 2.087

## Metricas no Conjunto de Teste

| Metrica | Valor |
|---|---:|
| Acurácia | 0.8445 |
| Precisão macro | 0.8429 |
| Revocação macro | 0.8408 |
| F1 macro | 0.8410 |

O desempenho atende ao requisito minimo do desafio, que pede assertividade acima de 75%.

## Comparacao de Modelos

Melhor modelo na comparacao inicial:

| Modelo | Acurácia média na validação cruzada | F1 macro médio na validação cruzada |
|---|---:|---:|
| RandomForest | 0.8508 | 0.8467 |
| ExtraTrees | 0.8274 | 0.8224 |
| GradientBoosting | 0.8083 | 0.8042 |
| DecisionTree | 0.7478 | 0.7398 |
| SVM | 0.7280 | 0.7194 |
| KNN | 0.7238 | 0.7038 |
| LogisticRegression | 0.6207 | 0.6022 |

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

O cenário preventivo foi promovido a modelo final. Ele não utiliza as variáveis antropométricas que definem diretamente a classe alvo, embora apresente desempenho inferior ao cenário completo.

## Interpretabilidade

Artefatos gerados:

- `reports/figures/confusion_matrix_final_model.png`
- `reports/figures/feature_importance_top15.png`
- `reports/figures/permutation_importance_top15.png`
- `reports/model_results/classification_report.csv`
- `reports/model_results/feature_importance.csv`
- `reports/model_results/permutation_importance.csv`

## Limitacoes

- O alvo original descreve o estado atual e não um desfecho futuro acompanhado longitudinalmente.
- A saída representa tendência comportamental associada às classes observadas, não previsão causal de obesidade futura.
- O modelo nao substitui avaliacao medica.
- O sistema deve ser usado apenas como apoio educacional/analitico.
