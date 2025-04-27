import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
SCROLL_PAUSE_TIME = float(os.getenv("SCROLL_PAUSE_TIME", "1.0"))

# Initialize Selenium WebDriver
def init_driver():
    """
    Initialize and return a Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    service = Service(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

class GoogleFormFiller:
    """
    Uses Selenium to submit each listing to the Google Form.
    """
    def __init__(self):
        self.driver = init_driver()
        self.wait = WebDriverWait(self.driver, 15)

    def fill_form(self, listings, form_url: str):
        for address, price, link in listings:
            self.driver.get(form_url)
            time.sleep(SCROLL_PAUSE_TIME)

            address_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Address']"))
            )
            address_input.send_keys(address)

            price_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Price']")
            price_input.send_keys(price)

            link_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Link']")
            link_input.send_keys(link)

            submit_btn = self.driver.find_element(By.XPATH, "//span[text()='Submit']")
            submit_btn.click()

            try:
                another = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Submit another response'))
                )
                another.click()
            except TimeoutException:
                pass

    def quit(self):
        """
        Close the browser session.
        """
        self.driver.quit()
