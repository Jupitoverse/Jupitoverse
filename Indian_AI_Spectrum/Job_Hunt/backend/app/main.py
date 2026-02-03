"""
Job Hunt Portal - Main FastAPI Application
A comprehensive job portal for Indian job seekers
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from sqlalchemy.orm import Session
from app.models.database import init_db, get_db
from fastapi import Depends
from app.api.routes import companies, jobs, resources, countries, agencies, referrals, reviews, users, scraper, auth, hr_contacts, profile, content

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Job Hunt Portal API...")
    init_db()
    logger.info("✅ Database initialized successfully!")
    yield
    logger.info("👋 Shutting down Job Hunt Portal API...")

app = FastAPI(
    title="Job Hunt Portal API",
    description="""
    🎯 **Indian AI Spectrum - Job Hunt Portal**
    
    A comprehensive job portal tailored for Indian job seekers in IT/AI/STEM fields.
    
    ## Features
    - 🏢 **Companies Database** - Product, Service, Startups with detailed info
    - 💼 **Jobs Aggregation** - From multiple sources
    - 🌍 **Abroad Jobs** - Migration guides for top countries
    - 📚 **Learning Resources** - Courses, tutorials, roadmaps
    - 🔗 **Referral System** - Get referred by company employees
    - ⭐ **Reviews & Ratings** - Honest company reviews
    - 🏃 **Career Roadmaps** - Step-by-step guides
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(countries.router, prefix="/api/v1/countries", tags=["Countries"])
app.include_router(agencies.router, prefix="/api/v1/agencies", tags=["Agencies"])
app.include_router(referrals.router, prefix="/api/v1/referrals", tags=["Referrals"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(hr_contacts.router, prefix="/api/v1/hr-contacts", tags=["HR Contacts"])
app.include_router(scraper.router, prefix="/api/v1/scraper", tags=["Scraper"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])

@app.get("/", tags=["Root"])
async def root():
    """API Root - Health check"""
    return {
        "status": "online",
        "message": "🎯 Job Hunt Portal API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/v1/stats", tags=["Stats"])
async def get_stats(db: Session = Depends(get_db)):
    """Get portal statistics"""
    from app.models.company import Company, CompanyType
    from app.models.job import Job
    from app.models.resource import Resource, Roadmap, ResourceType
    from app.models.country import Country, CountryMigration
    from app.models.agency import Agency
    from app.models.user import User
    from app.models.hr_contact import HRContact
    
    # Company stats
    total_companies = db.query(Company).count()
    product_companies = db.query(Company).filter(Company.company_type == CompanyType.PRODUCT).count()
    service_companies = db.query(Company).filter(Company.company_type == CompanyType.SERVICE).count()
    remote_companies = db.query(Company).filter(Company.is_remote_friendly == True).count()
    hiring_companies = db.query(Company).filter(Company.is_actively_hiring == True).count()
    
    # Job stats
    total_jobs = db.query(Job).count()
    active_jobs = db.query(Job).filter(Job.is_active == True).count()
    
    # Resource stats
    total_resources = db.query(Resource).count()
    courses = db.query(Resource).filter(Resource.resource_type == ResourceType.COURSE).count()
    roadmaps = db.query(Roadmap).count()
    
    # Country stats
    total_countries = db.query(Country).count()
    guides_available = db.query(CountryMigration).count()
    
    # User stats
    total_users = db.query(User).count()
    
    # Agency stats
    total_agencies = db.query(Agency).count()
    
    # HR Contact stats
    total_hr_contacts = db.query(HRContact).count()
    
    return {
        "companies": {
            "total": total_companies,
            "product_based": product_companies,
            "service_based": service_companies,
            "startups": 0,
            "remote_friendly": remote_companies,
            "actively_hiring": hiring_companies
        },
        "jobs": {
            "total": total_jobs,
            "active": active_jobs,
            "remote": 0,
            "abroad": 0
        },
        "resources": {
            "total": total_resources,
            "courses": courses,
            "roadmaps": roadmaps
        },
        "countries": {
            "total": total_countries,
            "guides_available": guides_available
        },
        "users": {
            "total": total_users,
            "verified_employees": 0
        },
        "agencies": {
            "total": total_agencies
        },
        "hr_contacts": {
            "total": total_hr_contacts
        }
    }
