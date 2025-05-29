import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Load configuration from .env
load_dotenv()
PRODUCT_URL = os.getenv("PRODUCT_URL")
API_URL     = os.getenv("API_URL")
API_KEY     = os.getenv("API_KEY")

def is_in_stock(driver):
    driver.get(PRODUCT_URL)
    time.sleep(5)  # give the page time to load
    try:
        # Adjust the selector to whatever your site uses for "out of stock"
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add to cart')]")
        return True
    except NoSuchElementException:
        return False

def notify_back_in_stock():
    payload = {
        "api_key": API_KEY,
        "message": f"✅ Product is back in stock! {PRODUCT_URL}"
    }
    resp = requests.post(API_URL, json=payload)
    if resp.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {resp.status_code} {resp.text}")

def main():
    # Initialize headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        if is_in_stock(driver):
            print("Item is in stock! Sending notification…")
            notify_back_in_stock()
        else:
            print("Still out of stock. Try again later.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
