import yaml

def parse_openapi_spec(spec_path):
    """
    Parses the OpenAPI specification YAML file and returns the parsed data.

    Args:
    - spec_path (str): The path to the OpenAPI YAML file.

    Returns:
    - dict: The parsed OpenAPI specification.
    """
    with open(spec_path, "r") as spec_file:
        spec = yaml.safe_load(spec_file)
    return spec
