# ---------------------------- IMPORTS ------------------------------- #

import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

# ---------------------------- CONFIG ------------------------------- #

load_dotenv()

CHROME_DRIVER_PATH    = os.getenv("CHROME_DRIVER_PATH")
TINDER_URL            = "https://tinder.com"
FACEBOOK_EMAIL        = os.getenv("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD     = os.getenv("FACEBOOK_PASSWORD")
SWIPES_PER_SESSION    = int(os.getenv("SWIPES_PER_SESSION", 100))
DELAY_BETWEEN_SWIPES  = float(os.getenv("DELAY_BETWEEN_SWIPES", 1.0))
POPUP_RETRY_LIMIT     = int(os.getenv("POPUP_RETRY_LIMIT", 3))

# ---------------------------- DRIVER SETUP ------------------------------- #

def init_driver():
    """
    Initialize and return a Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment to run headless
    service = Service(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

# ---------------------------- LOGIN VIA FACEBOOK ------------------------------- #

def login_with_facebook(driver):
    """
    Log into Tinder via Facebook using dummy credentials.
    """
    driver.get(TINDER_URL)
    wait = WebDriverWait(driver, 15)

    # Open login modal
    login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(),'Log in')]")
    ))
    login_btn.click()

    # Choose Facebook login
    fb_login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Log in with Facebook')]")
    ))
    fb_login_btn.click()

    # Wait for Facebook login window to appear
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

    # Switch to Facebook login window
    base_window = driver.window_handles[0]
    fb_window = driver.window_handles[1]
    driver.switch_to.window(fb_window)

    # Enter Facebook credentials
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(FACEBOOK_EMAIL)

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "pass"))
    )
    password_input.send_keys(FACEBOOK_PASSWORD)

    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "login"))
    )
    submit_btn.click()

    # Switch back to Tinder window
    driver.switch_to.window(base_window)

# ---------------------------- DISMISS POPUPS ------------------------------- #

def dismiss_popups(driver):
    """
    Dismiss location, notification, and cookie pop-ups.
    """
    wait = WebDriverWait(driver, 10)

    # Allow location
    try:
        allow_loc = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Allow')]")
        ))
        allow_loc.click()
    except TimeoutException:
        pass

    # Decline notifications
    try:
        not_interested = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Not interested')]")
        ))
        not_interested.click()
    except TimeoutException:
        pass

    # Accept cookies
    try:
        accept_cookies = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'I Accept')]")
        ))
        accept_cookies.click()
    except TimeoutException:
        pass

# ---------------------------- SWIPE ACTION ------------------------------- #

def swipe_right(driver):
    """
    Click the Like button, handling match pop-ups with a retry limit.
    """
    retries = 0
    while retries <= POPUP_RETRY_LIMIT:
        try:
            like_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Like']"))
            )
            like_btn.click()
            return  # successful swipe, exit function

        except (NoSuchElementException, TimeoutException):
            print("[-] Like button not found or not yet loaded.")
            return

        except ElementClickInterceptedException:
            if retries < POPUP_RETRY_LIMIT:
                try:
                    back_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Back to Tinder')]")
                    back_btn.click()
                    time.sleep(1)
                    retries += 1
                except Exception:
                    print("[-] Could not close match pop-up.")
                    return
            else:
                print(f"[-] Pop-up retry limit ({POPUP_RETRY_LIMIT}) reached.")
                return

# ---------------------------- MAIN ------------------------------- #

def main():
    # Validate configuration
    if not all([CHROME_DRIVER_PATH, FACEBOOK_EMAIL, FACEBOOK_PASSWORD]):
        raise RuntimeError("Missing required .env variables.")

    driver = init_driver()
    try:
        login_with_facebook(driver)
        dismiss_popups(driver)

        for _ in range(SWIPES_PER_SESSION):
            swipe_right(driver)
            time.sleep(DELAY_BETWEEN_SWIPES)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
