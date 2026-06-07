import os
import json
import logging
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO, format="%(message)s")


class StructuredDataExtractor:
    def __init__(self):
        pass

    def extract(self, raw_html: str, url: str) -> dict:
        soup = BeautifulSoup(raw_html, "html.parser")

        data = {
            "scheme_name": "",
            "url": url,
            "expense_ratio": "",
            "exit_load": "",
            "aum": "",
            "nav": "",
            "min_sip": "",
            "rating": "",
            "benchmark": "",
            "about_fund": "",
            "fund_manager": "",
            "launch_date": "",
        }

        h1 = soup.find("h1")
        if h1:
            data["scheme_name"] = h1.get_text(strip=True)

        def find_value_next_to_label(label):
            elem = soup.find(string=re.compile(label, re.IGNORECASE))
            if elem:
                parent = elem.parent
                if parent:
                    grandparent = parent.parent
                    if grandparent:
                        text = grandparent.get_text(separator="|", strip=True)
                        parts = [p.strip() for p in text.split("|")]
                        for i, p in enumerate(parts):
                            if label.lower() in p.lower() and i + 1 < len(parts):
                                val = parts[i + 1]
                                if val and "fee payable" not in val.lower():
                                    return val
            return ""

        data["expense_ratio"] = find_value_next_to_label("Expense ratio")
        data["nav"] = find_value_next_to_label("NAV:")
        data["aum"] = find_value_next_to_label("Fund size")
        data["min_sip"] = find_value_next_to_label("Min. for SIP")
        data["rating"] = find_value_next_to_label("Rating")
        data["benchmark"] = find_value_next_to_label("Fund benchmark")
        data["launch_date"] = find_value_next_to_label("Launch Date")

        exit_load_elem = soup.find(
            string=re.compile("Exit Load for units", re.IGNORECASE)
        )
        if exit_load_elem:
            data["exit_load"] = exit_load_elem.strip()
        else:
            exit_load_elem = soup.find(string=re.compile("Exit load of", re.IGNORECASE))
            if exit_load_elem:
                data["exit_load"] = exit_load_elem.strip()

        # About text
        if data["scheme_name"]:
            about_text = ""
            for tag in soup.find_all(["div", "section"]):
                text = tag.get_text(separator=" ", strip=True)
                if text.startswith(f"About {data['scheme_name']}"):
                    about_text = text
                    # Usually the tag contains the whole text
                    break

            if about_text:
                # Clean up the trailing things like "; Investment Objective..."
                about_text = re.sub(r";\s*Investment Objective.*", "", about_text)
                data["about_fund"] = about_text.strip()

                # Extract Fund Manager from About text
                match = re.search(
                    r"(?:^|\.\s*)([A-Za-z\s,&]+?)\s+(?:is|are)\s+the\s+Current\s+Fund\s+Manager",
                    data["about_fund"],
                    re.IGNORECASE,
                )
                if match:
                    data["fund_manager"] = match.group(1).strip()

        return data


def process_all_html():
    extractor = StructuredDataExtractor()
    raw_dir = "data/raw"
    processed_dir = "data/processed"

    for filename in os.listdir(raw_dir):
        if filename.endswith(".html"):
            scheme_id = filename.replace(".html", "")
            raw_path = os.path.join(raw_dir, filename)
            json_path = os.path.join(processed_dir, f"{scheme_id}.json")

            with open(raw_path, "r", encoding="utf-8") as f:
                html = f.read()

            data = extractor.extract(html, f"https://groww.in/mutual-funds/{scheme_id}")

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logging.info(f"Structured {scheme_id}.json")


if __name__ == "__main__":
    process_all_html()
