# ---------------------------- IMPORTS ------------------------------- #

import datetime as dt
from dotenv import dotenv_values

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# ---------------------------- CONFIG ------------------------------- #

config = dotenv_values()

SHEETY_TOKEN = config["SHEETY_TOKEN"]
SHEET_ENDPOINT = config["SHEET_ENDPOINT"]

SHEETY_AUTH_HEADERS = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

ORIGIN_CITY_IATA = "BER"  # Example: Berlin

# ---------------------------- OBJECTS ------------------------------- #

data_manager = DataManager(sheet_endpoint=SHEET_ENDPOINT, headers=SHEETY_AUTH_HEADERS)
flight_search = FlightSearch()
notifier = NotificationManager()

# ---------------------------- LOGIC ------------------------------- #

sheet_data = data_manager.get_destination_data()

# Fill missing IATA codes
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_city_code(row["city"])

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# Check for cheap flights
tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_months_later = tomorrow + dt.timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_later
    )

    if flight and float(flight.price) < destination["lowestPrice"]:
        message = (
            f"✈️ Low price alert! Only €{flight.price} to fly from "
            f"{flight.origin_city}-{flight.origin_airport} to "
            f"{flight.destination_city}-{flight.destination_airport}, "
            f"from {flight.out_date} to {flight.return_date}."
        )
        notifier.send_sms(message)
