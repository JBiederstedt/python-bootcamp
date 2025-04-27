# ---------------------------- IMPORTS ------------------------------- #

import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ---------------------------- CONFIG ------------------------------- #

load_dotenv()
LINKEDIN_EMAIL    = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
JOB_URL           = os.getenv("JOB_URL")       # LinkedIn search URL with filters applied
PHONE_NUMBER      = os.getenv("PHONE_NUMBER")  # Mobile number for Easy Apply

# ---------------------------- HELPERS ------------------------------- #

def wait_for_element(driver, by, value, timeout=10):
    """
    Wait until the specified element is present in the DOM and visible.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

# ---------------------------- LOGIN FUNCTION ------------------------------- #

def login(driver):
    """
    Log in to LinkedIn using provided credentials.
    """
    driver.get("https://www.linkedin.com/login")
    # Wait for login inputs
    wait_for_element(driver, By.ID, "username")
    wait_for_element(driver, By.ID, "password")

    # Enter credentials and submit
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD, Keys.ENTER)
    # Wait for the top nav bar to confirm login
    wait_for_element(driver, By.ID, "global-nav-search")

# ---------------------------- JOB APPLICATION FUNCTION ------------------------------- #

def apply_to_jobs():
    """
    Open job listings page, iterate through each job, and perform Easy Apply if available.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 1. Log in to LinkedIn
    login(driver)

    # 2. Open job search page
    driver.get(JOB_URL)
    # Wait for job cards to load
    wait_for_element(driver, By.CSS_SELECTOR, ".job-card-container--clickable")

    # 3. Collect all job cards available on the page
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
    print(f"Found {len(job_cards)} jobs to process.")

    # 4. Loop through each job listing and attempt Easy Apply
    for index, job_card in enumerate(job_cards, start=1):
        try:
            print(f"Processing job {index}...")
            job_card.click()
            # Wait for the Easy Apply button or skip after timeout
            easy_apply_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-button--top-card"))
            )
            easy_apply_btn.click()

            # Wait for application modal
            wait_for_element(driver, By.CSS_SELECTOR, "div.jobs-easy-apply-modal")

            # Fill phone number if required
            try:
                phone_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Telephone number']")
                if not phone_input.get_attribute("value"):
                    phone_input.send_keys(PHONE_NUMBER)
            except NoSuchElementException:
                pass  # Phone input not present

            # Submit application
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
            submit_btn.click()

            # Wait for confirmation and then close
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']"))
            )
            close_btn.click()
            print(f"Applied to job {index} successfully.")

        except (NoSuchElementException, TimeoutException):
            print(f"Skipping job {index}: Easy Apply not available or multi-step required.")
            continue

    driver.quit()

# ---------------------------- MAIN ------------------------------- #

if __name__ == "__main__":
    apply_to_jobs()
