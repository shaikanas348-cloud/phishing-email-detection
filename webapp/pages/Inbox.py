import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Inbox")

# Top actions
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Scan All"):
        res = requests.post(f"{BACKEND_URL}/scan_all")
        if res.status_code == 200:
            st.success("All mails scanned")
            st.rerun()
        else:
            st.error("Scan all failed")

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# Fetch inbox
res = requests.get(f"{BACKEND_URL}/inbox")

if res.status_code != 200:
    st.error("Failed to load inbox")
    st.stop()

mails = res.json()

if not mails:
    st.info("Inbox is empty.")
    st.stop()

for mail in mails:
    st.divider()

    st.subheader(f"From: {mail['sender']} → To: {mail['receiver']}")
    st.write(f"**Subject:** {mail['subject']}")
    st.write(f"**Message:** {mail['body']}")

    # Prediction (color-coded)
    prediction = mail.get("prediction", "Not Scanned")

    if "Phishing" in prediction:
        st.error(f"🚨 Prediction: {prediction}")
    elif "Safe" in prediction:
        st.success(f"✅ Prediction: {prediction}")
    else:
        st.warning(f"⚠️ Prediction: {prediction}")

    # Action buttons
    c1, c2 = st.columns(2)

    with c1:
        if st.button("🔍 Scan", key=f"scan_{mail['id']}"):
            res = requests.post(f"{BACKEND_URL}/scan/{mail['id']}")
            if res.status_code == 200:
                st.success("Mail scanned")
                st.rerun()
            else:
                st.error("Scan failed")

    with c2:
        if st.button("🗑️ Delete", key=f"del_{mail['id']}"):
            res = requests.delete(f"{BACKEND_URL}/mail/{mail['id']}")
            if res.status_code == 200:
                st.success("Mail deleted")
                st.rerun()
            else:
                st.error("Delete failed")
