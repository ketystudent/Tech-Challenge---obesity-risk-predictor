import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui import apply_theme, metric_card, render_page_header, render_sidebar, render_status_bar

st.set_page_config(page_title="VitaCare Risk Console", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Avaliacao de risco",
    "Sistema preditivo para apoio a triagem clinica e analise de niveis de obesidade.",
)
render_status_bar()

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Modelo final", "RandomForest", "Pipeline validada e serializada")
with col2:
    metric_card("F1 macro", "0.9775", "Desempenho no conjunto de teste")
with col3:
    metric_card("Dashboard", "Ativo", "Insights analiticos disponiveis")

st.markdown(
    """
    <div class="vc-card">
        <div class="vc-card-title">Fluxo da aplicacao</div>
        <div class="vc-card-muted">
            Use o menu lateral para acessar a predicao individual, a visao analitica dos dados
            e as informacoes do modelo. O sistema foi desenvolvido para fins academicos e nao
            substitui avaliacao medica.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
