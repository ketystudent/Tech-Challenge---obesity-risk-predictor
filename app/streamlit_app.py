import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Obesity Risk Predictor", page_icon="🩺", layout="wide")

st.title("Obesity Risk Predictor")
st.write("Aplicacao de apoio a triagem para prever o nivel de obesidade a partir de dados clinicos e habitos de vida.")

st.info("Use o menu lateral para acessar predicao, visao analitica e informacoes do modelo.")
