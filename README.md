# HATI AI - Agentic AI Auditor

Hati AI auditor is an agentic AI that verifies security documents for technical drifts.

## 🏗️ System Architecture

This application acts as an **integrator and system architect** for AI-powered technical auditing:

### Architecture Components:

1. **Presentation Layer** (Streamlit UI)
   - User interface for document upload
   - Credential management interface
   - Results visualization

2. **Security Layer** (Credential Management)
   - Environment-based configuration
   - Secure API key handling
   - No hardcoded credentials

3. **File Processing Engine** (PyPDF2)
   - PDF text extraction
   - Multi-format document support
   - Text preprocessing

4. **AI Integration Layer** (IBM Watson)
   - IBM Granite model integration
   - Prompt engineering for auditing
   - Response processing

5. **Business Logic Layer** (Audit Engine)
   - Technical drift detection
   - Specification vs implementation comparison
   - Security gap identification

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env` with your IBM Watson credentials:
```
IBM_API_KEY=your_actual_api_key
IBM_PROJECT_ID=your_actual_project_id
```

### 3. Run the Application
```bash
streamlit run app.py
```

## 🔐 Security Best Practices

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` excluded from version control
- ✅ Password-masked input fields
- ✅ Environment variable fallbacks
- ⚠️ Remember to rotate keys regularly

## 📋 Code Review Findings

### ✅ Fixed Issues:
1. **Hardcoded credentials** - Moved to environment variables
2. **Incorrect API parameter** - Fixed `"qZdEiLLD0Vd5fL-Uj2InNSipCL9-6AIKlCwiVel13hRK"` to `"apikey"`
3. **Missing function parameters** - Added api_key and project_id to run_audit()
4. **No .gitignore** - Created to protect sensitive files
5. **Missing dependencies file** - Created requirements.txt

### 🏗️ Architecture Assessment:
- ✅ **Separation of Concerns**: UI, processing, and AI logic are separated
- ✅ **Integration Pattern**: Properly integrates Streamlit + PyPDF2 + IBM Watson
- ✅ **Security**: Credentials managed through environment variables
- ✅ **Modularity**: Functions are well-defined and reusable
- ✅ **Documentation**: Code includes comments explaining each layer

## 🎯 System Integration Points

```
User Input (PDF) → Streamlit UI → PyPDF2 Parser → Text Extraction
                                                         ↓
User Credentials → Environment Variables → IBM Watson API
                                                         ↓
                                            AI Model (Granite-13b)
                                                         ↓
                                            Audit Results → UI Display
```

## 📦 Dependencies

- **streamlit**: Web UI framework
- **PyPDF2**: PDF processing
- **ibm-watsonx-ai**: IBM Watson AI integration
- **python-dotenv**: Environment variable management

## 🚀 Future Enhancements

1. Add support for more file formats (DOCX, TXT)
2. Implement result caching
3. Add audit history tracking
4. Export results to PDF/JSON
5. Implement batch processing
6. Add user authentication