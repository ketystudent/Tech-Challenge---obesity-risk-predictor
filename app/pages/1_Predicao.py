import pandas as pd
import streamlit as st

from src.predict import predict_obesity

st.set_page_config(page_title="Predicao", layout="wide")
st.title("Predicao")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Genero", ["Male", "Female"])
        age = st.number_input("Idade", min_value=1.0, max_value=120.0, value=25.0, step=1.0)
        height = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=75.0, step=1.0)
        family_history = st.selectbox("Historico familiar de sobrepeso", ["yes", "no"])
        favc = st.selectbox("Consome alimentos caloricos frequentemente", ["yes", "no"])

    with col2:
        fcvc = st.slider("Frequencia de vegetais", 1.0, 3.0, 2.0, 0.1)
        ncp = st.slider("Refeicoes principais por dia", 1.0, 4.0, 3.0, 0.1)
        caec = st.selectbox("Come entre refeicoes", ["no", "Sometimes", "Frequently", "Always"])
        smoke = st.selectbox("Fuma", ["yes", "no"], index=1)
        ch2o = st.slider("Consumo diario de agua", 1.0, 3.0, 2.0, 0.1)
        scc = st.selectbox("Monitora calorias", ["yes", "no"], index=1)

    with col3:
        faf = st.slider("Atividade fisica", 0.0, 3.0, 1.0, 0.1)
        tue = st.slider("Tempo em dispositivos tecnologicos", 0.0, 2.0, 1.0, 0.1)
        calc = st.selectbox("Consumo de alcool", ["no", "Sometimes", "Frequently", "Always"])
        mtrans = st.selectbox(
            "Meio de transporte",
            ["Walking", "Bike", "Motorbike", "Automobile", "Public_Transportation"],
        )

    submitted = st.form_submit_button("Prever")

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
        st.subheader(result["predicted_label"])
        st.caption(result["predicted_class"])
        if result["probabilities"]:
            probabilities = pd.DataFrame(
                result["probabilities"].items(), columns=["Classe", "Probabilidade"]
            ).sort_values("Probabilidade", ascending=False)
            st.bar_chart(probabilities, x="Classe", y="Probabilidade")
    except Exception as exc:
        st.error(str(exc))

