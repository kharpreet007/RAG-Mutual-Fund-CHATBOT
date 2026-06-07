import os
import re
import json
import logging
from src.scraper.scraper import GrowwScraper
from src.scraper.cleaner import HTMLCleaner

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_urls_from_markdown():
    urls = []
    markdown_path = "../docs/schemes.md"
    try:
        with open(markdown_path, "r", encoding="utf-8") as f:
            for line in f:
                if "groww.in/mutual-funds/" in line:
                    match = re.search(
                        r"\((https://groww\.in/mutual-funds/[^)]+)\)", line
                    )
                    if match:
                        urls.append(match.group(1))
    except Exception as e:
        logging.error(f"Failed to read {markdown_path}: {e}")
    return urls


def main():
    urls = get_urls_from_markdown()
    if not urls:
        logging.error("No URLs found in schemes.md")
        return

    # Remove duplicates just in case
    urls = list(set(urls))
    logging.info(f"Found {len(urls)} unique URLs to scrape.")

    scraper = GrowwScraper(delay=2.0)
    cleaner = HTMLCleaner()

    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    for i, url in enumerate(urls, 1):
        scheme_id = url.split("/")[-1]
        raw_path = os.path.join(raw_dir, f"{scheme_id}.html")
        processed_txt_path = os.path.join(processed_dir, f"{scheme_id}.txt")
        processed_json_path = os.path.join(processed_dir, f"{scheme_id}.json")

        # Skip if already processed JSON exists
        if os.path.exists(processed_json_path):
            logging.info(f"[{i}/{len(urls)}] Skipping {scheme_id}, already processed.")
            continue

        logging.info(f"[{i}/{len(urls)}] Processing {scheme_id}...")
        try:
            # Scrape or read existing HTML
            if os.path.exists(raw_path):
                with open(raw_path, "r", encoding="utf-8") as f:
                    html = f.read()
            else:
                html = scraper.fetch_page(url)
                with open(raw_path, "w", encoding="utf-8") as f:
                    f.write(html)

            # Clean
            clean_text = cleaner.clean_html(html)

            # Save as TXT
            with open(processed_txt_path, "w", encoding="utf-8") as f:
                f.write(clean_text)

            # Save as JSON
            data = {"scheme_id": scheme_id, "url": url, "text": clean_text}
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logging.info(
                f"Successfully processed {scheme_id} (Length: {len(clean_text)} chars)"
            )
        except Exception as e:
            logging.error(f"Failed processing {scheme_id}: {e}")


if __name__ == "__main__":
    main()
