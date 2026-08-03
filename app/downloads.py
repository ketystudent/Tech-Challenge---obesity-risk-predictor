import pandas as pd
import streamlit as st


def botao_download_csv(
    dataframe: pd.DataFrame,
    nome_arquivo: str,
    *,
    rotulo: str = "Baixar tabela em CSV",
    incluir_indice: bool = False,
    key: str | None = None,
) -> None:
    """Exibe um download CSV compatível com Excel em português."""
    conteudo = dataframe.to_csv(
        index=incluir_indice,
        sep=";",
        decimal=",",
    ).encode("utf-8-sig")
    st.download_button(
        label=rotulo,
        data=conteudo,
        file_name=nome_arquivo,
        mime="text/csv",
        key=key,
    )
