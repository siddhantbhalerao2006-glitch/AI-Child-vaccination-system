import streamlit as st
import pandas as pd
import time
import random
import plotly.graph_objects as go

# ==========================================
# 1. MOCK DATA & CONSTANTS
# ==========================================

DISEASES = ["Polio", "Measles", "Hepatitis B", "Tuberculosis", "Diphtheria", "Tetanus", "Rubella"]

DISEASE_ICONS = {
    "Polio":       "🦵",
    "Measles":     "🌡️",
    "Hepatitis B": "🫀",
    "Tuberculosis":"🫁",
    "Diphtheria":  "🦠",
    "Tetanus":     "💉",
    "Rubella":     "🔴"
}

DUMMY_CHILDREN = {
    "CHILD001": "Arjun Sharma",
    "CHILD002": "Priya Patel",
    "CHILD003": "Rahul Mehta",
    "CHILD004": "Sana Khan",
    "CHILD005": "Vikram Singh"
}

# Deterministic mock immunity profiles per child
IMMUNITY_PROFILES = {
    "CHILD001": [95, 40, 90, 85, 30, 70, 55],
    "CHILD002": [80, 75, 60, 90, 85, 40, 95],
    "CHILD003": [35, 25, 80, 45, 70, 90, 60],
    "CHILD004": [90, 85, 30, 70, 55, 80, 40],
    "CHILD005": [60, 90, 85, 30, 95, 45, 75]
}

UPCOMING_VACCINES = {
    "CHILD001": [("Measles Booster", "2024-07-15"), ("DPT Booster", "2024-08-20")],
    "CHILD002": [("Tetanus", "2024-07-01"), ("OPV Dose 3", "2024-09-10")],
    "CHILD003": [("BCG Repeat", "2024-06-25"), ("Measles Dose 2", "2024-07-30"), ("Polio Booster", "2024-08-05")],
    "CHILD004": [("Hepatitis B Dose 3", "2024-06-30"), ("Rubella", "2024-09-20")],
    "CHILD005": [("Tuberculosis Booster", "2024-07-10"), ("Diphtheria Dose 2", "2024-08-15")]
}


# ==========================================
# 2. BACKEND LOGIC LAYER (Mock)
# ==========================================

def get_immunity_data(child_id):
    """
    MOCK API: Fetch immunity profile for a given child
    -> Future Integration: Replace this with:
       response = requests.get(f"http://api/immunity-gaps/{child_id}")
       return response.json()
    """
    time.sleep(1.5)  # Simulate API latency

    if child_id not in IMMUNITY_PROFILES:
        return None

    levels = dict(zip(DISEASES, IMMUNITY_PROFILES[child_id]))
    overall = round(sum(levels.values()) / len(levels), 1)

    # Build gap analysis from levels
    gaps = []
    for disease, value in levels.items():
        if value < 40:
            gaps.append({
                "disease": disease,
                "level": value,
                "risk": "High 🔴",
                "action": f"Schedule {disease} vaccination immediately."
            })
        elif value < 70:
            gaps.append({
                "disease": disease,
                "level": value,
                "risk": "Medium 🟡",
                "action": f"Plan a {disease} booster dose soon."
            })

    # Generate advisory
    high_risks = [g["disease"] for g in gaps if "High" in g["risk"]]
    med_risks  = [g["disease"] for g in gaps if "Medium" in g["risk"]]

    if high_risks:
        advisory = (f"⚠️ URGENT: Child has critically low immunity for "
                    f"{', '.join(high_risks)}. Immediate vaccination is recommended "
                    f"to protect against serious health risks.")
        advisory_type = "error"
    elif med_risks:
        advisory = (f"📅 ATTENTION: Child has moderate immunity gaps in "
                    f"{', '.join(med_risks)}. Consult your healthcare provider to "
                    f"schedule booster doses at the earliest.")
        advisory_type = "warning"
    else:
        advisory = ("✅ Great News! Child is well protected across all tracked "
                    "diseases. Continue following the standard vaccination schedule "
                    "for optimal immunity.")
        advisory_type = "success"

    return {
        "levels": levels,
        "overall": overall,
        "gaps": gaps,
        "advisory": advisory,
        "advisory_type": advisory_type
    }


# ==========================================
# 3. VISUALIZATION HELPERS
# ==========================================

def create_radar_chart(levels):
    """Generates a Plotly Radar/Spider chart for immunity visualization."""
    categories = list(levels.keys())
    values     = list(levels.values())

    # Close the loop for radar chart
    categories_loop = categories + [categories[0]]
    values_loop     = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_loop,
        theta=categories_loop,
        fill='toself',
        name='Immunity Level',
        line=dict(color='#4a90d9', width=2),
        fillcolor='rgba(74, 144, 217, 0.25)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[70] * len(categories_loop),
        theta=categories_loop,
        name='Safe Threshold (70%)',
        line=dict(color='#28a745', width=1.5, dash='dash'),
        fill=None
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        height=420,
        margin=dict(l=30, r=30, t=50, b=30),
        title="🛡️ Disease Immunity Radar"
    )
    return fig

def risk_color(value):
    if value >= 70: return "#28a745"   # Green
    if value >= 40: return "#ffc107"   # Yellow
    return "#dc3545"                   # Red


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar
apply_styles()
render_sidebar()

# ==========================================
# 5. UI LAYER
# ==========================================

st.title("🛡️ Child Immunity & Protection Dashboard")
st.markdown("Visual analytics for tracking child vaccination coverage and immunity gaps.")
st.markdown("---")

# ==========================================
# SECTION A: Child Selection / Input
# ==========================================
st.subheader("👶 Child Selection")

with st.container(border=True):
    inp_col1, inp_col2, inp_col3 = st.columns([1.5, 1.5, 1])
    with inp_col1:
        selected_name = st.selectbox(
            "Select a Child",
            options=["-- Select --"] + [f"{cid} — {name}" for cid, name in DUMMY_CHILDREN.items()]
        )
    with inp_col2:
        manual_id = st.text_input("Or Enter Child ID Manually", placeholder="e.g. CHILD001")
    with inp_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_clicked = st.button("🔍 Analyze Immunity", type="primary", use_container_width=True)

# Determine Child ID to analyze
child_id_to_use = None
if analyze_clicked:
    if manual_id.strip():
        child_id_to_use = manual_id.strip().upper()
    elif selected_name != "-- Select --":
        child_id_to_use = selected_name.split(" — ")[0]
    else:
        st.warning("⚠️ Please select a child or enter a Child ID first.")

st.markdown("---")

# ==========================================
# RESULTS: Sections B, C, D
# ==========================================

if child_id_to_use:
    with st.spinner(f"🔬 Analyzing immunity profile for {child_id_to_use}..."):
        data = get_immunity_data(child_id_to_use)

    if data is None:
        st.error(f"❌ No immunity data found for Child ID: **{child_id_to_use}**. Please check the ID.")
    else:
        child_name = DUMMY_CHILDREN.get(child_id_to_use, child_id_to_use)
        st.success(f"✅ Immunity profile loaded for: **{child_name}** ({child_id_to_use})")

        # Overall Score Banner
        score_color = risk_color(data['overall'])
        st.markdown(
            f"<div style='background:{score_color}22; border-left: 6px solid {score_color}; "
            f"padding: 16px 20px; border-radius:8px; margin-bottom:1rem;'>"
            f"<h3 style='color:{score_color}; margin:0;'>🏆 Overall Immunity Score: "
            f"{data['overall']}%</h3></div>",
            unsafe_allow_html=True
        )

        # ==========================================
        # SECTION B: Immunity Visualization
        # ==========================================
        st.subheader("📊 Immunity Visualization")

        viz_col, prog_col = st.columns([1.4, 1], gap="large")

        with viz_col:
            radar = create_radar_chart(data['levels'])
            st.plotly_chart(radar, use_container_width=True)

        with prog_col:
            st.markdown("#### 📈 Protection Levels by Disease")
            for disease, value in data['levels'].items():
                color  = risk_color(value)
                icon   = DISEASE_ICONS.get(disease, "💊")
                label  = f"{icon} {disease}"
                status = "Safe" if value >= 70 else ("Warning" if value >= 40 else "At Risk")
                st.markdown(
                    f"<div style='display:flex; justify-content:space-between; font-size:0.9rem;'>"
                    f"<span>{label}</span>"
                    f"<span style='color:{color}; font-weight:bold;'>{value}% — {status}</span></div>",
                    unsafe_allow_html=True
                )
                st.progress(value / 100)

        st.markdown("---")

        # ==========================================
        # SECTION C: Gap Analysis
        # ==========================================
        st.subheader("⚠️ Immunity Gap Analysis")

        if not data['gaps']:
            st.success("✅ No significant immunity gaps detected! Child is well protected.")
        else:
            gap_df_rows = []
            for gap in data['gaps']:
                gap_df_rows.append({
                    "Disease": f"{DISEASE_ICONS.get(gap['disease'], '💊')} {gap['disease']}",
                    "Current Level": f"{gap['level']}%",
                    "Risk Level": gap['risk'],
                    "Suggested Action": gap['action']
                })
            gap_df = pd.DataFrame(gap_df_rows)
            st.dataframe(gap_df, use_container_width=True, hide_index=True)

            # Also show as styled cards
            st.markdown("#### 🗂️ Detailed Gap Cards")
            num_cols = min(len(data['gaps']), 3)
            gap_cols = st.columns(num_cols)
            for i, gap in enumerate(data['gaps']):
                color = "#dc3545" if "High" in gap['risk'] else "#ffc107"
                with gap_cols[i % num_cols]:
                    st.markdown(
                        f"<div style='border:2px solid {color}; border-radius:10px; padding:14px; "
                        f"background:{color}15; margin-bottom:8px;'>"
                        f"<h4 style='color:{color}; margin-bottom:4px;'>{DISEASE_ICONS.get(gap['disease'], '💊')} {gap['disease']}</h4>"
                        f"<b>Level:</b> {gap['level']}%<br>"
                        f"<b>Risk:</b> {gap['risk']}<br>"
                        f"<b>Action:</b> {gap['action']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        st.markdown("---")

        # ==========================================
        # SECTION D: Advisory Panel + Vaccine Schedule
        # ==========================================
        st.subheader("👩‍⚕️ Advisory & Upcoming Schedule")

        adv_col, sched_col = st.columns([1.2, 1], gap="large")

        with adv_col:
            st.markdown("#### 🤖 AI Advisory Message")
            if data['advisory_type'] == "error":
                st.error(data['advisory'])
            elif data['advisory_type'] == "warning":
                st.warning(data['advisory'])
            else:
                st.success(data['advisory'])

        with sched_col:
            st.markdown("#### 📅 Upcoming Vaccine Schedule")
            upcoming = UPCOMING_VACCINES.get(child_id_to_use, [])
            if upcoming:
                sched_df = pd.DataFrame(upcoming, columns=["Vaccine", "Due Date"])
                st.dataframe(sched_df, use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming vaccines scheduled.")

else:
    st.info("👆 Select a child from the panel above and click **Analyze Immunity** to view the dashboard.")
