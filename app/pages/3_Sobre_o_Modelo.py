import json

import pandas as pd
import streamlit as st

from src.config import METRICS_PATH, MODEL_METADATA_PATH, REPORTS_DIR

st.set_page_config(page_title="Sobre o Modelo", layout="wide")
st.title("Sobre o Modelo")

if METRICS_PATH.exists():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    st.subheader("Metricas")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
    col2.metric("F1 macro", f"{metrics.get('f1_macro', 0):.4f}")
    col3.metric("Precision macro", f"{metrics.get('precision_macro', 0):.4f}")
    col4.metric("Recall macro", f"{metrics.get('recall_macro', 0):.4f}")

    with st.expander("Metricas completas"):
        st.json(metrics)
else:
    st.info("Metricas ainda nao encontradas. Treine e exporte o modelo final.")

if MODEL_METADATA_PATH.exists():
    metadata = json.loads(MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    st.subheader("Metadados")
    st.json(metadata)
else:
    st.info("Metadados ainda nao encontrados.")

st.subheader("Tuning")
tuning_results_path = REPORTS_DIR / "model_results" / "tuning_results.csv"
if tuning_results_path.exists():
    tuning_results = pd.read_csv(tuning_results_path)
    st.dataframe(tuning_results, use_container_width=True)
    tuned_metrics_path = REPORTS_DIR.parent / "models" / "tuned_metrics.json"
    if tuned_metrics_path.exists():
        tuned_metrics = json.loads(tuned_metrics_path.read_text(encoding="utf-8"))
        st.caption(
            "O modelo tunado e mantido como artefato separado. "
            "Ele so deve substituir o modelo final se superar as metricas atuais no conjunto de teste."
        )
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Tuned winner", tuned_metrics.get("winner", "-"))
        col_t2.metric("Tuned accuracy", f"{tuned_metrics.get('accuracy', 0):.4f}")
        col_t3.metric("Tuned F1 macro", f"{tuned_metrics.get('f1_macro', 0):.4f}")
else:
    st.info("Resultados de tuning ainda nao encontrados.")

st.subheader("Matriz de Confusao")
confusion_matrix_path = REPORTS_DIR / "figures" / "confusion_matrix_final_model.png"
if confusion_matrix_path.exists():
    st.image(str(confusion_matrix_path), use_container_width=True)
else:
    st.info("Matriz de confusao ainda nao gerada.")

st.subheader("Importancia das Variaveis")
col_feature, col_perm = st.columns(2)

with col_feature:
    st.caption("Importancia nativa do modelo")
    feature_importance_path = REPORTS_DIR / "figures" / "feature_importance_top15.png"
    feature_importance_csv = REPORTS_DIR / "model_results" / "feature_importance.csv"
    if feature_importance_path.exists():
        st.image(str(feature_importance_path), use_container_width=True)
    if feature_importance_csv.exists():
        st.dataframe(pd.read_csv(feature_importance_csv).head(15), use_container_width=True)

with col_perm:
    st.caption("Permutation importance")
    permutation_path = REPORTS_DIR / "figures" / "permutation_importance_top15.png"
    permutation_csv = REPORTS_DIR / "model_results" / "permutation_importance.csv"
    if permutation_path.exists():
        st.image(str(permutation_path), use_container_width=True)
    if permutation_csv.exists():
        st.dataframe(pd.read_csv(permutation_csv).head(15), use_container_width=True)

st.subheader("Limitacoes")
st.write(
    "Este sistema e uma ferramenta educacional de apoio a decisao. "
    "O resultado nao substitui avaliacao medica, exame clinico ou protocolo hospitalar."
)
