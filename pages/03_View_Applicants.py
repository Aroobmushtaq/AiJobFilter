import streamlit as st
import os

st.title("🔍 View Applicants")

job_code = st.text_input("Enter Your Job Code")

if st.button("View Applicants"):
    file_path = f"{job_code}_applicants.txt"
    if os.path.exists(file_path):
        st.subheader(f"👥 Applicants for: {job_code}")
        with open(file_path, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                parts = line.split("|||")
                resume = parts[0]
                feedback = parts[1] if len(parts) > 1 else "⚠ No AI feedback"
                st.markdown(f"---\n### Applicant #{i}\n📄 **Resume:**\n{resume}\n\n💬 **AI Feedback:**\n{feedback}")
    else:
        st.warning("⚠ No applicants found for this Job Code.")
