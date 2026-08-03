import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.links import LINKS_PROJETO
from app.ui import apply_theme, render_page_header, render_sidebar, render_status_bar

st.set_page_config(page_title="Links | VitaCare", layout="wide")
apply_theme()
render_sidebar()
render_page_header(
    "Links do projeto",
    "Acesso centralizado ao código-fonte, à aplicação publicada e aos materiais de apresentação.",
    "Entrega e documentação",
)
render_status_bar("Página disponível", "Links oficiais e materiais complementares do projeto")

st.markdown("### Acessos disponíveis")

for titulo, dados in LINKS_PROJETO.items():
    coluna_texto, coluna_acao = st.columns([4, 1])
    with coluna_texto:
        st.markdown(f"**{titulo}**")
        st.caption(dados["descricao"])
    with coluna_acao:
        if dados["url"]:
            st.link_button("Abrir link", dados["url"], use_container_width=True)
        else:
            st.button("Pendente", key=f"pendente_{titulo}", disabled=True, use_container_width=True)
    st.divider()

st.info(
    "Os links marcados como pendentes serão disponibilizados após a publicação dos respectivos materiais."
)
