import asyncio
from api_executor import APIExecutor
from agentic_api_planner import AgenticAPIPlanner
import os

async def run_load_test(users: int = 10):
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    # Initialize executor and planner once for each user or per run as needed.
    tasks = []
    for user in range(users):
        task = asyncio.create_task(run_user_flow(base_url, user))
        tasks.append(task)
    await asyncio.gather(*tasks)

async def run_user_flow(base_url, user_id):
    # For each user, instantiate a fresh executor (state isolated)
    executor = APIExecutor(base_url)
    # You might want to re-plan the execution for each user if necessary
    planner = AgenticAPIPlanner(openapi_spec_path="specs/petstore.yaml")
    sequence = planner.generate_execution_plan()
    results = []
    for api in sequence:
        method = api["method"]
        path = api["path"]
        # Optionally generate a payload if needed here
        try:
            response = executor.run_api_with_retries(method, path)
            results.append(response)
            print(f"User {user_id}: Executed {method} {path} successfully.")
        except Exception as e:
            print(f"User {user_id}: Error executing {method} {path} - {e}")
    return results
