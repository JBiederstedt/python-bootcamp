from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values()

TWILIO_SID = config["TWILIO_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_NUMBER = config["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER = config["TWILIO_TO_NUMBER"]

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
