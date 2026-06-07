import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

url = "https://groww.in/mutual-funds/hdfc-silver-etf-fof-direct-growth"
response = requests.get(url, headers=HEADERS)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")
print("Title:", soup.title.string if soup.title else "No title")
print("Body text length:", len(soup.body.get_text(separator=' ', strip=True)) if soup.body else "No body")
