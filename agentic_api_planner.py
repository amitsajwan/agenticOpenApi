import openai
import json
from langgraph import LangGraph
import time

# Set up OpenAI API key
openai.api_key = "your-openai-api-key"

class AgenticAPIPlanner:
    def __init__(self, openapi_spec, created_ids=None, langgraph=None):
        self.openapi_spec = openapi_spec
        self.created_ids = created_ids or {}
        self.langgraph = langgraph or LangGraph()

    def resolve_dependencies(self, api_sequence):
        """
        Resolve dependencies in the sequence (e.g., IDs that depend on prior API results).
        
        Args:
        - api_sequence (list): The sequence of APIs to be executed.

        Returns:
        - list: The sequence with resolved dependencies.
        """
        resolved_sequence = []
        for api in api_sequence:
            path = api["path"]
            for key, value in self.created_ids.items():
                # Replace any placeholders with the correct created IDs
                path = path.replace(f"{{{key}}}", str(value))
            api["path"] = path
            resolved_sequence.append(api)
        return resolved_sequence

    def generate_execution_plan(self):
        """
        Generates the optimal API execution plan using LangGraph and GPT.

        Returns:
        - list: The optimized execution plan with the API sequence.
        """
        # Extract relevant API endpoints from the OpenAPI spec
        endpoints = [{"method": "GET", "path": "/petstore"},
                     {"method": "POST", "path": "/pet"},
                     {"method": "PUT", "path": "/pet/{pet_id}"}]
        
        # Create a LangGraph instance and generate the execution order (DAG)
        graph = self.langgraph
        execution_plan = graph.generate_execution_order(endpoints)

        # Now, use LLM (OpenAI GPT) to optimize the execution plan considering dependencies
        prompt = f"Optimize the following API execution sequence considering dependencies (like created IDs, paths, etc.):\n{json.dumps(execution_plan, indent=2)}"
        
        # Request GPT to optimize the sequence
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        
        optimized_sequence = json.loads(response.choices[0].text.strip())

        # Resolve any dependencies or path adjustments
        return self.resolve_dependencies(optimized_sequence)

    def finalize_sequence(self, user_approved_sequence):
        """
        Finalize the API execution sequence after user approval.

        Args:
        - user_approved_sequence (list): The sequence the user approves (may include adjustments).

        Returns:
        - list: The final API execution plan.
        """
        # Handle any user-defined adjustments (like adding a GET request after a PUT)
        return self.resolve_dependencies(user_approved_sequence)

    def retry_failed_step(self, failed_step, retries=3):
        """
        Retry a failed step in the API sequence, with exponential backoff.

        Args:
        - failed_step (dict): The API step that failed.
        - retries (int): The number of retries.

        Returns:
        - dict: The response of the retried API call.
        """
        attempt = 0
        while attempt < retries:
            try:
                # Here, simulate executing the failed step
                print(f"Retrying API {failed_step['method']} {failed_step['path']} (Attempt {attempt + 1})")
                
                # Simulate API call (in real-world, you'd call an API function here)
                response = {"status": "success", "data": "response data"}
                
                # If successful, return the response
                if response["status"] == "success":
                    print(f"API {failed_step['method']} {failed_step['path']} succeeded.")
                    return response
            except Exception as e:
                print(f"Failed to execute {failed_step['method']} {failed_step['path']}: {e}")
            
            # Backoff before retrying
            time.sleep(2 ** attempt)  # Exponential backoff
            attempt += 1
        
        print(f"API {failed_step['method']} {failed_step['path']} failed after {retries} attempts.")
        return None

    def run_execution_plan(self, api_sequence):
        """
        Runs the finalized API sequence.

        Args:
        - api_sequence (list): The sequence of APIs to be executed.
        
        Returns:
        - list: Responses from each API call.
        """
        responses = []
        
        for api in api_sequence:
            response = None
            attempt = 0
            while attempt < 3:
                try:
                    # Simulate calling the API here
                    print(f"Executing {api['method']} {api['path']}...")
                    
                    # In a real-world scenario, this would execute the API and return the result
                    response = {"status": "success", "data": f"response from {api['path']}"}
                    
                    if response["status"] == "success":
                        print(f"Successfully executed {api['method']} {api['path']}")
                        responses.append(response)
                        break
                except Exception as e:
                    print(f"Failed to execute {api['method']} {api['path']}: {e}")
                
                attempt += 1
                time.sleep(1)  # Short delay before retrying
            else:
                # After retries, log a failure if the step did not succeed
                print(f"Failed to execute {api['method']} {api['path']} after 3 attempts.")
                responses.append({"status": "failure", "data": None})
        
        return responses
