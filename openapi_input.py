# openapi_input.py
import os
import json
import yaml
import requests

def load_openapi_spec(source, is_url=False, is_text=False):
    """
    Load an OpenAPI specification from a source.
    
    The source can be a local file, a URL, or raw text.
    
    Args:
        source (str): The location or content of the OpenAPI spec.
        is_url (bool): True if the source is a URL.
        is_text (bool): True if the source is raw text.
        
    Returns:
        dict: The parsed OpenAPI specification.
        
    Raises:
        Exception: If loading or parsing fails.
    """
    # Get the spec content from the appropriate source.
    if is_url:
        try:
            response = requests.get(source)
            response.raise_for_status()
            spec_content = response.text
        except Exception as e:
            raise Exception(f"Failed to retrieve spec from URL '{source}': {e}")
    elif is_text:
        spec_content = source
    else:
        if not os.path.exists(source):
            raise Exception(f"Spec file '{source}' does not exist.")
        with open(source, "r") as f:
            spec_content = f.read()
    
    # Determine the format
    ext = None
    if not is_url and not is_text:
        ext = os.path.splitext(source)[1].lower()
    else:
        # Use a simple heuristic
        if spec_content.strip().startswith("{") or spec_content.strip().startswith("["):
            ext = ".json"
        else:
            ext = ".yaml"
    
    try:
        if ext in [".yaml", ".yml"]:
            spec = yaml.safe_load(spec_content)
        elif ext == ".json":
            spec = json.loads(spec_content)
        else:
            raise ValueError(f"Unsupported spec format: {ext}")
    except Exception as e:
        raise Exception(f"Failed to parse OpenAPI spec: {e}")
    
    return spec
