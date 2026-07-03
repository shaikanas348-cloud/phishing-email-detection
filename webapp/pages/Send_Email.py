import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Send Email")

sender = st.text_input("Sender Email")
receiver = st.text_input("Receiver Email")
subject = st.text_input("Subject")
body = st.text_area("Message")

if st.button("Send"):
    if not sender or not receiver or not subject or not body:
        st.error("All fields are required")
    else:
        data = {
            "sender": sender,
            "receiver": receiver,
            "subject": subject,
            "body": body
        }

        res = requests.post(f"{BACKEND_URL}/send_mail", json=data)

        if res.status_code == 200:
            st.success("Mail sent successfully!")
        else:
            st.error(f"Failed to send mail (Error {res.status_code})")
            st.write(res.json())  # DEBUG: shows exact backend error
