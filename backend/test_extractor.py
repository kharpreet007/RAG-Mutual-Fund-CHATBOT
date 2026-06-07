from bs4 import BeautifulSoup
import json
import re

def extract_structured_data(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    data = {}
    
    # Scheme Name
    h1 = soup.find('h1')
    if h1:
        data['scheme_name'] = h1.get_text(strip=True)
        
    # Let's find the main "About" paragraph
    # It usually starts with "About <Scheme Name>"
    if 'scheme_name' in data:
        about_title = f"About {data['scheme_name']}"
        about_header = soup.find(string=re.compile(about_title, re.IGNORECASE))
        if about_header:
            parent = about_header.parent
            # The actual text is often in the same div or the next div
            grandparent = parent.parent
            if grandparent:
                data['about_fund'] = grandparent.get_text(separator=' ', strip=True)

    def find_value_next_to_label(label):
        elem = soup.find(string=re.compile(label, re.IGNORECASE))
        if elem:
            parent = elem.parent
            if parent:
                grandparent = parent.parent
                if grandparent:
                    text = grandparent.get_text(separator='|', strip=True)
                    parts = [p.strip() for p in text.split('|')]
                    for i, p in enumerate(parts):
                        if label.lower() in p.lower() and i + 1 < len(parts):
                            # Ensure the next part isn't just an icon or empty
                            val = parts[i+1]
                            if val and len(val) > 0 and "A fee payable" not in val:
                                return val
        return None

    data['expense_ratio'] = find_value_next_to_label('Expense ratio')
    data['nav'] = find_value_next_to_label('NAV:')
    data['aum'] = find_value_next_to_label('Fund size (AUM)')
    if not data['aum']:
        data['aum'] = find_value_next_to_label('Total AUM')
        
    data['min_sip'] = find_value_next_to_label('Min. for SIP')
    data['rating'] = find_value_next_to_label('Rating')
    data['benchmark'] = find_value_next_to_label('Fund benchmark')
    data['launch_date'] = find_value_next_to_label('Launch Date')
    
    exit_load_elem = soup.find(string=re.compile('Exit Load for units', re.IGNORECASE))
    if exit_load_elem:
        data['exit_load'] = exit_load_elem.strip()
    else:
        exit_load_elem = soup.find(string=re.compile('Exit load of', re.IGNORECASE))
        if exit_load_elem:
            data['exit_load'] = exit_load_elem.strip()
            
    # Fund Managers - find the section
    manager_section = soup.find(string=re.compile('Fund management', re.IGNORECASE))
    if manager_section:
        mgr_parent = manager_section.parent.parent
        if mgr_parent:
            mgr_text = mgr_parent.get_text(separator='|', strip=True)
            # managers are usually listed there. We can just keep the whole block or regex
            # Or rely on the 'about_fund' section which says "Anil Bamboli is the Current Fund Manager..."
            pass
            
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    extract_structured_data("backend/data/raw/hdfc-balanced-advantage-fund-direct-growth.html")
    print("---")
    extract_structured_data("backend/data/raw/hdfc-liquid-fund-direct-growth.html")
