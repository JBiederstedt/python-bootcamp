import requests
import datetime as dt
from dotenv import dotenv_values
from flight_data import FlightData

config = dotenv_values()

AMADEUS_CLIENT_ID = config["AMADEUS_CLIENT_ID"]
AMADEUS_CLIENT_SECRET = config["AMADEUS_CLIENT_SECRET"]

class FlightSearch:
    def __init__(self):
        self.token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(
            url="https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": AMADEUS_CLIENT_ID,
                "client_secret": AMADEUS_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_city_code(self, city_name):
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        return data[0]["iataCode"] if data else None
    
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        best_flight = None
        lowest_price = float("inf")

        for stay_duration in range(3, 15):  # Holiday from 3 to 14 days
            return_date = from_time + dt.timedelta(days=stay_duration)
            if return_date > to_time:
                break

            params = {
                "originLocationCode": origin_city_code,
                "destinationLocationCode": destination_city_code,
                "departureDate": from_time.strftime("%Y-%m-%d"),
                "returnDate": return_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "nonStop": True,
                "currencyCode": "EUR",
                "max": 1
            }

            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get("data")

            if not data:
                continue

            offer = data[0]
            price = float(offer["price"]["total"])
            if price < lowest_price:
                segments = offer["itineraries"][0]["segments"]
                best_flight = FlightData(
                    price=price,
                    origin_city=segments[0]["departure"]["iataCode"],
                    origin_airport=segments[0]["departure"]["iataCode"],
                    destination_city=segments[0]["arrival"]["iataCode"],
                    destination_airport=segments[0]["arrival"]["iataCode"],
                    out_date=segments[0]["departure"]["at"].split("T")[0],
                    return_date=offer["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
                )
                lowest_price = price

        return best_flight
