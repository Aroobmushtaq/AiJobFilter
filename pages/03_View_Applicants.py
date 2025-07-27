import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="View Applicants", layout="centered")
st.title("📋 View Applicants")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Feedback generator
def generate_feedback(resume, job):
    positives = []
    negatives = []

    resume_lower = resume.lower()

    # Skill check
    for skill in job['skills']:
        if skill.lower() in resume_lower:
            positives.append(f"Has experience with **{skill}**.")
        else:
            negatives.append(f"Missing experience in **{skill}**.")

    # Education check
    if job['education'].lower() in resume_lower:
        positives.append(f"Meets education requirement (**{job['education']}**).")
    else:
        negatives.append(f"Does not clearly mention required education (**{job['education']}**).")

    # Experience check (only if experience > 0)
    if job['experience'] > 0:
        if str(job['experience']) in resume_lower:
            positives.append(f"Mentions **{job['experience']} years** of experience.")
        else:
            negatives.append(f"No clear mention of **{job['experience']} years** experience.")

    return positives, negatives

# Similarity scoring
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

# Session check
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

            st.markdown("---")
            st.markdown(f"**👤 Name:** {app['name']}  \n**📧 Email:** {app['email']}  \n**🤖 AI Match Score:** `{score:.2f}`")

            # Match evaluation
            if score >= 0.75:
                st.success("✅ Strong Fit: This applicant is highly suitable for interview.")
                st.markdown("### ✅ Matched Points")
                for pos in positives:
                    st.markdown(f"- {pos}")

                if negatives:
                    st.markdown("### ⚠️ Double Check")
                    for neg in negatives:
                        st.markdown(f"- {neg}")

                st.markdown(f"""
                ---
                📩 **Contact Applicant**  
                👉 [Click to Email {app['email']}](mailto:{app['email']})
                """)

            elif 0.5 <= score < 0.75:
                st.warning("⚠ Partial Match: May require manual review.")
                st.markdown("### ✅ Matching Elements")
                for pos in positives:
                    st.markdown(f"- {pos}")
                st.markdown("### ❌ Missing Elements")
                for neg in negatives:
                    st.markdown(f"- {neg}")
                st.info("🧠 AI suggests: *Review the resume manually to make a final decision.*")

            else:
                st.error("❌ Not a Fit: This resume does not align well with job requirements.")
                st.markdown("### ❌ Key Mismatches")
                for neg in negatives:
                    st.markdown(f"- {neg}")
                st.caption("🔒 Contact option hidden as the candidate doesn't meet the baseline.")

else:
    if job_id:
        st.error("❌ Invalid Job Code")
