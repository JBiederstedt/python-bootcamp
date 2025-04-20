import requests

response = requests.get("http://api.open-notify.org/iss-now.json")

data = response.json()["timestamp"]

print(data)
