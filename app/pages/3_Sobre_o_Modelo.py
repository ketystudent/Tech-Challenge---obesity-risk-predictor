import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
    "Métricas, comparação, matriz de confusão e interpretabilidade do modelo preventivo.",
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
        modelos_grafico = comparacao_modelos.sort_values("F1 macro médio", ascending=False)
        posicoes = np.arange(len(modelos_grafico))
        fig, ax = plt.subplots(figsize=(11, 5.5))
        ax.hlines(
            y=posicoes,
            xmin=modelos_grafico["F1 macro médio"],
            xmax=modelos_grafico["Acurácia média"],
            color="#b8cbd7",
            linewidth=3,
        )
        ax.scatter(
            modelos_grafico["Acurácia média"], posicoes,
            color="#0f9f9a", s=90, label="Acurácia média", zorder=3,
        )
        ax.scatter(
            modelos_grafico["F1 macro médio"], posicoes,
            color="#072b4a", s=90, label="F1 macro médio", zorder=3,
        )
        for posicao, (_, linha) in enumerate(modelos_grafico.iterrows()):
            ax.annotate(
                f"{linha['F1 macro médio']:.4f}",
                (linha["F1 macro médio"], posicao),
                xytext=(-8, 9), textcoords="offset points", ha="right", fontsize=8,
            )
            ax.annotate(
                f"{linha['Acurácia média']:.4f}",
                (linha["Acurácia média"], posicao),
                xytext=(8, -14), textcoords="offset points", ha="left", fontsize=8,
            )
        menor_score = min(
            modelos_grafico["Acurácia média"].min(),
            modelos_grafico["F1 macro médio"].min(),
        )
        ax.set_xlim(max(0, menor_score - 0.025), 1.005)
        ax.set_yticks(posicoes, modelos_grafico["Modelo"])
        ax.invert_yaxis()
        ax.set_xlabel("Score médio na validação cruzada")
        ax.set_title("Acurácia e F1 macro por modelo")
        ax.grid(axis="x", alpha=0.2)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.legend(loc="lower right")
        plt.tight_layout()
        st.pyplot(fig)
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
    metadata = {}
    st.info("Metadados ainda não encontrados.")

preventive_model = metadata.get("model_purpose") == "preventive_behavioral_tendency"

if preventive_model:
    st.subheader("Configuração preventiva")
    st.info(
        "O modelo final não utiliza peso, altura, IMC ou classes derivadas dessas medidas. "
        "A redução de desempenho é esperada e evita que a estimativa apenas reproduza a classificação antropométrica."
    )

st.subheader("Otimização anterior" if preventive_model else "Otimização")
tuning_results_path = REPORTS_DIR / "model_results" / "tuning_results.csv"
if preventive_model:
    st.caption(
        "Os artefatos de otimização existentes pertencem ao cenário antropométrico anterior e não são usados pelo modelo publicado."
    )
elif tuning_results_path.exists():
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
