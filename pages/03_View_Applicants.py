import streamlit as st
import requests
import os

st.set_page_config(page_title="View Applicants", layout="centered")
st.title("📋 View Applicants")

# Set your Groq API key securely
GROQ_API_KEY = os.getenv("groqApiKey") or "your_groq_api_key_here"
MODEL = "mixtral-8x7b-32768"  # or use "llama3-8b-8192"

def evaluate_resume_with_ai(resume, job):
    prompt = f"""
You are an expert recruiter. Evaluate the following resume against the job description.
Return a JSON with:
- 'summary': 2–4 line review (strengths, missing info)
- 'verdict': 'suitable', 'maybe', or 'not suitable'

Job:
Title: {job['job_title']}
Skills: {', '.join(job['skills'])}
Experience: {job['experience']} years
Education: {job['education']}

Resume:
{resume}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4
        },
        headers=headers,
        timeout=20
    )

    result = response.json()
    message = result['choices'][0]['message']['content']
    return message

# Check for session state
if "jobs" not in st.session_state or "applications" not in st.session_state:
    st.warning("No jobs or applications found.")
    st.stop()

# Input job code
job_id = st.text_input("Enter your Job Code")

# Main logic
if job_id and job_id in st.session_state.jobs:
    job = st.session_state.jobs[job_id]
    applicants = st.session_state.applications.get(job_id, [])

    st.subheader(f"👥 Applicants for: {job['job_title']}")

    if not applicants:
        st.info("No applicants yet.")
    else:
        for app in applicants:
            with st.spinner(f"Analyzing {app['name']}'s resume..."):
                try:
                    analysis = evaluate_resume_with_ai(app['resume'], job)
                    st.markdown(f"""
---
**Name:** {app['name']}  
**Email:** {app['email']}  
**AI Feedback:**  
{analysis}
""")
                except Exception as e:
                    st.error(f"❌ AI evaluation failed: {e}")
else:
    if job_id:
        st.error("❌ Invalid Job Code")
