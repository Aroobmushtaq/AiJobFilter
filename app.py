import streamlit as st

# Page Configuration
st.set_page_config(page_title="AI Job Filter System", page_icon="💼", layout="centered")

# Title and Subtitle
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>💼 AI-Powered Job Filter System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Your smart assistant for job matching & resume evaluation</h4>", unsafe_allow_html=True)
st.markdown("---")

# Intro Section
st.markdown("""
### 👋 Welcome!

This platform connects **Job Providers** and **Job Seekers** through smart AI-powered matching. Whether you're hiring or applying, our system ensures efficient and intelligent screening.

""")

# Recruiter Instructions
st.markdown("""
#### 🧑‍💼 For Recruiters:
- 📝 **Post a Job** with complete requirements
- 🎯 Get a **Unique Job Code** for each job
- 👀 View only the candidates who applied to your job
- 🤖 Let AI analyze applicant resumes against your requirements
""")

# Applicant Instructions
st.markdown("""
#### 🧑‍🎓 For Applicants:
- 🔍 Use the **Job Code** to find relevant job posts
- 📤 **Upload your CV** or resume in PDF format
- 💡 Receive **AI-generated feedback** on your job match
- 📊 See a percentage-based **fit score** to help you understand your suitability
""")

# Benefits
st.markdown("""
#### 🌟 Why Use This App?
- ✅ Saves time for recruiters by **automating resume screening**
- ✅ Helps applicants understand how well they match a job
- ✅ Powered by **AI models** to analyze resume content and job descriptions
""")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>Made with ❤️ using Streamlit & Hugging Face Transformers</p>", unsafe_allow_html=True)
