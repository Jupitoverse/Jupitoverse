"""
Comprehensive Seed Data for Job Hunt Portal
Contains real company data, migration guides, and resources
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, init_db
from app.models.company import Company, CompanyType, CompanyCategory, Technology, Location
from app.models.job import Job, JobType, ExperienceLevel, WorkMode
from app.models.resource import Resource, Roadmap, RoadmapStep, ResourceType, ResourcePricing
from app.models.country import Country, CountryMigration
from app.models.agency import Agency
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# PRODUCT BASED COMPANIES - INDIA
# =============================================================================
PRODUCT_COMPANIES_INDIA = [
    # FAANG/MAANG
    {
        "name": "Google India",
        "slug": "google-india",
        "website": "https://careers.google.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.FAANG,
        "industry": "Technology",
        "employee_count_range": "10000+",
        "founded_year": 1998,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Gurgaon", "Mumbai"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.5,
        "work_life_balance": 4.2,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/google",
        "glassdoor_url": "https://glassdoor.com/google",
        "careers_page": "https://careers.google.com/locations/india/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Microsoft India",
        "slug": "microsoft-india",
        "website": "https://careers.microsoft.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.FAANG,
        "industry": "Technology",
        "employee_count_range": "10000+",
        "founded_year": 1975,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Noida", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.3,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/microsoft",
        "careers_page": "https://careers.microsoft.com/us/en/search-results?country=India",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Amazon India",
        "slug": "amazon-india",
        "website": "https://amazon.jobs",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.FAANG,
        "industry": "E-commerce/Technology",
        "employee_count_range": "50000+",
        "founded_year": 1994,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Chennai", "Delhi NCR", "Mumbai"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.4,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000},
        "linkedin_url": "https://linkedin.com/company/amazon",
        "careers_page": "https://amazon.jobs/en/locations/india",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Meta (Facebook) India",
        "slug": "meta-india",
        "website": "https://metacareers.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.FAANG,
        "industry": "Technology/Social Media",
        "employee_count_range": "1000-5000",
        "founded_year": 2004,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Gurgaon"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.6,
        "work_life_balance": 4.3,
        "avg_salary_india": {"entry": 3000000, "mid": 6000000, "senior": 12000000},
        "linkedin_url": "https://linkedin.com/company/meta",
        "careers_page": "https://metacareers.com/locations/india/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Apple India",
        "slug": "apple-india",
        "website": "https://jobs.apple.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.FAANG,
        "industry": "Technology/Consumer Electronics",
        "employee_count_range": "5000-10000",
        "founded_year": 1976,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad"],
        "is_remote_friendly": False,
        "remote_policy": "no",
        "interview_difficulty": 4.5,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 2800000, "mid": 5500000, "senior": 11000000},
        "linkedin_url": "https://linkedin.com/company/apple",
        "careers_page": "https://jobs.apple.com/en-in/search",
        "is_verified": True,
        "is_actively_hiring": True
    },
    # Indian Unicorns
    {
        "name": "Flipkart",
        "slug": "flipkart",
        "website": "https://www.flipkartcareers.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "E-commerce",
        "employee_count_range": "30000+",
        "founded_year": 2007,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Delhi NCR", "Mumbai", "Kolkata"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 3.8,
        "avg_salary_india": {"entry": 1800000, "mid": 3500000, "senior": 7000000},
        "linkedin_url": "https://linkedin.com/company/flipkart",
        "careers_page": "https://www.flipkartcareers.com/#!/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Zomato",
        "slug": "zomato",
        "website": "https://www.zomato.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "Food Tech",
        "employee_count_range": "5000-10000",
        "founded_year": 2008,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Gurgaon", "Bangalore", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.8,
        "work_life_balance": 3.7,
        "avg_salary_india": {"entry": 1500000, "mid": 3000000, "senior": 6000000},
        "linkedin_url": "https://linkedin.com/company/zomato",
        "careers_page": "https://www.zomato.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Swiggy",
        "slug": "swiggy",
        "website": "https://careers.swiggy.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "Food Tech",
        "employee_count_range": "5000-10000",
        "founded_year": 2014,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Mumbai", "Delhi NCR", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.9,
        "work_life_balance": 3.6,
        "avg_salary_india": {"entry": 1600000, "mid": 3200000, "senior": 6500000},
        "linkedin_url": "https://linkedin.com/company/swiggy",
        "careers_page": "https://careers.swiggy.com",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Razorpay",
        "slug": "razorpay",
        "website": "https://razorpay.com/jobs",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "FinTech",
        "employee_count_range": "3000-5000",
        "founded_year": 2014,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.1,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000},
        "linkedin_url": "https://linkedin.com/company/razorpay",
        "careers_page": "https://razorpay.com/jobs/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "CRED",
        "slug": "cred",
        "website": "https://cred.club/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "FinTech",
        "employee_count_range": "1000-3000",
        "founded_year": 2018,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.2,
        "work_life_balance": 4.1,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/caborite",
        "careers_page": "https://cred.club/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "PhonePe",
        "slug": "phonepe",
        "website": "https://www.phonepe.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "FinTech",
        "employee_count_range": "5000-10000",
        "founded_year": 2015,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Mumbai", "Delhi NCR", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 3.8,
        "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000},
        "linkedin_url": "https://linkedin.com/company/phonepe",
        "careers_page": "https://www.phonepe.com/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Paytm",
        "slug": "paytm",
        "website": "https://paytm.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "FinTech",
        "employee_count_range": "10000+",
        "founded_year": 2010,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Noida", "Bangalore", "Mumbai", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.7,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 1200000, "mid": 2500000, "senior": 5000000},
        "linkedin_url": "https://linkedin.com/company/paytm",
        "careers_page": "https://paytm.com/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Ola",
        "slug": "ola",
        "website": "https://www.olacabs.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "Mobility/EV",
        "employee_count_range": "5000-10000",
        "founded_year": 2010,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Mumbai", "Delhi NCR", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.8,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 1500000, "mid": 3000000, "senior": 6000000},
        "linkedin_url": "https://linkedin.com/company/ola-cabs",
        "careers_page": "https://www.olacabs.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Meesho",
        "slug": "meesho",
        "website": "https://meesho.io/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "E-commerce",
        "employee_count_range": "3000-5000",
        "founded_year": 2015,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 3.9,
        "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000},
        "linkedin_url": "https://linkedin.com/company/meesho",
        "careers_page": "https://meesho.io/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Zerodha",
        "slug": "zerodha",
        "website": "https://zerodha.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.INDIAN_UNICORN,
        "industry": "FinTech/Stock Broking",
        "employee_count_range": "1000-3000",
        "founded_year": 2010,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "interview_difficulty": 4.3,
        "work_life_balance": 4.5,
        "avg_salary_india": {"entry": 1800000, "mid": 3500000, "senior": 7000000},
        "linkedin_url": "https://linkedin.com/company/zerodha",
        "careers_page": "https://zerodha.com/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    # Tier 1 Tech Companies
    {
        "name": "Atlassian India",
        "slug": "atlassian-india",
        "website": "https://www.atlassian.com/company/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/SaaS",
        "employee_count_range": "1000-3000",
        "founded_year": 2002,
        "headquarters_country": "Australia",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "interview_difficulty": 4.2,
        "work_life_balance": 4.4,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/atlassian",
        "careers_page": "https://www.atlassian.com/company/careers/all-jobs?location=India",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Uber India",
        "slug": "uber-india",
        "website": "https://www.uber.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Mobility",
        "employee_count_range": "1000-3000",
        "founded_year": 2009,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.3,
        "work_life_balance": 3.8,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/uber",
        "careers_page": "https://www.uber.com/global/en/careers/list/?location=IND-Bangalore",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Salesforce India",
        "slug": "salesforce-india",
        "website": "https://www.salesforce.com/company/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/CRM",
        "employee_count_range": "5000-10000",
        "founded_year": 1999,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Mumbai"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.1,
        "work_life_balance": 4.2,
        "avg_salary_india": {"entry": 2000000, "mid": 4200000, "senior": 8500000},
        "linkedin_url": "https://linkedin.com/company/salesforce",
        "careers_page": "https://www.salesforce.com/company/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Adobe India",
        "slug": "adobe-india",
        "website": "https://adobe.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Creative Software",
        "employee_count_range": "5000-10000",
        "founded_year": 1982,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Noida"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.2,
        "work_life_balance": 4.3,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/adobe",
        "careers_page": "https://adobe.wd5.myworkdayjobs.com/external_experienced?locationCountry=3a5a5f8c8f2d0177c6b8deae4e14",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Oracle India",
        "slug": "oracle-india",
        "website": "https://oracle.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Database",
        "employee_count_range": "30000+",
        "founded_year": 1977,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Noida", "Mumbai", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 1500000, "mid": 3000000, "senior": 6000000},
        "linkedin_url": "https://linkedin.com/company/oracle",
        "careers_page": "https://oracle.com/corporate/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "SAP Labs India",
        "slug": "sap-labs-india",
        "website": "https://sap.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Enterprise Software",
        "employee_count_range": "10000+",
        "founded_year": 1972,
        "headquarters_country": "Germany",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Gurgaon", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 4.2,
        "avg_salary_india": {"entry": 1600000, "mid": 3200000, "senior": 6500000},
        "linkedin_url": "https://linkedin.com/company/sap",
        "careers_page": "https://jobs.sap.com/search/?q=&locationsearch=India",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Netflix India",
        "slug": "netflix-india",
        "website": "https://jobs.netflix.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Streaming",
        "employee_count_range": "100-500",
        "founded_year": 1997,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Mumbai"],
        "is_remote_friendly": False,
        "remote_policy": "no",
        "interview_difficulty": 4.5,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 3000000, "mid": 6000000, "senior": 12000000},
        "linkedin_url": "https://linkedin.com/company/netflix",
        "careers_page": "https://jobs.netflix.com/search?location=India",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "LinkedIn India",
        "slug": "linkedin-india",
        "website": "https://careers.linkedin.com",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Social Media",
        "employee_count_range": "1000-3000",
        "founded_year": 2002,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.3,
        "work_life_balance": 4.3,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/linkedin",
        "careers_page": "https://careers.linkedin.com/search?location=India",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Intuit India",
        "slug": "intuit-india",
        "website": "https://intuit.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/FinTech",
        "employee_count_range": "3000-5000",
        "founded_year": 1983,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.1,
        "work_life_balance": 4.4,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/intuit",
        "careers_page": "https://www.intuit.com/careers/search/?location=india",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "VMware India",
        "slug": "vmware-india",
        "website": "https://vmware.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Virtualization",
        "employee_count_range": "5000-10000",
        "founded_year": 1998,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Pune"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.0,
        "work_life_balance": 4.2,
        "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000},
        "linkedin_url": "https://linkedin.com/company/vmware",
        "careers_page": "https://careers.vmware.com/location/india/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Nvidia India",
        "slug": "nvidia-india",
        "website": "https://nvidia.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/AI/Hardware",
        "employee_count_range": "3000-5000",
        "founded_year": 1993,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Pune", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 4.5,
        "work_life_balance": 4.0,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/nvidia",
        "careers_page": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationCountry=3cfa47d8c2f901fd7f7dd2c4ee91",
        "is_verified": True,
        "is_actively_hiring": True
    },
]

# =============================================================================
# SERVICE BASED COMPANIES - INDIA
# =============================================================================
SERVICE_COMPANIES_INDIA = [
    {
        "name": "TCS (Tata Consultancy Services)",
        "slug": "tcs",
        "website": "https://tcs.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services",
        "employee_count_range": "600000+",
        "founded_year": 1968,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Mumbai", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Delhi NCR"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.0,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 400000, "mid": 800000, "senior": 2000000},
        "linkedin_url": "https://linkedin.com/company/tata-consultancy-services",
        "careers_page": "https://ibegin.tcs.com/iBegin/jobs/search",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Infosys",
        "slug": "infosys",
        "website": "https://infosys.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services",
        "employee_count_range": "300000+",
        "founded_year": 1981,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Pune", "Chennai", "Hyderabad", "Mysore", "Bhubaneswar"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.2,
        "work_life_balance": 3.4,
        "avg_salary_india": {"entry": 400000, "mid": 900000, "senior": 2200000},
        "linkedin_url": "https://linkedin.com/company/infosys",
        "careers_page": "https://career.infosys.com/joblist",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Wipro",
        "slug": "wipro",
        "website": "https://careers.wipro.com",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services",
        "employee_count_range": "250000+",
        "founded_year": 1945,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Chennai", "Pune", "Noida", "Kolkata"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.0,
        "work_life_balance": 3.6,
        "avg_salary_india": {"entry": 380000, "mid": 800000, "senior": 1800000},
        "linkedin_url": "https://linkedin.com/company/wipro",
        "careers_page": "https://careers.wipro.com/careers-home",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "HCL Technologies",
        "slug": "hcl-tech",
        "website": "https://hcltech.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services",
        "employee_count_range": "200000+",
        "founded_year": 1976,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Noida", "Bangalore", "Chennai", "Hyderabad", "Pune", "Lucknow"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.2,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 400000, "mid": 850000, "senior": 2000000},
        "linkedin_url": "https://linkedin.com/company/hcl-technologies",
        "careers_page": "https://www.hcltech.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Tech Mahindra",
        "slug": "tech-mahindra",
        "website": "https://techmahindra.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_2,
        "industry": "IT Services",
        "employee_count_range": "150000+",
        "founded_year": 1986,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Pune", "Hyderabad", "Chennai", "Bangalore", "Noida"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.0,
        "work_life_balance": 3.4,
        "avg_salary_india": {"entry": 350000, "mid": 750000, "senior": 1600000},
        "linkedin_url": "https://linkedin.com/company/tech-mahindra",
        "careers_page": "https://careers.techmahindra.com/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Cognizant",
        "slug": "cognizant",
        "website": "https://cognizant.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services",
        "employee_count_range": "350000+",
        "founded_year": 1994,
        "headquarters_country": "USA",
        "has_indian_office": True,
        "indian_cities": ["Chennai", "Bangalore", "Hyderabad", "Pune", "Kolkata", "Coimbatore"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.3,
        "work_life_balance": 3.4,
        "avg_salary_india": {"entry": 420000, "mid": 900000, "senior": 2200000},
        "linkedin_url": "https://linkedin.com/company/cognizant",
        "careers_page": "https://careers.cognizant.com/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Capgemini India",
        "slug": "capgemini-india",
        "website": "https://capgemini.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services/Consulting",
        "employee_count_range": "150000+",
        "founded_year": 1967,
        "headquarters_country": "France",
        "has_indian_office": True,
        "indian_cities": ["Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.4,
        "work_life_balance": 3.5,
        "avg_salary_india": {"entry": 400000, "mid": 850000, "senior": 2000000},
        "linkedin_url": "https://linkedin.com/company/capgemini",
        "careers_page": "https://www.capgemini.com/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Accenture India",
        "slug": "accenture-india",
        "website": "https://accenture.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_1,
        "industry": "IT Services/Consulting",
        "employee_count_range": "300000+",
        "founded_year": 1989,
        "headquarters_country": "Ireland",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Mumbai", "Chennai", "Pune", "Delhi NCR", "Kolkata"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.5,
        "work_life_balance": 3.3,
        "avg_salary_india": {"entry": 450000, "mid": 1000000, "senior": 2500000},
        "linkedin_url": "https://linkedin.com/company/accenture",
        "careers_page": "https://www.accenture.com/in-en/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "LTIMindtree",
        "slug": "ltimindtree",
        "website": "https://ltimindtree.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_2,
        "industry": "IT Services",
        "employee_count_range": "80000+",
        "founded_year": 2022,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Mumbai", "Bangalore", "Pune", "Chennai", "Hyderabad"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.3,
        "work_life_balance": 3.6,
        "avg_salary_india": {"entry": 400000, "mid": 850000, "senior": 1800000},
        "linkedin_url": "https://linkedin.com/company/ltimindtree",
        "careers_page": "https://www.ltimindtree.com/careers/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Mphasis",
        "slug": "mphasis",
        "website": "https://mphasis.com/careers",
        "company_type": CompanyType.SERVICE,
        "category": CompanyCategory.TIER_2,
        "industry": "IT Services",
        "employee_count_range": "40000+",
        "founded_year": 2000,
        "headquarters_country": "India",
        "has_indian_office": True,
        "indian_cities": ["Bangalore", "Hyderabad", "Chennai", "Pune", "Noida"],
        "is_remote_friendly": True,
        "remote_policy": "hybrid",
        "interview_difficulty": 3.2,
        "work_life_balance": 3.7,
        "avg_salary_india": {"entry": 400000, "mid": 850000, "senior": 1800000},
        "linkedin_url": "https://linkedin.com/company/mphasis",
        "careers_page": "https://www.mphasis.com/home/careers.html",
        "is_verified": True,
        "is_actively_hiring": True
    },
]

# =============================================================================
# REMOTE HIRING COMPANIES (Global)
# =============================================================================
REMOTE_COMPANIES = [
    {
        "name": "GitLab",
        "slug": "gitlab",
        "website": "https://about.gitlab.com/jobs",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/DevOps",
        "employee_count_range": "2000-3000",
        "founded_year": 2011,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.2,
        "work_life_balance": 4.5,
        "avg_salary_india": {"entry": 3000000, "mid": 6000000, "senior": 12000000},
        "linkedin_url": "https://linkedin.com/company/gitlab",
        "careers_page": "https://about.gitlab.com/jobs/all-jobs/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Automattic",
        "slug": "automattic",
        "website": "https://automattic.com/work-with-us",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Publishing",
        "employee_count_range": "1000-2000",
        "founded_year": 2005,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.0,
        "work_life_balance": 4.7,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/automattic",
        "careers_page": "https://automattic.com/work-with-us/",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Toptal",
        "slug": "toptal",
        "website": "https://toptal.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Freelance Platform",
        "employee_count_range": "500-1000",
        "founded_year": 2010,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.5,
        "work_life_balance": 4.5,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/toptal",
        "careers_page": "https://www.toptal.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Zapier",
        "slug": "zapier",
        "website": "https://zapier.com/jobs",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Automation",
        "employee_count_range": "500-1000",
        "founded_year": 2011,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.0,
        "work_life_balance": 4.6,
        "avg_salary_india": {"entry": 2800000, "mid": 5500000, "senior": 11000000},
        "linkedin_url": "https://linkedin.com/company/zapier",
        "careers_page": "https://zapier.com/jobs",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Basecamp",
        "slug": "basecamp",
        "website": "https://basecamp.com/about/jobs",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.STARTUP,
        "industry": "Technology/Project Management",
        "employee_count_range": "50-100",
        "founded_year": 1999,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.0,
        "work_life_balance": 4.8,
        "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000},
        "linkedin_url": "https://linkedin.com/company/basecamp",
        "careers_page": "https://basecamp.com/about/jobs",
        "is_verified": True,
        "is_actively_hiring": False
    },
    {
        "name": "Buffer",
        "slug": "buffer",
        "website": "https://buffer.com/journey",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.STARTUP,
        "industry": "Technology/Social Media",
        "employee_count_range": "50-100",
        "founded_year": 2010,
        "headquarters_country": "USA",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 3.8,
        "work_life_balance": 4.7,
        "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000},
        "linkedin_url": "https://linkedin.com/company/buffer",
        "careers_page": "https://buffer.com/journey",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Canonical",
        "slug": "canonical",
        "website": "https://canonical.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.TIER_1,
        "industry": "Technology/Open Source",
        "employee_count_range": "500-1000",
        "founded_year": 2004,
        "headquarters_country": "UK",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.3,
        "work_life_balance": 4.2,
        "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000},
        "linkedin_url": "https://linkedin.com/company/canonical",
        "careers_page": "https://canonical.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
    {
        "name": "Doist",
        "slug": "doist",
        "website": "https://doist.com/careers",
        "company_type": CompanyType.PRODUCT,
        "category": CompanyCategory.STARTUP,
        "industry": "Technology/Productivity",
        "employee_count_range": "100-200",
        "founded_year": 2007,
        "headquarters_country": "Remote-first",
        "has_indian_office": False,
        "indian_cities": [],
        "is_remote_friendly": True,
        "remote_policy": "full",
        "hires_from_india": True,
        "interview_difficulty": 4.0,
        "work_life_balance": 4.6,
        "avg_salary_india": {"entry": 2200000, "mid": 4500000, "senior": 9000000},
        "linkedin_url": "https://linkedin.com/company/doist",
        "careers_page": "https://doist.com/careers",
        "is_verified": True,
        "is_actively_hiring": True
    },
]

# =============================================================================
# COUNTRIES FOR ABROAD JOBS
# =============================================================================
COUNTRIES_DATA = [
    {
        "name": "Germany",
        "code": "DE",
        "flag_emoji": "🇩🇪",
        "continent": "Europe",
        "tech_hub_cities": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
        "popular_industries": ["Automotive", "Manufacturing", "FinTech", "AI/ML", "Enterprise Software"],
        "avg_tech_salary_usd": 75000,
        "indian_population_estimate": 200000,
        "indian_friendly_score": 8.5,
        "is_popular_destination": True,
        "difficulty_score": 6.0
    },
    {
        "name": "Canada",
        "code": "CA",
        "flag_emoji": "🇨🇦",
        "continent": "North America",
        "tech_hub_cities": ["Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary"],
        "popular_industries": ["FinTech", "AI/ML", "Gaming", "E-commerce", "SaaS"],
        "avg_tech_salary_usd": 85000,
        "indian_population_estimate": 1800000,
        "indian_friendly_score": 9.0,
        "is_popular_destination": True,
        "difficulty_score": 5.5
    },
    {
        "name": "Australia",
        "code": "AU",
        "flag_emoji": "🇦🇺",
        "continent": "Oceania",
        "tech_hub_cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "popular_industries": ["FinTech", "Mining Tech", "HealthTech", "E-commerce", "SaaS"],
        "avg_tech_salary_usd": 90000,
        "indian_population_estimate": 800000,
        "indian_friendly_score": 8.0,
        "is_popular_destination": True,
        "difficulty_score": 6.5
    },
    {
        "name": "United Arab Emirates",
        "code": "AE",
        "flag_emoji": "🇦🇪",
        "continent": "Asia",
        "tech_hub_cities": ["Dubai", "Abu Dhabi", "Sharjah"],
        "popular_industries": ["FinTech", "E-commerce", "PropTech", "LogisticsTech", "Banking"],
        "avg_tech_salary_usd": 65000,
        "indian_population_estimate": 3500000,
        "indian_friendly_score": 9.5,
        "is_popular_destination": True,
        "difficulty_score": 3.5
    },
    {
        "name": "United Kingdom",
        "code": "GB",
        "flag_emoji": "🇬🇧",
        "continent": "Europe",
        "tech_hub_cities": ["London", "Manchester", "Edinburgh", "Cambridge", "Bristol"],
        "popular_industries": ["FinTech", "AI/ML", "HealthTech", "EdTech", "Cybersecurity"],
        "avg_tech_salary_usd": 80000,
        "indian_population_estimate": 1500000,
        "indian_friendly_score": 8.0,
        "is_popular_destination": True,
        "difficulty_score": 7.0
    },
    {
        "name": "United States",
        "code": "US",
        "flag_emoji": "🇺🇸",
        "continent": "North America",
        "tech_hub_cities": ["San Francisco", "New York", "Seattle", "Austin", "Boston"],
        "popular_industries": ["Big Tech", "AI/ML", "SaaS", "FinTech", "Cloud"],
        "avg_tech_salary_usd": 150000,
        "indian_population_estimate": 4500000,
        "indian_friendly_score": 7.5,
        "is_popular_destination": True,
        "difficulty_score": 8.5
    },
    {
        "name": "Netherlands",
        "code": "NL",
        "flag_emoji": "🇳🇱",
        "continent": "Europe",
        "tech_hub_cities": ["Amsterdam", "Rotterdam", "The Hague", "Eindhoven", "Utrecht"],
        "popular_industries": ["FinTech", "E-commerce", "AgriTech", "LogisticsTech", "AI"],
        "avg_tech_salary_usd": 70000,
        "indian_population_estimate": 50000,
        "indian_friendly_score": 8.5,
        "is_popular_destination": True,
        "difficulty_score": 5.5
    },
    {
        "name": "Singapore",
        "code": "SG",
        "flag_emoji": "🇸🇬",
        "continent": "Asia",
        "tech_hub_cities": ["Singapore"],
        "popular_industries": ["FinTech", "E-commerce", "AI/ML", "Cybersecurity", "Blockchain"],
        "avg_tech_salary_usd": 80000,
        "indian_population_estimate": 650000,
        "indian_friendly_score": 9.0,
        "is_popular_destination": True,
        "difficulty_score": 6.0
    },
    {
        "name": "New Zealand",
        "code": "NZ",
        "flag_emoji": "🇳🇿",
        "continent": "Oceania",
        "tech_hub_cities": ["Auckland", "Wellington", "Christchurch"],
        "popular_industries": ["AgriTech", "FinTech", "Gaming", "HealthTech", "SaaS"],
        "avg_tech_salary_usd": 70000,
        "indian_population_estimate": 250000,
        "indian_friendly_score": 8.5,
        "is_popular_destination": True,
        "difficulty_score": 6.0
    },
    {
        "name": "Poland",
        "code": "PL",
        "flag_emoji": "🇵🇱",
        "continent": "Europe",
        "tech_hub_cities": ["Warsaw", "Krakow", "Wroclaw", "Gdansk", "Poznan"],
        "popular_industries": ["Gaming", "FinTech", "E-commerce", "Outsourcing", "SaaS"],
        "avg_tech_salary_usd": 45000,
        "indian_population_estimate": 15000,
        "indian_friendly_score": 7.5,
        "is_popular_destination": False,
        "difficulty_score": 5.0
    },
    {
        "name": "Denmark",
        "code": "DK",
        "flag_emoji": "🇩🇰",
        "continent": "Europe",
        "tech_hub_cities": ["Copenhagen", "Aarhus", "Odense"],
        "popular_industries": ["CleanTech", "FinTech", "HealthTech", "Logistics", "Gaming"],
        "avg_tech_salary_usd": 80000,
        "indian_population_estimate": 15000,
        "indian_friendly_score": 8.0,
        "is_popular_destination": False,
        "difficulty_score": 6.5
    },
    {
        "name": "Sweden",
        "code": "SE",
        "flag_emoji": "🇸🇪",
        "continent": "Europe",
        "tech_hub_cities": ["Stockholm", "Gothenburg", "Malmo", "Uppsala"],
        "popular_industries": ["Gaming", "FinTech", "Music Tech", "CleanTech", "E-commerce"],
        "avg_tech_salary_usd": 75000,
        "indian_population_estimate": 25000,
        "indian_friendly_score": 8.0,
        "is_popular_destination": False,
        "difficulty_score": 6.0
    },
    {
        "name": "Luxembourg",
        "code": "LU",
        "flag_emoji": "🇱🇺",
        "continent": "Europe",
        "tech_hub_cities": ["Luxembourg City"],
        "popular_industries": ["FinTech", "Banking", "Space Tech", "Cybersecurity"],
        "avg_tech_salary_usd": 90000,
        "indian_population_estimate": 5000,
        "indian_friendly_score": 7.5,
        "is_popular_destination": False,
        "difficulty_score": 6.5
    },
]

# =============================================================================
# MIGRATION GUIDES
# =============================================================================
MIGRATION_GUIDES = [
    {
        "country_name": "Germany",
        "visa_types": [
            {
                "name": "EU Blue Card",
                "description": "For highly qualified professionals with job offer",
                "requirements": ["Job offer with minimum €58,400 salary (€45,552 for STEM)", "University degree", "Valid passport"],
                "processing_time": "4-8 weeks"
            },
            {
                "name": "Job Seeker Visa",
                "description": "6-month visa to search for job in Germany",
                "requirements": ["University degree", "Proof of funds (€947/month)", "Health insurance"],
                "processing_time": "8-12 weeks"
            }
        ],
        "visa_process_steps": [
            "Get job offer from German employer",
            "Collect documents (degree, passport, offer letter)",
            "Book VFS appointment",
            "Submit visa application",
            "Wait for processing",
            "Collect visa and travel"
        ],
        "visa_processing_time_weeks": 8,
        "visa_cost_usd": 100,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn Germany", "url": "https://linkedin.com/jobs", "description": "Best for professional networking"},
            {"name": "StepStone", "url": "https://stepstone.de", "description": "Major German job portal"},
            {"name": "Indeed Germany", "url": "https://indeed.de", "description": "Large job aggregator"},
            {"name": "Xing", "url": "https://xing.com", "description": "German professional network"},
            {"name": "Glassdoor DE", "url": "https://glassdoor.de", "description": "Reviews + jobs"}
        ],
        "recruitment_agencies": [
            {"name": "Michael Page Germany", "url": "https://michaelpage.de"},
            {"name": "Hays Germany", "url": "https://hays.de"},
            {"name": "Robert Half", "url": "https://roberthalf.de"}
        ],
        "resume_format": "Europass or German-style CV with photo, date of birth, and marital status",
        "resume_tips": [
            "Include professional photo",
            "Add date of birth",
            "Keep to 1-2 pages",
            "Include German language level",
            "Highlight relevant certifications"
        ],
        "cover_letter_required": True,
        "documents_required": [
            "Valid passport (6+ months validity)",
            "Original degree certificates",
            "Degree evaluation (anabin/ZAB)",
            "Job offer letter",
            "Proof of accommodation",
            "Health insurance",
            "Passport photos",
            "Filled visa application form"
        ],
        "monthly_expenses_estimate": {"single": 1500, "family": 3500},
        "initial_settlement_cost": 5000,
        "language_requirements": {"work": "English (German preferred)", "residence": "A1 German recommended"},
        "pr_eligibility_years": 4,
        "citizenship_eligibility_years": 8,
        "income_tax_rate": "14% - 45% progressive",
        "tax_treaties_with_india": True,
        "common_challenges": [
            "German language barrier",
            "Cold weather adjustment",
            "Bureaucracy (Anmeldung, etc.)",
            "Finding apartment",
            "Banking setup takes time"
        ],
        "tips_for_indians": [
            "Start learning German immediately",
            "Join Indian community groups",
            "Open blocked account before visa",
            "Get health insurance early",
            "Research city before choosing"
        ],
        "facebook_groups": [
            {"name": "Indians in Germany", "url": "https://facebook.com/groups/indiansingermany"},
            {"name": "IT Professionals in Germany", "url": "https://facebook.com/groups/itprofessionalsgermany"}
        ],
        "youtube_channels": [
            {"name": "Bharat in Germany", "url": "https://youtube.com/@bharatingermany"},
            {"name": "Nikhilesh Dhure", "url": "https://youtube.com/@nikhileshdhure"}
        ]
    },
    {
        "country_name": "Canada",
        "visa_types": [
            {
                "name": "Express Entry",
                "description": "Points-based system for skilled workers",
                "requirements": ["CRS score 470+", "IELTS 8+", "Work experience", "Education credential assessment"],
                "processing_time": "6-12 months"
            },
            {
                "name": "Work Permit (LMIA)",
                "description": "Employer-sponsored work permit",
                "requirements": ["Job offer with positive LMIA", "Valid passport", "Proof of qualifications"],
                "processing_time": "8-16 weeks"
            },
            {
                "name": "Provincial Nominee Program",
                "description": "Province-specific immigration",
                "requirements": ["Nomination from province", "Meet provincial criteria"],
                "processing_time": "12-18 months"
            }
        ],
        "visa_process_steps": [
            "Create Express Entry profile",
            "Get IELTS scores",
            "Get ECA for education",
            "Wait for ITA (Invitation to Apply)",
            "Submit PR application",
            "Complete medical and biometrics",
            "Receive COPR and travel"
        ],
        "visa_processing_time_weeks": 26,
        "visa_cost_usd": 1500,
        "employer_sponsorship_required": False,
        "popular_job_portals": [
            {"name": "LinkedIn Canada", "url": "https://linkedin.com/jobs", "description": "Best for networking"},
            {"name": "Indeed Canada", "url": "https://indeed.ca", "description": "Largest job aggregator"},
            {"name": "Glassdoor Canada", "url": "https://glassdoor.ca", "description": "Reviews + jobs"},
            {"name": "Job Bank", "url": "https://jobbank.gc.ca", "description": "Government job portal"},
            {"name": "Workopolis", "url": "https://workopolis.com", "description": "Canadian job board"}
        ],
        "recruitment_agencies": [
            {"name": "Robert Half Canada", "url": "https://roberthalf.ca"},
            {"name": "Hays Canada", "url": "https://hays.ca"},
            {"name": "Randstad Canada", "url": "https://randstad.ca"}
        ],
        "resume_format": "Canadian-style: No photo, no personal info, achievement-focused",
        "resume_tips": [
            "No photo required",
            "Remove age/marital status",
            "Use Canadian spelling",
            "Focus on achievements with numbers",
            "Keep to 2 pages max"
        ],
        "cover_letter_required": True,
        "documents_required": [
            "Valid passport",
            "IELTS/CELPIP scores",
            "ECA (WES recommended)",
            "Police clearance certificate",
            "Medical exam results",
            "Proof of funds",
            "Reference letters from employers"
        ],
        "monthly_expenses_estimate": {"single": 2000, "family": 4500},
        "initial_settlement_cost": 8000,
        "language_requirements": {"work": "English (French bonus)", "residence": "CLB 7+ for Express Entry"},
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 3,
        "income_tax_rate": "15% - 33% federal + provincial",
        "tax_treaties_with_india": True,
        "common_challenges": [
            "Extreme cold weather",
            "Canadian work experience requirement",
            "High cost of living in Toronto/Vancouver",
            "Recognition of foreign experience",
            "Healthcare wait times"
        ],
        "tips_for_indians": [
            "Apply for Express Entry early",
            "Take IELTS seriously - aim for 8+",
            "Start WES ECA process 3 months before",
            "Consider smaller cities for lower CRS",
            "Network through LinkedIn before moving"
        ],
        "facebook_groups": [
            {"name": "Indians in Canada", "url": "https://facebook.com/groups/indiansincanada"},
            {"name": "Express Entry Canada", "url": "https://facebook.com/groups/expressentry"}
        ],
        "youtube_channels": [
            {"name": "Canada Immigration", "url": "https://youtube.com/@canadaimmigration"},
            {"name": "Desi to Videsi", "url": "https://youtube.com/@desividesi"}
        ]
    },
]

# =============================================================================
# LEARNING RESOURCES
# =============================================================================
LEARNING_RESOURCES = [
    # Data Science & ML
    {
        "title": "Machine Learning Specialization - Andrew Ng",
        "description": "The most famous ML course, updated for 2023 with Python",
        "url": "https://coursera.org/specializations/machine-learning-introduction",
        "resource_type": ResourceType.COURSE,
        "pricing": ResourcePricing.FREEMIUM,
        "author": "Andrew Ng",
        "platform": "Coursera",
        "language": "English",
        "duration_hours": 80,
        "category": "AI/ML",
        "subcategory": "Machine Learning",
        "skills_covered": ["Python", "NumPy", "TensorFlow", "Neural Networks", "Regression", "Classification"],
        "difficulty_level": "beginner",
        "relevant_roles": ["Data Scientist", "ML Engineer", "AI Engineer"],
        "rating": 4.9,
        "students_count": 5000000,
        "is_recommended": True
    },
    {
        "title": "Deep Learning Specialization",
        "description": "Master deep learning fundamentals",
        "url": "https://coursera.org/specializations/deep-learning",
        "resource_type": ResourceType.COURSE,
        "pricing": ResourcePricing.FREEMIUM,
        "author": "Andrew Ng",
        "platform": "Coursera",
        "language": "English",
        "duration_hours": 120,
        "category": "AI/ML",
        "subcategory": "Deep Learning",
        "skills_covered": ["CNN", "RNN", "LSTM", "TensorFlow", "Keras"],
        "difficulty_level": "intermediate",
        "relevant_roles": ["ML Engineer", "Deep Learning Engineer", "AI Researcher"],
        "rating": 4.9,
        "students_count": 1000000,
        "is_recommended": True
    },
    # Indian YouTube Channels
    {
        "title": "CampusX - Data Science Hindi",
        "description": "Complete Data Science in Hindi - Best for Indian learners",
        "url": "https://youtube.com/@campusx-official",
        "resource_type": ResourceType.YOUTUBE_CHANNEL,
        "pricing": ResourcePricing.FREE,
        "author": "Nitish Singh",
        "platform": "YouTube",
        "language": "Hindi",
        "category": "Data Science",
        "skills_covered": ["Python", "ML", "Deep Learning", "NLP", "SQL"],
        "difficulty_level": "beginner",
        "relevant_roles": ["Data Scientist", "Data Analyst", "ML Engineer"],
        "is_indian_creator": True,
        "is_india_focused": True,
        "is_recommended": True
    },
    {
        "title": "Krish Naik - Data Science",
        "description": "Comprehensive Data Science tutorials",
        "url": "https://youtube.com/@krishnaik06",
        "resource_type": ResourceType.YOUTUBE_CHANNEL,
        "pricing": ResourcePricing.FREE,
        "author": "Krish Naik",
        "platform": "YouTube",
        "language": "English/Hindi",
        "category": "Data Science",
        "skills_covered": ["Python", "ML", "Deep Learning", "MLOps", "GenAI"],
        "difficulty_level": "beginner",
        "relevant_roles": ["Data Scientist", "ML Engineer"],
        "is_indian_creator": True,
        "is_india_focused": True,
        "is_recommended": True
    },
    {
        "title": "Code With Harry",
        "description": "Programming tutorials in Hindi",
        "url": "https://youtube.com/@CodeWithHarry",
        "resource_type": ResourceType.YOUTUBE_CHANNEL,
        "pricing": ResourcePricing.FREE,
        "author": "Harry",
        "platform": "YouTube",
        "language": "Hindi",
        "category": "Programming",
        "skills_covered": ["Python", "JavaScript", "Web Development", "DSA"],
        "difficulty_level": "beginner",
        "relevant_roles": ["Software Developer", "Web Developer"],
        "is_indian_creator": True,
        "is_india_focused": True,
        "is_recommended": True
    },
    {
        "title": "Apna College - DSA & Development",
        "description": "DSA and development tutorials for placement prep",
        "url": "https://youtube.com/@ApnaCollegeOfficial",
        "resource_type": ResourceType.YOUTUBE_CHANNEL,
        "pricing": ResourcePricing.FREE,
        "author": "Shradha Khapra",
        "platform": "YouTube",
        "language": "Hindi",
        "category": "Programming",
        "skills_covered": ["Java", "C++", "DSA", "Web Development", "DBMS"],
        "difficulty_level": "beginner",
        "relevant_roles": ["Software Developer", "SDE"],
        "is_indian_creator": True,
        "is_india_focused": True,
        "is_recommended": True
    },
    {
        "title": "Striver (take U forward) - DSA",
        "description": "Best DSA content for FAANG interviews",
        "url": "https://youtube.com/@takeUforward",
        "resource_type": ResourceType.YOUTUBE_CHANNEL,
        "pricing": ResourcePricing.FREE,
        "author": "Raj Vikramaditya (Striver)",
        "platform": "YouTube",
        "language": "English",
        "category": "DSA",
        "skills_covered": ["Arrays", "Linked Lists", "Trees", "Graphs", "DP", "Recursion"],
        "difficulty_level": "intermediate",
        "relevant_roles": ["SDE", "Software Engineer"],
        "is_indian_creator": True,
        "is_india_focused": True,
        "is_recommended": True
    },
    # LeetCode & Practice
    {
        "title": "LeetCode",
        "description": "Best platform for coding interview preparation",
        "url": "https://leetcode.com",
        "resource_type": ResourceType.WEBSITE,
        "pricing": ResourcePricing.FREEMIUM,
        "platform": "LeetCode",
        "language": "English",
        "category": "DSA",
        "skills_covered": ["Problem Solving", "DSA", "System Design"],
        "difficulty_level": "all",
        "relevant_roles": ["SDE", "Software Engineer"],
        "is_recommended": True
    },
    {
        "title": "NeetCode",
        "description": "Curated LeetCode problems with explanations",
        "url": "https://neetcode.io",
        "resource_type": ResourceType.WEBSITE,
        "pricing": ResourcePricing.FREE,
        "author": "NeetCode",
        "platform": "NeetCode",
        "language": "English",
        "category": "DSA",
        "skills_covered": ["DSA", "Problem Solving", "Interview Prep"],
        "difficulty_level": "intermediate",
        "relevant_roles": ["SDE", "Software Engineer"],
        "is_recommended": True
    },
    # System Design
    {
        "title": "System Design Primer",
        "description": "Comprehensive system design guide on GitHub",
        "url": "https://github.com/donnemartin/system-design-primer",
        "resource_type": ResourceType.GITHUB_REPO,
        "pricing": ResourcePricing.FREE,
        "author": "Donne Martin",
        "platform": "GitHub",
        "language": "English",
        "category": "System Design",
        "skills_covered": ["Scalability", "Load Balancing", "Caching", "Databases"],
        "difficulty_level": "advanced",
        "relevant_roles": ["Senior SDE", "Staff Engineer", "System Architect"],
        "is_recommended": True
    },
]

# =============================================================================
# ROADMAPS
# =============================================================================
ROADMAPS_DATA = [
    {
        "title": "Software Developer Roadmap 2024",
        "slug": "software-developer-roadmap-2024",
        "description": "Complete roadmap to become a Software Developer in 2024",
        "role": "Software Developer",
        "experience_level": "fresher",
        "overview": "This roadmap covers everything from programming basics to getting placed at top tech companies.",
        "estimated_duration_months": 8,
        "is_official": True,
        "steps": [
            {
                "order": 1,
                "title": "Programming Fundamentals",
                "description": "Learn one programming language deeply - Python or Java recommended",
                "duration_weeks": 6,
                "skills_to_learn": ["Variables", "Data types", "Control flow", "Functions", "OOP"],
                "projects": ["Calculator", "To-do app", "Student management system"],
                "milestones": ["Complete 50 basic problems", "Build 3 mini projects"]
            },
            {
                "order": 2,
                "title": "Data Structures & Algorithms",
                "description": "Master DSA - crucial for interviews",
                "duration_weeks": 12,
                "skills_to_learn": ["Arrays", "Strings", "Linked Lists", "Trees", "Graphs", "DP", "Sorting", "Searching"],
                "projects": ["Implement all DS from scratch"],
                "milestones": ["Solve 200 LeetCode problems", "Complete Striver's SDE Sheet"]
            },
            {
                "order": 3,
                "title": "Database & SQL",
                "description": "Learn database fundamentals and SQL",
                "duration_weeks": 3,
                "skills_to_learn": ["SQL queries", "Joins", "Normalization", "Indexing", "ACID"],
                "projects": ["Design database for e-commerce"],
                "milestones": ["Complete HackerRank SQL", "Design 3 database schemas"]
            },
            {
                "order": 4,
                "title": "Web Development Basics",
                "description": "Learn frontend and backend basics",
                "duration_weeks": 6,
                "skills_to_learn": ["HTML", "CSS", "JavaScript", "React/Vue", "Node.js/Django", "REST APIs"],
                "projects": ["Portfolio website", "Full-stack CRUD app"],
                "milestones": ["Deploy portfolio", "Build and deploy one full-stack app"]
            },
            {
                "order": 5,
                "title": "System Design Basics",
                "description": "Understand system design fundamentals",
                "duration_weeks": 4,
                "skills_to_learn": ["Scalability", "Load balancing", "Caching", "Database sharding", "Microservices"],
                "projects": ["Design URL shortener", "Design rate limiter"],
                "milestones": ["Learn 5 common system designs"]
            },
            {
                "order": 6,
                "title": "Interview Preparation",
                "description": "Prepare for technical interviews",
                "duration_weeks": 4,
                "skills_to_learn": ["Resume building", "Mock interviews", "Behavioral questions", "Negotiation"],
                "projects": ["Prepare STAR format answers"],
                "milestones": ["Give 5 mock interviews", "Apply to 50+ companies"]
            }
        ]
    },
    {
        "title": "Data Scientist Roadmap 2024",
        "slug": "data-scientist-roadmap-2024",
        "description": "Complete roadmap to become a Data Scientist",
        "role": "Data Scientist",
        "experience_level": "fresher",
        "overview": "From Python basics to ML deployment, this roadmap covers the entire Data Science journey.",
        "estimated_duration_months": 10,
        "is_official": True,
        "steps": [
            {
                "order": 1,
                "title": "Python & Statistics",
                "description": "Master Python programming and statistics fundamentals",
                "duration_weeks": 6,
                "skills_to_learn": ["Python", "NumPy", "Pandas", "Statistics", "Probability"],
                "projects": ["Data analysis with Pandas"],
                "milestones": ["Complete Python course", "Solve Kaggle exercises"]
            },
            {
                "order": 2,
                "title": "Data Analysis & Visualization",
                "description": "Learn to analyze and visualize data",
                "duration_weeks": 4,
                "skills_to_learn": ["EDA", "Matplotlib", "Seaborn", "Plotly", "Tableau/Power BI"],
                "projects": ["COVID data analysis", "Stock market analysis"],
                "milestones": ["Complete 5 EDA projects"]
            },
            {
                "order": 3,
                "title": "Machine Learning",
                "description": "Learn ML algorithms and implementation",
                "duration_weeks": 10,
                "skills_to_learn": ["Regression", "Classification", "Clustering", "Ensemble methods", "Feature engineering"],
                "projects": ["House price prediction", "Customer segmentation"],
                "milestones": ["Complete Andrew Ng's ML course", "Win one Kaggle competition"]
            },
            {
                "order": 4,
                "title": "Deep Learning",
                "description": "Master deep learning and neural networks",
                "duration_weeks": 8,
                "skills_to_learn": ["Neural Networks", "CNN", "RNN", "Transformers", "TensorFlow/PyTorch"],
                "projects": ["Image classification", "Text classification"],
                "milestones": ["Build 3 DL projects", "Publish one on GitHub"]
            },
            {
                "order": 5,
                "title": "MLOps & Deployment",
                "description": "Learn to deploy ML models",
                "duration_weeks": 4,
                "skills_to_learn": ["Docker", "Flask/FastAPI", "MLflow", "AWS/GCP basics", "CI/CD"],
                "projects": ["Deploy ML model as API"],
                "milestones": ["Deploy 2 ML models to cloud"]
            },
            {
                "order": 6,
                "title": "GenAI & LLMs",
                "description": "Learn Generative AI and Large Language Models",
                "duration_weeks": 6,
                "skills_to_learn": ["LLMs", "Prompt Engineering", "LangChain", "RAG", "Fine-tuning"],
                "projects": ["Build RAG chatbot", "Document QA system"],
                "milestones": ["Build 2 GenAI applications"]
            }
        ]
    },
]

# =============================================================================
# AGENCIES
# =============================================================================
AGENCIES_DATA = [
    {
        "name": "Y-Axis",
        "slug": "y-axis",
        "website": "https://y-axis.com",
        "description": "One of India's largest immigration consultants",
        "agency_type": "abroad_placement",
        "specializations": ["IT", "Healthcare", "Engineering"],
        "headquarters_city": "Hyderabad",
        "headquarters_country": "India",
        "countries_served": ["Canada", "Australia", "Germany", "UK", "USA"],
        "visa_assistance": True,
        "relocation_support": True,
        "is_free_for_candidates": False,
        "fee_structure": "Varies by country and service",
        "is_verified": True,
        "is_government_registered": True,
        "rating": 3.8,
        "is_recommended": True
    },
    {
        "name": "Fragomen",
        "slug": "fragomen",
        "website": "https://fragomen.com",
        "description": "Global immigration law firm",
        "agency_type": "abroad_placement",
        "specializations": ["IT", "Legal", "Corporate"],
        "headquarters_country": "USA",
        "countries_served": ["USA", "UK", "Germany", "Canada", "Singapore"],
        "visa_assistance": True,
        "relocation_support": True,
        "is_free_for_candidates": True,
        "fee_structure": "Paid by employer",
        "is_verified": True,
        "rating": 4.5,
        "is_recommended": True
    },
    {
        "name": "Turing",
        "slug": "turing",
        "website": "https://turing.com",
        "description": "Remote US jobs for Indian developers",
        "agency_type": "remote_jobs",
        "specializations": ["Software Development", "AI/ML", "DevOps"],
        "headquarters_country": "USA",
        "countries_served": ["USA"],
        "visa_assistance": False,
        "relocation_support": False,
        "is_free_for_candidates": True,
        "fee_structure": "Free - company takes margin from hourly rate",
        "is_verified": True,
        "rating": 4.0,
        "is_recommended": True
    },
    {
        "name": "Toptal",
        "slug": "toptal-agency",
        "website": "https://toptal.com",
        "description": "Top 3% freelance talent network",
        "agency_type": "remote_jobs",
        "specializations": ["Software Development", "Design", "Finance"],
        "headquarters_country": "USA",
        "countries_served": ["Worldwide"],
        "visa_assistance": False,
        "relocation_support": False,
        "is_free_for_candidates": True,
        "fee_structure": "Free - Toptal takes margin",
        "is_verified": True,
        "rating": 4.3,
        "is_recommended": True
    },
    {
        "name": "Andela",
        "slug": "andela",
        "website": "https://andela.com",
        "description": "Global talent network for engineers",
        "agency_type": "remote_jobs",
        "specializations": ["Software Development", "Data Science"],
        "headquarters_country": "USA",
        "countries_served": ["USA", "Europe"],
        "visa_assistance": False,
        "relocation_support": False,
        "is_free_for_candidates": True,
        "fee_structure": "Free for candidates",
        "is_verified": True,
        "rating": 4.1,
        "is_recommended": True
    },
]


def seed_all():
    """Seed all data to database"""
    logger.info("🌱 Starting database seeding...")
    
    init_db()
    db = SessionLocal()
    
    try:
        # Seed companies
        logger.info("📊 Seeding companies...")
        for company_data in PRODUCT_COMPANIES_INDIA + SERVICE_COMPANIES_INDIA + REMOTE_COMPANIES:
            existing = db.query(Company).filter(Company.slug == company_data.get("slug")).first()
            if not existing:
                company = Company(**company_data)
                db.add(company)
        db.commit()
        logger.info(f"✅ Seeded {len(PRODUCT_COMPANIES_INDIA) + len(SERVICE_COMPANIES_INDIA) + len(REMOTE_COMPANIES)} companies")
        
        # Seed countries
        logger.info("🌍 Seeding countries...")
        for country_data in COUNTRIES_DATA:
            existing = db.query(Country).filter(Country.code == country_data.get("code")).first()
            if not existing:
                country = Country(**country_data)
                db.add(country)
        db.commit()
        logger.info(f"✅ Seeded {len(COUNTRIES_DATA)} countries")
        
        # Seed migration guides
        logger.info("📋 Seeding migration guides...")
        for guide_data in MIGRATION_GUIDES:
            existing = db.query(CountryMigration).filter(
                CountryMigration.country_name == guide_data.get("country_name")
            ).first()
            if not existing:
                guide = CountryMigration(**guide_data)
                db.add(guide)
        db.commit()
        logger.info(f"✅ Seeded {len(MIGRATION_GUIDES)} migration guides")
        
        # Seed resources
        logger.info("📚 Seeding learning resources...")
        for resource_data in LEARNING_RESOURCES:
            existing = db.query(Resource).filter(Resource.url == resource_data.get("url")).first()
            if not existing:
                resource = Resource(**resource_data)
                db.add(resource)
        db.commit()
        logger.info(f"✅ Seeded {len(LEARNING_RESOURCES)} resources")
        
        # Seed roadmaps
        logger.info("🗺️ Seeding roadmaps...")
        for roadmap_data in ROADMAPS_DATA:
            existing = db.query(Roadmap).filter(Roadmap.slug == roadmap_data.get("slug")).first()
            if not existing:
                steps_data = roadmap_data.pop("steps", [])
                roadmap = Roadmap(**roadmap_data)
                db.add(roadmap)
                db.flush()
                
                for step_data in steps_data:
                    step = RoadmapStep(roadmap_id=roadmap.id, **step_data)
                    db.add(step)
        db.commit()
        logger.info(f"✅ Seeded {len(ROADMAPS_DATA)} roadmaps")
        
        # Seed agencies
        logger.info("🏢 Seeding agencies...")
        for agency_data in AGENCIES_DATA:
            existing = db.query(Agency).filter(Agency.slug == agency_data.get("slug")).first()
            if not existing:
                agency = Agency(**agency_data)
                db.add(agency)
        db.commit()
        logger.info(f"✅ Seeded {len(AGENCIES_DATA)} agencies")
        
        logger.info("🎉 Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()




