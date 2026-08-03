import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.predict import predict_obesity
from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar, result_card

st.set_page_config(page_title="Predição | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Predição individual",
    "Preencha os dados do paciente para estimar o nível de obesidade e visualizar as probabilidades por classe.",
)
render_status_bar("Formulário pronto", "Pipeline final carregada para inferência")

top1, top2, top3 = st.columns(3)
with top1:
    metric_card("Modelo", "Floresta Aleatória", "Classificação multiclasse")
with top2:
    metric_card("F1 macro", "0.9775", "Métrica final do teste")
with top3:
    metric_card("Classes", "7", "Níveis de peso e obesidade")

OPCOES = {
    "Male": "Masculino", "Female": "Feminino", "yes": "Sim", "no": "Não",
    "Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre",
    "Walking": "A pé", "Bike": "Bicicleta", "Motorbike": "Motocicleta",
    "Automobile": "Automóvel", "Public_Transportation": "Transporte público",
}


def traduzir_opcao(valor: str) -> str:
    return OPCOES.get(valor, valor)

with st.form("prediction_form"):
    st.markdown('<div class="vc-card-title">Dados da avaliação</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gênero", ["Male", "Female"], format_func=traduzir_opcao)
        age = st.number_input("Idade", min_value=1.0, max_value=120.0, value=25.0, step=1.0)
        height = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=75.0, step=1.0)
        family_history = st.selectbox("Histórico familiar de sobrepeso", ["yes", "no"], format_func=traduzir_opcao)
        favc = st.selectbox("Consome alimentos calóricos frequentemente", ["yes", "no"], format_func=traduzir_opcao)

    with col2:
        fcvc = st.slider("Frequência de vegetais", 1.0, 3.0, 2.0, 0.1)
        ncp = st.slider("Refeições principais por dia", 1.0, 4.0, 3.0, 0.1)
        caec = st.selectbox("Come entre refeições", ["no", "Sometimes", "Frequently", "Always"], format_func=traduzir_opcao)
        smoke = st.selectbox("Fuma", ["yes", "no"], index=1, format_func=traduzir_opcao)
        ch2o = st.slider("Consumo diário de água", 1.0, 3.0, 2.0, 0.1)
        scc = st.selectbox("Monitora calorias", ["yes", "no"], index=1, format_func=traduzir_opcao)

    with col3:
        faf = st.slider("Atividade física", 0.0, 3.0, 1.0, 0.1)
        tue = st.slider("Tempo em dispositivos tecnológicos", 0.0, 2.0, 1.0, 0.1)
        calc = st.selectbox("Consumo de álcool", ["no", "Sometimes", "Frequently", "Always"], format_func=traduzir_opcao)
        mtrans = st.selectbox(
            "Meio de transporte",
            ["Walking", "Bike", "Motorbike", "Automobile", "Public_Transportation"],
            format_func=traduzir_opcao,
        )

    submitted = st.form_submit_button("Gerar avaliação")

if submitted:
    input_data = {
        "Gender": gender,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history": family_history,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans,
    }

    try:
        result = predict_obesity(input_data)
        result_card(
            "Resultado previsto",
            result["predicted_label"],
            f"Classe técnica: {result['predicted_class']}",
        )
        if result["probabilities"]:
            probabilities = pd.DataFrame(
                result["probabilities"].items(), columns=["Classe", "Probabilidade"]
            ).sort_values("Probabilidade", ascending=False)
            st.subheader("Distribuição de probabilidades")
            st.bar_chart(probabilities, x="Classe", y="Probabilidade")
    except Exception as exc:
        st.error(str(exc))
