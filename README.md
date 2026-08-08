# Preditor de Risco de Obesidade

Aplicação de aprendizado de máquina para estimar tendências associadas aos níveis de obesidade a partir de histórico e hábitos de vida. O projeto foi estruturado para atender ao Tech Challenge FIAP, com pipeline reproduzível, modelo serializado, painel analítico e aplicação em Streamlit.

## Problema de Negocio

Um hospital deseja apoiar a equipe médica na triagem de tendências relacionadas à obesidade. A solução final usa informações pessoais, histórico familiar e hábitos de vida, sem peso, altura ou IMC, evitando reproduzir diretamente a classificação antropométrica atual.

Este sistema e uma ferramenta educacional de apoio a decisao e nao substitui avaliacao medica.

## Estrutura

```text
app/                 Aplicacao Streamlit
data/raw/            Dataset original
docs/                Documentacao propria do projeto
models/              Artefatos de modelo e metricas
reports/eda/         Resumos de EDA
reports/figures/     Graficos gerados
reports/model_results/ Resultados de modelos
scripts/             Scripts reproduziveis
src/                 Codigo reutilizavel
tests/               Testes automatizados
```

## Conjunto de Dados

Arquivo esperado:

```text
data/raw/Obesity.csv
```

Resumo:

- Registros originais: 2.111
- Registros apos remocao de duplicatas: 2.087
- Duplicatas removidas: 24
- Valores ausentes: 0
- Classes alvo: 7

Veja o dicionario em [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## Pipeline

A pipeline preventiva final contém:

1. Engenharia de atributos com transformadores compatíveis com Scikit-Learn.
2. `ColumnTransformer` para numericas e categoricas.
3. `StandardScaler` nos atributos numéricos.
4. `OneHotEncoder(handle_unknown="ignore")` nas categoricas.
5. Classificador final `RandomForestClassifier`.

Atributos criados:

- `Faixa_Etaria`
- `Active_Lifestyle`
- `Healthy_Diet`
- `Good_Hydration`
- `High_Screen_Time`
- `Healthy_Score`

## Modelo Final

Modelo escolhido: `RandomForestClassifier`

Metricas no conjunto de teste:

| Metrica | Valor |
|---|---:|
| Acurácia | 0.8445 |
| Precisão macro | 0.8429 |
| Revocação macro | 0.8408 |
| F1 macro | 0.8410 |

O requisito minimo do desafio era assertividade acima de 75%, portanto o modelo atende ao criterio.

Mais detalhes em [docs/MODEL_CARD.md](docs/MODEL_CARD.md).

## Experimentos

Scripts principais:

```bash
python scripts/generate_eda_report.py
python scripts/evaluate_accuracy.py
python scripts/compare_redundancy_scenarios.py
python scripts/train_model.py
python scripts/generate_model_interpretability.py
python scripts/tune_models.py --n-iter 8 --cv 3
```

Resultados importantes:

- Modelo completo antropométrico: F1 macro médio 0.9868 (referência experimental).
- Sem atributos derivados redundantes: F1 macro médio 0.9627.
- Modelo preventivo/comportamental: F1 macro medio 0.8791.
- Modelo preventivo publicado, sem peso e altura: F1 macro em teste 0.8410.

Resumo em [docs/RESULTS_SUMMARY.md](docs/RESULTS_SUMMARY.md).

## Como Executar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Treine/exporte o modelo:

```bash
python scripts/train_model.py
```

Gere relatorios e figuras:

```bash
python scripts/generate_eda_report.py
python scripts/generate_model_interpretability.py
```

Execute os testes:

```bash
pytest
```

Execute o app:

```bash
streamlit run app/streamlit_app.py
```

## Aplicacao Streamlit

A aplicacao possui:

- Predicao individual.
- Visão analítica com distribuições e análises.
- Informações do modelo, métricas, otimização, matriz de confusão e importância dos atributos.

## Artefatos

```text
models/final_pipeline.joblib
models/label_encoder.joblib
models/metrics.json
models/model_metadata.json
```

## Limitacoes

- O alvo original possui forte relação com peso, altura e IMC, mas essas variáveis não entram no modelo publicado.
- A base não acompanha pessoas ao longo do tempo; portanto, a saída é uma associação de tendência, não uma previsão causal futura.
- O cenário preventivo tem menor desempenho que o antropométrico, mas permanece acima do critério mínimo.
- O resultado deve ser interpretado como apoio preventivo, não como diagnóstico médico.

## Links de Entrega

Preencher antes do envio final:

- App Streamlit: `TODO`
- Painel: `TODO`
- Repositorio GitHub: `TODO`
- Video: `TODO`

Instrucoes de deploy: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).
