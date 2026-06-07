import re
from bs4 import BeautifulSoup
import json

with open("backend/data/raw/hdfc-balanced-advantage-fund-direct-growth.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
    
scheme_name = soup.find('h1').get_text(strip=True)

for tag in soup.find_all(['h2', 'h3', 'h4', 'div', 'span']):
    text = tag.get_text(strip=True)
    if text.lower().startswith('about hdfc'):
        print(f"[{tag.name}] {text}")
