import re
from bs4 import BeautifulSoup
import json

with open("backend/data/raw/hdfc-balanced-advantage-fund-direct-growth.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
    
scheme_name = soup.find('h1').get_text(strip=True)
print("scheme_name:", scheme_name)

regex_str = f"About {scheme_name}"
print("regex_str:", regex_str)
about_header = soup.find(string=re.compile(regex_str, re.IGNORECASE))
print("about_header matched?", about_header is not None)

# what if we just find string containing 'About HDFC'
about_header2 = soup.find(string=re.compile(r"^About HDFC", re.IGNORECASE))
print("about_header2 matched?", about_header2 is not None)
if about_header2:
    print("Content:", about_header2.strip())
