"""
India Science and Technology Organizations Scraper
Extracts organization data from indiascienceandtechnology.gov.in
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_page(page_num):
    """Scrape a single page of organizations"""
    url = f"https://www.indiascienceandtechnology.gov.in/organisations/state-st-organisations/all-st-institution?page={page_num}"
    
    print(f"[PAGE {page_num}] Scraping...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        organizations = []
        
        # Find all organization entries
        # Adjust selectors based on actual HTML structure
        org_containers = soup.find_all(['div', 'article', 'section'], class_=lambda x: x and ('view-content' in str(x) or 'organization' in str(x).lower()))
        
        if not org_containers:
            # Try alternative selectors
            org_containers = soup.find_all(['div', 'li'], class_=lambda x: x and 'item' in str(x).lower())
        
        # If still not found, try finding all links in main content
        if not org_containers:
            main_content = soup.find(['main', 'div'], id=lambda x: x and 'content' in str(x).lower())
            if main_content:
                org_containers = main_content.find_all(['div', 'article'])
        
        print(f"   Found {len(org_containers)} potential containers")
        
        # Extract organization data
        for container in org_containers:
            org_data = {}
            
            # Find organization name and link
            link_tag = container.find('a', href=True)
            if link_tag:
                org_data['name'] = link_tag.get_text(strip=True)
                org_data['url'] = urljoin(url, link_tag['href'])
            
            # Find category/type
            category_tag = container.find(['span', 'div'], class_=lambda x: x and ('category' in str(x).lower() or 'type' in str(x).lower()))
            if category_tag:
                org_data['category'] = category_tag.get_text(strip=True)
            
            # Find location/state
            location_tag = container.find(['span', 'div'], class_=lambda x: x and ('location' in str(x).lower() or 'state' in str(x).lower()))
            if location_tag:
                org_data['location'] = location_tag.get_text(strip=True)
            
            # Find description
            desc_tag = container.find(['p', 'div'], class_=lambda x: x and 'description' in str(x).lower())
            if desc_tag:
                org_data['description'] = desc_tag.get_text(strip=True)
            
            if org_data.get('name') and org_data.get('url'):
                organizations.append(org_data)
        
        return organizations
        
    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] Error scraping page {page_num}: {e}")
        return []

def scrape_all_pages(max_pages=50):
    """Scrape all pages until no more data is found"""
    all_organizations = []
    page = 0
    consecutive_empty = 0
    
    print("Starting scraper for India S&T Organizations\n")
    
    while page < max_pages and consecutive_empty < 3:
        orgs = scrape_page(page)
        
        if orgs:
            all_organizations.extend(orgs)
            consecutive_empty = 0
            print(f"   [SUCCESS] Extracted {len(orgs)} organizations")
        else:
            consecutive_empty += 1
            print(f"   [WARNING] No organizations found (attempt {consecutive_empty}/3)")
        
        page += 1
        time.sleep(2)  # Be polite to the server
    
    return all_organizations

def categorize_organizations(organizations):
    """Organize organizations by category"""
    categorized = {}
    
    for org in organizations:
        category = org.get('category', 'Uncategorized')
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(org)
    
    return categorized

def save_data(organizations, categorized):
    """Save scraped data to JSON files"""
    
    # Save all organizations
    with open('all_organizations.json', 'w', encoding='utf-8') as f:
        json.dump(organizations, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] {len(organizations)} organizations to all_organizations.json")
    
    # Save categorized organizations
    with open('categorized_organizations.json', 'w', encoding='utf-8') as f:
        json.dump(categorized, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] {len(categorized)} categories to categorized_organizations.json")
    
    # Create summary
    summary = {
        'total_organizations': len(organizations),
        'total_categories': len(categorized),
        'categories': {cat: len(orgs) for cat, orgs in categorized.items()}
    }
    
    with open('summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] summary to summary.json")
    
    return summary

def main():
    """Main execution function"""
    print("=" * 60)
    print("India Science & Technology Organizations Scraper")
    print("=" * 60)
    
    # Scrape all pages
    organizations = scrape_all_pages(max_pages=50)
    
    if not organizations:
        print("\n[ERROR] No organizations found. The website structure may have changed.")
        print("   Please check the URL and HTML structure manually.")
        return
    
    # Categorize organizations
    categorized = categorize_organizations(organizations)
    
    # Save data
    summary = save_data(organizations, categorized)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)
    print(f"Total Organizations: {summary['total_organizations']}")
    print(f"Total Categories: {summary['total_categories']}")
    print("\nOrganizations by Category:")
    for category, count in sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count}")
    print("=" * 60)
    print("\n[COMPLETE] Scraping complete!")

if __name__ == "__main__":
    main()

