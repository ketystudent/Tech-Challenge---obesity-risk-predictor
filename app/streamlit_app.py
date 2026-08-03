import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar

st.set_page_config(page_title="Painel de Risco VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Avaliação de risco",
    "Sistema preditivo para apoio à triagem clínica e à análise de níveis de obesidade.",
)
render_status_bar()

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Modelo final", "Floresta Aleatória", "Pipeline validada e serializada")
with col2:
    metric_card("F1 macro", "0.9775", "Desempenho no conjunto de teste")
with col3:
    metric_card("Painel", "Ativo", "Análises disponíveis")

st.markdown(
    """
    <div class="vc-card">
        <div class="vc-card-title">Fluxo da aplicação</div>
        <div class="vc-card-muted">
            Use o menu lateral para acessar a predição individual, a visão analítica dos dados
            e as informações do modelo. O sistema foi desenvolvido para fins acadêmicos e não
            substitui avaliação médica.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
