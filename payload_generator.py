import os
import json
from langchain.chat_models.azure import AzureChatOpenAI

# Initialize Azure Chat model for payload generation
azure_model = AzureChatOpenAI(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    key=os.getenv("AZURE_OPENAI_KEY"),
    deployment_id=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-06-01-preview"),
    temperature=0.7,
)

def generate_payload(schema):
    """
    Generate a JSON payload using AzureChatOpenAI given a JSON schema.
    """
    prompt = f"Generate a valid JSON payload for the following schema:\n{json.dumps(schema, indent=2)}"
    response = azure_model.invoke_as_llm(prompt)
    try:
        payload = json.loads(response.strip())
    except Exception as e:
        payload = {}  # Fallback default payload
    return payload

def fill_payload_with_ids(payload, created_ids):
    """
    Replace placeholders in the payload (e.g., '{pet_id}') with actual values.
    """
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, str) and "{" in value:
                for placeholder, real_value in created_ids.items():
                    payload[key] = value.replace(f"{{{placeholder}}}", str(real_value))
    return payload
