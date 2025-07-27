import streamlit as st
import pdfplumber

st.set_page_config(page_title="Apply for Job", layout="centered")
st.title("📤 Apply for a Job")

if "jobs" not in st.session_state or not st.session_state.jobs:
    st.warning("No jobs found. Please ask recruiter to post a job.")
    st.stop()

if "applications" not in st.session_state:
    st.session_state.applications = {}

with st.form("apply_form"):
    job_id = st.text_input("Enter Job Code")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    submitted = st.form_submit_button("Submit Application")

    if submitted:
        if job_id not in st.session_state.jobs:
            st.error("❌ Invalid Job Code.")
        elif not file:
            st.error("❌ Please upload a PDF file.")
        else:
            with pdfplumber.open(file) as pdf:
                resume_text = "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())

            if job_id not in st.session_state.applications:
                st.session_state.applications[job_id] = []

            st.session_state.applications[job_id].append({
                "name": name,
                "email": email,
                "resume": resume_text
            })

            st.success("✅ Application submitted successfully!")
