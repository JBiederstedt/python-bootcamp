#!/usr/bin/env python3
"""
Scrapes Audible search results for "book" (Computers & Technology node)
and writes audiobook data to audible_books.csv.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.audible.com/search"
PARAMS = {
    "keywords": "book",
    "node": "18573211011",
    "page": 1
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
}
OUTPUT_CSV = "audible_books.csv"
PAGES_TO_SCRAPE = 5
DELAY_BETWEEN_REQUESTS = 1  # seconds

def parse_book_item(item):
    """Extracts data from one audiobook entry (a BeautifulSoup tag)."""
    def safe_select_text(selector):
        elem = item.select_one(selector)
        return elem.get_text(strip=True) if elem else ""

    title = safe_select_text("h3.bc-heading a") or safe_select_text("li.productListItem h3 a")
    authors = safe_select_text(".authorLabel .bc-pub-offscreen")
    narrators = safe_select_text(".narratorLabel .bc-pub-offscreen")
    length = safe_select_text(".runtimeLabel .bc-pub-offscreen")
    release_date = safe_select_text(".releaseDateLabel .bc-pub-offscreen")
    language = safe_select_text(".languageLabel .bc-pub-offscreen")

    # Ratings & count
    rating = ""
    count = ""
    overall = item.select_one(".ratingsLabel .bc-pub-offscreen")
    if overall:
        # e.g. "4.5 out of 5 stars"
        rating = overall.get_text(strip=True).split(" out")[0]
    count_elem = item.select_one(".ratingsLabel .bc-size-small")
    if count_elem:
        # e.g. "1,698 ratings"
        count = count_elem.get_text(strip=True).replace(" ratings", "")

    return {
        "Title": title,
        "Author(s)": authors,
        "Narrator(s)": narrators,
        "Length": length,
        "Release date": release_date,
        "Language": language,
        "Average rating": rating,
        "Ratings count": count
    }

def scrape():
    books = []
    for page in range(1, PAGES_TO_SCRAPE + 1):
        PARAMS["page"] = page
        print(f"Fetching page {page}...")
        resp = requests.get(BASE_URL, params=PARAMS, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Audible search results are listed in <li class="productListItem"> tags
        items = soup.select("li.productListItem, li.bc-list-item")
        if not items:
            print("  → No items found on this page (structure may have changed).")
            break

        for item in items:
            book = parse_book_item(item)
            # skip incomplete entries
            if book["Title"]:
                books.append(book)

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Write to CSV
    if books:
        print(f"Writing {len(books)} records to {OUTPUT_CSV}...")
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=books[0].keys())
            writer.writeheader()
            writer.writerows(books)
        print("Done.")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    scrape()
