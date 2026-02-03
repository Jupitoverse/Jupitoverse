"""
Additional Seed Data - More Companies, Resources, and Agencies
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.company import Company, CompanyType, CompanyCategory
from app.models.resource import Resource, ResourceType, ResourcePricing
from app.models.agency import Agency
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# More Product Companies
MORE_PRODUCT_COMPANIES = [
    # More FAANG/Tech Giants
    {"name": "Stripe", "slug": "stripe", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "FinTech", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "hires_from_india": True, "interview_difficulty": 4.5, "work_life_balance": 4.3, "avg_salary_india": {"entry": 3000000, "mid": 6000000, "senior": 12000000}, "careers_page": "https://stripe.com/jobs", "is_verified": True, "is_actively_hiring": True},
    {"name": "Airbnb", "slug": "airbnb", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Travel Tech", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "full", "interview_difficulty": 4.4, "work_life_balance": 4.4, "avg_salary_india": {"entry": 2800000, "mid": 5500000, "senior": 11000000}, "careers_page": "https://careers.airbnb.com", "is_verified": True, "is_actively_hiring": True},
    {"name": "Shopify", "slug": "shopify", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "E-commerce", "headquarters_country": "Canada", "has_indian_office": False, "is_remote_friendly": True, "remote_policy": "full", "hires_from_india": True, "interview_difficulty": 4.2, "work_life_balance": 4.5, "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000}, "careers_page": "https://shopify.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Spotify", "slug": "spotify", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Music/Entertainment", "headquarters_country": "Sweden", "has_indian_office": True, "indian_cities": ["Mumbai"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.3, "work_life_balance": 4.4, "avg_salary_india": {"entry": 2400000, "mid": 4800000, "senior": 9500000}, "careers_page": "https://spotifyjobs.com", "is_verified": True, "is_actively_hiring": True},
    {"name": "Twitter/X", "slug": "twitter-x", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Social Media", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.3, "work_life_balance": 3.8, "avg_salary_india": {"entry": 2600000, "mid": 5200000, "senior": 10000000}, "careers_page": "https://careers.twitter.com", "is_verified": True, "is_actively_hiring": True},
    {"name": "Snowflake", "slug": "snowflake", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Data/Cloud", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.4, "work_life_balance": 4.1, "avg_salary_india": {"entry": 2800000, "mid": 5600000, "senior": 11000000}, "careers_page": "https://careers.snowflake.com", "is_verified": True, "is_actively_hiring": True},
    {"name": "Databricks", "slug": "databricks", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Data/AI", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.5, "work_life_balance": 4.2, "avg_salary_india": {"entry": 3000000, "mid": 6000000, "senior": 12000000}, "careers_page": "https://databricks.com/company/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Confluent", "slug": "confluent", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Data/Streaming", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.2, "work_life_balance": 4.3, "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000}, "careers_page": "https://confluent.io/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "HashiCorp", "slug": "hashicorp", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "DevOps/Infrastructure", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "full", "hires_from_india": True, "interview_difficulty": 4.3, "work_life_balance": 4.4, "avg_salary_india": {"entry": 2600000, "mid": 5200000, "senior": 10500000}, "careers_page": "https://hashicorp.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Elastic", "slug": "elastic", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Search/Data", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore", "Hyderabad"], "is_remote_friendly": True, "remote_policy": "full", "interview_difficulty": 4.1, "work_life_balance": 4.3, "avg_salary_india": {"entry": 2400000, "mid": 4800000, "senior": 9500000}, "careers_page": "https://elastic.co/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "MongoDB", "slug": "mongodb", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Database", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.2, "work_life_balance": 4.2, "avg_salary_india": {"entry": 2500000, "mid": 5000000, "senior": 10000000}, "careers_page": "https://mongodb.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Redis", "slug": "redis", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Database", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 4.3, "avg_salary_india": {"entry": 2300000, "mid": 4600000, "senior": 9000000}, "careers_page": "https://redis.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Cloudflare", "slug": "cloudflare", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Security/CDN", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.3, "work_life_balance": 4.2, "avg_salary_india": {"entry": 2600000, "mid": 5200000, "senior": 10500000}, "careers_page": "https://cloudflare.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Twilio", "slug": "twilio", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Communications", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.1, "work_life_balance": 4.2, "avg_salary_india": {"entry": 2400000, "mid": 4800000, "senior": 9500000}, "careers_page": "https://twilio.com/company/jobs", "is_verified": True, "is_actively_hiring": True},
    {"name": "Okta", "slug": "okta", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Security/Identity", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 4.3, "avg_salary_india": {"entry": 2300000, "mid": 4600000, "senior": 9200000}, "careers_page": "https://okta.com/company/careers", "is_verified": True, "is_actively_hiring": True},
    
    # More Indian Startups/Unicorns
    {"name": "Dream11", "slug": "dream11", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Gaming/Sports", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Mumbai"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 3.8, "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000}, "careers_page": "https://dreamsports.group/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "MPL (Mobile Premier League)", "slug": "mpl", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Gaming", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.8, "work_life_balance": 3.7, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://mpl.live/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Groww", "slug": "groww", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 3.9, "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000}, "careers_page": "https://groww.in/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Jupiter (FinTech)", "slug": "jupiter-fintech", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "FinTech/Banking", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.8, "work_life_balance": 4.0, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://jupiter.money/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Navi", "slug": "navi", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.9, "work_life_balance": 3.8, "avg_salary_india": {"entry": 1600000, "mid": 3200000, "senior": 6500000}, "careers_page": "https://navi.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Slice", "slug": "slice", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.8, "work_life_balance": 3.9, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://sliceit.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Lenskart", "slug": "lenskart", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "E-commerce/Retail", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Delhi NCR", "Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.7, "work_life_balance": 3.6, "avg_salary_india": {"entry": 1400000, "mid": 2800000, "senior": 5500000}, "careers_page": "https://lenskart.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Unacademy", "slug": "unacademy", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.6, "work_life_balance": 3.4, "avg_salary_india": {"entry": 1400000, "mid": 2800000, "senior": 5500000}, "careers_page": "https://unacademy.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "BYJU'S", "slug": "byjus", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.5, "work_life_balance": 3.2, "avg_salary_india": {"entry": 1200000, "mid": 2400000, "senior": 5000000}, "careers_page": "https://byjus.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "upGrad", "slug": "upgrad", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Mumbai", "Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.6, "work_life_balance": 3.5, "avg_salary_india": {"entry": 1200000, "mid": 2400000, "senior": 5000000}, "careers_page": "https://upgrad.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Delhivery", "slug": "delhivery", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Logistics", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Gurgaon", "Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.6, "work_life_balance": 3.5, "avg_salary_india": {"entry": 1200000, "mid": 2400000, "senior": 5000000}, "careers_page": "https://delhivery.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "BigBasket", "slug": "bigbasket", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "E-commerce/Grocery", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.5, "work_life_balance": 3.4, "avg_salary_india": {"entry": 1200000, "mid": 2400000, "senior": 5000000}, "careers_page": "https://bigbasket.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "ShareChat", "slug": "sharechat", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Social Media", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.8, "work_life_balance": 3.7, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://sharechat.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Freshworks", "slug": "freshworks", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "SaaS/CRM", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Chennai", "Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.9, "work_life_balance": 4.0, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://freshworks.com/company/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Zoho", "slug": "zoho", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "SaaS", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Chennai", "Bangalore", "Coimbatore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.7, "work_life_balance": 4.2, "avg_salary_india": {"entry": 1000000, "mid": 2000000, "senior": 4000000}, "careers_page": "https://zoho.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Postman", "slug": "postman", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Developer Tools", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.1, "work_life_balance": 4.2, "avg_salary_india": {"entry": 2200000, "mid": 4400000, "senior": 9000000}, "careers_page": "https://postman.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Chargebee", "slug": "chargebee", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "SaaS/Billing", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Chennai"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.9, "work_life_balance": 4.1, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://chargebee.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "BrowserStack", "slug": "browserstack", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Developer Tools", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Mumbai"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 4.2, "avg_salary_india": {"entry": 2000000, "mid": 4000000, "senior": 8000000}, "careers_page": "https://browserstack.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Druva", "slug": "druva", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Data Protection", "headquarters_country": "USA", "has_indian_office": True, "indian_cities": ["Pune"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.9, "work_life_balance": 4.0, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://druva.com/company/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "CleverTap", "slug": "clevertap", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "MarTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Mumbai"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.7, "work_life_balance": 4.0, "avg_salary_india": {"entry": 1600000, "mid": 3200000, "senior": 6500000}, "careers_page": "https://clevertap.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "MoEngage", "slug": "moengage", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "MarTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.7, "work_life_balance": 4.0, "avg_salary_india": {"entry": 1600000, "mid": 3200000, "senior": 6500000}, "careers_page": "https://moengage.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "InMobi", "slug": "inmobi", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "AdTech", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 4.0, "work_life_balance": 3.9, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://inmobi.com/careers", "is_verified": True, "is_actively_hiring": True},
    {"name": "Glance (InMobi)", "slug": "glance", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Media/Content", "headquarters_country": "India", "has_indian_office": True, "indian_cities": ["Bangalore"], "is_remote_friendly": True, "remote_policy": "hybrid", "interview_difficulty": 3.8, "work_life_balance": 3.8, "avg_salary_india": {"entry": 1800000, "mid": 3600000, "senior": 7500000}, "careers_page": "https://glance.com/careers", "is_verified": True, "is_actively_hiring": True},
]

# More Learning Resources
MORE_RESOURCES = [
    # System Design
    {"title": "Grokking the System Design Interview", "description": "Popular system design course for interviews", "url": "https://designgurus.org/course/grokking-the-system-design-interview", "resource_type": ResourceType.COURSE, "pricing": ResourcePricing.PAID, "platform": "Design Gurus", "category": "System Design", "difficulty_level": "intermediate", "relevant_roles": ["Senior SDE", "Staff Engineer"], "is_recommended": True},
    {"title": "ByteByteGo - System Design", "description": "System design tutorials by Alex Xu", "url": "https://youtube.com/@ByteByteGo", "resource_type": ResourceType.YOUTUBE_CHANNEL, "pricing": ResourcePricing.FREE, "author": "Alex Xu", "platform": "YouTube", "category": "System Design", "difficulty_level": "intermediate", "is_recommended": True},
    {"title": "System Design by Gaurav Sen", "description": "In-depth system design videos", "url": "https://youtube.com/@gaborevich", "resource_type": ResourceType.YOUTUBE_CHANNEL, "pricing": ResourcePricing.FREE, "author": "Gaurav Sen", "platform": "YouTube", "category": "System Design", "difficulty_level": "intermediate", "is_indian_creator": True, "is_recommended": True},
    
    # More DSA
    {"title": "Striver's A2Z DSA Course", "description": "Complete DSA sheet for FAANG preparation", "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.FREE, "author": "Striver", "platform": "TakeUForward", "category": "DSA", "difficulty_level": "all", "is_indian_creator": True, "is_recommended": True},
    {"title": "Love Babbar DSA Sheet", "description": "450 DSA questions for placements", "url": "https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.FREE, "author": "Love Babbar", "platform": "GeeksforGeeks", "category": "DSA", "difficulty_level": "all", "is_indian_creator": True, "is_recommended": True},
    {"title": "Aditya Verma - DP Playlist", "description": "Best Dynamic Programming playlist", "url": "https://youtube.com/playlist?list=PL_z_8CaSLPWekqhdCPmFohncHwz8TY2Go", "resource_type": ResourceType.YOUTUBE_PLAYLIST, "pricing": ResourcePricing.FREE, "author": "Aditya Verma", "platform": "YouTube", "category": "DSA", "subcategory": "Dynamic Programming", "difficulty_level": "intermediate", "is_indian_creator": True, "is_recommended": True},
    
    # DevOps & Cloud
    {"title": "TechWorld with Nana", "description": "DevOps, Kubernetes, Docker tutorials", "url": "https://youtube.com/@TechWorldwithNana", "resource_type": ResourceType.YOUTUBE_CHANNEL, "pricing": ResourcePricing.FREE, "author": "Nana Janashia", "platform": "YouTube", "category": "DevOps", "difficulty_level": "intermediate", "is_recommended": True},
    {"title": "KodeKloud", "description": "DevOps & Kubernetes hands-on labs", "url": "https://kodekloud.com", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.PAID, "platform": "KodeKloud", "category": "DevOps", "difficulty_level": "all", "is_recommended": True},
    {"title": "AWS Certified Solutions Architect", "description": "Official AWS certification course", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "resource_type": ResourceType.COURSE, "pricing": ResourcePricing.PAID, "platform": "AWS", "category": "Cloud", "subcategory": "AWS", "difficulty_level": "intermediate", "is_recommended": True},
    
    # Interview Prep
    {"title": "Pramp", "description": "Free peer-to-peer mock interviews", "url": "https://pramp.com", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.FREE, "platform": "Pramp", "category": "Interview Prep", "difficulty_level": "all", "is_recommended": True},
    {"title": "Interviewing.io", "description": "Anonymous mock interviews with engineers", "url": "https://interviewing.io", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.FREEMIUM, "platform": "Interviewing.io", "category": "Interview Prep", "difficulty_level": "intermediate", "is_recommended": True},
    {"title": "InterviewBit", "description": "Coding practice for interviews", "url": "https://interviewbit.com", "resource_type": ResourceType.WEBSITE, "pricing": ResourcePricing.FREE, "platform": "InterviewBit", "category": "DSA", "difficulty_level": "all", "is_recommended": True},
    
    # GenAI & LLMs
    {"title": "DeepLearning.AI Short Courses", "description": "Free short courses on GenAI, LangChain, RAG", "url": "https://deeplearning.ai/short-courses/", "resource_type": ResourceType.COURSE, "pricing": ResourcePricing.FREE, "author": "Andrew Ng", "platform": "DeepLearning.AI", "category": "AI/ML", "subcategory": "GenAI", "difficulty_level": "intermediate", "is_recommended": True},
    {"title": "Andrej Karpathy - Neural Networks", "description": "Building neural networks from scratch", "url": "https://youtube.com/@AndrejKarpathy", "resource_type": ResourceType.YOUTUBE_CHANNEL, "pricing": ResourcePricing.FREE, "author": "Andrej Karpathy", "platform": "YouTube", "category": "AI/ML", "subcategory": "Deep Learning", "difficulty_level": "advanced", "is_recommended": True},
    {"title": "LangChain Documentation", "description": "Official LangChain docs and tutorials", "url": "https://python.langchain.com", "resource_type": ResourceType.DOCUMENTATION, "pricing": ResourcePricing.FREE, "platform": "LangChain", "category": "AI/ML", "subcategory": "GenAI", "difficulty_level": "intermediate", "is_recommended": True},
]

# More Agencies
MORE_AGENCIES = [
    {"name": "Indeed", "slug": "indeed-agency", "website": "https://indeed.com", "description": "World's largest job site", "agency_type": "general", "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.0},
    {"name": "Glassdoor", "slug": "glassdoor-agency", "website": "https://glassdoor.com", "description": "Jobs + Company Reviews", "agency_type": "general", "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.1},
    {"name": "Naukri", "slug": "naukri", "website": "https://naukri.com", "description": "India's #1 job portal", "agency_type": "general", "countries_served": ["India"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.0},
    {"name": "Instahyre", "slug": "instahyre", "website": "https://instahyre.com", "description": "Premium tech jobs in India", "agency_type": "general", "specializations": ["IT", "Tech"], "countries_served": ["India"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.2},
    {"name": "Cutshort", "slug": "cutshort", "website": "https://cutshort.io", "description": "AI-powered job matching", "agency_type": "general", "specializations": ["IT", "Startups"], "countries_served": ["India"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.0},
    {"name": "AngelList Talent", "slug": "angellist", "website": "https://angel.co/jobs", "description": "Startup jobs worldwide", "agency_type": "general", "specializations": ["Startups"], "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.1},
    {"name": "Remote.co", "slug": "remote-co", "website": "https://remote.co/remote-jobs", "description": "Curated remote jobs", "agency_type": "remote_jobs", "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.0},
    {"name": "FlexJobs", "slug": "flexjobs", "website": "https://flexjobs.com", "description": "Remote & flexible jobs", "agency_type": "remote_jobs", "countries_served": ["Worldwide"], "is_free_for_candidates": False, "is_verified": True, "rating": 4.2},
    {"name": "We Work Remotely", "slug": "weworkremotely", "website": "https://weworkremotely.com", "description": "Largest remote work community", "agency_type": "remote_jobs", "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.3},
    {"name": "RemoteOK", "slug": "remoteok", "website": "https://remoteok.com", "description": "Remote jobs by Pieter Levels", "agency_type": "remote_jobs", "countries_served": ["Worldwide"], "is_free_for_candidates": True, "is_verified": True, "rating": 4.1},
]


def seed_additional_data():
    """Seed additional data to database"""
    logger.info("🌱 Adding more seed data...")
    
    init_db()
    db = SessionLocal()
    
    try:
        # Seed more companies
        logger.info("📊 Adding more companies...")
        added_companies = 0
        for company_data in MORE_PRODUCT_COMPANIES:
            existing = db.query(Company).filter(Company.slug == company_data.get("slug")).first()
            if not existing:
                company = Company(**company_data)
                db.add(company)
                added_companies += 1
        db.commit()
        logger.info(f"✅ Added {added_companies} new companies")
        
        # Seed more resources
        logger.info("📚 Adding more resources...")
        added_resources = 0
        for resource_data in MORE_RESOURCES:
            existing = db.query(Resource).filter(Resource.url == resource_data.get("url")).first()
            if not existing:
                resource = Resource(**resource_data)
                db.add(resource)
                added_resources += 1
        db.commit()
        logger.info(f"✅ Added {added_resources} new resources")
        
        # Seed more agencies
        logger.info("🏢 Adding more agencies...")
        added_agencies = 0
        for agency_data in MORE_AGENCIES:
            existing = db.query(Agency).filter(Agency.slug == agency_data.get("slug")).first()
            if not existing:
                agency = Agency(**agency_data)
                db.add(agency)
                added_agencies += 1
        db.commit()
        logger.info(f"✅ Added {added_agencies} new agencies")
        
        logger.info("🎉 Additional data seeding completed!")
        
    except Exception as e:
        logger.error(f"❌ Error seeding additional data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_additional_data()




