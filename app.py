import streamlit as st

st.set_page_config(page_title="AI Job Filter", layout="centered")
st.title("💼 AI-Powered Job Filter System")

st.markdown("""
<style>
.big-title { font-size:28px; font-weight:bold; margin-top:20px; color:#4a90e2; }
.desc-text { font-size:18px; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Welcome to the AI Job Filter System 🚀</div>', unsafe_allow_html=True)

st.markdown("""
<div class="desc-text">
👩‍💼 <b>Recruiters</b> can:
<ul>
  <li>Post jobs</li>
  <li>Receive a unique <code>Job Code</code></li>
  <li>View applicants for their job only</li>
</ul>
</div>

<div class="desc-text">
🧑‍🎓 <b>Applicants</b> can:
<ul>
  <li>Use a <code>Job Code</code> to apply</li>
  <li>Upload their resume</li>
  <li>Get AI-based feedback on their eligibility</li>
</ul>
</div>
""", unsafe_allow_html=True)
