import openai
import json

# Set up OpenAI API key
openai.api_key = "your-openai-api-key"

def generate_payload(schema):
    """
    Generates a payload using OpenAI's GPT model based on the provided OpenAPI schema.

    Args:
    - schema (dict): The OpenAPI schema for the API request.

    Returns:
    - dict: The generated payload.
    """
    # Example logic for generating payload from schema using GPT (simplified)
    prompt = f"Generate a payload for the following OpenAPI schema:\n{json.dumps(schema, indent=2)}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    payload = response.choices[0].text.strip()
    return json.loads(payload)

def fill_payload_with_ids(payload, created_ids):
    """
    Replaces placeholders in the payload with real IDs from created resources.

    Args:
    - payload (dict): The API request payload.
    - created_ids (dict): A dictionary mapping resource names to created IDs.

    Returns:
    - dict: The updated payload with IDs inserted.
    """
    for key, value in payload.items():
        if isinstance(value, str) and "{" in value:
            for resource, created_id in created_ids.items():
                placeholder = f"{{{resource}}}"
                if placeholder in value:
                    payload[key] = value.replace(placeholder, str(created_id))
    return payload
