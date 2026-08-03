# Publicação no Streamlit Community Cloud

## Status

O projeto está preparado para publicação no Streamlit Community Cloud.

Validacoes locais realizadas:

- `pytest`: 7 testes passando.
- Sintaxe dos arquivos principais: OK.
- Streamlit local: respondeu HTTP 200.

## Arquivos Necessarios

Os arquivos abaixo precisam estar versionados no GitHub:

```text
app/
data/raw/Obesity.csv
docs/
models/final_pipeline.joblib
models/label_encoder.joblib
models/metrics.json
models/model_metadata.json
reports/
src/
.streamlit/config.toml
requirements.txt
runtime.txt
README.md
```

## Configuração no Streamlit Cloud

No Streamlit Community Cloud, crie um app com:

```text
Repository: ketystudent/Tech-Challenge---obesity-risk-predictor
Branch: main
Main file path: app/Inicio.py
```

Se estiver usando outra branch, selecione a branch correspondente.

## Passos

1. Confirme que os arquivos finais estao no GitHub.
2. Acesse `https://share.streamlit.io`.
3. Clique em `Create app` (Criar aplicativo).
4. Escolha a opcao para usar um app existente no GitHub.
5. Selecione o repositorio.
6. Configure o caminho principal como `app/Inicio.py`.
7. Clique em `Deploy` (Publicar).
8. Aguarde a instalacao das dependencias.
9. Copie a URL final gerada.

## Observacoes

- O arquivo `requirements.txt` esta na raiz do repositorio, que e um local aceito pelo Streamlit Cloud.
- O arquivo `.streamlit/config.toml` tambem esta na raiz, como recomendado.
- O app usa caminhos relativos a raiz do repositorio, o mesmo padrao usado no Streamlit Cloud.
- O modelo final e carregado de `models/final_pipeline.joblib`.

## Solução de Problemas

Se o aplicativo falhar na publicação:

1. Verifique se `models/final_pipeline.joblib` e `models/label_encoder.joblib` estao no GitHub.
2. Verifique se `data/raw/Obesity.csv` esta no GitHub.
3. Confira se a versao do Python esta como `python-3.12`.
4. Abra os logs do app no Streamlit Cloud.
5. Se houver erro de dependencia, ajuste `requirements.txt`.
