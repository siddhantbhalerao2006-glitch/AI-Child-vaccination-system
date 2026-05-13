import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar
apply_styles()
render_sidebar()

# ==========================================
# 1. MOCK DATA CONSTANTS
# ==========================================

PARENT_PROFILES = {
    "CHILD001": {"parent": "Mr. Ramesh Sharma",    "engagement": 82, "response_rate": 88, "missed": 2,  "pref_time": "Evening (6–8 PM)"},
    "CHILD002": {"parent": "Mrs. Sunita Patel",    "engagement": 55, "response_rate": 60, "missed": 7,  "pref_time": "Morning (9–11 AM)"},
    "CHILD003": {"parent": "Mr. Ajay Mehta",       "engagement": 31, "response_rate": 35, "missed": 14, "pref_time": "Afternoon (2–4 PM)"},
    "CHILD004": {"parent": "Mrs. Nazia Khan",      "engagement": 74, "response_rate": 79, "missed": 4,  "pref_time": "Evening (6–8 PM)"},
    "CHILD005": {"parent": "Mr. Deepak Singh",     "engagement": 91, "response_rate": 95, "missed": 1,  "pref_time": "Morning (8–10 AM)"},
}

DAYS   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HOURS  = ["6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"]

# ==========================================
# 2. BACKEND LOGIC LAYER (Mock)
# ==========================================

def get_behavior_data(child_id):
    """
    MOCK API: Fetch parent behavior analytics for a given child.
    -> Future Integration: Replace this with:
       response = requests.get(f"http://api/behavior/{child_id}")
       return response.json()
       OR: Firebase Realtime DB listener
    """
    time.sleep(1.5)

    if child_id not in PARENT_PROFILES:
        return None

    profile = PARENT_PROFILES[child_id]
    eng     = profile["engagement"]

    # Heatmap: 7 days x 6 hour-slots — rule-based seeding for determinism
    np.random.seed(list(PARENT_PROFILES.keys()).index(child_id))
    heatmap = np.random.randint(0, 10, size=(6, 7)).tolist()
    # Boost the preferred time slot
    peak_row = [0, 1, 2, 3, 4, 5][list(PARENT_PROFILES.keys()).index(child_id) % 6]
    for c in range(7):
        heatmap[peak_row][c] = min(10, heatmap[peak_row][c] + 5)

    # Channel comparison
    channels = {
        "SMS":       max(10, eng - 10 + np.random.randint(-5, 5)),
        "WhatsApp":  max(10, eng + 5  + np.random.randint(-5, 5)),
        "Calls":     max(10, eng - 20 + np.random.randint(-5, 5)),
    }

    # Engagement trend over 6 months
    base  = eng
    trend = [max(0, min(100, base + np.random.randint(-10, 10))) for _ in range(6)]

    # AI Insights
    if eng >= 75:
        level = "High 🟢"
        level_color = "#28a745"
        strategy = "Maintain current WhatsApp reminders. Send 2 days before due date."
        insights = [
            ("📱 Channel Preference", "Parent responds fastest to WhatsApp messages. SMS as backup."),
            ("🕕 Best Time to Send",  f"Peak response window: **{profile['pref_time']}**. Avoid late night."),
            ("📅 Reliability Score",  f"Excellent! Only **{profile['missed']}** missed reminders this quarter."),
        ]
    elif eng >= 50:
        level = "Medium 🟡"
        level_color = "#ffc107"
        strategy = "Switch to multi-channel: WhatsApp + SMS. Send 5 days before due date."
        insights = [
            ("⚠️ Engagement Drop",    "Engagement dropped on weekends. Avoid Saturday/Sunday reminders."),
            ("🕕 Best Time to Send",  f"Moderate response in **{profile['pref_time']}**. Try varying timings."),
            ("📞 Try Calls",          f"**{profile['missed']}** missed notifications. Add a follow-up call."),
        ]
    else:
        level = "Low 🔴"
        level_color = "#dc3545"
        strategy = "Escalate: Phone calls + ASHA worker visit. Immediate intervention needed."
        insights = [
            ("🚨 High Missed Count",  f"**{profile['missed']}** reminders missed this quarter — intervention required."),
            ("📋 Re-Engage Strategy", "Schedule an in-person visit through the nearest health center."),
            ("🕕 Last Active",        f"Parent was last responsive in **{profile['pref_time']}**. Try that window."),
        ]

    return {
        "parent_name":   profile["parent"],
        "engagement":    eng,
        "response_rate": profile["response_rate"],
        "missed":        profile["missed"],
        "pref_time":     profile["pref_time"],
        "heatmap":       heatmap,
        "channels":      channels,
        "trend":         trend,
        "level":         level,
        "level_color":   level_color,
        "strategy":      strategy,
        "insights":      insights,
    }


# ==========================================
# 3. UI LAYER
# ==========================================

st.title("📊 Parent Behavior & Engagement Analytics")
st.markdown("AI-powered insights to optimize vaccination reminder strategies per parent profile.")
st.markdown("---")

# ----------------------------------------
# Parent Selection
# ----------------------------------------
st.subheader("👨‍👩‍👧 Parent / Child Selection")

with st.container(border=True):
    inp1, inp2, inp3 = st.columns([1.5, 1.5, 1])
    with inp1:
        selected = st.selectbox(
            "Select a Child",
            ["-- Select --"] + [f"{cid} — {v['parent']}" for cid, v in PARENT_PROFILES.items()]
        )
    with inp2:
        manual_id = st.text_input("Or Enter Child ID", placeholder="e.g. CHILD001")
    with inp3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🔍 Analyze Behavior", type="primary", use_container_width=True)

child_id = None
if analyze_btn:
    if manual_id.strip():
        child_id = manual_id.strip().upper()
    elif selected != "-- Select --":
        child_id = selected.split(" — ")[0]
    else:
        st.warning("⚠️ Please select a child or enter a Child ID.")

st.markdown("---")

# ----------------------------------------
# Results Dashboard
# ----------------------------------------
if child_id:
    with st.spinner("🧠 Analyzing parent behavior patterns..."):
        data = get_behavior_data(child_id)

    if data is None:
        st.error(f"❌ No behavior data found for **{child_id}**. Please verify the Child ID.")
    else:
        st.success(f"✅ Behavior profile loaded for: **{data['parent_name']}** (Child: {child_id})")

        # Engagement Level Summary Banner
        st.markdown(
            f"<div style='background:{data['level_color']}18; border-left:6px solid {data['level_color']};"
            f"padding:14px 20px; border-radius:10px; margin-bottom:1rem;'>"
            f"<h3 style='color:{data['level_color']}; margin:0;'>🎯 Engagement Level: {data['level']}</h3>"
            f"<p style='margin:4px 0 0 0; color:#444;'>Strategy: <b>{data['strategy']}</b></p></div>",
            unsafe_allow_html=True
        )

        # ----------------------------------------
        # Engagement Metrics
        # ----------------------------------------
        st.subheader("📈 Key Engagement Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📬 Response Rate",      f"{data['response_rate']}%")
        m2.metric("❌ Missed Reminders",   data['missed'])
        m3.metric("🕐 Best Contact Time",  data['pref_time'])
        m4.metric("⭐ Engagement Score",   f"{data['engagement']} / 100")

        st.markdown("---")

        # ----------------------------------------
        # Visualizations
        # ----------------------------------------
        st.subheader("📊 Behavior Visualizations")

        chart_col1, chart_col2 = st.columns(2, gap="large")

        with chart_col1:
            # Heatmap: Response by Day × Time
            fig_heat = go.Figure(go.Heatmap(
                z=data['heatmap'],
                x=DAYS,
                y=HOURS,
                colorscale=[[0, "#eaf4fb"], [0.5, "#4a90d9"], [1, "#1a3a6e"]],
                showscale=True,
                colorbar=dict(title="Responses")
            ))
            fig_heat.update_layout(
                title="🗓️ Response Activity (Day vs Time)",
                height=300,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        with chart_col2:
            # Bar Chart: Channel comparison
            ch_names  = list(data['channels'].keys())
            ch_values = list(data['channels'].values())
            ch_colors = ["#4a90d9", "#28a745", "#ffc107"]
            fig_bar = go.Figure(go.Bar(
                x=ch_names, y=ch_values,
                marker_color=ch_colors,
                text=[f"{v}%" for v in ch_values],
                textposition='outside'
            ))
            fig_bar.update_layout(
                title="📱 Response Rate by Channel (%)",
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                yaxis=dict(range=[0, 110])
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Line Chart: Engagement Trend
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        fig_line = go.Figure()
        # Convert hex color to rgba with 10% opacity (Plotly doesn't support 8-digit hex)
        hex_c = data['level_color'].lstrip('#')
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        fill_rgba = f"rgba({r},{g},{b},0.10)"

        fig_line.add_trace(go.Scatter(
            x=months, y=data['trend'],
            mode='lines+markers',
            name='Engagement Score',
            line=dict(color=data['level_color'], width=2.5),
            fill='tozeroy',
            fillcolor=fill_rgba
        ))
        fig_line.update_layout(
            title="📅 6-Month Engagement Trend",
            height=260,
            margin=dict(l=10, r=10, t=40, b=10),
            yaxis=dict(range=[0, 110], title="Score")
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("---")

        # ----------------------------------------
        # Smart AI Insights
        # ----------------------------------------
        st.subheader("🤖 Smart Insights & Recommendations")

        ins_cols = st.columns(3)
        for i, (title, body) in enumerate(data['insights']):
            with ins_cols[i]:
                st.markdown(
                    f"<div style='background:rgba(255,255,255,0.85); border-radius:12px; padding:16px;"
                    f"box-shadow:0 2px 12px rgba(74,144,217,0.12); border-top:4px solid {data['level_color']};'>"
                    f"<h4 style='color:{data['level_color']}; margin-bottom:8px;'>{title}</h4>"
                    f"<p style='margin:0; color:#333; font-size:0.92rem;'>{body}</p></div>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Recommended Reminder Strategy")
        if data['engagement'] >= 75:
            st.success(f"✅ **{data['strategy']}**")
        elif data['engagement'] >= 50:
            st.warning(f"⚠️ **{data['strategy']}**")
        else:
            st.error(f"🚨 **{data['strategy']}**")

else:
    st.info("👆 Select a child above and click **Analyze Behavior** to load the analytics dashboard.")
