# Obesity Risk Predictor

Projeto de Machine Learning para prever o nivel de obesidade a partir de dados clinicos e habitos de vida.

## Estado Atual

Esta base foi reorganizada a partir de notebooks exportados do Google Colab. Os arquivos originais foram preservados na raiz nesta primeira etapa.

## Estrutura

- `src/`: logica reutilizavel de dados, validacao, features, pipeline, modelagem, avaliacao e predicao.
- `app/`: aplicacao Streamlit.
- `data/raw/`: local esperado para `Obesity.csv`.
- `models/`: artefatos gerados pelo treinamento.
- `tests/`: testes automatizados minimos.
- `reports/`: graficos e resultados.

## Como Executar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Coloque o dataset em:

```text
data/raw/Obesity.csv
```

Execute os testes:

```bash
pytest
```

Execute o app:

```bash
streamlit run app/streamlit_app.py
```

## Observacao Medica

Este projeto tem finalidade educacional e nao substitui avaliacao medica.

