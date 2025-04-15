import openai
import json
from langgraph import LangGraph
from openapi_parser import parse_openapi_spec

# Set your OpenAI API key via env variable ideally
openai.api_key = "your-openai-api-key"

class AgenticAPIPlanner:
    def __init__(self, openapi_spec_path):
        self.openapi_spec = parse_openapi_spec(openapi_spec_path)
        self.langgraph = LangGraph()  # Assuming LangGraph is properly configured

    def extract_endpoints(self):
        # Extract endpoints with their HTTP methods from the spec
        endpoints = []
        for path, methods in self.openapi_spec.get("paths", {}).items():
            for method in methods.keys():
                endpoints.append({"method": method.upper(), "path": path})
        return endpoints

    def generate_execution_plan(self):
        endpoints = self.extract_endpoints()
        # Create a basic sequence using LangGraph (for demo, sort by method type)
        sequence = sorted(endpoints, key=lambda x: x["method"] != "POST")
        
        # Use OpenAI to optimize the sequence
        prompt = f"Optimize the following API sequence for dependency resolution:\n{json.dumps(sequence, indent=2)}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        try:
            optimized = json.loads(response.choices[0].text.strip())
        except Exception as e:
            optimized = sequence  # Fallback to the basic sequence
        return optimized

    def finalize_sequence(self, user_sequence):
        # Here, one can integrate user modifications
        return user_sequence
