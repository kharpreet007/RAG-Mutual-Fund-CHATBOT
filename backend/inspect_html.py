from bs4 import BeautifulSoup
import json

def extract_scheme_data(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    data = {}
    
    # h1 is usually the scheme name
    h1 = soup.find('h1')
    if h1:
        data['scheme_name'] = h1.get_text(strip=True)
        
    # We can look for divs or tables containing keys like "Expense ratio", "Exit load", "AUM", "NAV"
    # Usually they are in key-value pairs in divs next to each other
    
    # Let's just find elements containing these texts and print their parent/siblings to understand the DOM
    keywords = ["Expense ratio", "Exit load", "Fund size (AUM)", "NAV", "Min. for SIP", "Rating", "Launch Date", "Fund benchmark", "Fund Manager"]
    
    found_data = {}
    
    for text in soup.stripped_strings:
        for kw in keywords:
            if kw.lower() in text.lower() and len(text) < 50:
                # Find the element containing this text
                element = soup.find(lambda tag: tag.name and tag.string and text in tag.string)
                if element:
                    parent = element.parent
                    # usually the value is in the next sibling or somewhere inside the parent
                    found_data[text] = parent.get_text(separator=" | ", strip=True)

    print(json.dumps(found_data, indent=2))

if __name__ == "__main__":
    extract_scheme_data("backend/data/raw/hdfc-balanced-advantage-fund-direct-growth.html")
