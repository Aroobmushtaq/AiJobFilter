import streamlit as st
import uuid

st.title("📝 Post a Job")

job_title = st.text_input("Job Title")
job_description = st.text_area("Job Description")
required_skills = st.text_area("Required Skills (comma-separated)")
education = st.text_input("Required Education")

if st.button("Post Job"):
    job_code = str(uuid.uuid4())[:8]
    with open("job_data.txt", "a") as f:
        f.write(f"{job_code}|{job_title}|{job_description}|{required_skills}|{education}\n")
    st.success(f"✅ Job Posted Successfully!\n🔑 Your Job Code: `{job_code}`")
