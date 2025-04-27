from dotenv import load_dotenv

load_dotenv()

import os
import sys
from zillow_scraper import ZillowScraper
from form_filler import GoogleFormFiller

# verify environment variables
required = ['CHROME_DRIVER_PATH', 'GOOGLE_FORM_URL']
missing = [v for v in required if not os.getenv(v)]
if missing:
    print(f"Error: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")

def main():
    # scrape listings
    scraper = ZillowScraper()
    try:
        listings = scraper.get_listings()
        if not listings:
            print("No listings found. Check selectors and site structure.")
            sys.exit(1)
    finally:
        scraper.close()

    # fill Google Form
    filler = GoogleFormFiller()
    try:
        filler.fill_form(listings, GOOGLE_FORM_URL)
    finally:
        filler.quit()

if __name__ == "__main__":
    main()
