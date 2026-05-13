import streamlit as st
from utils import apply_styles, render_footer, render_sidebar

st.set_page_config(
    page_title="AI Child Vaccination System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()

apply_styles()
render_sidebar()

# ---- Home Page ----
st.markdown("""
<div style='text-align:center; padding: 28px 0 10px 0;'>
    <div style='font-size:3.5rem; margin-bottom:8px;'>🏥</div>
    <h1 style='font-size:2.4rem; margin-bottom:6px;'>AI Child Vaccination System</h1>
    <p style='color:#4a7fa5; font-size:1.08rem; max-width:600px; margin:0 auto;'>
        An intelligent, data-driven platform for managing child immunization programs
        with AI-powered risk prediction, behavior analytics, and real-time triage.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- Live System Stats ----
st.markdown("### 📊 System Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👶 Children Enrolled",  "1,284")
c2.metric("💉 Vaccines Administered", "8,940")
c3.metric("🔴 High Risk Cases",    "47")
c4.metric("📨 Reminders Sent",     "3,610")
c5.metric("✅ Coverage Rate",       "82%")

st.markdown("---")

# ---- Feature Cards ----
st.markdown("### 🗂️ Application Modules")

pages = [
    ("📋", "Child Records",         "Register children, manage profiles, and track vaccination history.",       "#145da0"),
    ("🤖", "Risk Predictor",        "AI-powered tool to assess vaccination delay risk for each child.",         "#dc3545"),
    ("🔔", "Notifications",         "Automated and manual reminder system with SMS/WhatsApp templates.",        "#fd7e14"),
    ("🛡️", "Immunity Dashboard",    "Visual radar charts showing disease protection levels and immunity gaps.", "#6f42c1"),
    ("🗺️", "Coverage Map",          "Geographic heatmap of district-level vaccination coverage across India.",  "#0d7c6e"),
    ("📈", "Behavior Analytics",    "Parent engagement analytics and optimized reminder strategy insights.",     "#1a7db8"),
    ("👨‍⚕️","Doctor Directory",     "Manage healthcare providers, schedules, and health center assignments.",   "#28a745"),
    ("⚠️", "Symptom Triage",        "Post-vaccination symptom checker with AI-powered emergency triage logic.", "#e83e8c"),
]

row1 = st.columns(4)
row2 = st.columns(4)
rows = row1 + row2

for i, (icon, name, desc, color) in enumerate(pages):
    with rows[i]:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.90); border-radius:16px; padding:20px 16px;
            box-shadow:0 3px 18px rgba(13,59,110,0.10); border-top:4px solid {color};
            min-height:140px; transition:all 0.2s;'>
            <div style='font-size:1.8rem; margin-bottom:8px;'>{icon}</div>
            <h3 style='color:{color}; font-size:0.95rem; margin:0 0 6px 0;'>{name}</h3>
            <p style='color:#555; font-size:0.82rem; margin:0; line-height:1.5;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---- Quick Alerts Banner ----
st.markdown("### 🚨 Active System Alerts")
al1, al2, al3 = st.columns(3)
with al1:
    st.error("🔴 **47 children** classified as HIGH RISK this week. Immediate follow-up required.")
with al2:
    st.warning("🟡 **132 vaccination reminders** are overdue. Check Notifications page.")
with al3:
    st.info("🔵 **Coverage in 3 districts** below 50%. Review the Coverage Map.")

render_footer()
