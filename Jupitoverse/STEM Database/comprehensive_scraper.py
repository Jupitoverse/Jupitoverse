"""
Comprehensive India Science and Technology Portal Scraper
Extracts data from all major sections of indiascienceandtechnology.gov.in
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import urllib3
import os

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.indiascienceandtechnology.gov.in"

class ISTIPortalScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.verify = False
        
    def fetch_page(self, url):
        """Fetch a page with error handling"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"   [ERROR] Failed to fetch {url}: {e}")
            return None
    
    def scrape_organizations(self, max_pages=200):
        """Scrape all organizations"""
        print("\n[SECTION] Scraping Organizations...")
        organizations = []
        
        for page in range(max_pages):
            url = f"{BASE_URL}/organisations/state-st-organisations/all-st-institution?page={page}"
            soup = self.fetch_page(url)
            
            if not soup:
                break
            
            table = soup.find('table')
            if not table:
                break
            
            tbody = table.find('tbody')
            if not tbody:
                break
            
            rows = tbody.find_all('tr')
            if not rows:
                break
            
            page_orgs = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    org_data = {}
                    
                    # Name and URL
                    link = cells[0].find('a')
                    if link:
                        org_data['name'] = link.get_text(strip=True)
                        org_data['url'] = link.get('href', '')
                    
                    # Category
                    org_data['category'] = cells[1].get_text(strip=True)
                    
                    # State
                    org_data['state'] = cells[2].get_text(strip=True)
                    
                    # City
                    org_data['city'] = cells[3].get_text(strip=True)
                    
                    # Contact (if exists)
                    if len(cells) >= 5:
                        org_data['contact'] = cells[4].get_text(strip=True)
                    
                    if org_data.get('name'):
                        page_orgs.append(org_data)
            
            if page_orgs:
                organizations.extend(page_orgs)
                print(f"   Page {page}: {len(page_orgs)} orgs (Total: {len(organizations)})")
            else:
                print(f"   Page {page}: No data, stopping")
                break
            
            time.sleep(0.5)
        
        print(f"   [DONE] Total organizations: {len(organizations)}")
        return organizations
    
    def scrape_science_centres(self):
        """Scrape science centres"""
        print("\n[SECTION] Scraping Science Centres...")
        centres = []
        
        url = f"{BASE_URL}/organisations/science-centres"
        soup = self.fetch_page(url)
        
        if soup:
            # Find all centre links
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                
                if 'science-centres' in href and text and len(text) > 10:
                    centres.append({
                        'name': text,
                        'url': urljoin(BASE_URL, href),
                        'type': 'Science Centre'
                    })
        
        print(f"   [DONE] Total centres: {len(centres)}")
        return centres
    
    def scrape_research_labs(self):
        """Scrape research labs"""
        print("\n[SECTION] Scraping Research Labs...")
        labs = []
        
        # Try different lab URLs
        lab_urls = [
            f"{BASE_URL}/organisations/research-labs",
            f"{BASE_URL}/organisations/central-sector-labs-research-institutions",
        ]
        
        for url in lab_urls:
            soup = self.fetch_page(url)
            if soup:
                table = soup.find('table')
                if table:
                    rows = table.find_all('tr')[1:]  # Skip header
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            link = cells[0].find('a')
                            if link:
                                labs.append({
                                    'name': link.get_text(strip=True),
                                    'url': link.get('href', ''),
                                    'category': cells[1].get_text(strip=True) if len(cells) > 1 else 'Research Lab'
                                })
        
        print(f"   [DONE] Total labs: {len(labs)}")
        return labs
    
    def scrape_universities(self):
        """Scrape universities and educational institutions"""
        print("\n[SECTION] Scraping Universities...")
        universities = []
        
        url = f"{BASE_URL}/organisations/higher-education-sector"
        soup = self.fetch_page(url)
        
        if soup:
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        link = cells[0].find('a')
                        if link:
                            universities.append({
                                'name': link.get_text(strip=True),
                                'url': link.get('href', ''),
                                'state': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                                'type': 'University'
                            })
        
        print(f"   [DONE] Total universities: {len(universities)}")
        return universities
    
    def scrape_funding_schemes(self):
        """Scrape funding schemes"""
        print("\n[SECTION] Scraping Funding Schemes...")
        schemes = []
        
        url = f"{BASE_URL}/nurturing-minds/funding-opportunities"
        soup = self.fetch_page(url)
        
        if soup:
            # Find scheme links
            content = soup.find(['div', 'main'], class_=lambda x: x and 'content' in str(x).lower())
            if content:
                links = content.find_all('a', href=True)
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if text and len(text) > 10 and 'funding' in href.lower():
                        schemes.append({
                            'name': text,
                            'url': urljoin(BASE_URL, href),
                            'type': 'Funding Scheme'
                        })
        
        print(f"   [DONE] Total schemes: {len(schemes)}")
        return schemes
    
    def scrape_programs(self):
        """Scrape programs and initiatives"""
        print("\n[SECTION] Scraping Programs...")
        programs = []
        
        program_urls = [
            f"{BASE_URL}/nurturing-minds/programs",
            f"{BASE_URL}/nurturing-minds/fellowships",
            f"{BASE_URL}/nurturing-minds/scholarships"
        ]
        
        for url in program_urls:
            soup = self.fetch_page(url)
            if soup:
                links = soup.find_all('a', href=True)
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if text and len(text) > 10 and any(keyword in href.lower() for keyword in ['program', 'fellowship', 'scholarship']):
                        programs.append({
                            'name': text,
                            'url': urljoin(BASE_URL, href),
                            'category': 'Program'
                        })
        
        print(f"   [DONE] Total programs: {len(programs)}")
        return programs
    
    def scrape_policies(self):
        """Scrape policies and documents"""
        print("\n[SECTION] Scraping Policies...")
        policies = []
        
        url = f"{BASE_URL}/policies"
        soup = self.fetch_page(url)
        
        if soup:
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                
                if text and len(text) > 10 and ('.pdf' in href.lower() or 'policy' in href.lower()):
                    policies.append({
                        'name': text,
                        'url': urljoin(BASE_URL, href),
                        'type': 'Policy Document'
                    })
        
        print(f"   [DONE] Total policies: {len(policies)}")
        return policies
    
    def scrape_all(self):
        """Scrape all sections"""
        print("="*70)
        print("COMPREHENSIVE ISTI PORTAL SCRAPER")
        print("="*70)
        
        data = {
            'organizations': self.scrape_organizations(),
            'science_centres': self.scrape_science_centres(),
            'research_labs': self.scrape_research_labs(),
            'universities': self.scrape_universities(),
            'funding_schemes': self.scrape_funding_schemes(),
            'programs': self.scrape_programs(),
            'policies': self.scrape_policies()
        }
        
        return data

def categorize_data(data):
    """Organize data by various categories"""
    categorized = {
        'by_type': {},
        'by_state': {},
        'by_category': {}
    }
    
    # Categorize organizations
    for org in data['organizations']:
        # By category
        cat = org.get('category', 'Uncategorized')
        if cat not in categorized['by_category']:
            categorized['by_category'][cat] = []
        categorized['by_category'][cat].append(org)
        
        # By state
        state = org.get('state', 'Unknown')
        if state not in categorized['by_state']:
            categorized['by_state'][state] = []
        categorized['by_state'][state].append(org)
    
    # By type
    categorized['by_type']['Organizations'] = data['organizations']
    categorized['by_type']['Science Centres'] = data['science_centres']
    categorized['by_type']['Research Labs'] = data['research_labs']
    categorized['by_type']['Universities'] = data['universities']
    categorized['by_type']['Funding Schemes'] = data['funding_schemes']
    categorized['by_type']['Programs'] = data['programs']
    categorized['by_type']['Policies'] = data['policies']
    
    return categorized

def save_data(data, categorized):
    """Save all data to JSON files"""
    print("\n" + "="*70)
    print("SAVING DATA")
    print("="*70)
    
    # Create output directory
    os.makedirs('data', exist_ok=True)
    
    # Save complete data
    with open('data/complete_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("[SAVED] Complete data to data/complete_data.json")
    
    # Save each section separately
    for section, items in data.items():
        filename = f'data/{section}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"[SAVED] {len(items)} items to {filename}")
    
    # Save categorized data
    for cat_type, cat_data in categorized.items():
        filename = f'data/categorized_{cat_type}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)
        print(f"[SAVED] Categorized data to {filename}")
    
    # Create summary
    summary = {
        'total_items': sum(len(items) for items in data.values()),
        'sections': {section: len(items) for section, items in data.items()},
        'categories': {cat: len(items) for cat, items in categorized['by_category'].items()},
        'states': {state: len(items) for state, items in categorized['by_state'].items()},
        'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('data/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("[SAVED] Summary to data/summary.json")
    
    return summary

def print_summary(summary):
    """Print detailed summary"""
    print("\n" + "="*70)
    print("SCRAPING SUMMARY")
    print("="*70)
    print(f"Total Items Scraped: {summary['total_items']}")
    print(f"Scrape Date: {summary['scrape_date']}")
    
    print("\nItems by Section:")
    for section, count in sorted(summary['sections'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {section.replace('_', ' ').title()}: {count}")
    
    print(f"\nTotal Categories: {len(summary['categories'])}")
    print("Top 10 Categories:")
    for i, (cat, count) in enumerate(sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"  {i}. {cat}: {count}")
    
    print(f"\nTotal States: {len(summary['states'])}")
    print("Top 10 States:")
    for i, (state, count) in enumerate(sorted(summary['states'].items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"  {i}. {state}: {count}")
    
    print("="*70)

def main():
    """Main execution"""
    scraper = ISTIPortalScraper()
    
    # Scrape all data
    data = scraper.scrape_all()
    
    # Categorize data
    categorized = categorize_data(data)
    
    # Save data
    summary = save_data(data, categorized)
    
    # Print summary
    print_summary(summary)
    
    print("\n[COMPLETE] All data scraped and saved successfully!")
    print("Check the 'data' folder for all JSON files.")

if __name__ == "__main__":
    main()





