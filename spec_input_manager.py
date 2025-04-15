# spec_input_manager.py
from openapi_input import load_openapi_spec

class SpecInputManager:
    def __init__(self):
        self.spec = None
        self.loaded = False
    
    def is_loaded(self):
        return self.loaded
    
    def load_spec_from_input(self, user_input: str, source_type: str):
        """
        Load the OpenAPI spec from user input.
        
        Args:
            user_input (str): The input provided by the user.
            source_type (str): 'file', 'url', or 'text'
            
        Returns:
            tuple: (True, spec) on success; (False, error_message) on failure.
        """
        try:
            if source_type == 'url':
                self.spec = load_openapi_spec(user_input, is_url=True)
            elif source_type == 'text':
                self.spec = load_openapi_spec(user_input, is_text=True)
            else:
                # Default: treat input as a file path
                self.spec = load_openapi_spec(user_input)
            self.loaded = True
            return True, self.spec
        except Exception as e:
            return False, str(e)
