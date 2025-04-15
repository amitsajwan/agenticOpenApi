import json
import logging
import os
from typing import Any


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def cache_data(file_name: str, data: Any) -> None:
    """
    Cache data to a JSON file to avoid recomputing expensive operations.

    Args:
    - file_name (str): The name of the cache file.
    - data (Any): The data to cache.

    Returns:
    - None
    """
    try:
        os.makedirs("cache", exist_ok=True)
        cache_file = os.path.join("cache", file_name)

        with open(cache_file, "w") as file:
            json.dump(data, file)
        logger.info(f"Data cached to {cache_file}")
    except Exception as e:
        logger.error(f"Error caching data: {e}")


def load_cached_data(file_name: str) -> Any:
    """
    Load cached data from a JSON file.

    Args:
    - file_name (str): The name of the cache file.

    Returns:
    - data (Any): The loaded data.
    """
    try:
        cache_file = os.path.join("cache", file_name)

        if os.path.exists(cache_file):
            with open(cache_file, "r") as file:
                data = json.load(file)
            logger.info(f"Loaded data from cache: {cache_file}")
            return data
        else:
            logger.info(f"No cached data found for {file_name}")
            return None
    except Exception as e:
        logger.error(f"Error loading cached data: {e}")
        return None


def log_api_call(endpoint: str, request_data: dict, response_data: dict) -> None:
    """
    Logs the details of an API call, including the request and response.

    Args:
    - endpoint (str): The API endpoint that was called.
    - request_data (dict): The request payload sent to the endpoint.
    - response_data (dict): The response received from the endpoint.

    Returns:
    - None
    """
    try:
        logger.info(f"API Call: {endpoint}")
        logger.info(f"Request Payload: {json.dumps(request_data, indent=2)}")
        logger.info(f"Response: {json.dumps(response_data, indent=2)}")
    except Exception as e:
        logger.error(f"Error logging API call: {e}")


def retry_on_failure(func, retries: int = 3, delay: int = 5, *args, **kwargs):
    """
    Retry a function call on failure.

    Args:
    - func (function): The function to call.
    - retries (int): The number of retry attempts.
    - delay (int): Delay between retries (in seconds).
    - *args: Arguments to pass to the function.
    - **kwargs: Keyword arguments to pass to the function.

    Returns:
    - result: The result of the function call.
    """
    import time
    attempts = 0
    while attempts < retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempts += 1
            logger.warning(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    logger.error(f"Function failed after {retries} attempts.")
    return None
