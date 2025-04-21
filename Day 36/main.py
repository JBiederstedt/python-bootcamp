# ---------------------------- IMPORTS ------------------------------- #

import requests
from dotenv import dotenv_values
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# ---------------------------- CONSTANTS ------------------------------- #

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

config = dotenv_values()

ALPHA_VANTAGE_API = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = config["ALPHA_VANTAGE_API_KEY"]
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = config["NEWS_API_KEY"]
TWILIO_ACCOUNT_SID = config["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = config["TWILIO_PHONE_NUMBER"]
RECIPIENT_PHONE_NUMBER = config["RECIPIENT_PHONE_NUMBER"]

# ---------------------------- GET PRICE CHANGE ------------------------------- #

def get_price_change(stock_symbol):
    stock_endpoint = ALPHA_VANTAGE_API
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    response = requests.get(stock_endpoint, params=params)
    response.raise_for_status()
    
    try:
        data = response.json()["Time Series (Daily)"]
    except KeyError:
        print("Error retrieving stock data. API limit might have been reached.")
        return None

    # Sort by date
    sorted_dates = sorted(data.keys(), reverse=True)
    yesterday = sorted_dates[0]
    day_before_yesterday = sorted_dates[1]

    close_yesterday = float(data[yesterday]["4. close"])
    close_day_before = float(data[day_before_yesterday]["4. close"])

    change_percent = ((close_yesterday - close_day_before) / close_day_before) * 100

    return round(change_percent, 2)

# ---------------------------- GET NEWS ------------------------------- #

def get_news(company_name):
    news_endpoint = NEWS_API
    params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": company_name,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 3
    }

    response = requests.get(news_endpoint, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    
    news_list = [
        f"Headline: {article['title']}\nBrief: {article['description']}" 
        for article in articles[:3]
    ]

    return news_list

# ---------------------------- SEND TEXT MESSAGE ------------------------------- #

def send_text_message(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        response = client.messages.create(
            to=RECIPIENT_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )

        print(f"Message sent successfully! SID: {response.sid}")

    except TwilioRestException as e:
        print(f"Twilio API error: {e.msg}")
    except Exception as e:
        print(f"Unexpected error while sending message: {e}")

# ---------------------------- ENTRY POINT ------------------------------- #

change = get_price_change(STOCK)

if change is None:
    print("Aborting: Could not retrieve stock change.")
    send_text_message("⚠️ Error: Could not retrieve stock data. Check API.")
else:
    up_down = "🔺" if change > 0 else "🔻"

    if abs(change) >= 5:
        news = get_news(COMPANY_NAME)
        message_lines = [f"{STOCK}: {up_down}{abs(change):.2f}%"] + news
        message = "\n\n".join(message_lines)
        send_text_message(message)
    else:
        print(f"{STOCK} change is {change}%. No SMS sent.")
