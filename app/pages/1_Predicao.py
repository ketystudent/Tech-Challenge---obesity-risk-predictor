import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.downloads import botao_download_csv
from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar, result_card
from src.config import CLASS_LABELS_PT
from src.predict import predict_obesity

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


ESCALA_VEGETAIS = {
    1: "Nunca",
    2: "Às vezes",
    3: "Sempre",
}
ESCALA_ATIVIDADE = {
    0: "Não pratica",
    1: "1 a 2 vezes por semana",
    2: "2 a 4 vezes por semana",
    3: "4 a 5 vezes por semana",
}
ESCALA_TEMPO_TELA = {
    0: "Até 2 horas por dia",
    1: "De 3 a 5 horas por dia",
    2: "Mais de 5 horas por dia",
}
ESCALA_AGUA = {
    1: "Menos de 1 litro por dia",
    2: "Entre 1 e 2 litros por dia",
    3: "Mais de 2 litros por dia",
}

INTERPRETACOES = {
    "Insufficient_Weight": "O perfil informado foi associado à faixa de peso insuficiente pelo modelo.",
    "Normal_Weight": "O perfil informado foi associado à faixa de peso considerada adequada pelo modelo.",
    "Overweight_Level_I": "O perfil informado foi associado à primeira faixa de sobrepeso pelo modelo.",
    "Overweight_Level_II": "O perfil informado foi associado à segunda faixa de sobrepeso pelo modelo.",
    "Obesity_Type_I": "O perfil informado foi associado à obesidade tipo I pelo modelo.",
    "Obesity_Type_II": "O perfil informado foi associado à obesidade tipo II pelo modelo.",
    "Obesity_Type_III": "O perfil informado foi associado à obesidade tipo III pelo modelo.",
}


def orientacoes_clinicas(classe: str) -> list[str]:
    orientacoes = [
        "Confirmar peso e altura aferidos e interpretar o IMC no contexto de idade e condições individuais.",
        "Revisar histórico de saúde, medicamentos, hábitos, aspectos psicossociais e objetivos da pessoa.",
    ]
    if classe == "Insufficient_Weight":
        orientacoes.append("Investigar evolução ponderal, ingestão alimentar e possível perda de peso não intencional.")
    elif classe == "Normal_Weight":
        orientacoes.append("Manter acompanhamento longitudinal e ações de promoção de alimentação e atividade física adequadas.")
    else:
        orientacoes.extend([
            "Avaliar circunferência da cintura, pressão arterial e risco cardiovascular, quando aplicável.",
            "Pesquisar comorbidades e construir um plano de cuidado compartilhado, sem estigma e conforme julgamento clínico.",
        ])
    return orientacoes


with st.form("prediction_form"):
    st.markdown('<div class="vc-card-title">Dados da avaliação</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gênero", ["Male", "Female"], format_func=traduzir_opcao)
        age = st.number_input("Idade (anos)", min_value=1, max_value=120, value=25, step=1)
        height = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=75.0, step=1.0)
        family_history = st.selectbox("Histórico familiar de sobrepeso", ["yes", "no"], format_func=traduzir_opcao)
        favc = st.selectbox("Consome alimentos calóricos frequentemente", ["yes", "no"], format_func=traduzir_opcao)

    with col2:
        fcvc = st.select_slider(
            "Frequência de consumo de vegetais",
            options=list(ESCALA_VEGETAIS),
            value=2,
            format_func=ESCALA_VEGETAIS.get,
        )
        ncp = st.slider("Refeições principais por dia", min_value=1, max_value=4, value=3, step=1)
        caec = st.selectbox("Come entre refeições", ["no", "Sometimes", "Frequently", "Always"], format_func=traduzir_opcao)
        smoke = st.selectbox("Fuma", ["yes", "no"], index=1, format_func=traduzir_opcao)
        ch2o = st.select_slider(
            "Consumo diário de água",
            options=list(ESCALA_AGUA),
            value=2,
            format_func=ESCALA_AGUA.get,
        )
        scc = st.selectbox("Monitora calorias", ["yes", "no"], index=1, format_func=traduzir_opcao)

    with col3:
        faf = st.select_slider(
            "Frequência de atividade física",
            options=list(ESCALA_ATIVIDADE),
            value=1,
            format_func=ESCALA_ATIVIDADE.get,
        )
        tue = st.select_slider(
            "Tempo diário em dispositivos tecnológicos",
            options=list(ESCALA_TEMPO_TELA),
            value=1,
            format_func=ESCALA_TEMPO_TELA.get,
        )
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
        imc = weight / (height ** 2)
        probabilidades_ordenadas = sorted(
            result["probabilities"].items(), key=lambda item: item[1], reverse=True
        )
        probabilidade_principal = probabilidades_ordenadas[0][1] if probabilidades_ordenadas else None
        alternativa = probabilidades_ordenadas[1] if len(probabilidades_ordenadas) > 1 else None

        result_card(
            "Classificação estimada pelo modelo",
            result["predicted_label"],
            INTERPRETACOES.get(result["predicted_class"], "Resultado calculado a partir dos dados informados."),
        )

        resumo1, resumo2, resumo3 = st.columns(3)
        resumo1.metric(
            "Probabilidade estimada",
            f"{probabilidade_principal:.1%}" if probabilidade_principal is not None else "Indisponível",
            help="Probabilidade produzida pelo modelo; não equivale à certeza diagnóstica.",
        )
        resumo2.metric(
            "IMC calculado",
            f"{imc:.1f} kg/m²",
            help="Calculado como peso dividido pela altura ao quadrado.",
        )
        segunda_classe = (
            CLASS_LABELS_PT.get(alternativa[0], alternativa[0]) if alternativa else "Indisponível"
        )
        segunda_probabilidade = f"{alternativa[1]:.1%} de probabilidade" if alternativa else ""
        resumo3.markdown(
            f"""
            <div class="vc-card" style="min-height:9.7rem;margin-bottom:0;">
                <div class="vc-card-muted" style="font-size:1rem;">Segunda possibilidade</div>
                <div style="font-size:1.55rem;font-weight:800;color:var(--vc-teal-dark);
                            line-height:1.15;margin:0.75rem 0 0.55rem;overflow-wrap:anywhere;">
                    {segunda_classe}
                </div>
                <div class="vc-card-muted">{segunda_probabilidade}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if probabilidade_principal is not None and probabilidade_principal < 0.60:
            st.warning(
                "O modelo apresentou baixa separação entre as classificações. Dê atenção especial às alternativas e confirme os dados informados."
            )

        st.subheader("Interpretação clínica sugerida")
        st.markdown(
            "\n".join(f"- {orientacao}" for orientacao in orientacoes_clinicas(result["predicted_class"]))
        )

        if age < 18:
            st.warning(
                "Paciente menor de 18 anos: a interpretação do IMC deve considerar idade e sexo em curvas específicas. "
                "Não utilize pontos de corte de adultos."
            )
        elif age >= 60:
            st.info(
                "Em pessoas idosas, o IMC exige interpretação específica e deve ser complementado pela avaliação clínica e funcional."
            )

        with st.expander("Resumo dos dados informados"):
            resumo_paciente = pd.DataFrame(
                {
                    "Indicador": [
                        "Idade", "Altura", "Peso", "Histórico familiar", "Atividade física",
                        "Consumo de água", "Tempo em dispositivos",
                    ],
                    "Valor informado": [
                        f"{age} anos", f"{height:.2f} m", f"{weight:.1f} kg",
                        traduzir_opcao(family_history), ESCALA_ATIVIDADE[faf], ESCALA_AGUA[ch2o],
                        ESCALA_TEMPO_TELA[tue],
                    ],
                }
            )
            st.dataframe(resumo_paciente, use_container_width=True, hide_index=True)
            botao_download_csv(
                resumo_paciente,
                "resumo_avaliacao_paciente.csv",
                key="download_resumo_paciente",
            )

        if probabilidades_ordenadas:
            probabilities = pd.DataFrame(
                [
                    {
                        "Classe": CLASS_LABELS_PT.get(classe, classe),
                        "Probabilidade": probabilidade * 100,
                    }
                    for classe, probabilidade in probabilidades_ordenadas
                ]
            ).sort_values("Probabilidade", ascending=True)
            st.subheader("Como o modelo distribuiu as probabilidades")
            fig, ax = plt.subplots(figsize=(10, 5))
            cores = ["#0f9f9a" if classe == result["predicted_label"] else "#b8cbd7" for classe in probabilities["Classe"]]
            barras = ax.barh(probabilities["Classe"], probabilities["Probabilidade"], color=cores)
            ax.bar_label(barras, labels=[f"{valor:.1f}%" for valor in probabilities["Probabilidade"]], padding=4)
            ax.set_xlabel("Probabilidade estimada (%)")
            ax.set_xlim(0, max(100, probabilities["Probabilidade"].max() * 1.15))
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.grid(axis="x", alpha=0.2)
            ax.set_axisbelow(True)
            plt.tight_layout()
            st.pyplot(fig)

        st.caption(
            "Ferramenta acadêmica de apoio à decisão. O resultado não constitui diagnóstico nem substitui avaliação profissional. "
            "Referência clínica: Ministério da Saúde — Linha de Cuidado da Obesidade no Adulto."
        )
        st.link_button(
            "Consultar referência do Ministério da Saúde",
            "https://linhasdecuidado.saude.gov.br/portal/obesidade-no-adulto/unidade-de-atencao-primaria/rastreamento-diagnostico/",
        )
    except Exception as exc:
        st.error(str(exc))
