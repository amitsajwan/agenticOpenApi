import os
import json
from langgraph import LangGraph
from openapi_parser import parse_openapi_spec

# Use AzureChatOpenAI via LangChain
from langchain.chat_models.azure import AzureChatOpenAI

# Initialize Azure Chat model using environment variables
azure_model = AzureChatOpenAI(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    key=os.getenv("AZURE_OPENAI_KEY"),
    deployment_id=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-06-01-preview"),
    temperature=0.7,
)

class AgenticAPIPlanner:
    def __init__(self, openapi_spec_path):
        self.openapi_spec = parse_openapi_spec(openapi_spec_path)
        self.langgraph = LangGraph()

    def extract_endpoints(self):
        endpoints = []
        for path, methods in self.openapi_spec.get("paths", {}).items():
            for method in methods.keys():
                endpoints.append({"method": method.upper(), "path": path})
        return endpoints

    def generate_execution_plan(self):
        endpoints = self.extract_endpoints()
        # Create a baseline sequence: For example, POST first then others.
        sequence = sorted(endpoints, key=lambda x: x["method"] != "POST")
        
        # Use AzureChatOpenAI to refine the sequence.
        prompt = (
            "Optimize the following API sequence for dependency resolution and efficiency. "
            "Consider that POST requests must precede GET/PUT/DELETE calls that require their IDs:\n"
            f"{json.dumps(sequence, indent=2)}"
        )
        # Get the completion
        response = azure_model.invoke_as_llm(prompt)
        try:
            optimized_sequence = json.loads(response.strip())
        except Exception as e:
            optimized_sequence = sequence  # Fallback if parsing fails
        return optimized_sequence

    def finalize_sequence(self, user_sequence):
        # Process user modifications; for production, you could merge changes with automated plan.
        return user_sequence
