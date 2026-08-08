import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar
from src.config import METRICS_PATH

metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8")) if METRICS_PATH.exists() else {}

st.set_page_config(page_title="Início | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Apoio inteligente à avaliação da obesidade",
    "Uma ferramenta acadêmica que reúne predição individual, análise populacional e transparência do modelo para apoiar a equipe de saúde.",
    "VitaCare — visão geral",
)
render_status_bar("Sistema disponível", "Modelo preditivo e painel analítico prontos para utilização")

st.markdown(
    """
    <div class="vc-card">
        <div class="vc-card-title">Objetivo da aplicação</div>
        <div class="vc-card-muted">
            O VitaCare foi desenvolvido para apoiar a triagem e a discussão clínica sobre o estado
            nutricional. A aplicação combina características pessoais, histórico familiar e
            hábitos de vida para estimar tendências associadas a sete níveis de peso e obesidade,
            sem utilizar peso, altura ou IMC como preditores. Também
            oferece uma visão analítica da população estudada, permitindo identificar padrões que
            podem orientar ações de prevenção, acompanhamento e educação em saúde.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### O que você encontra na aplicação")

col_predicao, col_analise = st.columns(2)
with col_predicao:
    with st.container(border=True):
        st.subheader("Predição individual")
        st.write(
            "Registre hábitos e histórico de uma pessoa para obter a tendência estimada, "
            "as probabilidades do modelo e pontos de verificação para a avaliação preventiva."
        )
        st.page_link("pages/1_Predicao.py", label="Acessar predição", icon="🩺")

with col_analise:
    with st.container(border=True):
        st.subheader("Visão analítica")
        st.write(
            "Explore indicadores da população, distribuições de peso, perfil antropométrico "
            "e associações observadas com hábitos e histórico familiar."
        )
        st.page_link("pages/2_Visao_Analitica.py", label="Acessar painel analítico", icon="📊")

col_modelo, col_links = st.columns(2)
with col_modelo:
    with st.container(border=True):
        st.subheader("Sobre o modelo")
        st.write(
            "Consulte desempenho, metodologia, matriz de confusão, importância das variáveis, "
            "otimização e limitações da solução preditiva."
        )
        st.page_link("pages/3_Sobre_o_Modelo.py", label="Conhecer o modelo", icon="🔎")

with col_links:
    with st.container(border=True):
        st.subheader("Links do projeto")
        st.write(
            "Encontre o repositório no GitHub, o endereço da aplicação publicada e os materiais "
            "utilizados na apresentação e entrega do projeto."
        )
        st.page_link("pages/4_Links.py", label="Consultar links", icon="🔗")

st.markdown("### Como utilizar")
etapa1, etapa2, etapa3 = st.columns(3)
with etapa1:
    metric_card("1. Informe", "Dados", "Preencha histórico e hábitos com informações atualizadas")
with etapa2:
    metric_card("2. Analise", "Resultado", "Observe a tendência e a distribuição das probabilidades")
with etapa3:
    metric_card("3. Contextualize", "Cuidado", "Combine o resultado com avaliação clínica profissional")

st.markdown("### Escopo do estudo")
dado1, dado2, dado3 = st.columns(3)
dado1.metric("Registros analisados", "2.087", "Após remoção de duplicatas")
dado2.metric("Classificações", "7", "De peso insuficiente à obesidade tipo III")
dado3.metric(
    "F1 macro do modelo",
    f"{metrics.get('f1_macro', 0):.4f}".replace(".", ","),
    "Modelo preventivo no conjunto de teste",
)

st.markdown(
    """
    <div class="vc-warning-card">
        <strong>Uso responsável:</strong> o VitaCare é um projeto acadêmico de apoio à decisão.
        A estimativa comportamental não constitui diagnóstico nem confirma o estado nutricional atual.
        Não deve ser utilizada isoladamente para definir
        tratamento. Confirme as medidas e considere anamnese, exame físico, contexto psicossocial,
        comorbidades e protocolos assistenciais aplicáveis.
    </div>
    """,
    unsafe_allow_html=True,
)
