import requests
from dotenv import dotenv_values

config = dotenv_values()
PRICES_TAB = config["PRICES_TAB"]
USERS_ENDPOINT = config["USERS_ENDPOINT"]
USERS_TAB = config["USERS_TAB"]

class DataManager:
    def __init__(self, sheet_endpoint, headers):
        self.sheet_endpoint = sheet_endpoint
        self.headers = headers
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.sheet_endpoint, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        if PRICES_TAB not in data:
            raise ValueError(f"⚠️ Sheet tab '{PRICES_TAB}' not found in Sheety response. Available keys: {list(data.keys())}")
        self.destination_data = data[PRICES_TAB]
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

    def user_exists(self, email):
        response = requests.get(url=USERS_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        users = response.json().get(USERS_TAB, [])
        return any(user.get("email", "").lower() == email.lower() for user in users)

    def add_user(self, first_name, last_name, email):
        if self.user_exists(email):
            print("⚠️ User already exists with this email.")
            return

        new_data = {
            USERS_TAB[:-1]: {  # e.g. "user"
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        response = requests.post(url=USERS_ENDPOINT, json=new_data, headers=self.headers)
        response.raise_for_status()
        print("✅ You're in the club!")

    def get_customer_emails(self):
        response = requests.get(url=USERS_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        if USERS_TAB not in data:
            raise ValueError(f"⚠️ Sheet tab '{USERS_TAB}' not found in Sheety response. Available keys: {list(data.keys())}")
        return [user["email"] for user in data[USERS_TAB] if user.get("email")]
