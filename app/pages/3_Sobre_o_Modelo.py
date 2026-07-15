import json

import streamlit as st

from src.config import METRICS_PATH, MODEL_METADATA_PATH

st.set_page_config(page_title="Sobre o Modelo", layout="wide")
st.title("Sobre o Modelo")

if METRICS_PATH.exists():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    st.subheader("Metricas")
    st.json(metrics)
else:
    st.info("Metricas ainda nao encontradas. Treine e exporte o modelo final.")

if MODEL_METADATA_PATH.exists():
    metadata = json.loads(MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    st.subheader("Metadados")
    st.json(metadata)
else:
    st.info("Metadados ainda nao encontrados.")

st.subheader("Limitacoes")
st.write(
    "Este sistema e uma ferramenta educacional de apoio a decisao. "
    "O resultado nao substitui avaliacao medica, exame clinico ou protocolo hospitalar."
)

