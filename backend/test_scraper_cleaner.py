import logging
from src.scraper.scraper import GrowwScraper
from src.scraper.cleaner import HTMLCleaner

logging.basicConfig(level=logging.INFO)

url = "https://groww.in/mutual-funds/hdfc-silver-etf-fof-direct-growth"
scraper = GrowwScraper()
html = scraper.fetch_page(url)

cleaner = HTMLCleaner()
clean_text = cleaner.clean_html(html)

print(f"Cleaned Text Length: {len(clean_text)}")
print(f"First 500 chars: {clean_text[:500]}")
