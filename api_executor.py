import time
import requests
from concurrent.futures import ThreadPoolExecutor
from .state import State

class APIExecutor:
    def __init__(self, base_url, headers, langgraph, state=None):
        self.base_url = base_url
        self.headers = headers
        self.langgraph = langgraph
        self.state = state or State()

    def execute_api(self, method, path, payload=None):
        """
        Executes a single API call based on the HTTP method, path, and payload.

        Args:
        - method (str): The HTTP method (e.g., 'GET', 'POST').
        - path (str): The API endpoint path.
        - payload (dict, optional): The request payload for POST/PUT requests.

        Returns:
        - dict: The response data.
        """
        url = f"{self.base_url}{path}"
        response = None

        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=self.headers)
        elif method == "PUT":
            response = requests.put(url, json=payload, headers=self.headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=self.headers)

        if response.status_code in range(200, 299):
            return response.json()  # Success
        else:
            return {"error": response.text, "status_code": response.status_code}

    def run_single_api(self, api):
        """
        Executes a single API in the sequence, handles retries and updates state.

        Args:
        - api (dict): The API information (method, path, payload).

        Returns:
        - dict: The response from the API call.
        """
        response = None
        attempt = 0
        while attempt < 3:
            try:
                print(f"Executing API {api['method']} {api['path']} with payload: {api.get('payload')}")
                response = self.execute_api(api['method'], api['path'], api.get('payload'))
                
                # Update state with the response if the API call was successful
                if 'error' not in response:
                    self.state.update_state(api['path'], response)
                    print(f"API {api['method']} {api['path']} executed successfully.")
                    break
            except Exception as e:
                print(f"Error executing {api['method']} {api['path']}: {e}")
            
            time.sleep(2 ** attempt)  # Exponential backoff
            attempt += 1

        return response

    def run_parallel(self, api_sequence):
        """
        Runs the API sequence in parallel using a ThreadPoolExecutor.

        Args:
        - api_sequence (list): List of API calls to be executed.

        Returns:
        - list: Responses for each API call.
        """
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.run_single_api, api_sequence))
        return results

    def run_sequential(self, api_sequence):
        """
