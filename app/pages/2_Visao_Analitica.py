import streamlit as st

from src.config import RAW_DATA_PATH
from src.data_loading import load_obesity_data

st.set_page_config(page_title="Visao Analitica", layout="wide")
st.title("Visao Analitica")

try:
    df = load_obesity_data(RAW_DATA_PATH)
except Exception as exc:
    st.warning(str(exc))
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Registros", f"{len(df):,}".replace(",", "."))
col2.metric("Colunas", df.shape[1])
col3.metric("Duplicatas", int(df.duplicated().sum()))

st.subheader("Distribuicao do nivel de obesidade")
st.bar_chart(df["Obesity"].value_counts())

st.subheader("Resumo numerico")
st.dataframe(df.describe(), use_container_width=True)

st.subheader("Amostra dos dados")
st.dataframe(df.head(50), use_container_width=True)

