import yaml

def parse_openapi_spec(spec_path):
    """
    Parse the OpenAPI YAML file and return the parsed spec.
    For full $ref resolution, consider a library like 'prance'.
    """
    with open(spec_path, "r") as f:
        spec = yaml.safe_load(f)
    return spec
