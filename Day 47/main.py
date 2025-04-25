# ---------------------------- IMPORTS ------------------------------- #

import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------------- CONFIG ------------------------------- #

load_dotenv()

SMTP_ADDRESS   = os.getenv("SMTP_ADDRESS")
SMTP_PORT      = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS  = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TARGET_PRICE   = float(os.getenv("TARGET_PRICE"))
PRODUCT_URL    = os.getenv("PRODUCT_URL")  # must be set in .env

# ---------------------------- HEADERS ------------------------------- #

# Copied from https://httpbin.org/headers (Host & X-Amzn-Trace-Id removed)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/112.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# ---------------------------- SCRAPE AMAZON ------------------------------- #

def get_product_info(url):
    """
    Fetch the live Amazon product page and return (title, price).
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    # Uncomment for debugging raw HTML
    # debug_soup = BeautifulSoup(response.content, "html.parser")
    # print(debug_soup.prettify())

    soup = BeautifulSoup(response.content, "lxml")

    # Get product title
    title_el = soup.find(id="productTitle")
    if not title_el:
        raise Exception("Product title not found.")
    title = title_el.get_text().strip()

    # Get product price from common Amazon ID patterns
    price = None
    for pid in ("priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice"):
        pe = soup.find(id=pid)
        if pe:
            raw = pe.get_text().strip()
            price = float(raw.replace("$", "").replace(",", ""))
            break

    if price is None:
        raise Exception("Product price not found.")

    return title, price

# ---------------------------- EMAIL ALERT ------------------------------- #

def send_price_alert(title, current_price, product_url):
    """
    Build and send an email alert with product title, current price, and link.
    """
    subject = f"Price Alert: {title}"
    body = (
        f"The price for '{title}' has dropped below your target of ${TARGET_PRICE:.2f}!\n\n"
        f"Current price: ${current_price:.2f}\n"
        f"Buy here: {product_url}"
    )

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT) as conn:
        conn.starttls()
        conn.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        conn.send_message(msg)

# ---------------------------- MAIN ------------------------------- #

def main():
    if not PRODUCT_URL:
        raise RuntimeError("PRODUCT_URL not set in .env")

    title, current_price = get_product_info(PRODUCT_URL)
    print(f"Product: {title}")
    print(f"Checked price: ${current_price:.2f}")

    if current_price < TARGET_PRICE:
        print("Price is below target! Sending email...")
        send_price_alert(title, current_price, PRODUCT_URL)
    else:
        print("Price is still above target. No email sent.")

if __name__ == "__main__":
    main()
