import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.config import RAW_DATA_PATH, REPORTS_DIR, TARGET_COLUMN
from src.data_loading import load_obesity_data

st.set_page_config(page_title="Visao Analitica", layout="wide")
st.title("Visao Analitica")

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
col1.metric("Registros", f"{len(df_clean):,}".replace(",", "."))
col2.metric("Colunas", df.shape[1])
col3.metric("Duplicatas", int(df.duplicated().sum()))

tab_overview, tab_profile, tab_behavior, tab_figures, tab_data = st.tabs(
    ["Resumo", "Perfil Clinico", "Habitos", "Figuras", "Dados"]
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
    ax.legend(title="Nivel", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


def plot_box(column: str, title: str):
    classes = sorted(df_clean[TARGET_COLUMN].unique())
    values = [df_clean.loc[df_clean[TARGET_COLUMN] == class_name, column].values for class_name in classes]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.boxplot(values, tick_labels=classes, patch_artist=True)
    ax.set_title(title)
    ax.set_xlabel("Nivel de obesidade")
    ax.set_ylabel(column)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


with tab_overview:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Distribuicao do nivel de obesidade")
        target_distribution = df_clean[TARGET_COLUMN].value_counts()
        st.bar_chart(target_distribution)
    with right:
        st.subheader("Principais pontos")
        duplicates = eda_summary.get("duplicate_rows", int(df.duplicated().sum()))
        missing_total = sum(eda_summary.get("missing_values", {}).values())
        st.write(f"- A base possui {len(df_clean)} registros apos remover {duplicates} duplicatas.")
        st.write(f"- Total de valores ausentes encontrados: {missing_total}.")
        st.write("- As classes apresentam distribuicao relativamente equilibrada para classificacao multiclasse.")
        st.write("- Peso e altura concentram grande parte do sinal preditivo, exigindo leitura clinica cuidadosa.")

    st.subheader("Resumo numerico")
    st.dataframe(df_clean.describe(), use_container_width=True)

with tab_profile:
    col_age, col_weight = st.columns(2)
    with col_age:
        plot_box("Age", "Idade por nivel de obesidade")
    with col_weight:
        plot_box("Weight", "Peso por nivel de obesidade")

    fig, ax = plt.subplots(figsize=(10, 6))
    for class_name in sorted(df_clean[TARGET_COLUMN].unique()):
        subset = df_clean[df_clean[TARGET_COLUMN] == class_name]
        ax.scatter(subset["Height"], subset["Weight"], alpha=0.65, s=25, label=class_name)
    ax.set_title("Peso e altura por nivel de obesidade")
    ax.set_xlabel("Altura (m)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(title="Nivel", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    st.pyplot(fig)

with tab_behavior:
    col_a, col_b = st.columns(2)
    with col_a:
        plot_grouped_rate("family_history", "Historico familiar por nivel de obesidade")
        plot_grouped_rate("FAVC", "Consumo frequente de alimentos caloricos")
    with col_b:
        plot_grouped_rate("CAEC", "Consumo entre refeicoes")
        plot_grouped_rate("MTRANS", "Meio de transporte")

    st.subheader("Medias de habitos por classe")
    habit_summary = (
        df_clean.groupby(TARGET_COLUMN)[["FCVC", "NCP", "CH2O", "FAF", "TUE"]]
        .mean()
        .round(2)
        .reset_index()
    )
    st.dataframe(habit_summary, use_container_width=True)

with tab_figures:
    figure_files = [
        ("Distribuicao do alvo", "target_distribution.png"),
        ("Histogramas numericos", "numeric_histograms.png"),
        ("Correlacao numerica", "numeric_correlation_heatmap.png"),
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
            st.info(f"Figura ainda nao gerada: {filename}")

with tab_data:
    st.subheader("Amostra dos dados")
    st.dataframe(df_clean.head(100), use_container_width=True)

    st.subheader("Valores unicos categoricos")
    categorical_summary = {
        column: ", ".join(sorted(df_clean[column].dropna().astype(str).unique()))
        for column in df_clean.select_dtypes(include="object").columns
    }
    st.dataframe(
        pd.DataFrame(categorical_summary.items(), columns=["Coluna", "Valores"]),
        use_container_width=True,
    )
