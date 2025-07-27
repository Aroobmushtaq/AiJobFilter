import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="View Applicants", layout="centered")
st.title("📋 View Applicants")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Helper to generate a feedback paragraph
def generate_feedback(resume, job):
    positives = []
    negatives = []

    resume_lower = resume.lower()

    # Skill matching
    for skill in job['skills']:
        if skill.lower() in resume_lower:
            positives.append(f"Has experience with **{skill}**")
        else:
            negatives.append(f"Missing experience in **{skill}**")

    # Education match
    if job['education'].lower() in resume_lower:
        positives.append(f"Meets education requirement (**{job['education']}**)")

    else:
        negatives.append(f"Does not clearly mention required education (**{job['education']}**)")

    # Experience match (just rough mention of years)
    if str(job['experience']) in resume_lower:
        positives.append(f"Mentions **{job['experience']} years** of experience")
    else:
        negatives.append(f"No clear mention of **{job['experience']} years** experience")

    return positives, negatives

# AI similarity score
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

# Session state check
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
            positives, negatives = generate_feedback(app['resume'], job)

            st.markdown(f"""---  
            **👤 Name:** {app['name']}  
            **📧 Email:** {app['email']}  
            **🤖 AI Score:** `{score:.2f}`  
            """)

            if score > 0.7:
                st.success("✅ This applicant is a strong match for the job.")

                st.markdown("### 🔍 Positive Points")
                for pos in positives:
                    st.markdown(f"- ✅ {pos}")

                if negatives:
                    st.markdown("### ⚠️ Areas to Double-Check")
                    for neg in negatives:
                        st.markdown(f"- ⚠️ {neg}")

                st.markdown(f"""  
                ---  
                📩 **Contact Applicant**  
                [Send Email to {app['email']}](mailto:{app['email']})  
                """)

            elif score > 0.4:
                st.warning("⚠ This application may need manual review.")

                st.markdown("### ✅ Matching Points")
                for pos in positives:
                    st.markdown(f"- ✅ {pos}")

                st.markdown("### ❌ Not Matching / Missing Info")
                for neg in negatives:
                    st.markdown(f"- ❌ {neg}")

                st.info("You may want to review the CV manually for a better decision.")

            else:
                st.error("❌ This applicant does not meet the basic requirements.")

                st.markdown("### ❌ Gaps Found")
                for neg in negatives:
                    st.markdown(f"- ❌ {neg}")

                st.caption("Not recommended for interview at this stage.")

else:
    if job_id:
        st.error("❌ Invalid Job Code")
