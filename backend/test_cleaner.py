import logging
from bs4 import BeautifulSoup
import re

def clean_groww_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")

    tags_to_remove = ["script", "style", "nav", "footer", "header", "noscript", "svg", "button", "iframe", "form", "input", "meta"]
    for tag in soup(tags_to_remove):
        tag.decompose()

    elements_to_remove = []
    for element in soup.find_all(['div', 'section', 'ul', 'li', 'a']):
        classes = element.get('class')
        if classes:
            if isinstance(classes, list):
                class_str = " ".join(classes).lower()
            else:
                class_str = str(classes).lower()
            if any(x in class_str for x in ['header', 'footer', 'nav', 'sidebar', 'menu', 'dropdown', 'banner', 'disclaimer', 'quicklink']):
                elements_to_remove.append(element)

    for element in elements_to_remove:
        try:
            element.decompose()
        except Exception:
            pass

    body = soup.body if soup.body else soup
    text = body.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    with open("backend/data/raw/hdfc-liquid-fund-direct-growth.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    clean_text = clean_groww_html(html)
    print("START:")
    print(clean_text[:1000])
    print("\nEND:")
    print(clean_text[-1000:])
