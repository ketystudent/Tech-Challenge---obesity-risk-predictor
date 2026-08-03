import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import RAW_DATA_PATH, REPORTS_DIR, TARGET_COLUMN
from src.data_loading import load_obesity_data
from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar

st.set_page_config(page_title="Visão Analítica | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Visão analítica",
    "Painel de exploração dos dados, perfil clínico e hábitos associados aos níveis de obesidade.",
)
render_status_bar("Dados carregados", "Base limpa e relatórios analíticos disponíveis")

try:
    df = load_obesity_data(RAW_DATA_PATH)
except Exception as exc:
    st.warning(str(exc))
    st.stop()

df_clean = df.drop_duplicates().reset_index(drop=True)
eda_summary_path = REPORTS_DIR / "eda" / "eda_summary.json"
figures_dir = REPORTS_DIR / "figures"

if eda_summary_path.exists():
    eda_summary = json.loads(eda_summary_path.read_text(encoding="utf-8"))
else:
    eda_summary = {}

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Registros", f"{len(df_clean):,}".replace(",", "."), "Após remoção de duplicatas")
with col2:
    metric_card("Colunas", str(df.shape[1]), "Variáveis da base original")
with col3:
    metric_card("Duplicatas", str(int(df.duplicated().sum())), "Registros removidos na modelagem")

tab_overview, tab_profile, tab_behavior, tab_figures, tab_data = st.tabs(
    ["Resumo", "Perfil Clínico", "Hábitos", "Figuras", "Dados"]
)


def plot_grouped_rate(column: str, title: str):
    grouped = (
        pd.crosstab(df_clean[column], df_clean[TARGET_COLUMN], normalize="index")
        .mul(100)
        .round(1)
        .sort_index()
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    grouped.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title(title)
    ax.set_xlabel(column)
    ax.set_ylabel("% dentro do grupo")
    ax.legend(title="Nível", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


def plot_box(column: str, title: str):
    classes = sorted(df_clean[TARGET_COLUMN].unique())
    values = [df_clean.loc[df_clean[TARGET_COLUMN] == class_name, column].values for class_name in classes]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.boxplot(values, tick_labels=classes, patch_artist=True)
    ax.set_title(title)
    ax.set_xlabel("Nível de obesidade")
    ax.set_ylabel(column)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


with tab_overview:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Distribuição do nível de obesidade")
        target_distribution = df_clean[TARGET_COLUMN].value_counts()
        st.bar_chart(target_distribution)
    with right:
        st.subheader("Principais pontos")
        duplicates = eda_summary.get("duplicate_rows", int(df.duplicated().sum()))
        missing_total = sum(eda_summary.get("missing_values", {}).values())
        st.markdown(
            f"""
            <div class="vc-card">
                <div class="vc-card-title">Leitura executiva</div>
                <div class="vc-card-muted">
                    A base possui {len(df_clean)} registros após remover {duplicates} duplicatas.
                    O total de valores ausentes encontrados foi {missing_total}. As classes apresentam
                    distribuição relativamente equilibrada, e peso/altura concentram grande parte do
                    sinal preditivo.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Resumo numérico")
    st.dataframe(df_clean.describe(), use_container_width=True)

with tab_profile:
    col_age, col_weight = st.columns(2)
    with col_age:
        plot_box("Age", "Idade por nível de obesidade")
    with col_weight:
        plot_box("Weight", "Peso por nível de obesidade")

    fig, ax = plt.subplots(figsize=(10, 6))
    for class_name in sorted(df_clean[TARGET_COLUMN].unique()):
        subset = df_clean[df_clean[TARGET_COLUMN] == class_name]
        ax.scatter(subset["Height"], subset["Weight"], alpha=0.65, s=25, label=class_name)
    ax.set_title("Peso e altura por nível de obesidade")
    ax.set_xlabel("Altura (m)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(title="Nível", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    st.pyplot(fig)

with tab_behavior:
    col_a, col_b = st.columns(2)
    with col_a:
        plot_grouped_rate("family_history", "Histórico familiar por nível de obesidade")
        plot_grouped_rate("FAVC", "Consumo frequente de alimentos calóricos")
    with col_b:
        plot_grouped_rate("CAEC", "Consumo entre refeições")
        plot_grouped_rate("MTRANS", "Meio de transporte")

    st.subheader("Médias de hábitos por classe")
    habit_summary = (
        df_clean.groupby(TARGET_COLUMN)[["FCVC", "NCP", "CH2O", "FAF", "TUE"]]
        .mean()
        .round(2)
        .reset_index()
    )
    st.dataframe(habit_summary, use_container_width=True)

with tab_figures:
    figure_files = [
        ("Distribuição do alvo", "target_distribution.png"),
        ("Histogramas numéricos", "numeric_histograms.png"),
        ("Correlação numérica", "numeric_correlation_heatmap.png"),
        ("Peso x altura", "weight_height_by_obesity.png"),
        ("Idade por classe", "age_by_obesity.png"),
        ("Peso por classe", "weight_by_obesity.png"),
    ]
    for title, filename in figure_files:
        path = figures_dir / filename
        if path.exists():
            st.subheader(title)
            st.image(str(path), use_container_width=True)
        else:
            st.info(f"Figura ainda não gerada: {filename}")

with tab_data:
    st.subheader("Amostra dos dados")
    st.dataframe(df_clean.head(100), use_container_width=True)

    st.subheader("Valores únicos categóricos")
    categorical_summary = {
        column: ", ".join(sorted(df_clean[column].dropna().astype(str).unique()))
        for column in df_clean.select_dtypes(include="object").columns
    }
    st.dataframe(
        pd.DataFrame(categorical_summary.items(), columns=["Coluna", "Valores"]),
        use_container_width=True,
    )
