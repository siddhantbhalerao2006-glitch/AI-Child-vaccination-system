import streamlit as st
import pandas as pd
import time
import re
from datetime import datetime, timedelta
import random

# ==========================================
# 1. MOCK DATA INITIALIZATION
# ==========================================

SAMPLE_QUEUE = [
    {"Child Name": "Arjun Sharma", "Vaccine Name": "DPT Booster", "Due Date": "2024-06-10", "Status": "Scheduled", "Contact": "9876543210"},
    {"Child Name": "Priya Patel", "Vaccine Name": "OPV Dose 2", "Due Date": "2024-06-12", "Status": "Sent", "Contact": "9123456780"},
    {"Child Name": "Rahul Mehta", "Vaccine Name": "Measles", "Due Date": "2024-05-28", "Status": "Missed", "Contact": "9988776655"},
    {"Child Name": "Sana Khan", "Vaccine Name": "Hepatitis B", "Due Date": "2024-06-15", "Status": "Scheduled", "Contact": "9871234560"},
    {"Child Name": "Vikram Singh", "Vaccine Name": "BCG", "Due Date": "2024-06-08", "Status": "Sent", "Contact": "9765432100"},
    {"Child Name": "Anjali Rao", "Vaccine Name": "Vitamin A", "Due Date": "2024-05-30", "Status": "Missed", "Contact": "9654321009"},
    {"Child Name": "Kabir Nair", "Vaccine Name": "MMR", "Due Date": "2024-06-20", "Status": "Scheduled", "Contact": "9543210098"},
]

MESSAGE_TEMPLATES = {
    "Friendly": {
        "English": "Dear Parent, 😊 This is a gentle reminder that {child_name}'s {vaccine_name} vaccination is due soon. Please visit your nearest health center. Stay healthy!",
        "Hindi":   "प्रिय माता-पिता, 😊 यह याद दिलाना है कि {child_name} का {vaccine_name} टीका जल्द देय है। कृपया नजदीकी स्वास्थ्य केंद्र पर जाएं।"
    },
    "Reminder": {
        "English": "📅 REMINDER: {child_name} is due for {vaccine_name} vaccination. Please schedule an appointment at your health center at your earliest convenience.",
        "Hindi":   "📅 अनुस्मारक: {child_name} को {vaccine_name} टीके की आवश्यकता है। कृपया शीघ्र अपॉइंटमेंट लें।"
    },
    "Urgent": {
        "English": "⚠️ URGENT: {child_name}'s {vaccine_name} vaccination is OVERDUE. Delaying further may put your child at risk. Please visit a health center immediately.",
        "Hindi":   "⚠️ तत्काल: {child_name} का {vaccine_name} टीका अतिदेय है। देरी से बच्चे को खतरा हो सकता है। तुरंत स्वास्थ्य केंद्र जाएं।"
    },
    "Alert": {
        "English": "🚨 HEALTH ALERT: {child_name} has missed a critical vaccine ({vaccine_name}). Contact your doctor today. Child health is at risk!",
        "Hindi":   "🚨 स्वास्थ्य अलर्ट: {child_name} ने महत्वपूर्ण टीका ({vaccine_name}) चूक लिया है। आज ही डॉक्टर से संपर्क करें!"
    }
}

# Initialize session state
if 'notification_queue' not in st.session_state:
    st.session_state.notification_queue = SAMPLE_QUEUE.copy()
if 'sent_log' not in st.session_state:
    st.session_state.sent_log = []

# ==========================================
# 2. BACKEND LOGIC LAYER (Mock APIs)
# ==========================================

def send_reminder(child_name, phone, vaccine_name, message_type):
    """
    MOCK SMS SENDER
    -> Future Integration: Replace this with:
       Option A (Fast2SMS):
           import requests
           requests.post("https://www.fast2sms.com/dev/bulkV2", ...)
       Option B (Firebase FCM):
           from firebase_admin import messaging
           messaging.send(message)
    """
    time.sleep(2) # Simulate API call delay

    log_entry = {
        "Child Name": child_name,
        "Vaccine Name": vaccine_name,
        "Due Date": (datetime.now() + timedelta(days=random.randint(3, 14))).strftime("%Y-%m-%d"),
        "Status": "Sent",
        "Contact": phone
    }
    st.session_state.notification_queue.append(log_entry)
    st.session_state.sent_log.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Child": child_name,
        "Phone": phone,
        "Vaccine": vaccine_name,
        "Type": message_type
    })
    return True

def get_notification_queue(status_filter=None):
    """
    MOCK QUEUE FETCHER
    -> Future Integration: Replace with:
       response = requests.get("http://api/notifications/queue")
       return response.json()
    """
    queue = st.session_state.notification_queue
    if status_filter and status_filter != "All":
        queue = [n for n in queue if n["Status"] == status_filter]
    return queue

def get_analytics():
    """Computes summary stats from the queue. Replace with API stats later."""
    q = st.session_state.notification_queue
    total     = len(q)
    sent      = sum(1 for n in q if n["Status"] == "Sent")
    scheduled = sum(1 for n in q if n["Status"] == "Scheduled")
    missed    = sum(1 for n in q if n["Status"] == "Missed")
    rate      = round((sent / total) * 100, 1) if total > 0 else 0
    return {"total": total, "sent": sent, "scheduled": scheduled, "missed": missed, "rate": rate}

def validate_phone(phone):
    return bool(re.match(r"^[6-9]\d{9}$", phone.strip()))

# ==========================================
# 3. STATUS STYLING HELPERS
# ==========================================

STATUS_COLOR = {"Sent": "🟢", "Scheduled": "🔵", "Missed": "🔴"}

def style_status(status):
    return f"{STATUS_COLOR.get(status, '⚪')} {status}"

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar
apply_styles()
render_sidebar()

# ==========================================
# 5. UI LAYER
# ==========================================

st.title("🔔 Vaccination Notification & Reminder System")
st.markdown("Automate, manage, and monitor vaccination reminders for enrolled children.")
st.markdown("---")

# --- TOP ANALYTICS BANNER ---
stats = get_analytics()
a1, a2, a3, a4, a5 = st.columns(5)
a1.metric("📨 Total Reminders", stats["total"])
a2.metric("✅ Sent",            stats["sent"])
a3.metric("📅 Scheduled",      stats["scheduled"])
a4.metric("❌ Missed",          stats["missed"])
a5.metric("📈 Success Rate",   f"{stats['rate']}%")

st.markdown("---")

# ==========================================
# SECTION A: Notification Queue Dashboard
# ==========================================
st.subheader("📋 Notification Queue")

filter_col, _, _ = st.columns([1, 2, 2])
with filter_col:
    status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "Sent", "Missed"])

queue_data = get_notification_queue(status_filter)

if queue_data:
    df = pd.DataFrame(queue_data)
    df["Status"] = df["Status"].apply(style_status)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No records found for the selected filter.")

st.markdown("---")

# ==========================================
# SECTION B & C side by side
# ==========================================
sec_b, sec_c = st.columns([1, 1], gap="large")

# ==========================================
# SECTION B: Send Manual Reminder
# ==========================================
with sec_b:
    st.subheader("📤 Send Manual Reminder")

    with st.container(border=True):
        r_child_name = st.text_input("👶 Child Name *")
        r_phone      = st.text_input("📞 Phone Number *", placeholder="10-digit Indian mobile number")
        r_vaccine    = st.text_input("💉 Vaccine Name *")
        r_msg_type   = st.selectbox("📝 Message Type *", ["Friendly", "Reminder", "Urgent", "Alert"])

        send_clicked = st.button("📲 Send Reminder", type="primary", use_container_width=True)

        if send_clicked:
            if not r_child_name or not r_phone or not r_vaccine:
                st.error("⚠️ Please fill in all required fields.")
            elif not validate_phone(r_phone):
                st.error("❌ Invalid phone number. Must be a 10-digit Indian mobile number starting with 6–9.")
            else:
                with st.spinner(f"📡 Sending {r_msg_type} reminder to {r_phone}..."):
                    success = send_reminder(r_child_name, r_phone, r_vaccine, r_msg_type)
                if success:
                    st.success(f"✅ {r_msg_type} reminder sent to {r_child_name} ({r_phone})!")
                    st.caption("📝 Reminder has been logged in the queue above.")

    # Sent Log
    if st.session_state.sent_log:
        st.markdown("#### 📜 Recent Sent Log")
        log_df = pd.DataFrame(st.session_state.sent_log)
        st.dataframe(log_df, use_container_width=True, hide_index=True)

# ==========================================
# SECTION C: Message Template Preview
# ==========================================
with sec_c:
    st.subheader("🗒️ Message Template Preview")

    with st.container(border=True):
        preview_type  = st.selectbox("Select Message Type", ["Friendly", "Reminder", "Urgent", "Alert"], key="preview_type")
        preview_lang  = st.selectbox("Select Language",     ["English", "Hindi"])
        sample_child  = st.text_input("Sample Child Name",  value="Arjun")
        sample_vacc   = st.text_input("Sample Vaccine",     value="DPT Booster")

        st.markdown("#### 💬 Message Preview:")
        if preview_type and preview_lang:
            template = MESSAGE_TEMPLATES[preview_type][preview_lang]
            filled   = template.format(child_name=sample_child or "Child", vaccine_name=sample_vacc or "Vaccine")
            st.info(filled)

        st.markdown("---")
        st.markdown("**All Templates Quick Reference:**")
        for mtype, langs in MESSAGE_TEMPLATES.items():
            with st.expander(f"📄 {mtype} Template"):
                st.markdown(f"**English:** {langs['English']}")
                st.markdown(f"**Hindi:** {langs['Hindi']}")

render_footer()
