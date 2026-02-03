"""
Quick script to inspect the HTML structure of the website
"""

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.indiascienceandtechnology.gov.in/organisations/state-st-organisations/all-st-institution?page=0"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Fetching page...")
response = requests.get(url, headers=headers, verify=False, timeout=30)
soup = BeautifulSoup(response.content, 'html.parser')

# Save HTML for inspection
with open('page_structure.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print("Saved HTML to page_structure.html")

# Find all links
all_links = soup.find_all('a', href=True)
print(f"\nTotal links found: {len(all_links)}")

# Find links that look like organizations
org_links = []
for link in all_links:
    href = link.get('href', '')
    text = link.get_text(strip=True)
    
    # Filter organization links
    if text and len(text) > 5 and 'http' in href:
        org_links.append({
            'name': text,
            'url': href
        })

print(f"Potential organization links: {len(org_links)}")

# Print first 10
print("\nFirst 10 organizations:")
for i, org in enumerate(org_links[:10], 1):
    print(f"{i}. {org['name']}")
    print(f"   {org['url']}")

# Check for pagination
pagination = soup.find_all(['a', 'li'], class_=lambda x: x and 'page' in str(x).lower())
print(f"\nPagination elements found: {len(pagination)}")





