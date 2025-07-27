import streamlit as st
import os
from PyPDF2 import PdfReader
import docx

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    elif uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ]:
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None

# Get job details from file
def get_job_details(code):
    if not os.path.exists("job_data.txt"):
        return None
    with open("job_data.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) < 5:
                continue  # ✅ Skip lines that don't have all required fields
            if parts[0] == code:
                return {
                    "code": parts[0],
                    "title": parts[1],
                    "description": parts[2],
                    "skills": parts[3],
                    "education": parts[4]
                }
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
            if not cv_text or cv_text.strip() == "":
                st.error("❌ Could not extract text from uploaded file.")
            else:
                # Save only the raw CV text, no AI result here
                with open(f"{job_code}_applicants.txt", "a", encoding="utf-8") as f:
                    f.write(f"{cv_text}|||PENDING\n")  # placeholder
                st.success("✅ Application submitted successfully!")
