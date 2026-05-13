import streamlit as st
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar

apply_styles()
render_sidebar()

# Try to import Plotly for the gauge chart. If not installed, it safely falls back.
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# ==========================================
# 1. AI/ML LOGIC LAYER (Mock)
# ==========================================

def predict_risk(child_data):
    """
    MOCK ML MODEL: Predict vaccination delay/health risk
    -> Future Integration: Replace this logic with your FastAPI call:
       response = requests.post("http://api/predict-risk", json=child_data)
       return response.json()
    """
    time.sleep(1.2) # Simulate inference speed
    
    score = 5 # Base score
    reasons = []
    
    # -- Mock Logic Rules --
    if child_data['age_months'] < 6:
        score += 15
        reasons.append("👶 Infant age group (< 6 months) indicates higher vulnerability.")
    elif child_data['age_months'] > 48:
        score -= 5 # Older children might be slightly lower risk if vaccines complete
        
    if child_data['missed_vaccines'] > 0:
        score += child_data['missed_vaccines'] * 20
        reasons.append(f"⚠️ Missed {child_data['missed_vaccines']} scheduled vaccines.")
        
    if child_data['health'] == "Weak":
        score += 20
        reasons.append("🩺 Current health condition is marked as 'Weak'.")
    elif child_data['health'] == "Chronic":
        score += 40
        reasons.append("⚕️ Underlying 'Chronic' health condition present.")
        
    if child_data['nutrition'] == "Average":
        score += 10
    elif child_data['nutrition'] == "Poor":
        score += 25
        reasons.append("🍎 Poor nutrition status impacts immunity.")
        
    score = min(max(score, 0), 100) # Cap between 0 and 100
    
    # Determine Level, Color, and Recommendation
    if score < 30:
        level = "LOW"
        color = "#28a745" # Professional Green
        recommendation = "Maintain regular checkups and the standard vaccination schedule."
        insight = "Child is at low risk. Keep up the good work with the vaccination schedule."
    elif score < 70:
        level = "MEDIUM"
        color = "#ffc107" # Professional Yellow
        recommendation = "Schedule a consultation soon. Catch up on any missed vaccine doses."
        insight = f"Child is at moderate risk primarily due to {child_data['missed_vaccines']} missed vaccinations." if child_data['missed_vaccines'] > 0 else "Child is at moderate risk due to health/nutrition factors."
    else:
        level = "HIGH"
        color = "#dc3545" # Professional Red
        recommendation = "URGENT: Immediate medical consultation required to address missed vaccines and health vulnerabilities."
        insight = "Critical risk detected! Immediate intervention is highly recommended."
        
    if not reasons:
        reasons.append("✅ No significant risk factors detected.")
        
    return {
        "risk_level": level,
        "risk_score": score,
        "top_reasons": reasons[:3],
        "color": color,
        "recommendation": recommendation,
        "confidence": 92 + (score % 5), # mock confidence metric 92-96%
        "insight": insight
    }

def create_gauge_chart(score, color):
    """Generates a Plotly Gauge Chart for a professional dashboard look."""
    if not HAS_PLOTLY:
        return None
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "AI Risk Score", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e0e0e0",
            'steps': [
                {'range': [0, 30], 'color': '#e6f4ea'}, # Light green
                {'range': [30, 70], 'color': '#fef7e0'}, # Light yellow
                {'range': [70, 100], 'color': '#fce8e6'} # Light red
            ],
        }
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# ==========================================
# 2. UI LAYER (Dashboard Design)
# ==========================================

st.title("🤖 AI Risk Dashboard")
st.markdown("Advanced predictive analytics for child vaccination and health vulnerabilities.")
st.markdown("---")

# Main Dashboard Layout
col1, col2 = st.columns([1, 1.8], gap="large")

# ----------------------------------------
# SECTION A: Input Panel (Left)
# ----------------------------------------
with col1:
    st.markdown("### 📋 Patient Input Panel")
    
    # Using st.container for a card-like look
    with st.container(border=True):
        st.markdown("Enter patient parameters to run the AI prediction.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        age_input = st.slider("👶 Age (in months)", min_value=0, max_value=60, value=12, help="Age of the child in months")
        missed_vaccines_input = st.slider("💉 Missed Vaccines", min_value=0, max_value=10, value=0, help="Number of standard vaccines missed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        health_input = st.selectbox("🏥 Health Condition", ["Normal", "Weak", "Chronic"], help="Current overall health state")
        nutrition_input = st.selectbox("🍎 Nutrition Status", ["Good", "Average", "Poor"], help="General nutritional assessment")
        
        st.markdown("<br>", unsafe_allow_html=True)
        predict_clicked = st.button("🚀 Run AI Prediction", type="primary", use_container_width=True)

# ----------------------------------------
# SECTION B: Results Dashboard (Right)
# ----------------------------------------
with col2:
    st.markdown("### 📊 Results Dashboard")
    
    if not predict_clicked:
        # Empty State
        st.info("👈 Fill out the Input Panel and click **Run AI Prediction** to generate the dashboard.")
        with st.container(border=True):
            st.markdown("<br><br><h4 style='text-align: center; color: gray;'>Waiting for Patient Data...</h4><br><br>", unsafe_allow_html=True)
    else:
        # Processing State
        with st.spinner("🧠 AI Model analyzing patient risk factors..."):
            payload = {
                "age_months": age_input,
                "missed_vaccines": missed_vaccines_input,
                "health": health_input,
                "nutrition": nutrition_input
            }
            result = predict_risk(payload)
            
        # Top Metrics Cards
        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric(label="Predicted Status", value=result['risk_level'])
        with met2:
            st.metric(label="AI Risk Score", value=f"{result['risk_score']} / 100")
        with met3:
            st.metric(label="Model Confidence", value=f"{result['confidence']}%")
            
        st.markdown("---")
        
        # Visuals and Insights
        vis1, vis2 = st.columns([1.2, 1])
        
        with vis1:
            if HAS_PLOTLY:
                fig = create_gauge_chart(result['risk_score'], result['color'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback if Plotly isn't installed
                st.markdown(f"<h1 style='text-align: center; color: {result['color']}; font-size: 5rem; margin-bottom: 0px;'>{result['risk_score']}%</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-weight: bold; color: gray;'>Risk Score</p>", unsafe_allow_html=True)
                st.progress(result['risk_score'] / 100.0)
                st.caption("*Tip: Install `plotly` (pip install plotly) for advanced gauge charts!*")
                
        with vis2:
            st.markdown("#### 💡 AI Insight")
            st.info(result['insight'])
            
            st.markdown("#### 🔍 Contributing Factors")
            for reason in result['top_reasons']:
                st.markdown(f"{reason}")
                
        st.markdown("---")
        
        # Final Recommendation Advisory Box
        st.markdown("#### 👩‍⚕️ Advisory Recommendation")
        if result['risk_level'] == "LOW":
            st.success(result['recommendation'])
        elif result['risk_level'] == "MEDIUM":
            st.warning(result['recommendation'])
        else:
            st.error(result['recommendation'])
