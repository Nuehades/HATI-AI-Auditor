from ibm_watsonx_ai.foundation_models import Model

def run_hati_audit(api_key, proj_id, spec_text, impl_text):
    credentials = {"url": "https://us-south.ml.cloud.ibm.com", "apikey": api_key}
    model_id = "ibm/granite-13b-instruct-v2"
    
    # Initialize IBM Model
    model = Model(
        model_id=model_id,
        credentials=credentials,
        project_id=proj_id
    )

    prompt = f"Audit these for technical drift:\nSpec: {spec_text}\nActual: {impl_text}"
    return model.generate_text(prompt=prompt)
