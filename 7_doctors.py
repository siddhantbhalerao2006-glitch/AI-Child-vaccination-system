import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar

apply_styles()
render_sidebar()

# ==========================================
# PAGE: Doctor Management
# ==========================================

st.title("👨‍⚕️ Doctor & Healthcare Provider Directory")
st.markdown("Manage and view doctors assigned to vaccination programs.")
st.markdown("---")

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("👨‍⚕️ Total Doctors",   "48")
m2.metric("✅ Active",            "39")
m3.metric("🏥 Health Centers",    "12")
m4.metric("📍 Districts Covered", "8")

st.markdown("---")

col1, col2 = st.columns([1.4, 1], gap="large")

with col1:
    st.subheader("🗂️ Doctor Directory")

    DOCTORS = [
        {"Name": "Dr. Anjali Mehta",  "Specialization": "Pediatrics",      "Center": "PHC Andheri",    "Status": "✅ Active",   "Phone": "9876543210"},
        {"Name": "Dr. Ramesh Kumar",  "Specialization": "General Medicine", "Center": "CHC Borivali",   "Status": "✅ Active",   "Phone": "9765432109"},
        {"Name": "Dr. Sunita Rao",    "Specialization": "Immunology",       "Center": "District Hosp.", "Status": "✅ Active",   "Phone": "9654321098"},
        {"Name": "Dr. Vikram Patel",  "Specialization": "Pediatrics",      "Center": "PHC Malad",      "Status": "⛔ Inactive", "Phone": "9543210987"},
        {"Name": "Dr. Priya Sharma",  "Specialization": "Public Health",   "Center": "Urban Health",   "Status": "✅ Active",   "Phone": "9432109876"},
        {"Name": "Dr. Karan Joshi",   "Specialization": "General Medicine", "Center": "PHC Kandivali",  "Status": "✅ Active",   "Phone": "9321098765"},
        {"Name": "Dr. Meena Nair",    "Specialization": "Immunology",       "Center": "Tribal Center",  "Status": "✅ Active",   "Phone": "9210987654"},
    ]

    search = st.text_input("🔍 Search by Name or Specialization", placeholder="e.g. Pediatrics")
    filtered = [d for d in DOCTORS if
                search.lower() in d["Name"].lower() or
                search.lower() in d["Specialization"].lower()] if search else DOCTORS

    st.dataframe(pd.DataFrame(filtered), use_container_width=True, hide_index=True)

with col2:
    st.subheader("➕ Add New Doctor")
    with st.form("add_doctor_form", clear_on_submit=True):
        doc_name   = st.text_input("👨‍⚕️ Full Name *")
        doc_spec   = st.selectbox("🔬 Specialization *",
                                  ["Pediatrics", "General Medicine", "Immunology", "Public Health"])
        doc_center = st.text_input("🏥 Health Center *")
        doc_phone  = st.text_input("📞 Phone Number")
        submitted  = st.form_submit_button("➕ Add Doctor", type="primary")
        if submitted:
            if not doc_name or not doc_center:
                st.error("⚠️ Please fill in all required fields.")
            else:
                st.success(f"✅ Dr. {doc_name} has been added to the directory!")

st.markdown("---")

st.subheader("📅 Vaccination Schedule by Doctor")
schedule = pd.DataFrame({
    "Doctor":              ["Dr. Anjali Mehta", "Dr. Sunita Rao", "Dr. Priya Sharma", "Dr. Karan Joshi"],
    "Date":                ["2024-06-10", "2024-06-11", "2024-06-12", "2024-06-13"],
    "Center":              ["PHC Andheri", "District Hosp.", "Urban Health", "PHC Kandivali"],
    "Children Scheduled":  [18, 25, 12, 20],
    "Vaccines":            ["OPV, BCG", "DPT, MMR", "Hepatitis B", "Measles, Vitamin A"]
})
st.dataframe(schedule, use_container_width=True, hide_index=True)

render_footer()
