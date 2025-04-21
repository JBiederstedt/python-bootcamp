# ---------------------------- IMPORTS ------------------------------- #

import requests
from dotenv import dotenv_values
from twilio.rest import Client

# ---------------------------- CONSTANTS ------------------------------- #

config = dotenv_values()

OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/forecast"
OPEN_WEATHER_API_NUMBER_OF_TIMESTAMPS = 4 # Check next ~12 hours of forecast for rain
OPEN_WEATHER_API_KEY = config["OPEN_WEATHER_API_KEY"]
TWILIO_ACCOUNT_SID = config["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = config["TWILIO_PHONE_NUMBER"]
RECIPIENT_PHONE_NUMBER = config["RECIPIENT_PHONE_NUMBER"]

# Coordinates for Berlin
MY_LATITUDE = 52.520008
MY_LONGITUDE = 13.404954

# ---------------------------- SEND TEXT MESSAGE ------------------------------- #

def send_text_message(message):
    try:
        # Create a Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send the SMS message
        client.messages.create(
            to=RECIPIENT_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )

        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send the message: {e}")

# ---------------------------- ENTRY POINT ------------------------------- #

weather_params = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": OPEN_WEATHER_API_KEY,
    "cnt": OPEN_WEATHER_API_NUMBER_OF_TIMESTAMPS,
}

try:
    response = requests.get(OPEN_WEATHER_API, params=weather_params)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    data = {}

if data:
    if "list" in data:
        for i in data["list"]:
            if int(i["weather"][0]["id"]) < 700:
                send_text_message("It's going to rain today. Remember to bring an ☂️.")
                break
    else:
        print("Unexpected API response structure:", data)
