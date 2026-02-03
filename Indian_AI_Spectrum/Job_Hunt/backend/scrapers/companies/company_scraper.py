"""
Company Scraper - Scrapes company data from multiple sources
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
import json
import re
from typing import Optional, Dict, List
from datetime import datetime
import aiohttp
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompanyScraper:
    """Scraper for company data from various sources"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.scraped_count = 0
        self.failed_count = 0
        
    def get_company_from_linkedin(self, company_name: str) -> Optional[Dict]:
        """Scrape company info from LinkedIn (public data only)"""
        try:
            search_url = f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}"
            logger.info(f"Attempting to scrape: {search_url}")
            
            # Note: LinkedIn blocks direct scraping, this is placeholder
            # In production, use LinkedIn API or official data sources
            return {
                "source": "linkedin",
                "url": search_url,
                "scraped_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error scraping LinkedIn for {company_name}: {e}")
            return None
    
    def get_company_from_glassdoor(self, company_name: str) -> Optional[Dict]:
        """Scrape company reviews from Glassdoor (public data)"""
        try:
            # Note: Glassdoor blocks direct scraping
            # This is a placeholder for API/authorized access
            return {
                "source": "glassdoor",
                "company_name": company_name,
                "scraped_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error scraping Glassdoor for {company_name}: {e}")
            return None
    
    def get_company_from_ambitionbox(self, company_name: str) -> Optional[Dict]:
        """Scrape from AmbitionBox - Indian job review site"""
        try:
            slug = company_name.lower().replace(' ', '-').replace('.', '')
            url = f"https://www.ambitionbox.com/overview/{slug}-overview"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                data = {
                    "source": "ambitionbox",
                    "url": url,
                    "company_name": company_name,
                    "scraped_at": datetime.now().isoformat()
                }
                
                # Extract rating
                rating_elem = soup.select_one('.rating-container .rating')
                if rating_elem:
                    data['rating'] = float(rating_elem.text.strip())
                
                # Extract review count
                review_elem = soup.select_one('.total-reviews')
                if review_elem:
                    data['review_count'] = review_elem.text.strip()
                
                self.scraped_count += 1
                return data
            
            return None
        except Exception as e:
            logger.error(f"Error scraping AmbitionBox for {company_name}: {e}")
            self.failed_count += 1
            return None
    
    def get_naukri_company_data(self, company_name: str) -> Optional[Dict]:
        """Scrape company data from Naukri"""
        try:
            slug = company_name.lower().replace(' ', '-')
            url = f"https://www.naukri.com/{slug}-careers"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                data = {
                    "source": "naukri",
                    "url": url,
                    "company_name": company_name,
                    "scraped_at": datetime.now().isoformat()
                }
                
                # Extract job count
                job_count = soup.select_one('.job-count')
                if job_count:
                    data['active_jobs'] = job_count.text.strip()
                
                self.scraped_count += 1
                return data
            
            return None
        except Exception as e:
            logger.error(f"Error scraping Naukri for {company_name}: {e}")
            self.failed_count += 1
            return None
    
    def scrape_google_maps_business(self, company_name: str, city: str = "Bangalore") -> Optional[Dict]:
        """Search for company on Google Maps for location data"""
        try:
            # Google Maps scraping requires API or Selenium
            # This is a placeholder for the data structure
            return {
                "source": "google_maps",
                "query": f"{company_name} {city}",
                "scraped_at": datetime.now().isoformat(),
                "note": "Requires Google Places API for actual implementation"
            }
        except Exception as e:
            logger.error(f"Error with Google Maps for {company_name}: {e}")
            return None
    
    def get_github_org_data(self, org_name: str) -> Optional[Dict]:
        """Get company's GitHub organization data"""
        try:
            url = f"https://api.github.com/orgs/{org_name}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "github",
                    "org_name": data.get('login'),
                    "public_repos": data.get('public_repos'),
                    "followers": data.get('followers'),
                    "blog": data.get('blog'),
                    "description": data.get('description'),
                    "scraped_at": datetime.now().isoformat()
                }
            return None
        except Exception as e:
            logger.error(f"Error getting GitHub data for {org_name}: {e}")
            return None
    
    async def scrape_multiple_companies(self, companies: List[str]) -> List[Dict]:
        """Scrape data for multiple companies"""
        results = []
        
        for company in companies:
            logger.info(f"Scraping data for: {company}")
            
            company_data = {
                "name": company,
                "sources": {}
            }
            
            # Collect from multiple sources
            ambitionbox_data = self.get_company_from_ambitionbox(company)
            if ambitionbox_data:
                company_data["sources"]["ambitionbox"] = ambitionbox_data
            
            naukri_data = self.get_naukri_company_data(company)
            if naukri_data:
                company_data["sources"]["naukri"] = naukri_data
            
            github_slug = company.lower().replace(' ', '')
            github_data = self.get_github_org_data(github_slug)
            if github_data:
                company_data["sources"]["github"] = github_data
            
            results.append(company_data)
            
            # Rate limiting
            time.sleep(2)
        
        return results
    
    def run(self, source: str = "all"):
        """Run the scraper"""
        logger.info(f"Starting company scraper with source: {source}")
        
        # Sample companies to scrape
        companies = [
            "TCS", "Infosys", "Wipro", "Google", "Microsoft",
            "Amazon", "Flipkart", "Razorpay", "Zomato", "Swiggy"
        ]
        
        try:
            results = asyncio.run(self.scrape_multiple_companies(companies))
            
            # Save results
            output_file = "backend/data/raw/company_scraped_data.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Scraping complete. Scraped: {self.scraped_count}, Failed: {self.failed_count}")
            logger.info(f"Results saved to {output_file}")
            
            return results
        except Exception as e:
            logger.error(f"Error running scraper: {e}")
            raise


class JobScraper:
    """Scraper for job listings"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    def scrape_linkedin_jobs(self, keyword: str, location: str = "India") -> List[Dict]:
        """Scrape jobs from LinkedIn (public listings)"""
        # Note: LinkedIn has strict scraping policies
        # Use LinkedIn Jobs API for production
        logger.info(f"LinkedIn job search: {keyword} in {location}")
        return []
    
    def scrape_naukri_jobs(self, keyword: str, location: str = "India") -> List[Dict]:
        """Scrape jobs from Naukri.com"""
        try:
            url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.lower()}"
            logger.info(f"Scraping Naukri: {url}")
            
            # Note: Naukri blocks direct scraping
            # Would need Selenium or API access
            return []
        except Exception as e:
            logger.error(f"Error scraping Naukri jobs: {e}")
            return []
    
    def scrape_indeed_jobs(self, keyword: str, location: str = "India") -> List[Dict]:
        """Scrape jobs from Indeed"""
        try:
            url = f"https://www.indeed.co.in/jobs?q={keyword}&l={location}"
            logger.info(f"Scraping Indeed: {url}")
            
            # Note: Indeed has rate limiting
            return []
        except Exception as e:
            logger.error(f"Error scraping Indeed jobs: {e}")
            return []


class RemoteJobScraper:
    """Scraper for remote job listings"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
    def scrape_weworkremotely(self) -> List[Dict]:
        """Scrape from WeWorkRemotely"""
        try:
            url = "https://weworkremotely.com/categories/remote-programming-jobs"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = []
                
                for job in soup.select('.feature')[:20]:
                    title = job.select_one('.title')
                    company = job.select_one('.company')
                    
                    if title and company:
                        jobs.append({
                            "title": title.text.strip(),
                            "company": company.text.strip(),
                            "source": "weworkremotely"
                        })
                
                return jobs
            return []
        except Exception as e:
            logger.error(f"Error scraping WeWorkRemotely: {e}")
            return []
    
    def scrape_remoteok(self) -> List[Dict]:
        """Scrape from RemoteOK"""
        try:
            url = "https://remoteok.com/api"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                for job in data[1:21]:  # Skip first item (metadata)
                    if isinstance(job, dict):
                        jobs.append({
                            "title": job.get("position", ""),
                            "company": job.get("company", ""),
                            "location": job.get("location", "Remote"),
                            "salary": job.get("salary_min", ""),
                            "tags": job.get("tags", []),
                            "url": job.get("url", ""),
                            "source": "remoteok"
                        })
                
                return jobs
            return []
        except Exception as e:
            logger.error(f"Error scraping RemoteOK: {e}")
            return []


if __name__ == "__main__":
    # Test the scraper
    scraper = CompanyScraper()
    scraper.run()




