import os
import requests
from bs4 import BeautifulSoup

ZILLOW_CLONE_URL = os.getenv(
    "ZILLOW_CLONE_URL",
    "https://appbrewery.github.io/Zillow-Clone/"
)
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
ACCEPT_LANGUAGES = os.getenv(
    "ACCEPT_LANGUAGES",
    "en-US,en;q=0.9"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGES
}

class ZillowScraper:
    """
    Scrapes listings from the Zillow-Clone site using BeautifulSoup.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def clean_price(self, raw_price: str) -> str:
        price = raw_price.replace("+", "").replace("/mo", "").strip()
        return price.split()[0]

    def clean_address(self, raw_address: str) -> str:
        return raw_address.replace("\n", " ").replace("|", "").strip()

    def get_listings(self):
        response = self.session.get(ZILLOW_CLONE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select("div.list-card")
        listings = []
        for card in cards:
            link_tag = card.find("a", href=True)
            raw_link = link_tag["href"]
            link = (
                raw_link
                if raw_link.startswith("http")
                else ZILLOW_CLONE_URL.rstrip("/") + raw_link
            )

            raw_price = card.select_one(".list-card-price").get_text()
            price = self.clean_price(raw_price)

            raw_address = card.select_one(".list-card-addr").get_text()
            address = self.clean_address(raw_address)

            listings.append((address, price, link))
        return listings

    def close(self):
        """
        Close the underlying HTTP session.
        """
        self.session.close()
