import streamlit as st
import os
import requests


GROQ_API_KEY = "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"

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
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an expert hiring assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ AI evaluation failed: {response.text}"

def get_job_details(code):
    if not os.path.exists("job_data.txt"):
        return None
    with open("job_data.txt", "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if parts[0] == code:
                return {"code": parts[0], "title": parts[1], "description": parts[2], "skills": parts[3], "education": parts[4]}
    return None

st.title("📄 Apply for a Job")

job_code = st.text_input("Enter Job Code")
cv = st.text_area("Paste your Resume / CV text")

if st.button("Submit Application"):
    job = get_job_details(job_code)
    if not job:
        st.error("❌ Invalid Job Code")
    else:
        ai_result = evaluate_with_ai(job, cv)
        with open(f"{job_code}_applicants.txt", "a") as f:
            f.write(f"{cv}|||{ai_result}\n")
        st.success("✅ Application submitted!")
        st.markdown("### 🤖 AI Evaluation:")
        st.info(ai_result)
