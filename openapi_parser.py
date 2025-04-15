import os
import json
import yaml

def parse_openapi_spec(spec_path):
    """
    Parse an OpenAPI specification from a given file path.
    
    This function supports both YAML and JSON formatted specifications.
    
    Args:
        spec_path (str): The file path to the OpenAPI spec.
    
    Returns:
        dict: The parsed specification.
        
    Raises:
        ValueError: If the file format is not supported.
    """
    ext = os.path.splitext(spec_path)[1].lower()
    try:
        with open(spec_path, "r") as spec_file:
            if ext in [".yaml", ".yml"]:
                spec = yaml.safe_load(spec_file)
            elif ext == ".json":
                spec = json.load(spec_file)
            else:
                raise ValueError(f"Unsupported spec file format: {ext}")
    except Exception as e:
        raise Exception(f"Failed to parse OpenAPI spec from {spec_path}: {e}")
    
    return spec
