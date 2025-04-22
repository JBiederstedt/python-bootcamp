# ---------------------------- IMPORTS ------------------------------- #

import requests
import datetime as dt
from dotenv import dotenv_values

# ---------------------------- CONSTANTS ------------------------------- #

config = dotenv_values()

PIXELA_API = "https://pixe.la/v1/users"
PIXELA_TOKEN = config["PIXELA_TOKEN"]
PIXELA_USERNAME = config["PIXELA_USERNAME"]

# Configure your tracking habit
HABIT_GRAPH_ID = "graph1"
HABIT_GRAPH_NAME = "Cycling Graph"
HABIT_GRAPH_COLOR = "ajisai"
HABIT_UNIT = "Km"
HABIT_UNIT_TYPE = "float"

# ---------------------------- CREATE A USER ACCOUNT ------------------------------- #

def create_user_account():
    user_params = {
        "token": PIXELA_TOKEN,
        "username": PIXELA_USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }

    try:
        response = requests.post(url=PIXELA_API, json=user_params)
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        print(f"Something went wrong: {e}")

# ---------------------------- CREATE A GRAPH ------------------------------- #

def create_graph():
    graph_endpoint = f"{PIXELA_API}/{PIXELA_USERNAME}/graphs"

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
    }

    graph_params = {
        "id": HABIT_GRAPH_ID,
        "name": HABIT_GRAPH_NAME,
        "unit": HABIT_UNIT,
        "type": HABIT_UNIT_TYPE,
        "color": HABIT_GRAPH_COLOR,
    }

    try:
        response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        print(f"Something went wrong: {e}")

# ---------------------------- POST A PIXEL ------------------------------- #

def post_pixel(quantity):
    pixel_endpoint = f"{PIXELA_API}/{PIXELA_USERNAME}/graphs/{HABIT_GRAPH_ID}"
    today = dt.datetime.now().strftime("%Y%m%d")

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
    }

    pixel_params = {
        "date": today,
        "quantity": quantity,
    }

    try:
        response = requests.post(url=pixel_endpoint, json=pixel_params, headers=headers)
        response.raise_for_status()

        res_data = response.json()
        if res_data.get("isSuccess"):
            print(f"✅ Tracked {quantity} {HABIT_UNIT} successfully!")
        else:
            print(f"⚠️ Pixela error: {res_data.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"⚠️ Something went wrong: {e}")

# ---------------------------- UPDATE A PIXEL ------------------------------- #

def update_pixel(quantity):
    pixel_endpoint = f"{PIXELA_API}/{PIXELA_USERNAME}/graphs/{HABIT_GRAPH_ID}/{dt.datetime.now().strftime('%Y%m%d')}"

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
    }

    pixel_params = {
        "quantity": quantity
    }

    try:
        response = requests.put(url=pixel_endpoint, json=pixel_params, headers=headers)
        response.raise_for_status()

        res_data = response.json()
        if res_data.get("isSuccess"):
            print(f"🔄 Updated pixel to {quantity} {HABIT_UNIT} successfully!")
        else:
            print(f"⚠️ Pixela error: {res_data.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"⚠️ Something went wrong: {e}")

# ---------------------------- DELETE A PIXEL ------------------------------- #

def delete_pixel():
    pixel_endpoint = f"{PIXELA_API}/{PIXELA_USERNAME}/graphs/{HABIT_GRAPH_ID}/{dt.datetime.now().strftime('%Y%m%d')}"

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
    }

    try:
        response = requests.delete(url=pixel_endpoint, headers=headers)
        response.raise_for_status()

        res_data = response.json()
        if res_data.get("isSuccess"):
            print("🗑️ Pixel deleted successfully!")
        else:
            print(f"⚠️ Pixela error: {res_data.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"⚠️ Something went wrong: {e}")

# ---------------------------- ENTRY POINT ------------------------------- #

# Step 1: Create an user account
# create_user_account()

# Step 2: Create a habit graph
# create_graph()

# Step 3: Choose action
while True:
    action = input("\nWhat do you want to do? (post / update / delete / q to quit)\n>").lower()

    if action == "q":
        print("👋 Exiting. No action performed.")
        break

    if action in ["post", "update"]:
        quantity_input = input(f"How many {HABIT_UNIT} do you want to {action}?\n>")

        try:
            if HABIT_UNIT_TYPE == "int":
                quantity = str(int(quantity_input))
            elif HABIT_UNIT_TYPE == "float":
                quantity = str(float(quantity_input))
            else:
                raise ValueError(f"Unsupported HABIT_UNIT_TYPE: '{HABIT_UNIT_TYPE}'. Must be 'int' or 'float'.")
        except ValueError:
            print(f"⚠️ Invalid input: please enter a valid {HABIT_UNIT_TYPE} value.")
        else:
            if action == "post":
                post_pixel(quantity)
            else:
                update_pixel(quantity)
            break

    elif action == "delete":
        confirm = input("❗ Are you sure you want to delete today's pixel? (y/n)\n>").lower()
        if confirm == "y":
            delete_pixel()
            break
        else:
            print("✅ Deletion cancelled.")
    else:
        print("⚠️ Invalid choice. Please type: post, update, delete, or q.")
