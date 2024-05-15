import os
import requests

class Connector:
    def __init__(self):
        if os.environ.get('model_service_url') is None:
            os.environ["model_service_url"] = "localhost:2222"
            self.model_service_url = os.environ["model_service_url"]
        
        self.model_service_url = os.environ["model_service_url"]
        print(f"Using model service url: {self.model_service_url}")

    def get_url_data(self, url: str) -> str:
        response = requests.post(f"{self.model_service_url}/predict", json={"url": url})  
        return response.json()