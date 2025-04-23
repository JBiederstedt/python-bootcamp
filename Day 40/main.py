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

register = input("Do you want to register as a new user? (y/n): ").strip().lower()

if register == "y":
    print("Welcome to Flight Club.")
    print("We find the best flight deals and email you.")
    first = input("What is your first name? ").strip()
    last = input("What is your last name? ").strip()
    email = input("What is your email? ").strip()
    email_check = input("Type your email again. ").strip()

    if email == email_check:
        data_manager.add_user(first_name=first, last_name=last, email=email)
    else:
        print("⚠️ Emails do not match. Try again.")
        exit()

# Load destination data
sheet_data = data_manager.get_destination_data()

# Fill in missing IATA codes
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_city_code(row["city"])

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# Load customer emails
emails = data_manager.get_customer_emails()

# Define search window
tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_months_later = tomorrow + dt.timedelta(days=180)

# Search for deals
start_date = dt.datetime.now() + dt.timedelta(days=1)
end_date = start_date + dt.timedelta(days=180)

for destination in sheet_data:
    search_date = start_date
    while search_date <= end_date:
        flight = flight_search.check_flights(
            origin_city_code=ORIGIN_CITY_IATA,
            destination_city_code=destination["iataCode"],
            from_time=search_date,
            to_time=end_date,
            is_direct=True
        )

        if not flight:
            flight = flight_search.check_flights(
                origin_city_code=ORIGIN_CITY_IATA,
                destination_city_code=destination["iataCode"],
                from_time=search_date,
                to_time=end_date,
                is_direct=False
            )

        if flight and float(flight.price) < destination["lowestPrice"]:
            stop_info = (
                "non-stop flight" if flight.stops == 0
                else f"flight with {flight.stops} stopover(s)"
            )

            message = (
                f"✈️ Low price alert! Only EUR {flight.price} to fly from "
                f"{flight.origin_city}-{flight.origin_airport} to "
                f"{flight.destination_city}-{flight.destination_airport}, "
                f"from {flight.out_date} to {flight.return_date}. This is a {stop_info}!"
            )

            notifier.send_sms(message)
            notifier.send_emails(
                recipient_list=emails,
                subject="New Flight Deal Alert! ✈️",
                body=message
            )

        search_date += dt.timedelta(days=1)
