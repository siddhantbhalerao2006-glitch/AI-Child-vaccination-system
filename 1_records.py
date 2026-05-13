import streamlit as st
import pandas as pd
import time
import uuid
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar

apply_styles()
render_sidebar()


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================

if 'children_db' not in st.session_state:
    st.session_state.children_db = {}
if 'history_db' not in st.session_state:
    st.session_state.history_db = {}


# ==========================================
# 3. BACKEND LOGIC LAYER (Mock)
# ==========================================

def register_child(data):
    """
    MOCK API: Register a new child.
    -> Future Integration: Replace with:
       response = requests.post("http://api/child", json=data)
       return response.json()["child_id"]
    """
    time.sleep(1.2)
    child_id = str(uuid.uuid4())[:8].upper()
    data['id'] = child_id
    st.session_state.children_db[child_id] = data
    st.session_state.history_db[child_id] = [
        {"Vaccine Name": "BCG",          "Date Given": "2023-01-15", "Next Due Date": "—",         "Status": "✅ Completed"},
        {"Vaccine Name": "OPV Dose 1",   "Date Given": "2023-03-20", "Next Due Date": "2023-04-20", "Status": "✅ Completed"},
        {"Vaccine Name": "DPT Dose 1",   "Date Given": "2023-03-20", "Next Due Date": "2023-04-20", "Status": "✅ Completed"},
        {"Vaccine Name": "Hepatitis B",  "Date Given": "2023-01-15", "Next Due Date": "—",         "Status": "✅ Completed"},
        {"Vaccine Name": "Measles",      "Date Given": "Pending",    "Next Due Date": "2024-10-15", "Status": "⏳ Upcoming"},
        {"Vaccine Name": "Vitamin A",    "Date Given": "Pending",    "Next Due Date": "2024-10-15", "Status": "⏳ Upcoming"},
    ]
    return child_id

def get_child_history(child_id):
    """
    MOCK API: Fetch vaccination history.
    -> Future Integration: Replace with:
       response = requests.get(f"http://api/child/{child_id}/history")
       return response.json()
    """
    time.sleep(0.8)
    return st.session_state.history_db.get(child_id, None)


# ==========================================
# 4. UI LAYER
# ==========================================

# Header
st.markdown("""
<div style='text-align:center; padding: 0 0 8px 0;'>
    <h1>🏥 Child Registration & Vaccination Records</h1>
    <p style='color:#4a7fa5; font-size:1.05rem; margin-top:-8px;'>
        AI Child Vaccination System — Secure & Trusted Healthcare Management
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Summary metrics
total_children = len(st.session_state.children_db)
total_vaccinated = sum(
    sum(1 for r in records if "Completed" in r["Status"])
    for records in st.session_state.history_db.values()
)
m1, m2, m3 = st.columns(3)
m1.metric("👶 Registered Children", total_children)
m2.metric("💉 Completed Vaccinations", total_vaccinated)
m3.metric("📋 Pending Vaccinations",
          max(0, total_children * 2 - total_vaccinated))  # 2 pending per child

st.markdown("---")

# Two main columns
col1, col2 = st.columns([1, 1.2], gap="large")

# ----------------------------------------
# SECTION A: Registration Form
# ----------------------------------------
with col1:
    st.subheader("📝 Child Registration Form")

    with st.form("registration_form", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            child_name = st.text_input("👶 Child Name *")
        with f2:
            dob = st.date_input("📅 Date of Birth *", min_value=datetime(2000, 1, 1))

        gender = st.selectbox("⚥ Gender *", ["Select...", "Male", "Female", "Other"])
        parent_name = st.text_input("👨‍👩‍👦 Parent / Guardian Name *")
        phone  = st.text_input("📞 Phone Number", placeholder="10-digit mobile number")
        address = st.text_area("🏠 Address", placeholder="Village / Ward / City")

        submitted = st.form_submit_button("✅ Register Child", type="primary")

        if submitted:
            if not child_name or not parent_name or gender == "Select...":
                st.error("⚠️ Please fill in all required fields marked with *.")
            else:
                with st.spinner("Registering to system..."):
                    payload = {
                        "name": child_name, "dob": str(dob),
                        "gender": gender, "parent_name": parent_name,
                        "phone": phone, "address": address
                    }
                    new_id = register_child(payload)
                st.success(f"✅ Registered successfully! Child ID: **{new_id}**")
                st.caption("💡 Save this ID to look up vaccination history.")

    # Registered children list
    st.markdown("#### 📋 Registered Children")
    if st.session_state.children_db:
        for cid, info in st.session_state.children_db.items():
            st.markdown(
                f"<div style='background:rgba(74,144,217,0.08); border-left:3px solid #4a90d9;"
                f"padding:6px 12px; border-radius:6px; margin-bottom:6px; font-size:0.9rem;'>"
                f"👶 <b>{info['name']}</b> &nbsp;|&nbsp; ID: <code>{cid}</code> &nbsp;|&nbsp; "
                f"DOB: {info['dob']}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No children registered yet. Use the form above to register.")

# ----------------------------------------
# SECTION B: Vaccination History
# ----------------------------------------
with col2:
    st.subheader("💉 Vaccination History")

    s1, s2 = st.columns([3, 1])
    with s1:
        search_id = st.text_input("Enter Child ID", placeholder="e.g. 4F8A2B1D",
                                  label_visibility="collapsed")
    with s2:
        fetch_clicked = st.button("🔍 Fetch", type="secondary", use_container_width=True)

    if fetch_clicked:
        if not search_id:
            st.warning("⚠️ Please enter a Child ID to search.")
        else:
            with st.spinner("Fetching records..."):
                history = get_child_history(search_id.strip().upper())
            if history:
                child_info = st.session_state.children_db.get(search_id.strip().upper(), {})
                if child_info:
                    st.markdown(
                        f"<div style='background:rgba(40,167,69,0.1); border-left:4px solid #28a745;"
                        f"padding:8px 14px; border-radius:8px; margin-bottom:10px;'>"
                        f"👶 <b>{child_info.get('name','')}</b> &nbsp; | &nbsp; "
                        f"Parent: {child_info.get('parent_name','')} &nbsp; | &nbsp; "
                        f"📞 {child_info.get('phone','N/A')}</div>",
                        unsafe_allow_html=True
                    )
                df = pd.DataFrame(history)
                st.dataframe(df, use_container_width=True, hide_index=True)

                completed = sum(1 for r in history if "Completed" in r["Status"])
                upcoming  = sum(1 for r in history if "Upcoming" in r["Status"])
                b1, b2 = st.columns(2)
                b1.metric("✅ Completed", completed)
                b2.metric("⏳ Upcoming", upcoming)

                if upcoming > 0:
                    st.info(f"📅 {upcoming} vaccine(s) are upcoming. Please schedule soon.")
            else:
                st.error(f"❌ No records found for ID: **{search_id}**. Please verify the Child ID.")

    # Static sample table when no search is performed
    else:
        st.markdown("#### 📊 Sample Vaccination Record")
        sample = {
            "Vaccine Name": ["BCG", "OPV Dose 1", "DPT Dose 1", "Measles", "Vitamin A"],
            "Date Given":   ["2023-01-15", "2023-03-20", "2023-03-20", "Pending", "Pending"],
            "Next Due Date":["—", "2023-04-20", "2023-04-20", "2024-10-15", "2024-10-15"],
            "Status":       ["✅ Completed", "✅ Completed", "✅ Completed", "⏳ Upcoming", "⏳ Upcoming"]
        }
        st.dataframe(pd.DataFrame(sample), use_container_width=True, hide_index=True)
        st.caption("👆 Register a child and use their ID to look up real records.")

render_footer()
