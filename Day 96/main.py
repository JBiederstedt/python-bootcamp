import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configuration from environment
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("index.html", error="Please enter a search term.")
    try:
        response = requests.get(
            f"{API_URL}/search",
            params={"q": query, "api_key": API_KEY},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return render_template("index.html", error=str(e))
    return render_template("index.html", data=data, query=query)

if __name__ == "__main__":
    app.run(debug=True)
