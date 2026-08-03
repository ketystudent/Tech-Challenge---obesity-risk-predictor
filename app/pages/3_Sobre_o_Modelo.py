import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.downloads import botao_download_csv
from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar
from src.config import METRICS_PATH, MODEL_METADATA_PATH, REPORTS_DIR

st.set_page_config(page_title="Sobre o Modelo | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Informações do modelo",
    "Métricas, otimização, matriz de confusão e interpretabilidade da pipeline final.",
)
render_status_bar("Modelo validado", "Artefatos finais carregados para auditoria")

if METRICS_PATH.exists():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Acurácia", f"{metrics.get('accuracy', 0):.4f}", "Conjunto de teste")
    with col2:
        metric_card("F1 macro", f"{metrics.get('f1_macro', 0):.4f}", "Métrica principal")
    with col3:
        metric_card("Precisão macro", f"{metrics.get('precision_macro', 0):.4f}", "Média entre classes")
    with col4:
        metric_card("Revocação macro", f"{metrics.get('recall_macro', 0):.4f}", "Média entre classes")

    with st.expander("Métricas completas"):
        st.json(metrics)

    comparacao_modelos = pd.DataFrame(metrics.get("comparison", []))
    if not comparacao_modelos.empty:
        comparacao_modelos = comparacao_modelos.rename(
            columns={
                "model": "Modelo",
                "accuracy_mean": "Acurácia média",
                "accuracy_std": "Desvio da acurácia",
                "f1_macro_mean": "F1 macro médio",
                "f1_macro_std": "Desvio do F1 macro",
                "precision_macro_mean": "Precisão macro média",
                "recall_macro_mean": "Revocação macro média",
            }
        ).sort_values("F1 macro médio", ascending=False)
        comparacao_modelos.insert(0, "Posição", range(1, len(comparacao_modelos) + 1))

        st.subheader("Comparação dos modelos")
        st.caption(
            "Scores médios obtidos na validação cruzada. O F1 macro considera igualmente o desempenho nas sete classes."
        )
        st.dataframe(
            comparacao_modelos.style.format(
                {
                    "Acurácia média": "{:.4f}",
                    "Desvio da acurácia": "{:.4f}",
                    "F1 macro médio": "{:.4f}",
                    "Desvio do F1 macro": "{:.4f}",
                    "Precisão macro média": "{:.4f}",
                    "Revocação macro média": "{:.4f}",
                }
            ).highlight_max(subset=["Acurácia média", "F1 macro médio"], color="#d9f3ef"),
            use_container_width=True,
            hide_index=True,
        )
        st.bar_chart(
            comparacao_modelos,
            x="Modelo",
            y=["Acurácia média", "F1 macro médio"],
            horizontal=True,
            x_label="Score médio",
            y_label="Modelo",
        )
        botao_download_csv(
            comparacao_modelos,
            "comparacao_scores_modelos.csv",
            key="download_comparacao_modelos",
        )
else:
    st.info("Métricas ainda não encontradas. Treine e exporte o modelo final.")

if MODEL_METADATA_PATH.exists():
    metadata = json.loads(MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    st.subheader("Metadados")
    st.json(metadata)
else:
    st.info("Metadados ainda não encontrados.")

st.subheader("Otimização")
tuning_results_path = REPORTS_DIR / "model_results" / "tuning_results.csv"
if tuning_results_path.exists():
    tuning_results = pd.read_csv(tuning_results_path)
    st.dataframe(tuning_results, use_container_width=True)
    botao_download_csv(
        tuning_results,
        "resultados_otimizacao_modelos.csv",
        key="download_otimizacao",
    )
    tuned_metrics_path = REPORTS_DIR.parent / "models" / "tuned_metrics.json"
    if tuned_metrics_path.exists():
        tuned_metrics = json.loads(tuned_metrics_path.read_text(encoding="utf-8"))
        st.caption(
            "O modelo otimizado é mantido como artefato separado. "
            "Ele só deve substituir o modelo final se superar as métricas atuais no conjunto de teste."
        )
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Melhor modelo otimizado", tuned_metrics.get("winner", "-"))
        col_t2.metric("Acurácia otimizada", f"{tuned_metrics.get('accuracy', 0):.4f}")
        col_t3.metric("F1 macro otimizado", f"{tuned_metrics.get('f1_macro', 0):.4f}")
else:
    st.info("Resultados da otimização ainda não encontrados.")

st.subheader("Matriz de Confusão")
confusion_matrix_path = REPORTS_DIR / "figures" / "confusion_matrix_final_model.png"
if confusion_matrix_path.exists():
    st.image(str(confusion_matrix_path), use_container_width=True)
else:
    st.info("Matriz de confusão ainda não gerada.")

st.subheader("Importância das Variáveis")
col_feature, col_perm = st.columns(2)

with col_feature:
    st.caption("Importância nativa do modelo")
    feature_importance_path = REPORTS_DIR / "figures" / "feature_importance_top15.png"
    feature_importance_csv = REPORTS_DIR / "model_results" / "feature_importance.csv"
    if feature_importance_path.exists():
        st.image(str(feature_importance_path), use_container_width=True)
    if feature_importance_csv.exists():
        feature_importance = pd.read_csv(feature_importance_csv).head(15)
        st.dataframe(feature_importance, use_container_width=True)
        botao_download_csv(
            feature_importance,
            "importancia_variaveis_modelo.csv",
            key="download_importancia_modelo",
        )

with col_perm:
    st.caption("Importância por permutação")
    permutation_path = REPORTS_DIR / "figures" / "permutation_importance_top15.png"
    permutation_csv = REPORTS_DIR / "model_results" / "permutation_importance.csv"
    if permutation_path.exists():
        st.image(str(permutation_path), use_container_width=True)
    if permutation_csv.exists():
        permutation_importance = pd.read_csv(permutation_csv).head(15)
        st.dataframe(permutation_importance, use_container_width=True)
        botao_download_csv(
            permutation_importance,
            "importancia_variaveis_permutacao.csv",
            key="download_importancia_permutacao",
        )

st.subheader("Limitações")
st.write(
    "Este sistema é uma ferramenta educacional de apoio à decisão. "
    "O resultado não substitui avaliação médica, exame clínico ou protocolo hospitalar."
)
