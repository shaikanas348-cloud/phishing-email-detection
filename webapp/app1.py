import streamlit as st

# Page config
st.set_page_config(
    page_title="Phishing Detection System",
    page_icon="📧",
    layout="centered"
)

# Hero section
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>
        📧 Phishing Detection Mail System
    </h1>
    <h4 style='text-align: center; color: gray;'>
        Detect malicious and phishing emails
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

# Description box
st.info(
    """
    🔐 **This system helps you identify phishing emails.**  

    - 📤 Send emails through the system  
    - 📥 View inbox securely  
    - 🧠 Detect phishing using ML models and NLP 
    - 🚨 Get instant alerts for suspicious content  
    """
)

st.write("")

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.success("📤 Send Mail")
    st.write(
        """
        - Compose an email  
        - Submit it to the system  
        - Automatically scanned for phishing  
        """
    )

with col2:
    st.warning("📥 Inbox")
    st.write(
        """
        - View received emails  
        - See phishing predictions  
        - Delete messages  
        """
    )

with col3:
    st.error("🚨 Phishing Detection")
    st.write(
        """
        - ML-based analysis  
        - Real-time scanning  
        """
    )

st.write("")
st.write("")

# Call to action
st.markdown(
    """
    <h3 style='text-align: center;'>
        👉 Get started
    </h3>
    """,
    unsafe_allow_html=True
)

st.caption(
    "   Mini project | Streamlit + FastAPI + ML + NLP"
)
