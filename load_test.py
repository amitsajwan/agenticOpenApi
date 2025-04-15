import asyncio
import os
from api_executor import APIExecutor
from agentic_api_planner import AgenticAPIPlanner

async def run_load_test(users: int = 10):
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    tasks = [asyncio.create_task(run_user_flow(base_url, user_id)) for user_id in range(users)]
    await asyncio.gather(*tasks)

async def run_user_flow(base_url, user_id):
    executor = APIExecutor(base_url)
    planner = AgenticAPIPlanner(openapi_spec_path="specs/petstore.yaml")
    sequence = planner.generate_execution_plan()  # Each user uses the planned sequence
    results = []
    for api in sequence:
        method = api["method"]
        path = api["path"]
        # For production, you could also add dynamic payload generation here
        try:
            response = executor.run_api_with_retries(method, path)
            results.append(response)
            print(f"User {user_id}: Executed {method} {path} successfully.")
        except Exception as e:
            print(f"User {user_id}: Error executing {method} {path}: {e}")
    return results
