import os
import json
import re
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from openapi_parser import parse_openapi_spec

class AgenticAPIPlanner:
    def __init__(self, openapi_spec_path):
        self.openapi_spec = parse_openapi_spec(openapi_spec_path)
        self.azure_model = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
            temperature=0.7,
            max_tokens=1000
        )

    def extract_endpoints(self):
        endpoints = []
        for path, methods in self.openapi_spec.get("paths", {}).items():
            for method, details in methods.items():
                endpoints.append({
                    "method": method.upper(),
                    "path": path,
                    "summary": details.get("summary", ""),
                    "operationId": details.get("operationId", "")
                })
        return endpoints

    def extract_json_block(self, text):
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return None
        return None

    def generate_execution_plan(self):
        endpoints = self.extract_endpoints()
        sequence = sorted(endpoints, key=lambda x: x["method"] != "POST")

        prompt = (
            "Optimize the following API sequence for dependency resolution and efficiency. "
            "Consider that POST requests must precede GET/PUT/DELETE calls that require their IDs:\n"
            f"{json.dumps(sequence, indent=2)}"
        )

        try:
            llm_response = self.azure_model([HumanMessage(content=prompt)])
            llm_output = llm_response[0].content
            optimized_sequence = self.extract_json_block(llm_output) or sequence
        except Exception as e:
            optimized_sequence = sequence

        return optimized_sequence

    def finalize_sequence(self, user_sequence):
        return user_sequence
