"""
Scraper API Routes - Trigger and monitor scraping jobs
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Scraping status tracking
scraping_status = {
    "companies": {"status": "idle", "progress": 0, "total": 0, "last_run": None},
    "jobs": {"status": "idle", "progress": 0, "total": 0, "last_run": None},
    "resources": {"status": "idle", "progress": 0, "total": 0, "last_run": None}
}

@router.get("/status")
async def get_scraper_status():
    """Get current scraping status"""
    return scraping_status

@router.post("/companies/start")
async def start_company_scraping(
    background_tasks: BackgroundTasks,
    source: Optional[str] = "all"  # "linkedin", "glassdoor", "ambitionbox", "all"
):
    """Start company data scraping"""
    if scraping_status["companies"]["status"] == "running":
        raise HTTPException(status_code=400, detail="Company scraping already in progress")
    
    from backend.scrapers.companies.company_scraper import CompanyScraper
    
    scraper = CompanyScraper()
    background_tasks.add_task(scraper.run, source)
    
    scraping_status["companies"]["status"] = "running"
    
    return {"message": "Company scraping started", "source": source}

@router.post("/jobs/start")
async def start_job_scraping(
    background_tasks: BackgroundTasks,
    source: Optional[str] = "all"  # "linkedin", "naukri", "indeed", "all"
):
    """Start job scraping"""
    if scraping_status["jobs"]["status"] == "running":
        raise HTTPException(status_code=400, detail="Job scraping already in progress")
    
    scraping_status["jobs"]["status"] = "running"
    
    return {"message": "Job scraping started", "source": source}

@router.post("/resources/start")
async def start_resource_scraping(
    background_tasks: BackgroundTasks,
    source: Optional[str] = "all"
):
    """Start learning resources scraping"""
    if scraping_status["resources"]["status"] == "running":
        raise HTTPException(status_code=400, detail="Resource scraping already in progress")
    
    scraping_status["resources"]["status"] = "running"
    
    return {"message": "Resource scraping started", "source": source}

@router.post("/stop/{scraper_type}")
async def stop_scraping(scraper_type: str):
    """Stop a running scraper"""
    if scraper_type not in scraping_status:
        raise HTTPException(status_code=404, detail="Invalid scraper type")
    
    scraping_status[scraper_type]["status"] = "stopped"
    return {"message": f"{scraper_type} scraping stopped"}

@router.post("/seed")
async def seed_database(background_tasks: BackgroundTasks):
    """Seed database with initial data"""
    from backend.data.seeds.seed_data import seed_all
    
    background_tasks.add_task(seed_all)
    return {"message": "Database seeding started"}




