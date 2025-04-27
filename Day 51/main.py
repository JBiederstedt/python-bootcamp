# ---------------------------- IMPORTS ------------------------------- #

import os
import sys
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ---------------------------- CONFIGURATION --------------------------- #

load_dotenv()

CHROME_DRIVER_PATH    = os.getenv("CHROME_DRIVER_PATH")
TWITTER_EMAIL         = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD      = os.getenv("TWITTER_PASSWORD")
# Twitter handle of the ISP (without @)
PROVIDER_HANDLE       = os.getenv("PROVIDER_HANDLE", "Provider")
# Promised internet speeds from your ISP
PROMISED_DOWN         = float(os.getenv("PROMISED_DOWN", 150.0))
PROMISED_UP           = float(os.getenv("PROMISED_UP", 10.0))
# URLs for speed test and Twitter login
SPEEDTEST_URL         = "https://www.speedtest.net"
TWITTER_LOGIN_URL     = "https://twitter.com/login"
# Maximum wait time for speed test results (in seconds)
WAIT_LONG             = 120

# ---------------------------- DRIVER SETUP ----------------------------- #

def init_driver():
    """
    Initialize and return a Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment the next line to run Chrome in headless mode
    # options.add_argument("--headless")
    service = Service(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

# ---------------------------- BOT CLASS -------------------------------- #

class InternetSpeedTwitterBot:
    """
    Bot that measures internet speed and tweets the results.
    """

    def __init__(self):
        # Initialize the WebDriver and speed attributes
        self.driver = init_driver()
        self.down = 0.0
        self.up = 0.0

    def get_internet_speed(self):
        """
        Run a speed test and store download/upload speeds.
        """
        self.driver.get(SPEEDTEST_URL)
        wait = WebDriverWait(self.driver, 30)

        # Click the 'Go' button to start the test
        try:
            go_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".start-button a")
            ))
            go_btn.click()
        except TimeoutException:
            print("[-] Speedtest 'Go' button not found.")
            return

        # Wait for the test to complete
        time.sleep(WAIT_LONG)

        # Extract download and upload speeds
        try:
            self.down = float(wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".download-speed")
            )).text)
            self.up = float(wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".upload-speed")
            )).text)
            print(f"[+] Measured: Download={self.down} Mbps, Upload={self.up} Mbps")
        except (TimeoutException, ValueError):
            print("[-] Error reading speed results.")

    def tweet_at_provider(self):
        """
        Log in to Twitter and post a tweet with the speed test results.
        """
        self.driver.get(TWITTER_LOGIN_URL)
        wait = WebDriverWait(self.driver, 30)

        # Perform login
        try:
            email_input = wait.until(EC.visibility_of_element_located(
                (By.NAME, "session[username_or_email]")
            ))
            email_input.send_keys(TWITTER_EMAIL)
            pw_input = self.driver.find_element(By.NAME, "session[password]")
            pw_input.send_keys(TWITTER_PASSWORD)
            pw_input.submit()
        except (TimeoutException, NoSuchElementException):
            print("[-] Twitter login failed.")
            return

        # Wait for tweet composition field
        try:
            tweet_box = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[aria-label='Tweet text']")
            ))
            tweet_message = (
                f"Hey @{PROVIDER_HANDLE}, my speedtest shows {self.down} Mbps down / {self.up} Mbps up, "
                f"but you promised {PROMISED_DOWN} Mbps down / {PROMISED_UP} Mbps up. "
                "#internet #speedtest"
            )
            tweet_box.send_keys(tweet_message)
            send_btn = self.driver.find_element(
                By.XPATH, "//div[@data-testid='tweetButtonInline']"
            )
            send_btn.click()
            print("[+] Tweet sent successfully.")
        except (TimeoutException, NoSuchElementException):
            print("[-] Error composing or sending tweet.")

    def quit(self):
        """
        Close the WebDriver session.
        """
        self.driver.quit()

# ---------------------------- MAIN FUNCTION ----------------------------- #

def main():
    # Ensure required environment variables are set
    missing = []
    for var in ["CHROME_DRIVER_PATH", "TWITTER_EMAIL", "TWITTER_PASSWORD", "PROVIDER_HANDLE"]:
        if not os.getenv(var):
            missing.append(var)
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    bot = InternetSpeedTwitterBot()
    try:
        bot.get_internet_speed()
        bot.tweet_at_provider()
    finally:
        bot.quit()

if __name__ == "__main__":
    main()
