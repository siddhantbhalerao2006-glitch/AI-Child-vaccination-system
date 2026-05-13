import streamlit as st
import time
import pandas as pd
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar
apply_styles()
render_sidebar()

# ==========================================
# 1. SESSION STATE
# ==========================================
if 'triage_history' not in st.session_state:
    st.session_state.triage_history = []

# ==========================================
# 2. TRIAGE LOGIC LAYER (Mock)
# ==========================================

def triage_symptoms(symptoms):
    """
    MOCK TRIAGE ENGINE: Rule-based symptom classification.
    -> Future Integration: Replace this with:
       Option A (FastAPI ML endpoint):
           response = requests.post("http://api/triage-symptoms", json=symptoms)
           return response.json()
       Option B (Local ML Model):
           model = joblib.load("triage_model.pkl")
           result = model.predict([feature_vector])
    """
    time.sleep(1.5)  # Simulate inference delay

    fever        = symptoms.get("fever", False)
    swelling     = symptoms.get("swelling", False)
    rash         = symptoms.get("rash", False)
    vomiting     = symptoms.get("vomiting", False)
    breathing    = symptoms.get("breathing", False)
    temperature  = symptoms.get("temperature", 98.6)

    # --- Rule-Based Triage Logic ---

    # EMERGENCY: Life-threatening indicators
    if breathing or temperature >= 104.0:
        return {
            "level":       "EMERGENCY",
            "color":       "#dc3545",
            "icon":        "🚨",
            "confidence":  96,
            "guidance":    "SEEK IMMEDIATE EMERGENCY CARE. Call 108 or visit the nearest hospital right away. Do not wait.",
            "doctor_visit":"Visit the ER immediately. Do not drive yourself — call an ambulance.",
            "reasons":     [r for r in [
                "Difficulty breathing detected — anaphylactic reaction possible." if breathing else None,
                f"Extremely high fever ({temperature}°F) — risk of febrile seizure." if temperature >= 104.0 else None,
            ] if r]
        }

    # URGENT: Serious combination of symptoms
    if (fever and vomiting) or (temperature >= 102.5 and (rash or vomiting)):
        return {
            "level":       "URGENT",
            "color":       "#fd7e14",
            "icon":        "⚠️",
            "confidence":  88,
            "guidance":    "Contact your doctor or visit a clinic TODAY. Do not ignore these symptoms — they need medical evaluation.",
            "doctor_visit":"Visit a clinic or call your doctor within 4–6 hours.",
            "reasons":     [r for r in [
                "Fever combined with vomiting suggests systemic reaction." if fever and vomiting else None,
                f"High temperature ({temperature}°F) with additional symptoms warrants evaluation." if temperature >= 102.5 else None,
                "Rash may indicate allergic response." if rash else None,
            ] if r]
        }

    # MONITOR: Mild-to-moderate symptoms present
    if fever or rash or vomiting or swelling or temperature >= 100.4:
        return {
            "level":       "MONITOR",
            "color":       "#ffc107",
            "icon":        "👁️",
            "confidence":  81,
            "guidance":    "These are common post-vaccination side effects. Monitor the child closely for the next 24–48 hours. Contact a doctor if symptoms worsen.",
            "doctor_visit":"Call your doctor if symptoms persist beyond 48 hours or intensity increases.",
            "reasons":     [r for r in [
                "Mild fever present — common after vaccination." if fever else None,
                "Swelling at injection site — expected, apply cold compress." if swelling else None,
                "Rash observed — monitor for spread." if rash else None,
                "Mild vomiting noted — ensure hydration." if vomiting else None,
                f"Low-grade temperature ({temperature}°F)." if 100.4 <= temperature < 102.5 else None,
            ] if r]
        }

    # NORMAL: No significant symptoms
    return {
        "level":       "NORMAL",
        "color":       "#28a745",
        "icon":        "✅",
        "confidence":  94,
        "guidance":    "No significant side effects detected. This is completely normal. Ensure the child is well-rested and hydrated.",
        "doctor_visit":"Routine follow-up at next scheduled appointment.",
        "reasons":     ["No concerning symptoms reported.", "Temperature within normal range."]
    }

# ==========================================
# 3. UI LAYER
# ==========================================

st.title("🩺 Post-Vaccination Symptom Checker & Triage System")
st.markdown("An intelligent triage assistant to evaluate post-vaccination side effects and guide parents.")
st.markdown("---")

# Warning Banner for serious symptoms awareness
st.markdown("""
<div style='background:#fff3cd; border:1px solid #ffc107; border-radius:10px; padding:10px 16px; margin-bottom:16px;'>
    ⚠️ <b>Important:</b> If your child is having <b>difficulty breathing, seizures, or loses consciousness</b>,
    call <b>108 (Emergency)</b> immediately. Do not use this tool — go to the ER.
</div>
""", unsafe_allow_html=True)

# Main layout
left, right = st.columns([1, 1.3], gap="large")

# ----------------------------------------
# Symptom Input Panel
# ----------------------------------------
with left:
    st.subheader("📋 Symptom Input Panel")

    with st.container(border=True):
        child_name_input = st.text_input("👶 Child Name (optional)", placeholder="e.g. Arjun Sharma")
        vaccine_given    = st.selectbox("💉 Vaccine Recently Given", ["Select...", "BCG", "OPV", "DPT", "Measles", "Hepatitis B", "MMR", "Vitamin A"])

        st.markdown("**🤒 Select All Symptoms Observed:**")
        c1, c2 = st.columns(2)
        with c1:
            sym_fever     = st.checkbox("🌡️ Fever")
            sym_swelling  = st.checkbox("🔴 Injection Site Swelling")
            sym_rash      = st.checkbox("🧴 Rash / Skin Reaction")
        with c2:
            sym_vomiting  = st.checkbox("🤢 Vomiting / Nausea")
            sym_breathing = st.checkbox("😮‍💨 Difficulty Breathing")

        temperature = st.slider(
            "🌡️ Measured Temperature (°F)",
            min_value=96.0, max_value=106.0, value=98.6, step=0.1,
            help="Normal: 97–99°F | Low-grade fever: 99–100.3°F | Fever: ≥100.4°F"
        )

        # Temp color label
        if temperature >= 104:
            temp_label = f"<span style='color:#dc3545; font-weight:bold;'>🔴 Dangerously High ({temperature}°F)</span>"
        elif temperature >= 102.5:
            temp_label = f"<span style='color:#fd7e14; font-weight:bold;'>🟠 High Fever ({temperature}°F)</span>"
        elif temperature >= 100.4:
            temp_label = f"<span style='color:#ffc107; font-weight:bold;'>🟡 Low-grade Fever ({temperature}°F)</span>"
        else:
            temp_label = f"<span style='color:#28a745; font-weight:bold;'>🟢 Normal ({temperature}°F)</span>"
        st.markdown(temp_label, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🔬 Analyze Symptoms", type="primary", use_container_width=True)

# ----------------------------------------
# Triage Result + Guidance
# ----------------------------------------
with right:
    st.subheader("🎯 Triage Result")

    if not analyze_btn:
        st.info("👈 Enter symptoms on the left panel and click **Analyze Symptoms** to get a triage assessment.")
        with st.container(border=True):
            st.markdown("<br><h4 style='text-align:center; color:gray;'>Waiting for symptom input...</h4><br>", unsafe_allow_html=True)
    else:
        symptom_payload = {
            "fever":       sym_fever,
            "swelling":    sym_swelling,
            "rash":        sym_rash,
            "vomiting":    sym_vomiting,
            "breathing":   sym_breathing,
            "temperature": temperature,
        }

        with st.spinner("🧠 AI Triage Engine analyzing symptoms..."):
            result = triage_symptoms(symptom_payload)

        # Save to history
        history_entry = {
            "Time":        datetime.now().strftime("%H:%M:%S"),
            "Child":       child_name_input or "—",
            "Vaccine":     vaccine_given if vaccine_given != "Select..." else "—",
            "Triage":      result['level'],
            "Temperature": f"{temperature}°F",
            "Confidence":  f"{result['confidence']}%"
        }
        st.session_state.triage_history.insert(0, history_entry)

        # Triage Level Display
        st.markdown(
            f"<div style='background:{result['color']}18; border:3px solid {result['color']};"
            f"border-radius:14px; padding:20px; text-align:center; margin-bottom:16px;'>"
            f"<h1 style='color:{result['color']}; margin:0; font-size:3rem;'>{result['icon']}</h1>"
            f"<h2 style='color:{result['color']}; margin:4px 0;'>{result['level']}</h2>"
            f"<p style='color:#555; margin:0;'>Model Confidence: <b>{result['confidence']}%</b></p>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Confidence Progress Bar
        st.progress(result['confidence'] / 100)

        # Reasons
        st.markdown("#### 🔍 Detected Indicators:")
        for reason in result['reasons']:
            st.markdown(f"- {reason}")

        st.markdown("---")

        # Guidance Panel
        st.subheader("👩‍⚕️ Guidance & Recommended Action")

        if result['level'] == "EMERGENCY":
            st.error(f"🚨 **EMERGENCY ACTION REQUIRED:** {result['guidance']}")
        elif result['level'] == "URGENT":
            st.warning(f"⚠️ **URGENT:** {result['guidance']}")
        elif result['level'] == "MONITOR":
            st.warning(f"👁️ **MONITOR:** {result['guidance']}")
        else:
            st.success(f"✅ **ALL CLEAR:** {result['guidance']}")

        # When to visit doctor
        st.markdown(
            f"<div style='background:rgba(74,144,217,0.08); border-left:4px solid #4a90d9;"
            f"padding:10px 16px; border-radius:8px; margin-top:12px;'>"
            f"<b>🏥 When to Visit a Doctor:</b><br>{result['doctor_visit']}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")

# ----------------------------------------
# Previous Checks History
# ----------------------------------------
st.subheader("📜 Previous Checks History")
if st.session_state.triage_history:
    hist_df = pd.DataFrame(st.session_state.triage_history)
    st.dataframe(hist_df, use_container_width=True, hide_index=True)
    if st.button("🗑️ Clear History"):
        st.session_state.triage_history = []
        st.rerun()
else:
    st.info("No checks performed yet in this session. Use the panel above to analyze symptoms.")

# ----------------------------------------
# General Reference Table
# ----------------------------------------
st.markdown("---")
st.subheader("📖 Quick Reference: Normal vs Concerning Side Effects")
ref_df = pd.DataFrame({
    "Side Effect":    ["Mild fever (< 100.4°F)", "Injection site redness", "Fussiness / crying",
                       "High fever (≥ 102.5°F)", "Persistent vomiting", "Difficulty breathing", "Seizures"],
    "Type":           ["🟢 Normal", "🟢 Normal", "🟢 Normal",
                       "🟡 Monitor", "🟠 Urgent", "🔴 Emergency", "🔴 Emergency"],
    "Action":         ["Rest & fluids", "Cold compress", "Comfort the child",
                       "Contact doctor", "Visit clinic today", "Call 108 now", "Call 108 now"]
})
st.dataframe(ref_df, use_container_width=True, hide_index=True)
