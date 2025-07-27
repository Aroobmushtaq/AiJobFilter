import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="AI Job Filter | Submit CV", layout="centered")
st.title("🧑‍💼 Submit Your Application")

# 🔄 Load job data
if 'job_data' not in st.session_state or not st.session_state.job_data:
    st.warning("⚠️ Please post job requirements first on the main page.")
    st.stop()

job_data = st.session_state.job_data

# 🧠 Load AI model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# 🧠 Simulate AI evaluation using sentence embeddings
def simulate_ai_with_embeddings(resume_text, job_data):
    job_prompt = f"""
    Job Title: {job_data['job_title']}
    Required Skills: {', '.join(job_data['skills'])}
    Minimum Experience: {job_data['experience']} years
    Education Level: {job_data['education']}
    """

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_prompt, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()

    if similarity > 0.7:
        return "Suitable", similarity
    elif similarity > 0.4:
        return "Partially Suitable", similarity
    else:
        return "Not Suitable", similarity

# 🧾 Candidate Form
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
        st.text_area("Extracted Resume Text", resume_text, height=250)

        # 🧠 AI evaluation
        result, score = simulate_ai_with_embeddings(resume_text, job_data)
        st.markdown(f"**🔍 AI Similarity Score:** `{score:.2f}`")

        if result == "Suitable":
            st.success("✅ Candidate is Suitable based on AI evaluation.")
        elif result == "Partially Suitable":
            st.warning("⚠ Candidate is Partially Suitable based on AI evaluation.")
        else:
            st.error("❌ Candidate is Not Suitable.")
