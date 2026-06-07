import requests
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


class GrowwScraper:
    """Scraper for fetching mutual fund pages from Groww."""

    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_page(self, url: str) -> str:
        """Fetches the HTML content of the given URL.

        Args:
            url (str): The URL of the scheme page to scrape.

        Returns:
            str: The raw HTML content of the page.

        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # Politeness delay to avoid rate limiting
            time.sleep(self.delay)

            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
