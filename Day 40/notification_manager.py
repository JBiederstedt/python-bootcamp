from twilio.rest import Client
from dotenv import dotenv_values
import smtplib

config = dotenv_values()

TWILIO_SID = config["TWILIO_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_NUMBER = config["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER = config["TWILIO_TO_NUMBER"]

EMAIL = config["EMAIL_SENDER"]
PASSWORD = config["EMAIL_PASSWORD"]
SMTP = config["SMTP_ADDRESS"]

class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        print(f"SMS sent successfully: SID={message.sid}")

    def send_emails(self, recipient_list, subject, body):
        with smtplib.SMTP(SMTP, port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            for email in recipient_list:
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=email,
                    msg=f"Subject:{subject}\n\n{body}".encode("utf-8")
                )
        print("📧 Emails sent successfully.")
