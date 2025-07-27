import streamlit as st

st.set_page_config(page_title="AI Job Filter", layout="centered")
st.title("💼 AI-Powered Job Filter System")
st.markdown("""
Welcome to the **AI Job Filter System**!

🔹 Recruiters can:
- Post a job
- Get a **Job Code**
- View applicants only for their job

🔹 Applicants can:
- Apply using a **Job Code**
- Upload their CV

🔍 An AI model will analyze their resume and give eligibility feedback.
""")
