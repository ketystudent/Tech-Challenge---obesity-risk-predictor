import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.downloads import botao_download_csv
from app.ui import apply_theme, render_page_header, render_sidebar, render_status_bar
from src.config import CLASS_LABELS_PT, CLASS_ORDER, RAW_DATA_PATH, TARGET_COLUMN
from src.data_loading import load_obesity_data

st.set_page_config(page_title="Painel Clínico | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Painel de saúde e obesidade",
    "Visão populacional para apoiar triagem, prevenção e discussão clínica multiprofissional.",
    "Inteligência clínica",
)
render_status_bar("Dados disponíveis", "Indicadores calculados a partir da população selecionada")

CORES_CLASSES = ["#4C78A8", "#54A24B", "#F2CF5B", "#F28E2B", "#E45756", "#B14A77", "#7A3E9D"]
ROTULOS_COLUNAS = {
    "Gender": "Gênero", "Age": "Idade", "Height": "Altura", "Weight": "Peso",
    "family_history": "Histórico familiar", "FAVC": "Alimentos calóricos",
    "FCVC": "Vegetais", "NCP": "Refeições principais", "CAEC": "Entre refeições",
    "SMOKE": "Tabagismo", "CH2O": "Água", "SCC": "Monitoramento de calorias",
    "FAF": "Atividade física", "TUE": "Tempo de tela", "CALC": "Álcool",
    "MTRANS": "Transporte", TARGET_COLUMN: "Nível de peso",
}
ROTULOS_VALORES = {
    "Female": "Feminino", "Male": "Masculino", "yes": "Sim", "no": "Não",
    "Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre",
    "Walking": "A pé", "Bike": "Bicicleta", "Motorbike": "Motocicleta",
    "Automobile": "Automóvel", "Public_Transportation": "Transporte público",
    **CLASS_LABELS_PT,
}
CLASSES_OBESIDADE = {"Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III"}
CLASSES_EXCESSO = CLASSES_OBESIDADE | {"Overweight_Level_I", "Overweight_Level_II"}


def percentual(parte: int, total: int) -> float:
    return 100 * parte / total if total else 0.0


def taxa_obesidade(base: pd.DataFrame) -> float:
    return percentual(base[TARGET_COLUMN].isin(CLASSES_OBESIDADE).sum(), len(base))


def formatar_delta(valor: float) -> str:
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.1f} p.p. vs. população total"


def traduzir_dataframe(base: pd.DataFrame) -> pd.DataFrame:
    exibicao = base.rename(columns=ROTULOS_COLUNAS).copy()
    for coluna in exibicao.select_dtypes(include="object").columns:
        exibicao[coluna] = exibicao[coluna].map(lambda valor: ROTULOS_VALORES.get(valor, valor))
    return exibicao


def categorizar_habito(base: pd.DataFrame, coluna: str) -> pd.Series:
    if coluna == "FAF":
        return pd.cut(
            base[coluna], [-0.01, 0.99, 1.99, 3],
            labels=["Baixa", "Moderada", "Alta"],
        )
    if coluna == "CH2O":
        return pd.cut(
            base[coluna], [0.99, 1.66, 2.33, 3],
            labels=["Baixo", "Intermediário", "Alto"],
        )
    if coluna == "FCVC":
        return pd.cut(
            base[coluna], [0.99, 1.66, 2.33, 3],
            labels=["Baixa", "Intermediária", "Alta"],
        )
    if coluna == "TUE":
        return pd.cut(
            base[coluna], [-0.01, 0.66, 1.33, 2],
            labels=["Baixo", "Intermediário", "Alto"],
        )
    return base[coluna].map(lambda valor: ROTULOS_VALORES.get(str(valor), str(valor)))


def resumo_habito_por_grupo(base: pd.DataFrame, coluna: str, grupo: str) -> pd.DataFrame:
    dados = base.copy()
    dados["Categoria do hábito"] = categorizar_habito(dados, coluna)
    dados["Com obesidade"] = dados[TARGET_COLUMN].isin(CLASSES_OBESIDADE)
    resumo = (
        dados.groupby([grupo, "Categoria do hábito"], observed=True)
        .agg(Registros=(TARGET_COLUMN, "size"), Taxa_obesidade=("Com obesidade", "mean"))
        .reset_index()
    )
    resumo["Taxa de obesidade (%)"] = resumo.pop("Taxa_obesidade") * 100
    resumo[grupo] = resumo[grupo].map(lambda valor: ROTULOS_VALORES.get(str(valor), str(valor)))
    return resumo.rename(columns={grupo: ROTULOS_COLUNAS.get(grupo, grupo)})


try:
    df = load_obesity_data(RAW_DATA_PATH).drop_duplicates().reset_index(drop=True)
except Exception as exc:
    st.warning(str(exc))
    st.stop()

df = df.assign(IMC=df["Weight"] / df["Height"].pow(2))
df["Faixa etária"] = pd.cut(
    df["Age"], bins=[0, 17, 29, 39, 49, 59, float("inf")],
    labels=["Até 17", "18–29", "30–39", "40–49", "50–59", "60 ou mais"],
)

st.markdown("### Filtros da população")
filtro_1, filtro_2, filtro_3 = st.columns([1, 1, 2])
with filtro_1:
    generos = st.multiselect(
        "Gênero",
        ["Female", "Male"],
        format_func=lambda x: ROTULOS_VALORES[x],
        placeholder="Todos os gêneros",
    )
with filtro_2:
    faixas = st.multiselect(
        "Faixa etária",
        list(df["Faixa etária"].cat.categories),
        placeholder="Todas as faixas etárias",
    )
with filtro_3:
    classes = st.multiselect(
        "Nível de peso", CLASS_ORDER, format_func=lambda x: CLASS_LABELS_PT[x],
        placeholder="Todas as classificações",
    )

df_filtrado = df.copy()
if generos:
    df_filtrado = df_filtrado[df_filtrado["Gender"].isin(generos)]
if faixas:
    df_filtrado = df_filtrado[df_filtrado["Faixa etária"].isin(faixas)]
if classes:
    df_filtrado = df_filtrado[df_filtrado[TARGET_COLUMN].isin(classes)]

if df_filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados.")
    st.stop()

total = len(df_filtrado)
obesidade = df_filtrado[TARGET_COLUMN].isin(CLASSES_OBESIDADE).sum()
excesso_peso = df_filtrado[TARGET_COLUMN].isin(CLASSES_EXCESSO).sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Pessoas avaliadas", f"{total:,}".replace(",", "."), f"{percentual(total, len(df)):.1f}% da base")
kpi2.metric("Com obesidade", f"{percentual(obesidade, total):.1f}%", f"{obesidade} registros")
kpi3.metric("Sobrepeso ou obesidade", f"{percentual(excesso_peso, total):.1f}%", f"{excesso_peso} registros")
kpi4.metric("IMC médio (kg/m²)", f"{df_filtrado['IMC'].mean():.1f}", "Indicador descritivo")

st.caption(
    "Os percentuais descrevem esta base e não representam prevalência populacional. "
    "Os achados apoiam a triagem, mas não substituem anamnese, exame físico ou julgamento clínico."
)

tab_resumo, tab_recortes, tab_perfil, tab_habitos, tab_dados = st.tabs(
    ["Visão executiva", "Gênero e idade", "Perfil antropométrico", "Hábitos e contexto", "Dados da população"]
)

with tab_resumo:
    grafico, leitura = st.columns([1.25, 1])
    with grafico:
        st.subheader("Distribuição dos níveis de peso")
        distribuicao = df_filtrado[TARGET_COLUMN].value_counts().reindex(CLASS_ORDER, fill_value=0)
        fig, ax = plt.subplots(figsize=(9, 5))
        barras = ax.barh(
            [CLASS_LABELS_PT[classe] for classe in CLASS_ORDER],
            distribuicao.values,
            color=CORES_CLASSES,
        )
        ax.bar_label(barras, labels=[f"{percentual(v, total):.1f}%" for v in distribuicao], padding=4)
        ax.set_xlabel("Número de pessoas")
        ax.invert_yaxis()
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)

    with leitura:
        st.subheader("Leitura para a equipe")
        classe_principal = distribuicao.idxmax()
        st.markdown(
            f"""
            <div class="vc-card">
                <div class="vc-card-title">Panorama da população selecionada</div>
                <div class="vc-card-muted">
                    A classificação mais frequente é <strong>{CLASS_LABELS_PT[classe_principal]}</strong>,
                    com {distribuicao.max()} pessoas ({percentual(distribuicao.max(), total):.1f}%).
                    No conjunto, {percentual(excesso_peso, total):.1f}% estão nas faixas de sobrepeso
                    ou obesidade, um grupo relevante para avaliação clínica e ações preventivas.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info(
            "Prioridade sugerida para triagem: combinar classificação de peso, histórico familiar "
            "e hábitos modificáveis antes de definir qualquer encaminhamento."
        )

    st.subheader("Indicadores para planejamento do cuidado")
    base_taxa = taxa_obesidade(df)
    historico_sim = df[df["family_history"] == "yes"]
    baixa_atividade = df[df["FAF"] < 1]
    caloricos = df[df["FAVC"] == "yes"]
    i1, i2, i3 = st.columns(3)
    i1.metric(
        "Obesidade com histórico familiar",
        f"{taxa_obesidade(historico_sim):.1f}%",
        formatar_delta(taxa_obesidade(historico_sim) - base_taxa),
    )
    i2.metric(
        "Obesidade com baixa atividade",
        f"{taxa_obesidade(baixa_atividade):.1f}%",
        formatar_delta(taxa_obesidade(baixa_atividade) - base_taxa),
    )
    i3.metric(
        "Obesidade e consumo calórico",
        f"{taxa_obesidade(caloricos):.1f}%",
        formatar_delta(taxa_obesidade(caloricos) - base_taxa),
        help="Taxa de obesidade entre os registros com consumo frequente de alimentos altamente calóricos.",
    )
    st.caption(
        "Comparações descritivas calculadas na base completa. Diferenças em pontos percentuais indicam associação observada, não causalidade."
    )

with tab_recortes:
    st.subheader("Distribuição dos níveis de peso por gênero")
    distribuicao_genero = (
        pd.crosstab(df_filtrado["Gender"], df_filtrado[TARGET_COLUMN], normalize="index")
        .reindex(columns=CLASS_ORDER, fill_value=0)
        .mul(100)
    )
    distribuicao_genero.index = [ROTULOS_VALORES.get(valor, valor) for valor in distribuicao_genero.index]
    distribuicao_genero.columns = [CLASS_LABELS_PT[coluna] for coluna in distribuicao_genero.columns]
    fig, ax = plt.subplots(figsize=(11, 4.5))
    distribuicao_genero.plot(kind="barh", stacked=True, ax=ax, color=CORES_CLASSES)
    ax.set_xlabel("Composição dentro de cada gênero (%)")
    ax.set_ylabel("Gênero")
    ax.set_xlim(0, 100)
    ax.legend(title="Nível de peso", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Distribuição dos níveis de peso por faixa etária")
    distribuicao_idade = (
        pd.crosstab(df_filtrado["Faixa etária"], df_filtrado[TARGET_COLUMN], normalize="index")
        .reindex(columns=CLASS_ORDER, fill_value=0)
        .mul(100)
    )
    distribuicao_idade.columns = [CLASS_LABELS_PT[coluna] for coluna in distribuicao_idade.columns]
    fig, ax = plt.subplots(figsize=(11, 5.5))
    distribuicao_idade.plot(kind="barh", stacked=True, ax=ax, color=CORES_CLASSES)
    ax.set_xlabel("Composição dentro de cada faixa etária (%)")
    ax.set_ylabel("Faixa etária")
    ax.set_xlim(0, 100)
    ax.legend(title="Nível de peso", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Onde a obesidade está mais concentrada na base")
    analise = df_filtrado.assign(
        Com_obesidade=df_filtrado[TARGET_COLUMN].isin(CLASSES_OBESIDADE),
        Com_excesso=df_filtrado[TARGET_COLUMN].isin(CLASSES_EXCESSO),
    )
    resumo_genero = (
        analise.groupby("Gender", observed=True)
        .agg(Registros=(TARGET_COLUMN, "size"), Obesidade=("Com_obesidade", "mean"), Excesso=("Com_excesso", "mean"))
        .reset_index()
        .rename(columns={"Gender": "Grupo"})
    )
    resumo_genero.insert(0, "Recorte", "Gênero")
    resumo_genero["Grupo"] = resumo_genero["Grupo"].map(ROTULOS_VALORES)
    resumo_idade = (
        analise.groupby("Faixa etária", observed=True)
        .agg(Registros=(TARGET_COLUMN, "size"), Obesidade=("Com_obesidade", "mean"), Excesso=("Com_excesso", "mean"))
        .reset_index()
        .rename(columns={"Faixa etária": "Grupo"})
    )
    resumo_idade.insert(0, "Recorte", "Faixa etária")
    sensibilidade = pd.concat([resumo_genero, resumo_idade], ignore_index=True)
    sensibilidade["Obesidade (%)"] = sensibilidade.pop("Obesidade") * 100
    sensibilidade["Sobrepeso ou obesidade (%)"] = sensibilidade.pop("Excesso") * 100

    maior_genero = resumo_genero.loc[resumo_genero["Obesidade"].idxmax()]
    maior_idade = resumo_idade.loc[resumo_idade["Obesidade"].idxmax()]
    menor_grupo = sensibilidade.loc[sensibilidade["Registros"].idxmin()]
    s1, s2, s3 = st.columns(3)
    s1.metric(
        "Maior taxa por gênero",
        str(maior_genero["Grupo"]),
        f"{maior_genero['Obesidade'] * 100:.1f}% com obesidade",
        delta_color="off",
    )
    s2.metric(
        "Maior taxa por idade",
        str(maior_idade["Grupo"]),
        f"{maior_idade['Obesidade'] * 100:.1f}% com obesidade",
        delta_color="off",
    )
    s3.metric(
        "Menor representação",
        str(menor_grupo["Grupo"]),
        f"{int(menor_grupo['Registros'])} registros",
        delta_color="off",
    )
    st.dataframe(
        sensibilidade.style.format(
            {"Obesidade (%)": "{:.1f}", "Sobrepeso ou obesidade (%)": "{:.1f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    botao_download_csv(
        sensibilidade,
        "sensibilidade_genero_faixa_etaria.csv",
        key="download_sensibilidade_demografica",
    )

    st.subheader("Associação dos hábitos com obesidade")
    habito_recorte = st.selectbox(
        "Hábito para comparar por gênero e idade",
        ["family_history", "FAVC", "FCVC", "FAF", "CH2O", "TUE", "CAEC"],
        format_func=lambda coluna: ROTULOS_COLUNAS[coluna],
        key="habito_recortes",
    )
    habito_genero = resumo_habito_por_grupo(df_filtrado, habito_recorte, "Gender")
    habito_idade = resumo_habito_por_grupo(df_filtrado, habito_recorte, "Faixa etária")

    grafico_genero, grafico_idade = st.columns(2)
    with grafico_genero:
        pivot_genero = habito_genero.pivot(
            index="Categoria do hábito", columns="Gênero", values="Taxa de obesidade (%)"
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot_genero.plot(kind="bar", ax=ax, color=["#B14A77", "#4C78A8"])
        ax.set_title(f"{ROTULOS_COLUNAS[habito_recorte]} por gênero")
        ax.set_xlabel(ROTULOS_COLUNAS[habito_recorte])
        ax.set_ylabel("Pessoas com obesidade (%)")
        ax.tick_params(axis="x", rotation=25)
        ax.legend(title="Gênero")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    with grafico_idade:
        pivot_idade = habito_idade.pivot(
            index="Categoria do hábito", columns="Faixa etária", values="Taxa de obesidade (%)"
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot_idade.plot(kind="bar", ax=ax, colormap="viridis")
        ax.set_title(f"{ROTULOS_COLUNAS[habito_recorte]} por idade")
        ax.set_xlabel(ROTULOS_COLUNAS[habito_recorte])
        ax.set_ylabel("Pessoas com obesidade (%)")
        ax.tick_params(axis="x", rotation=25)
        ax.legend(title="Faixa etária", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)

    with st.expander("Ver tabelas detalhadas dos hábitos"):
        st.markdown("**Comparação por gênero**")
        st.dataframe(
            habito_genero.style.format({"Taxa de obesidade (%)": "{:.1f}"}),
            use_container_width=True,
            hide_index=True,
        )
        botao_download_csv(
            habito_genero,
            f"habito_{habito_recorte}_por_genero.csv",
            key=f"download_habito_genero_{habito_recorte}",
        )
        st.markdown("**Comparação por faixa etária**")
        st.dataframe(
            habito_idade.style.format({"Taxa de obesidade (%)": "{:.1f}"}),
            use_container_width=True,
            hide_index=True,
        )
        botao_download_csv(
            habito_idade,
            f"habito_{habito_recorte}_por_idade.csv",
            key=f"download_habito_idade_{habito_recorte}",
        )

    st.warning(
        "Sensibilidade, nesta seção, indica concentração e diferença entre grupos da base. "
        "Os resultados são descritivos, dependem do tamanho de cada grupo e não demonstram causalidade."
    )

with tab_perfil:
    st.subheader("Peso e IMC ao longo das classificações")
    resumo_clinico = (
        df_filtrado.groupby(TARGET_COLUMN, observed=False)
        .agg(Pessoas=(TARGET_COLUMN, "size"), Idade_média=("Age", "mean"), Peso_médio=("Weight", "mean"), IMC_médio=("IMC", "mean"))
        .reindex(CLASS_ORDER)
        .dropna(subset=["Idade_média"])
        .reset_index()
    )
    resumo_clinico[TARGET_COLUMN] = resumo_clinico[TARGET_COLUMN].map(CLASS_LABELS_PT)
    resumo_clinico.columns = ["Nível de peso", "Pessoas", "Idade média", "Peso médio (kg)", "IMC médio (kg/m²)"]
    st.dataframe(
        resumo_clinico.style.format({"Idade média": "{:.1f}", "Peso médio (kg)": "{:.1f}", "IMC médio (kg/m²)": "{:.1f}"}),
        use_container_width=True,
        hide_index=True,
    )
    botao_download_csv(
        resumo_clinico,
        "resumo_perfil_antropometrico.csv",
        key="download_resumo_clinico",
    )

    col_peso, col_idade = st.columns(2)
    with col_peso:
        fig, ax = plt.subplots(figsize=(8, 5))
        dados = [df_filtrado.loc[df_filtrado[TARGET_COLUMN] == c, "IMC"] for c in CLASS_ORDER if c in df_filtrado[TARGET_COLUMN].values]
        nomes = [CLASS_LABELS_PT[c] for c in CLASS_ORDER if c in df_filtrado[TARGET_COLUMN].values]
        ax.boxplot(dados, tick_labels=nomes, patch_artist=True)
        ax.set_title("Distribuição do IMC por nível de peso")
        ax.set_ylabel("IMC (kg/m²)")
        ax.tick_params(axis="x", rotation=35)
        plt.tight_layout()
        st.pyplot(fig)
    with col_idade:
        faixa_resumo = df_filtrado.groupby("Faixa etária", observed=False)[TARGET_COLUMN].apply(
            lambda serie: serie.isin(CLASSES_OBESIDADE).mean() * 100
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(faixa_resumo.index.astype(str), faixa_resumo.values, color="#0f9f9a")
        ax.set_title("Obesidade observada por faixa etária")
        ax.set_ylabel("Pessoas com obesidade (%)")
        ax.tick_params(axis="x", rotation=30)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)

with tab_habitos:
    st.subheader("Hábitos e contexto associados à classificação")
    variavel = st.selectbox(
        "Comparar por",
        ["family_history", "FAVC", "CAEC", "FAF", "CH2O", "MTRANS"],
        format_func=lambda x: ROTULOS_COLUNAS[x],
    )
    base_comparacao = df_filtrado.copy()
    if variavel == "FAF":
        base_comparacao[variavel] = pd.cut(base_comparacao[variavel], [-0.01, 0.99, 1.99, 3], labels=["Baixa", "Moderada", "Alta"])
    elif variavel == "CH2O":
        base_comparacao[variavel] = pd.cut(base_comparacao[variavel], [0.99, 1.66, 2.33, 3], labels=["Baixo", "Intermediário", "Alto"])

    comparacao = pd.crosstab(base_comparacao[variavel], base_comparacao[TARGET_COLUMN], normalize="index")
    comparacao = comparacao.reindex(columns=CLASS_ORDER, fill_value=0) * 100
    comparacao.index = [ROTULOS_VALORES.get(str(valor), str(valor)) for valor in comparacao.index]
    comparacao.columns = [CLASS_LABELS_PT[coluna] for coluna in comparacao.columns]
    fig, ax = plt.subplots(figsize=(11, 5))
    comparacao.plot(kind="bar", stacked=True, ax=ax, color=CORES_CLASSES)
    ax.set_xlabel(ROTULOS_COLUNAS[variavel])
    ax.set_ylabel("Composição do grupo (%)")
    ax.legend(title="Nível de peso", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    st.pyplot(fig)

    st.warning(
        "Use estes agrupamentos para formular perguntas durante a avaliação. Eles não devem ser usados isoladamente para atribuir risco ou definir conduta."
    )

with tab_dados:
    st.subheader("População selecionada")
    colunas_exibidas = ["Gender", "Age", "Height", "Weight", "family_history", "FAVC", "FCVC", "CH2O", "FAF", "TUE", TARGET_COLUMN]
    dados_exibidos = traduzir_dataframe(df_filtrado[colunas_exibidas])
    st.dataframe(
        dados_exibidos.head(500),
        use_container_width=True,
        hide_index=True,
    )
    botao_download_csv(
        dados_exibidos,
        "populacao_selecionada.csv",
        rotulo="Baixar população selecionada em CSV",
        key="download_populacao",
    )
    st.caption(f"Exibindo até 500 dos {total} registros selecionados. Dados destinados a análise acadêmica.")
