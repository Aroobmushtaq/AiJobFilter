import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="View Applicants", layout="centered")
st.title("📋 View Applicants")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def ai_score(resume, job):
    job_prompt = f"""
    Job Title: {job['job_title']}
    Required Skills: {', '.join(job['skills'])}
    Experience: {job['experience']} years
    Education: {job['education']}
    """
    r_embed = model.encode(resume, convert_to_tensor=True)
    j_embed = model.encode(job_prompt, convert_to_tensor=True)
    return util.pytorch_cos_sim(r_embed, j_embed).item()

if "jobs" not in st.session_state or "applications" not in st.session_state:
    st.warning("No jobs or applications found.")
    st.stop()

job_id = st.text_input("Enter your Job Code")

if job_id and job_id in st.session_state.jobs:
    job = st.session_state.jobs[job_id]
    applicants = st.session_state.applications.get(job_id, [])

    st.subheader(f"👥 Applicants for: {job['job_title']}")

    if not applicants:
        st.info("No applicants yet.")
    else:
        for app in applicants:
            score = ai_score(app['resume'], job)
            st.markdown(f"""
            ---
            **Name:** {app['name']}  
            **Email:** {app['email']}  
            **AI Score:** `{score:.2f}`
            """)
            if score > 0.7:
                st.success("✅ Suitable for Interview")
            elif score > 0.4:
                st.warning("⚠ May Need Manual Review")
            else:
                st.error("❌ Not Suitable")
else:
    if job_id:
        st.error("❌ Invalid Job Code")
