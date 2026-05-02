from ibm_watsonx_ai.foundation_models import Model

def get_model(credentials, project_id):
    model_id = "ibm/granite-13b-instruct-v2"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 1000,
        "temperature": 0.2 # Low temperature for high factual accuracy
    }
    return Model(model_id, parameters, credentials, project_id)

def run_audit(model, spec_text, implementation_text):
    prompt = f"""[Role: Senior Cybersecurity Auditor]
    Analyze the difference between the Requirement and the Reality.
    
    REQUIREMENT: {spec_text}
    REALITY: {implementation_text}
    
    Identify 'Technical Drift' (discrepancies). 
    Provide: 
    1. List of Security Gaps
    2. Compliance Status (Pass/Fail)
    3. Remediation Steps"""
    
    return model.generate_text(prompt=prompt)
