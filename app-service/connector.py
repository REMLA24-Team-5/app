import os
import requests
import json

class Connector:
    def __init__(self):
        if os.environ.get('model_service_url') is None:
            os.environ["model_service_url"] = "http://127.0.0.1:8000"
            self.model_service_url = os.environ["model_service_url"]
        
        self.model_service_url = os.environ["model_service_url"]
        print(f"Using model service url: {self.model_service_url}")

    def get_url_data(self, url: str) -> str:
        print(f"{self.model_service_url}/predict")
        try:
            response = requests.post(f"{self.model_service_url}/predict", json={"url": url}) 
            return response.json()
        except:
            return json.loads('{ "prediction":"Uknown"}')