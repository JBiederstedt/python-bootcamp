# ---------------------------- IMPORTS ------------------------------- #

import os
import sys
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException
)

# ---------------------------- CONFIG --------------------------- #

load_dotenv()

CHROME_DRIVER_PATH       = os.getenv("CHROME_DRIVER_PATH")
INSTAGRAM_USERNAME       = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD       = os.getenv("INSTAGRAM_PASSWORD")
TARGET_ACCOUNT           = os.getenv("TARGET_ACCOUNT")
# How many followers to load/attempt to follow
NUM_FOLLOWERS_TO_FOLLOW  = int(os.getenv("NUM_FOLLOWERS_TO_FOLLOW", "50"))
# Pause between scrolls and clicks to seem more human
SCROLL_PAUSE_TIME        = float(os.getenv("SCROLL_PAUSE_TIME", "1.0"))

INSTAGRAM_BASE_URL       = "https://www.instagram.com/"
INSTAGRAM_LOGIN_URL      = INSTAGRAM_BASE_URL + "accounts/login/"

# ---------------------------- DRIVER SETUP ----------------------------- #

def init_driver():
    """
    Initialize and return a Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # run in headless mode if desired
    service = Service(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

# ---------------------------- BOT CLASS -------------------------------- #

class InstaFollower:
    def __init__(self):
        self.driver = init_driver()
        self.follow_buttons = []

    def login(self):
        """
        Log in to Instagram, dismissing any pop-ups.
        """
        self.driver.get(INSTAGRAM_LOGIN_URL)
        wait = WebDriverWait(self.driver, 15)

        # dismiss cookie banner if present
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Accept')]")
            ))
            cookie_btn.click()
        except TimeoutException:
            pass

        # enter credentials and submit
        username_input = wait.until(EC.visibility_of_element_located(
            (By.NAME, "username")
        ))
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys(INSTAGRAM_USERNAME)
        password_input.send_keys(INSTAGRAM_PASSWORD)
        password_input.submit()

        # dismiss "Save Your Login Info?" popup
        try:
            not_now = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Not Now')]")
            ))
            not_now.click()
        except TimeoutException:
            pass

        # dismiss "Turn on Notifications" popup
        try:
            not_now2 = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Not Now')]")
            ))
            not_now2.click()
        except TimeoutException:
            pass

    def find_followers(self):
        """
        Navigate to target account and load followers in the popup.
        """
        self.driver.get(f"{INSTAGRAM_BASE_URL}{TARGET_ACCOUNT}/")
        wait = WebDriverWait(self.driver, 15)

        # open followers modal
        followers_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href, '/followers/')]")
        ))
        followers_link.click()

        # the followers list is inside a <ul> within the dialog
        modal = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[role='dialog'] ul")
        ))

        # scroll until enough followers are loaded
        loaded = []
        while len(loaded) < NUM_FOLLOWERS_TO_FOLLOW:
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", modal
            )
            time.sleep(SCROLL_PAUSE_TIME)
            loaded = modal.find_elements(By.TAG_NAME, "li")

        # collect the follow buttons
        self.follow_buttons = modal.find_elements(By.CSS_SELECTOR, "button")

    def follow(self):
        """
        Click each follow button, handling any intercepting pop-ups.
        """
        for btn in self.follow_buttons[:NUM_FOLLOWERS_TO_FOLLOW]:
            try:
                btn.click()
                # Pause for a random 1–2 seconds to mimic human behavior
                time.sleep(random.uniform(1, 2))
            except ElementClickInterceptedException:
                # dismiss "Unfollow?" confirm dialog
                try:
                    cancel = self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Cancel')]"
                    )
                    cancel.click()
                except NoSuchElementException:
                    pass

    def quit(self):
        """Close the browser session."""
        self.driver.quit()

# ---------------------------- MAIN ----------------------------- #

def main():
    # ensure all required env vars are set
    missing = [v for v in [
        "CHROME_DRIVER_PATH",
        "INSTAGRAM_USERNAME",
        "INSTAGRAM_PASSWORD",
        "TARGET_ACCOUNT"
    ] if not os.getenv(v)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    bot = InstaFollower()
    try:
        bot.login()
        bot.find_followers()
        bot.follow()
    finally:
        bot.quit()

if __name__ == "__main__":
    main()
