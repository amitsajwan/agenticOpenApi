class State:
    def __init__(self):
        # Stores the state for tracking created IDs, responses, etc.
        self.created_ids = {}
        self.responses = {}

    def update_state(self, endpoint, response):
        """
        Updates the state with the response from an API call.

        Args:
        - endpoint (str): The API endpoint (e.g., "/pet/{id}").
        - response (dict): The response data from the API call.
        """
        if isinstance(response, dict):
            if "id" in response:
                # Track created IDs (assuming 'id' is a key in the response)
                self.created_ids[endpoint] = response["id"]
            self.responses[endpoint] = response
        else:
            print(f"Invalid response format for {endpoint}. Expected a dictionary.")

    def get_created_id(self, endpoint):
        """
        Retrieves the created ID for a specific endpoint.

        Args:
        - endpoint (str): The API endpoint (e.g., "/pet/{id}").

        Returns:
        - str or None: The created ID for the endpoint, or None if not available.
        """
        return self.created_ids.get(endpoint, None)

    def get_response(self, endpoint):
        """
        Retrieves the response for a specific endpoint.

        Args:
        - endpoint (str): The API endpoint (e.g., "/pet/{id}").

        Returns:
        - dict or None: The response for the endpoint, or None if not available.
        """
        return self.responses.get(endpoint, None)

    def reset(self):
        """
        Resets the state, clearing created IDs and responses.
        Useful for re-running tests or clearing the state.
        """
        self.created_ids.clear()
        self.responses.clear()
