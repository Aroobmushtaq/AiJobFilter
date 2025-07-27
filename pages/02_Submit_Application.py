import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI Job Filter | Submit CV", layout="centered")
st.title("🧑‍💼 Submit Your Application")

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
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        st.subheader("📄 CV Preview:")
        st.text_area("Extracted Resume Text", text, height=200)

        # ---- Dummy AI Logic (Simple String Matching) ----
        matched_skills = [skill for skill in job_data['skills'] if skill in text.lower()]
        missing_skills = list(set(job_data['skills']) - set(matched_skills))

        experience_pass = str(job_data['experience']) in text or f"{job_data['experience']}+" in text
        education_pass = job_data['education'] in text.lower()

        # --- Determine Result ---
        if matched_skills == job_data['skills'] and experience_pass and education_pass:
            st.success("✅ Suitable Candidate!")
        elif matched_skills or experience_pass or education_pass:
            st.warning("⚠ Partially Suitable Candidate")
            st.markdown("**Missing Criteria:**")
            if missing_skills:
                st.markdown(f"- Skills: `{', '.join(missing_skills)}`")
            if not experience_pass:
                st.markdown(f"- Experience: `{job_data['experience']}+ years` not found.")
            if not education_pass:
                st.markdown(f"- Education: `{job_data['education'].capitalize()}` not matched.")
        else:
            st.error("❌ Not Suitable Candidate")
