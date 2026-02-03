"""
Improved India Science and Technology Organizations Scraper
Extracts organization data from table structure
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
    """Scrape a single page of organizations from table"""
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
        
        # Find the table
        table = soup.find('table')
        if not table:
            print(f"   [WARNING] No table found on page {page_num}")
            return []
        
        # Find all rows in tbody
        tbody = table.find('tbody')
        if not tbody:
            print(f"   [WARNING] No tbody found on page {page_num}")
            return []
        
        rows = tbody.find_all('tr')
        print(f"   Found {len(rows)} rows")
        
        for row in rows:
            org_data = {}
            cells = row.find_all('td')
            
            if len(cells) >= 4:
                # Cell 0: Name and URL
                name_cell = cells[0]
                link = name_cell.find('a')
                if link:
                    org_data['name'] = link.get_text(strip=True)
                    org_data['url'] = link.get('href', '')
                
                # Cell 1: Category
                category_cell = cells[1]
                org_data['category'] = category_cell.get_text(strip=True)
                
                # Cell 2: State
                state_cell = cells[2]
                org_data['state'] = state_cell.get_text(strip=True)
                
                # Cell 3: District/City
                city_cell = cells[3]
                org_data['city'] = city_cell.get_text(strip=True)
                
                # Cell 4: Contact Info (if exists)
                if len(cells) >= 5:
                    contact_cell = cells[4]
                    org_data['contact'] = contact_cell.get_text(strip=True)
                
                if org_data.get('name'):
                    organizations.append(org_data)
        
        return organizations
        
    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] Error scraping page {page_num}: {e}")
        return []

def scrape_all_pages(max_pages=200):
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
            print(f"   [SUCCESS] Extracted {len(orgs)} organizations (Total: {len(all_organizations)})")
        else:
            consecutive_empty += 1
            print(f"   [WARNING] No organizations found (attempt {consecutive_empty}/3)")
        
        page += 1
        time.sleep(1)  # Be polite to the server
    
    return all_organizations

def categorize_organizations(organizations):
    """Organize organizations by category and state"""
    by_category = {}
    by_state = {}
    
    for org in organizations:
        # By category
        category = org.get('category', 'Uncategorized')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(org)
        
        # By state
        state = org.get('state', 'Unknown')
        if state not in by_state:
            by_state[state] = []
        by_state[state].append(org)
    
    return {
        'by_category': by_category,
        'by_state': by_state
    }

def save_data(organizations, categorized):
    """Save scraped data to JSON files"""
    
    # Save all organizations
    with open('all_organizations.json', 'w', encoding='utf-8') as f:
        json.dump(organizations, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] {len(organizations)} organizations to all_organizations.json")
    
    # Save by category
    with open('organizations_by_category.json', 'w', encoding='utf-8') as f:
        json.dump(categorized['by_category'], f, indent=2, ensure_ascii=False)
    print(f"[SAVED] {len(categorized['by_category'])} categories to organizations_by_category.json")
    
    # Save by state
    with open('organizations_by_state.json', 'w', encoding='utf-8') as f:
        json.dump(categorized['by_state'], f, indent=2, ensure_ascii=False)
    print(f"[SAVED] {len(categorized['by_state'])} states to organizations_by_state.json")
    
    # Create summary
    summary = {
        'total_organizations': len(organizations),
        'total_categories': len(categorized['by_category']),
        'total_states': len(categorized['by_state']),
        'categories': {cat: len(orgs) for cat, orgs in categorized['by_category'].items()},
        'states': {state: len(orgs) for state, orgs in categorized['by_state'].items()}
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
    organizations = scrape_all_pages(max_pages=200)
    
    if not organizations:
        print("\n[ERROR] No organizations found. The website structure may have changed.")
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
    print(f"Total States: {summary['total_states']}")
    
    print("\nTop 10 Categories:")
    for i, (category, count) in enumerate(sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"  {i}. {category}: {count}")
    
    print("\nTop 10 States:")
    for i, (state, count) in enumerate(sorted(summary['states'].items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"  {i}. {state}: {count}")
    
    print("=" * 60)
    print("\n[COMPLETE] Scraping complete!")

if __name__ == "__main__":
    main()





