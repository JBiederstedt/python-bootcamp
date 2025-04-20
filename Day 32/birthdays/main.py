# ---------------------------- IMPORTS ------------------------------- #

from dotenv import dotenv_values
import smtplib
import datetime as dt
import random
import pandas

# ---------------------------- CONSTANTS ------------------------------- #

config = dotenv_values()

my_email = config["MY_EMAIL"]
my_email_password = config["MY_EMAIL_PASSWORD"]
my_email_smtp = config["MY_EMAIL_SMTP"]

FILE_BIRTHDAYS = "birthdays.csv"
LETTER_DIR = "letter_templates"

# ---------------------------- SEND BIRTHDAY EMAIL ------------------------------- #

def send_birthday_email(name, to_email):
    random_birthday_letter = random.choice(["letter_1.txt", "letter_2.txt", "letter_3.txt"])
    letter_path = f"{LETTER_DIR}/{random_birthday_letter}"

    try:
        with open(letter_path, "r") as file:
            letter_contents = file.read()
            personalized_letter = letter_contents.replace("[NAME]", name)

        message = f"""\
Subject: Happy Birthday, {name} 🎉

{personalized_letter}
"""

        with smtplib.SMTP(my_email_smtp, 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_email_password)
            connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=message)

    except Exception as e:
        print(f"Something went wrong: {e}")

# ---------------------------- CHECK IF BIRTHDAY TODAY ------------------------------- #

date_today_str = dt.date.today().strftime("%m/%d")

birthdays_df = pandas.read_csv(FILE_BIRTHDAYS)

birthdays_df["birthday_str"] = (
    birthdays_df["month"].astype(str).str.zfill(2) + "/" +
    birthdays_df["day"].astype(str).str.zfill(2)
)

if date_today_str in birthdays_df["birthday_str"].values:
    birthdays = birthdays_df[birthdays_df["birthday_str"] == date_today_str]

    for _, row in birthdays.iterrows():
        send_birthday_email(row["name"], row["email"])
