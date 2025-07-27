import streamlit as st

st.set_page_config(page_title="AI Job Filter | Post Job", layout="centered")
st.title("📄 Post Job Requirements")

# Initialize session state
if 'job_data' not in st.session_state:
    st.session_state.job_data = {}

with st.form("job_form"):
    job_title = st.text_input("Job Title", placeholder="e.g. Frontend Developer")
    required_skills = st.text_input("Required Skills (comma-separated)", placeholder="e.g. HTML, CSS, React")
    min_experience = st.number_input("Minimum Years of Experience", min_value=0, step=1)
    education_level = st.selectbox("Required Education Level", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])

    submitted = st.form_submit_button("Save Job Requirements")
    if submitted:
        st.session_state.job_data = {
            "job_title": job_title.strip(),
            "skills": [skill.strip().lower() for skill in required_skills.split(",") if skill.strip()],
            "experience": min_experience,
            "education": education_level.lower()
        }
        st.success("✅ Job requirements saved successfully!")