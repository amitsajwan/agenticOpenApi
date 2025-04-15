import yaml

def parse_openapi_spec(spec_path):
    """
    Parses the OpenAPI spec YAML file and returns the specification.
    """
    with open(spec_path, "r") as spec_file:
        spec = yaml.safe_load(spec_file)
    # (Optional) Process $ref resolutions here or use an external tool
    return spec
