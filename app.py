import streamlit as st
from PyPDF2 import PdfReader
from ibm_watsonx_ai.foundation_models import ModelInference
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# UI SETUP
st.set_page_config(page_title="HATI AI | Technical Drift Auditor", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stAlert { border-left: 5px solid #0062ff; }
.stButton>button { 
    background-color: #0062ff; 
    color: white; 
    border-radius: 8px; 
    font-weight: bold; 
}
</style>
""", unsafe_allow_html=True)

# CREDENTIALS
DEFAULT_API_KEY = os.getenv("IBM_API_KEY", "")
DEFAULT_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

with st.sidebar:
    st.title("🛡️ HATI Secure Control")
    api_key = st.text_input("IBM Watson API Key", value=DEFAULT_API_KEY, type="password")
    project_id = st.text_input("IBM Project ID", value=DEFAULT_PROJECT_ID)
    st.info("Rotate keys regularly for security.")

# FILE PROCESSING
def extract_text(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        return " ".join([page.extract_text() for page in pdf.pages])
    return str(file.read(), "utf-8")

# AI AUDIT ENGINE
def run_audit(spec, impl, api_key, project_id):
    try:
        credentials = {"url": IBM_URL, "apikey": api_key}
        
        model = ModelInference(
            model_id=os.getenv("MODEL_ID", "ibm/granite-13b-instruct-v2"),
            params={
                "decoding_method": "greedy",
                "max_new_tokens": int(os.getenv("MAX_TOKENS", "1000")),
                "temperature": 0.2
            },
            credentials=credentials,
            project_id=project_id
        )
        
        prompt = f"""[Role: Senior Cybersecurity Auditor]
Analyze the difference between the Requirement and the Reality for Technical Drift.

REQUIREMENT SPECIFICATION:
{spec[:2000]}

ACTUAL IMPLEMENTATION:
{impl[:2000]}

Provide:
1. List of Security Gaps
2. Compliance Status (Pass/Fail)
3. Critical Remediation Steps"""
        
        return model.generate_text(prompt=prompt)
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease verify your IBM Watson credentials and project ID are correct."

# DASHBOARD
st.title("🛡️ HATI AI - Agentic Technical Drift Auditor")
st.write("Upload technical documents to verify compliance and detect security drift.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Reference Specification")
    spec_file = st.file_uploader("Upload Original Spec", type=['pdf', 'txt'], key="spec")

with col2:
    st.subheader("📋 Current Implementation")
    impl_file = st.file_uploader("Upload Implementation Doc", type=['pdf', 'txt'], key="impl")

if st.button("🚀 EXECUTE AUDIT", use_container_width=True):
    if not api_key or not project_id:
        st.error("⚠️ Missing IBM Watson credentials!")
    elif not spec_file or not impl_file:
        st.error("⚠️ Please upload both documents!")
    else:
        with st.spinner("🔍 HATI AI is analyzing for technical drift..."):
            spec_text = extract_text(spec_file)
            impl_text = extract_text(impl_file)
            results = run_audit(spec_text, impl_text, api_key, project_id)
            
            st.success("✅ Audit Complete!")
            st.markdown("### 📊 Audit Findings")
            st.markdown(results)

# Made with Bob
