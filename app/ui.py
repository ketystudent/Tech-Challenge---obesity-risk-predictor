import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --vc-navy: #072b4a;
            --vc-navy-2: #0a3a63;
            --vc-teal: #0f9f9a;
            --vc-teal-dark: #087b78;
            --vc-mint: #e8f7f6;
            --vc-ink: #10233f;
            --vc-muted: #6b7a90;
            --vc-border: #dbe5ee;
            --vc-bg: #f5f8fb;
            --vc-warning: #b7791f;
            --vc-warning-bg: #fff5df;
            --vc-shadow: 0 14px 35px rgba(15, 35, 60, 0.08);
        }

        .stApp {
            background: linear-gradient(180deg, #f7fbfd 0%, #eef5f8 100%);
            color: var(--vc-ink);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #062846 0%, #05345f 54%, #03213b 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #eaf6fb;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 12px;
            margin: 0.15rem 0.45rem;
            padding: 0.65rem 0.9rem;
            font-weight: 650;
        }

        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(90deg, #10aaa4, #087e84);
            color: #ffffff;
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        h1, h2, h3 {
            color: var(--vc-ink);
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--vc-border);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: var(--vc-shadow);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--vc-muted);
            font-weight: 650;
        }

        div[data-testid="stMetricValue"] {
            color: var(--vc-teal-dark);
            font-weight: 800;
        }

        .vc-sidebar-brand {
            padding: 1.1rem 0.7rem 1.7rem 0.7rem;
        }

        .vc-brand-name {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.05;
        }

        .vc-brand-subtitle {
            color: #32ddd4;
            font-size: 1rem;
            font-weight: 650;
            margin-top: 0.35rem;
        }

        .vc-user-card {
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 16px;
            padding: 1rem;
            margin: 2rem 0.45rem 0 0.45rem;
            background: rgba(255, 255, 255, 0.06);
        }

        .vc-page-kicker {
            color: var(--vc-teal-dark);
            font-weight: 750;
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .vc-page-title {
            font-size: 2.35rem;
            font-weight: 800;
            color: var(--vc-ink);
            line-height: 1.08;
            margin-bottom: 0.35rem;
        }

        .vc-page-subtitle {
            color: var(--vc-muted);
            font-size: 1.02rem;
            margin-bottom: 1.25rem;
        }

        .vc-status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            background: #ffffff;
            border: 1px solid var(--vc-border);
            border-radius: 18px;
            padding: 1rem 1.15rem;
            box-shadow: var(--vc-shadow);
            margin: 0.4rem 0 1rem 0;
        }

        .vc-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--vc-ink);
            font-weight: 750;
        }

        .vc-dot {
            width: 0.65rem;
            height: 0.65rem;
            border-radius: 999px;
            background: #32c36c;
            display: inline-block;
        }

        .vc-card {
            background: #ffffff;
            border: 1px solid var(--vc-border);
            border-radius: 18px;
            padding: 1.15rem;
            box-shadow: var(--vc-shadow);
            margin-bottom: 1rem;
        }

        .vc-card-title {
            color: var(--vc-ink);
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .vc-card-muted {
            color: var(--vc-muted);
            font-size: 0.92rem;
        }

        .vc-result-card {
            background: linear-gradient(135deg, #ffffff 0%, #e9f8f7 100%);
            border: 1px solid #bfe7e4;
            border-radius: 20px;
            padding: 1.35rem;
            box-shadow: var(--vc-shadow);
            margin: 1rem 0;
        }

        .vc-result-label {
            color: var(--vc-muted);
            font-weight: 700;
        }

        .vc-result-value {
            color: var(--vc-teal-dark);
            font-size: 2rem;
            font-weight: 850;
            line-height: 1.1;
        }

        .vc-warning-card {
            background: var(--vc-warning-bg);
            border: 1px solid #f4d49a;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            color: #744f12;
            font-weight: 650;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background: linear-gradient(90deg, #0f9f9a, #087b78);
            color: #ffffff;
            border: 0;
            border-radius: 12px;
            padding: 0.72rem 1.4rem;
            font-weight: 750;
            box-shadow: 0 10px 20px rgba(8, 123, 120, 0.22);
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background: linear-gradient(90deg, #10aaa4, #086e72);
            color: #ffffff;
            border: 0;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            border-bottom: 1px solid var(--vc-border);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 12px 12px 0 0;
            color: var(--vc-muted);
            font-weight: 750;
            padding: 0.75rem 1.2rem;
        }

        .stTabs [aria-selected="true"] {
            color: var(--vc-teal-dark);
            border-bottom: 3px solid var(--vc-teal);
        }

        div[data-baseweb="input"],
        div[data-baseweb="select"] > div,
        textarea {
            border-radius: 12px;
        }

        .stDataFrame {
            border: 1px solid var(--vc-border);
            border-radius: 14px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.markdown(
        """
        <div class="vc-sidebar-brand">
            <div class="vc-brand-name">VitaCare</div>
            <div class="vc-brand-subtitle">Inteligência Clínica</div>
        </div>
        <div class="vc-user-card">
            <div style="font-weight:800;color:#ffffff;">Equipe de Saúde</div>
            <div style="color:#b9d8e7;margin-top:0.2rem;">Ambiente acadêmico FIAP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, kicker: str = "Painel clínico") -> None:
    st.markdown(
        f"""
        <div class="vc-page-kicker">{kicker}</div>
        <div class="vc-page-title">{title}</div>
        <div class="vc-page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def render_status_bar(status: str = "Sistema ativo", detail: str = "Modelo carregado e serviços operacionais") -> None:
    st.markdown(
        f"""
        <div class="vc-status-bar">
            <div>
                <div class="vc-status-pill"><span class="vc-dot"></span>{status}</div>
                <div class="vc-card-muted" style="margin-left:1.2rem;">{detail}</div>
            </div>
            <div class="vc-card-muted">Painel de Risco VitaCare</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="vc-card">
            <div class="vc-card-muted">{title}</div>
            <div style="font-size:2rem;font-weight:850;color:var(--vc-teal-dark);line-height:1.1;">{value}</div>
            <div class="vc-card-muted">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_card(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="vc-result-card">
            <div class="vc-result-label">{label}</div>
            <div class="vc-result-value">{value}</div>
            <div class="vc-card-muted">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
