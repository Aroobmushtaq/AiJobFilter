import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI Job Filter | Submit CV", layout="centered")
st.title("🧑‍💼 Submit Your Application")

# -------------------------------
# 🧠 Simulated Groq AI function
# -------------------------------
def simulate_groq_ai_evaluation(resume_text, job_data):
    text = resume_text.lower()

    matched_skills = [skill for skill in job_data['skills'] if skill in text]
    missing_skills = list(set(job_data['skills']) - set(matched_skills))

    experience_pass = str(job_data['experience']) in text or f"{job_data['experience']}+" in text
    education_pass = job_data['education'] in text

    score = 0
    if matched_skills:
        score += 1
    if experience_pass:
        score += 1
    if education_pass:
        score += 1

    if score == 3:
        return "Suitable", []
    elif score >= 1:
        missing = []
        if missing_skills:
            missing.append(f"Skills: {', '.join(missing_skills)}")
        if not experience_pass:
            missing.append(f"Experience: {job_data['experience']}+ years not found")
        if not education_pass:
            missing.append(f"Education: {job_data['education'].capitalize()} not matched")
        return "Partially Suitable", missing
    else:
        return "Not Suitable", []

# -------------------------------
# 🔄 Page logic
# -------------------------------
if 'job_data' not in st.session_state or not st.session_state.job_data:
    st.warning("⚠️ Please post job requirements first on the main page.")
    st.stop()

job_data = st.session_state.job_data

# --- Candidate Form ---
with st.form("candidate_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    uploaded_file = st.file_uploader("Upload CV (PDF only)", type=["pdf"])
    submitted = st.form_submit_button("Submit Application")

if submitted:
    if not uploaded_file:
        st.error("❌ Please upload a valid PDF file.")
    else:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        st.subheader("📄 CV Preview:")
        st.text_area("Extracted Resume Text", resume_text, height=200)

        # 🧠 Simulate Groq AI logic
        result, missing_info = simulate_groq_ai_evaluation(resume_text, job_data)

        if result == "Suitable":
            st.success("✅ Candidate is Suitable for this job.")
        elif result == "Partially Suitable":
            st.warning("⚠ Candidate is Partially Suitable.")
            st.markdown("**Missing Elements:**")
            for item in missing_info:
                st.markdown(f"- {item}")
        else:
            st.error("❌ Candidate is Not Suitable.")
