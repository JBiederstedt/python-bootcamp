# ---------------------------- IMPORTS ------------------------------- #

import requests
import datetime as dt
from dotenv import dotenv_values
import smtplib
import time

# ---------------------------- CONSTANTS ------------------------------- #

API_PATH_SUNRISE_SUNSET = "https://api.sunrise-sunset.org/json"
API_PATH_ISS = "http://api.open-notify.org/iss-now.json"

# Coordinates for Berlin
MY_LATITUDE = 52.520008
MY_LONGITUDE = 13.404954

MY_COORDS = (MY_LATITUDE, MY_LONGITUDE)
COORDS_MATCH_TOLERANCE = 5.0

config = dotenv_values()

MY_EMAIL = config["MY_EMAIL"]
MY_EMAIL_PASSWORD = config["MY_EMAIL_PASSWORD"]
MY_EMAIL_SMTP = config["MY_EMAIL_SMTP"]

TIME_TO_REPEAT_EXEC = 60 #seconds

# ---------------------------- GET CURRENT HOUR ------------------------------- #

def get_current_hour():
    return dt.datetime.now().hour

# ---------------------------- GET SUNRISE AND SUNSET HOURS ------------------------------- #

def get_sunrise_and_sunset_hours():
    try:
        parameters = {
            "lat": MY_LATITUDE,
            "lng": MY_LONGITUDE,
            "formatted": 0,
        }

        response = requests.get(API_PATH_SUNRISE_SUNSET, params=parameters)
        response.raise_for_status()

        data = response.json()
        sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        return {"sunrise": sunrise_hour, "sunset": sunset_hour}
    except Exception as e:
        print(f"Something went wrong:\n{e}")
        return None

# ---------------------------- CHECK IF DARK CURRENTLY ------------------------------- #

def check_if_dark():
    current_hour = get_current_hour()
    hours = get_sunrise_and_sunset_hours()

    if hours is None:
        return False

    sunrise_hour = hours["sunrise"]
    sunset_hour = hours["sunset"]

    return not (sunrise_hour <= current_hour <= sunset_hour)

# ---------------------------- GET ISS COORDS ------------------------------- #

def get_iss_coords():
    response = requests.get(API_PATH_ISS)
    response.raise_for_status()

    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    return (iss_lat, iss_lng)

# ---------------------------- CHECK IF COORDS MATCH ------------------------------- #

def check_coords_match():
    iss_coords = get_iss_coords()

    my_lat, my_lng = MY_COORDS
    iss_lat, iss_lng = iss_coords

    return (
        abs(my_lat - iss_lat) <= COORDS_MATCH_TOLERANCE and
        abs(my_lng - iss_lng) <= COORDS_MATCH_TOLERANCE
    )

# ---------------------------- SEND EMAIL ------------------------------- #

def send_email():
    message = """\
Subject: ISS is near you!

The International Space Station is currently flying over your location — and it's dark!
Go outside and look up! 🚀✨
"""
    
    try:
        with smtplib.SMTP(MY_EMAIL_SMTP, 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message)
    except Exception as e:
        print(f"Something went wrong:\n{e}")

# ---------------------------- ENTRY POINT ------------------------------- #

while True:
    try:
        if check_if_dark() and check_coords_match():
            send_email()
    except Exception as e:
        print(f"Unexpected error in main loop: {e}")
    
    time.sleep(TIME_TO_REPEAT_EXEC)
