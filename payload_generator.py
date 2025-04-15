import openai
import json

openai.api_key = "your-openai-api-key"

def generate_payload(schema):
    """
    Generates a JSON payload using OpenAI based on the schema definition.
    """
    prompt = f"Given the following JSON schema, produce a valid JSON payload:\n{json.dumps(schema, indent=2)}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    payload_text = response.choices[0].text.strip()
    try:
        payload = json.loads(payload_text)
    except Exception as e:
        payload = {}  # Fallback
    return payload

def fill_payload_with_ids(payload, created_ids):
    """
    Replaces placeholders in the payload (e.g., {pet_id}) using the created_ids dictionary.
    """
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, str) and "{" in value:
                for placeholder, real_value in created_ids.items():
                    payload[key] = value.replace(f"{{{placeholder}}}", str(real_value))
    return payload
