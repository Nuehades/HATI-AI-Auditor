import streamlit as st
from PyPDF2 import PdfReader # Tool to read PDFs
from engine import run_hati_audit

# --- FUNCTION TO EXTRACT TEXT ---
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        # If it's a plain text file
        return str(uploaded_file.read(), "utf-8")

# --- UI SECTION ---
st.title("🛡️ Hati AI Auditor")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Reference Spec")
    spec_file = st.file_uploader("Upload Original Specification (PDF/TXT)", type=["pdf", "txt"])

with col2:
    st.subheader("Implementation Doc")
    impl_file = st.file_uploader("Upload System Logs/Docs (PDF/TXT)", type=["pdf", "txt"])

if st.button("🚀 Start Audit"):
    if spec_file and impl_file:
        with st.spinner("Hati AI is reading your files..."):
            # Extract text from both files
            spec_text = extract_text(spec_file)
            impl_text = extract_text(impl_file)
            
            # Send to IBM Watsonx (Make sure your backend function is ready)
            result = run_hati_audit("user_api_key", "user_proj_id", spec_text, impl_text)
            
            st.success("Audit Complete!")
            st.markdown(f"### Results\n{result}")
    else:
        st.warning("Please upload both documents to proceed.")
