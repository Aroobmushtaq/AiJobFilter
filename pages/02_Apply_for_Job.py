import streamlit as st
import os
import requests
from PyPDF2 import PdfReader
import docx

GROQ_API_KEY = "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"

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return None

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
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an expert hiring assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content']
        except KeyError:
            return f"❌ AI evaluation failed: Missing 'choices' in response"
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

# Streamlit UI
st.title("📄 Apply for a Job")

job_code = st.text_input("Enter Job Code")
uploaded_cv = st.file_uploader("Upload your Resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

if st.button("Submit Application"):
    if not uploaded_cv:
        st.error("❌ Please upload a CV file.")
    else:
        job = get_job_details(job_code)
        if not job:
            st.error("❌ Invalid Job Code")
        else:
            cv_text = extract_text_from_file(uploaded_cv)
            if not cv_text:
                st.error("❌ Could not extract text from uploaded file.")
            else:
                ai_result = evaluate_with_ai(job, cv_text)
                with open(f"{job_code}_applicants.txt", "a", encoding="utf-8") as f:
                    f.write(f"{cv_text}|||{ai_result}\n")
                st.success("✅ Application submitted!")
                st.markdown("### 🤖 AI Evaluation:")
                st.info(ai_result)
