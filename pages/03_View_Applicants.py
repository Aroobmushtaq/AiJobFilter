import streamlit as st
import os
import requests

# ✅ Groq API Key (same as Apply page)
GROQ_API_KEY = "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"

# ✅ Get job details
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

# ✅ AI Evaluation (same logic as apply)
def evaluate_with_ai(job, cv_text):
    prompt = f"""
You are an AI recruiter assistant. Evaluate the applicant's resume against this job:
Job Title: {job['title']}
Description: {job['description']}
Required Skills: {job['skills']}
Required Education: {job['education']}
Resume:
{cv_text}

Return a short assessment of match, skills fit, education fit, and whether a human should manually review it.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert hiring assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content']
        except KeyError:
            return f"❌ AI evaluation failed: Missing 'choices' in response"
    else:
        return f"❌ AI evaluation failed: {response.text}"

# ✅ Streamlit UI
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
                parts = applicant.split("|||")
                if len(parts) == 2:
                    cv_text, ai_result = parts
                else:
                    cv_text = parts[0]
                    ai_result = evaluate_with_ai(job, cv_text)  # fallback

                st.markdown(f"### 👤 Applicant {i}")
                with st.expander("📄 View CV"):
                    st.text(cv_text.strip())

                st.markdown("**🤖 AI Evaluation:**")
                st.code(ai_result.strip())
                st.markdown("---")
