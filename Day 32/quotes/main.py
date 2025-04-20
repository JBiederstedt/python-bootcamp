# ---------------------------- IMPORTS ------------------------------- #

from dotenv import dotenv_values
import smtplib
import datetime as dt
import random

# ---------------------------- CONSTANTS ------------------------------- #

config = dotenv_values()

my_email = config["MY_EMAIL"]
my_email_password = config["MY_EMAIL_PASSWORD"]
my_email_smtp = config["MY_EMAIL_SMTP"]
to_email = config["TO_EMAIL"]

FILE_QUOTES = "quotes.txt"

# ---------------------------- GET CURRENT WEEKDAY ------------------------------- #

# Returns weekday as int
weekday = dt.datetime.now().weekday()

# ---------------------------- SEND RANDOM QUOTE IF MONDAY ------------------------------- #

if weekday == 0:
    try:
        with open(FILE_QUOTES, "r") as file:
            quotes_list = [line.strip() for line in file if line.strip()]

            if quotes_list:
                random_quote = random.choice(quotes_list)
            else:
                random_quote = "No quotes available."
    except FileNotFoundError:
        random_quote = "No file found."

    # Two \n after Subject line
    message = f"""\
Subject: Motivational Monday 💪

{random_quote}
"""

    try:
        with smtplib.SMTP(my_email_smtp, 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_email_password)
            connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=message)
    except Exception as e:
        print(f"Connectivity issues. Email could not be sent.\nError: {e}")
