import streamlit as st
import uuid

st.set_page_config(page_title="Post Job", layout="centered")
st.title("📝 Post a Job")

if "jobs" not in st.session_state:
    st.session_state.jobs = {}
if "applications" not in st.session_state:
    st.session_state.applications = {}

with st.form("post_job_form"):
    recruiter_name = st.text_input("Your Name")
    job_title = st.text_input("Job Title")
    required_skills = st.text_input("Required Skills (comma-separated)")
    experience = st.number_input("Minimum Years of Experience", 0)
    education = st.selectbox("Education Level", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])
    submit = st.form_submit_button("Create Job")

    if submit:
        job_id = str(uuid.uuid4())[:8]  # simple job code
        st.session_state.jobs[job_id] = {
            "recruiter": recruiter_name,
            "job_title": job_title,
            "skills": [s.strip().lower() for s in required_skills.split(",")],
            "experience": experience,
            "education": education.lower()
        }
        st.success(f"✅ Job posted successfully!")
        st.code(f"Your Job Code: {job_id}", language='text')
