import requests
from dotenv import dotenv_values

config = dotenv_values()
TAB_NAME = config["SHEET_TAB"]

class DataManager:
    def __init__(self, sheet_endpoint, headers):
        self.sheet_endpoint = sheet_endpoint
        self.headers = headers
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.sheet_endpoint, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        if TAB_NAME not in data:
            raise ValueError(f"⚠️ Sheet tab '{TAB_NAME}' not found in Sheety response. Available keys: {list(data.keys())}")
        self.destination_data = data[TAB_NAME]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            update_url = f"{self.sheet_endpoint}/{city['id']}"
            response = requests.put(url=update_url, json=new_data, headers=self.headers)
            response.raise_for_status()
