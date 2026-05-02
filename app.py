import streamlit as st
from PyPDF2 import PdfReader
from ibm_watsonx_ai.foundation_models import Model
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#UI SETUP
st.set_page_config(page_title="Hati AI | Auditor",layout="wide" )

#Custom CSS for professional Branding
st.markdown("""
<style>
.stAlert{border-left:5px}
.stAlert { border-left: 5px solid #0062ff; }
    .stButton>button { background-color: #0062ff; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SECURITY LAYER (Credential Management) ---
# Load credentials from environment variables
DEFAULT_API_KEY = os.getenv("IBM_API_KEY", "")
DEFAULT_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

with st.sidebar:
    st.title("🛡️ HatiSecure Control")
    api_key = st.text_input("IBM Watson API Key", value=DEFAULT_API_KEY, type="password", help="Enter your IBM Watson API key")
    project_id = st.text_input("IBM Project ID", value=DEFAULT_PROJECT_ID, help="Enter your IBM Watson project ID")
    st.info("As the auditor, ensure your keys are rotated regularly.")

# --- 3. THE FILE PROCESSING ENGINE ---
def get_text_from_file(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        return " ".join([page.extract_text() for page in pdf.pages])
    return str(file.read(), "utf-8")

# --- 4. THE AI AUDIT ENGINE (The Heart of Hati AI) ---
def run_audit(spec, impl, api_key, project_id):
    """
    Runs an AI-powered audit comparing specification against implementation.
    
    Args:
        spec: Original specification text
        impl: Current implementation text
        api_key: IBM Watson API key
        project_id: IBM Watson project ID
    
    Returns:
        Audit results as text
    """
    credentials = {
        "url": IBM_URL,
        "apikey": api_key  # Fixed: was using the actual key value as parameter name
    }
    
    model = Model(
        model_id=os.getenv("MODEL_ID", "ibm/granite-13b-instruct-v2"),
        params={
            "decoding_method": "greedy",
            "max_new_tokens": int(os.getenv("MAX_TOKENS", "1000"))
        },
        credentials=credentials,
        project_id=project_id
    )
    
    prompt = f"""[System: Cybersecurity Auditor]
    Compare the following technical documents for 'Technical Drift'.
    Requirement: {spec}
    Actual: {impl}
    
    Identify critical security gaps and implementation failures."""
    
    return model.generate_text(prompt=prompt)

# --- 5. THE DASHBOARD ---
st.title("Agentic Technical Drift Auditor")
st.write("Upload your technical docs to verify compliance.")

c1, c2 = st.columns(2)
with c1:
    spec_file = st.file_uploader("Upload Original Spec (PDF)", type=['pdf'])
with c2:
    impl_file = st.file_uploader("Upload Current Implementation (PDF)", type=['pdf'])

if st.button("EXECUTE AUDIT"):
    if api_key and project_id and spec_file and impl_file:
        with st.spinner("Hati AI is analyzing..."):
            s_text = get_text_from_file(spec_file)
            i_text = get_text_from_file(impl_file)
            results = run_audit(s_text, i_text, api_key, project_id)
            st.markdown("### 📊 Audit Findings")
            st.write(results)
    else:
        st.error("Missing Credentials or Files!")









