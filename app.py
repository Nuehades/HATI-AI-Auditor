import streamlit as st
from PyPDF2 import PdfReader
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
USE_DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

with st.sidebar:
    st.title("🛡️ HATI Secure Control")
    
    if USE_DEMO_MODE:
        st.warning("⚠️ Running in DEMO MODE")
        st.info("Set DEMO_MODE=false in .env to use IBM Watson")
    
    api_key = st.text_input("IBM Watson API Key", value=DEFAULT_API_KEY, type="password")
    project_id = st.text_input("IBM Project ID", value=DEFAULT_PROJECT_ID)
    st.info("Rotate keys regularly for security.")

# FILE PROCESSING
def extract_text(file):
    try:
        if file.type == "application/pdf":
            pdf = PdfReader(file)
            return " ".join([page.extract_text() for page in pdf.pages])
        return str(file.read(), "utf-8")
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# DEMO AUDIT (for testing without IBM Watson)
def demo_audit(spec, impl):
    return f"""### 🔍 Technical Drift Analysis (DEMO MODE)

**Specification Summary:**
- Length: {len(spec)} characters
- First 200 chars: {spec[:200]}...

**Implementation Summary:**
- Length: {len(impl)} characters  
- First 200 chars: {impl[:200]}...

**Detected Issues:**
1. ⚠️ Potential configuration drift detected
2. ⚠️ Security parameter mismatch found
3. ⚠️ Version inconsistency identified

**Compliance Status:** ⚠️ REVIEW REQUIRED

**Recommendations:**
1. Verify authentication mechanisms match specification
2. Review encryption settings
3. Update documentation to reflect current state

*Note: This is DEMO output. Connect IBM Watson for real AI analysis.*
"""

# AI AUDIT ENGINE
def run_audit(spec, impl, api_key, project_id):
    if USE_DEMO_MODE or not api_key or not project_id:
        return demo_audit(spec, impl)
    
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        
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
        st.error(f"IBM Watson Error: {str(e)}")
        st.info("Falling back to DEMO mode...")
        return demo_audit(spec, impl)

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
    if not spec_file or not impl_file:
        st.error("⚠️ Please upload both documents!")
    else:
        with st.spinner("🔍 HATI AI is analyzing for technical drift..."):
            spec_text = extract_text(spec_file)
            impl_text = extract_text(impl_file)
            
            if "Error" in spec_text or "Error" in impl_text:
                st.error("Failed to extract text from files. Please check file format.")
            else:
                results = run_audit(spec_text, impl_text, api_key, project_id)
                
                st.success("✅ Audit Complete!")
                st.markdown("### 📊 Audit Findings")
                st.markdown(results)

# Made with Bob
