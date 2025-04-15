class State:
    def __init__(self):
        self.created_ids = {}
        self.responses = {}

    def update_state(self, endpoint, response):
        if isinstance(response, dict):
            if "id" in response:
                self.created_ids[endpoint] = response["id"]
            self.responses[endpoint] = response
        else:
            print(f"Unexpected response format for {endpoint}")

    def get_created_id(self, endpoint):
        return self.created_ids.get(endpoint)

    def reset(self):
        self.created_ids.clear()
        self.responses.clear()
