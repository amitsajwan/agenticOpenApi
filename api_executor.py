import time
import requests
from state import State

class APIExecutor:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "application/json"}
        self.state = State()

    def execute_api(self, method, path, payload=None):
        url = f"{self.base_url}{path}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, headers=self.headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload, headers=self.headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            if response.status_code < 300:
                return response.json()
            else:
                raise Exception(f"Status {response.status_code}: {response.text}")
        except Exception as e:
            raise e

    def run_api_with_retries(self, method, path, payload=None, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                result = self.execute_api(method, path, payload)
                if isinstance(result, dict) and "id" in result:
                    self.state.update_state(path, result)
                return result
            except Exception as e:
                print(f"Error calling {method} {path}: {e} (Attempt {attempt + 1}/{retries})")
                time.sleep(2 ** attempt)
                attempt += 1
        return {"error": "Failed after retries"}
