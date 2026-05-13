"""
utils.py — Shared UI utilities for AI Child Vaccination System
Import this in every page: from utils import apply_styles, render_footer
"""
import streamlit as st

# =====================================================
# GLOBAL CSS — Premium Healthcare Dashboard Theme
# =====================================================

GLOBAL_CSS = """
<style>

/* ---- Google Font Import ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ---- Base & Background ---- */
html, body, .stApp {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
.stApp {
    background: linear-gradient(150deg, #eaf4fd 0%, #d5eaf7 25%, #e6f4f1 60%, #daeef5 100%);
    background-attachment: fixed;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(74,144,217,0.10) 0%, transparent 55%),
        radial-gradient(ellipse at 90% 80%, rgba(40,167,69,0.08) 0%, transparent 55%),
        radial-gradient(ellipse at 60% 5%,  rgba(23,162,184,0.09) 0%, transparent 45%);
    pointer-events: none;
    z-index: 0;
}

/* ---- Hide default auto-nav (replaced with custom page_link nav) ---- */
section[data-testid="stSidebarNav"],
section[data-testid="stSidebarNav"] ul,
div[data-testid="stSidebarNavItems"],
div[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNavLink"] {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d3b6e 0%, #145da0 60%, #1a7db8 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(13,59,110,0.18);
}
section[data-testid="stSidebar"] * {
    color: #e8f4fd !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {
    color: #b8d9f0 !important;
    font-size: 0.8rem !important;
}
section[data-testid="stSidebar"] a {
    color: #a8d4f0 !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] a:hover {
    color: #ffffff !important;
}

/* ---- Page Titles ---- */
h1 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #0d3b6e !important;
    font-size: 2rem !important;
    letter-spacing: -0.5px;
}
h2 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: #145da0 !important;
    font-size: 1.35rem !important;
}
h3 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: #1a5f9e !important;
    font-size: 1.1rem !important;
}

/* ---- Metric Cards ---- */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.90) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 16px rgba(13,59,110,0.10) !important;
    border-left: 5px solid #145da0 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(13,59,110,0.16) !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #4a7fa5 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #0d3b6e !important;
}

/* ---- Buttons ---- */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #145da0 0%, #1a7db8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px;
    box-shadow: 0 3px 12px rgba(20,93,160,0.30) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0d3b6e 0%, #145da0 100%) !important;
    box-shadow: 0 6px 18px rgba(13,59,110,0.35) !important;
    transform: translateY(-1px);
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(255,255,255,0.85) !important;
    color: #145da0 !important;
    border: 2px solid #145da0 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: #145da0 !important;
    color: #ffffff !important;
}

/* ---- Form Containers ---- */
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.88) !important;
    border-radius: 16px !important;
    padding: 8px 16px !important;
    box-shadow: 0 4px 20px rgba(13,59,110,0.09) !important;
    border: 1px solid rgba(20,93,160,0.12) !important;
}

/* ---- Bordered Containers ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(20,93,160,0.12) !important;
    box-shadow: 0 2px 14px rgba(13,59,110,0.08) !important;
}

/* ---- DataFrames ---- */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.90) !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(13,59,110,0.07) !important;
    overflow: hidden;
}

/* ---- Alerts / Info Boxes ---- */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-weight: 500;
}

/* ---- Input fields ---- */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 8px !important;
    border: 1.5px solid rgba(20,93,160,0.20) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ---- Dividers ---- */
hr {
    border: none !important;
    border-top: 1.5px solid rgba(20,93,160,0.12) !important;
    margin: 1.2rem 0 !important;
}

/* ---- Spinner ---- */
div[data-testid="stSpinner"] {
    color: #145da0 !important;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(20,93,160,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(20,93,160,0.6); }

</style>
"""


def apply_styles():
    """Call this at the top of every page to apply global premium styles."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_sidebar():
    """Renders the branded sidebar navigation on every page."""
    st.sidebar.markdown("""
<div style='text-align:center; padding: 18px 0 12px 0;'>
    <div style='font-size:2.5rem;'>🏥</div>
    <h2 style='color:#ffffff !important; font-size:1.05rem; margin:4px 0 2px 0;
        font-weight:700; letter-spacing:0.3px;'>AI Child Vaccination</h2>
    <p style='color:#a8d4f0 !important; font-size:0.75rem; margin:0;'>System Dashboard</p>
</div>
<hr style='border-color:rgba(255,255,255,0.15); margin:0 0 8px 0;'>
""", unsafe_allow_html=True)
    st.sidebar.page_link("app.py",                   label="🏠  Dashboard")
    st.sidebar.page_link("pages/1_records.py",       label="📋  Child Records")
    st.sidebar.page_link("pages/2_risk.py",          label="🤖  Risk Predictor")
    st.sidebar.page_link("pages/3_notifications.py", label="🔔  Notifications")
    st.sidebar.page_link("pages/4_immunity.py",      label="🛡️  Immunity Dashboard")
    st.sidebar.page_link("pages/5_map.py",           label="🗺️  Coverage Map")
    st.sidebar.page_link("pages/6_behavior.py",      label="📈  Behavior Analytics")
    st.sidebar.page_link("pages/7_doctors.py",       label="👨‍⚕️  Doctor Directory")
    st.sidebar.page_link("pages/8_side_effects.py",  label="⚠️  Symptom Triage")
    st.sidebar.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin:8px 0;'>",
                        unsafe_allow_html=True)




def render_page_header(title: str, subtitle: str = ""):
    """Renders a consistent branded page header."""
    st.markdown(f"""
    <div style='margin-bottom: 0.5rem;'>
        <h1 style='margin-bottom:2px;'>{title}</h1>
        {"<p style='color:#4a7fa5; font-size:0.97rem; margin-top:0;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_footer():
    """Renders a consistent branded footer across all pages."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 4px 0; color:#4a7fa5; font-size:0.82rem;'>
        🏥 <b>AI Child Vaccination System</b> &nbsp;|&nbsp;
        Built with Streamlit &nbsp;|&nbsp;
        Ministry of Health & Family Welfare — Demo Project &nbsp;|&nbsp;
        © 2024
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, color: str = "#145da0", icon: str = ""):
    """Renders a custom styled HTML metric card."""
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.90); border-radius:14px; padding:16px 20px;
        box-shadow:0 2px 16px rgba(13,59,110,0.10); border-left:5px solid {color};
        margin-bottom:8px;'>
        <p style='margin:0; font-size:0.75rem; font-weight:600; color:#4a7fa5;
            text-transform:uppercase; letter-spacing:0.5px;'>{icon} {label}</p>
        <p style='margin:4px 0 0 0; font-size:1.6rem; font-weight:700; color:#0d3b6e;'>{value}</p>
    </div>
    """, unsafe_allow_html=True)


def insight_card(title: str, body: str, color: str = "#145da0"):
    """Renders a styled AI insight card."""
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.90); border-radius:14px; padding:18px 20px;
        box-shadow:0 2px 14px rgba(13,59,110,0.09); border-top:4px solid {color};
        margin-bottom:10px;'>
        <h4 style='color:{color}; margin:0 0 8px 0; font-size:0.95rem;'>{title}</h4>
        <p style='margin:0; color:#333; font-size:0.9rem; line-height:1.5;'>{body}</p>
    </div>
    """, unsafe_allow_html=True)
