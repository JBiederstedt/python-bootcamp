# ---------------------------- IMPORTS ------------------------------- #
import requests
import datetime as dt
from dotenv import dotenv_values

# ---------------------------- CONSTANTS ------------------------------- #
config = dotenv_values()

NUTRITIONIX_API = config.get("NUTRITIONIX_API")
NUTRITIONIX_ID = config.get("NUTRITIONIX_ID")
NUTRITIONIX_KEY = config.get("NUTRITIONIX_KEY")

MY_PROJECT = config["MY_PROJECT"]
SHEET_ENDPOINT = f"https://api.sheety.co/{MY_PROJECT}/workouts"
SHEETY_TOKEN =config["SHEETY_TOKEN"]
SHEETY_AUTH_HEADERS = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

# Configure to your needs
GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 175
AGE = 30

# ---------------------------- GET EXERCISE DATA ------------------------------- #

def get_exercise_data(query: str):
    """Send natural language input to Nutritionix and get structured exercise data."""
    headers = {
        "x-app-id": NUTRITIONIX_ID,
        "x-app-key": NUTRITIONIX_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "query": query,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    try:
        response = requests.post(url=NUTRITIONIX_API, json=body, headers=headers)
        response.raise_for_status()
        return response.json().get("exercises", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching exercise data: {e}")
        return []
    
# ---------------------------- LOG EXERCISE DATA TO SHEET ------------------------------- #

def log_exercise_to_sheet(exercise_data: list):
    """Log each exercise entry to the Google Sheet."""
    now = dt.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")

    for exercise in exercise_data:
        sheet_input = {
            "workout": {
                "date": date,
                "time": time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        try:
            response = requests.post(
                url=SHEET_ENDPOINT,
                json=sheet_input,
                headers=SHEETY_AUTH_HEADERS,
            )
            response.raise_for_status()
            print(f"✅ Logged: {exercise['name'].title()} for {exercise['duration_min']} min")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error logging to sheet: {e}")

# ---------------------------- ENTRY POINT ------------------------------- #

user_input = input("Tell me what exercises you did: ")
exercise_data = get_exercise_data(user_input)

if exercise_data:
    log_exercise_to_sheet(exercise_data)
else:
    print("⚠️ No exercise data returned. Nothing to log.")
