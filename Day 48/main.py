# ---------------------------- IMPORTS ------------------------------- #

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------------------------- CONFIG ------------------------------- #

GAME_URL       = "http://orteil.dashnet.org/experiments/cookie/"
CHECK_INTERVAL = 5         # seconds between upgrade checks
RUNTIME        = 5 * 60    # total run time in seconds (5 minutes)
MAX_WAIT       = 10        # max seconds to wait for elements

# ---------------------------- INITIALIZE DRIVER ------------------------------- #

def init_driver():
    """
    Initialize and return a Chrome WebDriver instance.
    Waits for key elements to be present before returning.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(GAME_URL)

    # Ensure main elements are loaded
    WebDriverWait(driver, MAX_WAIT).until(
        EC.element_to_be_clickable((By.ID, "cookie"))
    )
    WebDriverWait(driver, MAX_WAIT).until(
        EC.presence_of_element_located((By.ID, "store"))
    )
    return driver

# ---------------------------- BOT LOGIC ------------------------------- #

def play_game(driver):
    """
    Main loop: click the cookie and purchase upgrades periodically.
    After runtime expires, print the cookies per second rate.
    Uses time.sleep(CHECK_INTERVAL) to pause between checks.
    """
    # Track overall start and last upgrade-check times
    start_time = time.time()
    end_time = start_time + RUNTIME
    last_check = start_time

    # Loop until total runtime expires
    while time.time() < end_time:
        # Attempt cookie click, ignore transient errors
        try:
            cookie = WebDriverWait(driver, MAX_WAIT).until(
                EC.element_to_be_clickable((By.ID, "cookie"))
            )
            cookie.click()
        except Exception:
            pass

        # If interval elapsed, perform upgrade logic
        current_time = time.time()
        if current_time - last_check >= CHECK_INTERVAL:
            last_check = current_time  # reset interval timer

            # Fetch current cookie count
            money_text = WebDriverWait(driver, MAX_WAIT).until(
                EC.presence_of_element_located((By.ID, "money"))
            ).text
            money = int(money_text.replace(",", ""))

            # Fetch upgrade items dynamically
            items = WebDriverWait(driver, MAX_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#store div"))
            )
            item_ids = [item.get_attribute("id") for item in items]

            # Map prices to item IDs
            prices = {}
            for item_id in item_ids:
                elem = driver.find_element(By.ID, item_id)
                text = elem.text
                if " - " in text:
                    cost_str = text.split(" - ")[1].strip()
                    price = int(cost_str.replace(",", ""))
                    prices[price] = item_id

            # Purchase the most expensive affordable upgrade
            affordable = {p: i for p, i in prices.items() if p <= money}
            if affordable:
                best_price = max(affordable)
                WebDriverWait(driver, MAX_WAIT).until(
                    EC.element_to_be_clickable((By.ID, affordable[best_price]))
                ).click()

            # Pause precisely before next interval
            time.sleep(CHECK_INTERVAL)

    # After runtime, print cookies per second
    cps = WebDriverWait(driver, MAX_WAIT).until(
        EC.presence_of_element_located((By.ID, "cps"))
    ).text
    print(f"Cookies per second: {cps}")

# ---------------------------- MAIN ------------------------------- #

def main():
    """
    Entry point: initialize driver and start the bot.
    """
    driver = init_driver()
    try:
        play_game(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
