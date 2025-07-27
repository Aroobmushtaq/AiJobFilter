import streamlit as st
import os
from groq import Groq

# ✅ Manually set your API key here
client = Groq(api_key="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")

# Get job details
def get_job_details(code):
    if not os.path.exists("job_data.txt"):
        return None
    with open("job_data.txt", "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if parts[0] == code:
                return {
                    "code": parts[0],
                    "title": parts[1],
                    "description": parts[2],
                    "skills": parts[3],
                    "education": parts[4]
                }
    return None

# AI evaluation using Groq
def evaluate_cv_with_ai(cv_text, job_description, job_skills, job_education):
    prompt = f"""
You are an AI recruiter. A job is posted with the following details:

Job Description:
{job_description}

Required Skills:
{job_skills}

Required Education:
{job_education}

Now, a candidate has submitted the following CV:
{cv_text}

Evaluate the CV and provide a score out of 100 based on how well the candidate matches the job. Also give a short summary of the candidate's strengths or weaknesses.
Respond in this format:
Score: <score>/100
Summary: <short summary>
    """
    try:
        response = client.chat.completions.create(
            model="gemma-7b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("👀 View Applications")

job_code = st.text_input("Enter Job Code")

if job_code and st.button("View Applications"):
    job = get_job_details(job_code)
    if not job:
        st.error("❌ Job not found")
    else:
        file_path = f"{job_code}_applicants.txt"
        if not os.path.exists(file_path):
            st.info("ℹ️ No applicants yet.")
        else:
            st.subheader(f"📄 Applicants for Job: {job['title']}")
            with open(file_path, "r", encoding="utf-8") as f:
                applicants = f.readlines()

            for i, applicant in enumerate(applicants, start=1):
                cv_text, _ = applicant.split("|||")
                st.markdown(f"### Applicant {i}")
                with st.expander("📜 View CV"):
                    st.text(cv_text.strip())

                with st.spinner("🧠 Evaluating with AI..."):
                    result = evaluate_cv_with_ai(
                        cv_text,
                        job["description"],
                        job["skills"],
                        job["education"]
                    )
                st.success("✅ AI Evaluation:")
                st.code(result, language="text")
                st.markdown("---")
