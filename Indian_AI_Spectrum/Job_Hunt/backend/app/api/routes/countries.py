"""
Countries API Routes - Migration guides for abroad jobs
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models.database import get_db
from app.models.country import Country, CountryMigration

router = APIRouter()

# Common country name aliases
COUNTRY_ALIASES = {
    "UAE": "United Arab Emirates",
    "UK": "United Kingdom",
    "USA": "United States",
    "US": "United States",
}

def get_country_search_term(country_code: str) -> str:
    """Get the search term for a country, handling aliases"""
    return COUNTRY_ALIASES.get(country_code.upper(), country_code)

@router.get("/")
async def get_countries(
    db: Session = Depends(get_db),
    is_popular_destination: Optional[bool] = None
):
    """Get list of countries for abroad jobs"""
    query = db.query(Country)
    if is_popular_destination is not None:
        query = query.filter(Country.is_popular_destination == is_popular_destination)
    return query.all()

@router.get("/migrations")
async def get_all_migrations(db: Session = Depends(get_db)):
    """Get all migration guides"""
    return db.query(CountryMigration).all()

@router.get("/popular")
async def get_popular_countries(db: Session = Depends(get_db)):
    """Get popular destination countries for Indians"""
    return db.query(Country).filter(
        Country.is_popular_destination == True
    ).order_by(Country.indian_friendly_score.desc()).all()

@router.get("/{country_code}")
async def get_country(country_code: str, db: Session = Depends(get_db)):
    """Get country details"""
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.get("/{country_code}/migration-guide")
async def get_migration_guide(country_code: str, db: Session = Depends(get_db)):
    """Get detailed migration guide for a country"""
    search_term = get_country_search_term(country_code)
    guide = db.query(CountryMigration).filter(
        CountryMigration.country_name.ilike(f"%{search_term}%")
    ).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Migration guide not found")
    return guide

@router.get("/{country_code}/visa-info")
async def get_visa_info(country_code: str, db: Session = Depends(get_db)):
    """Get visa information for a country"""
    search_term = get_country_search_term(country_code)
    guide = db.query(CountryMigration).filter(
        CountryMigration.country_name.ilike(f"%{search_term}%")
    ).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Visa info not found")
    return {
        "visa_types": guide.visa_types,
        "visa_process_steps": guide.visa_process_steps,
        "processing_time_weeks": guide.visa_processing_time_weeks,
        "cost_usd": guide.visa_cost_usd,
        "employer_sponsorship_required": guide.employer_sponsorship_required
    }

@router.get("/{country_code}/job-portals")
async def get_job_portals(country_code: str, db: Session = Depends(get_db)):
    """Get job portals for a country"""
    search_term = get_country_search_term(country_code)
    guide = db.query(CountryMigration).filter(
        CountryMigration.country_name.ilike(f"%{search_term}%")
    ).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Info not found")
    return {
        "job_portals": guide.popular_job_portals,
        "recruitment_agencies": guide.recruitment_agencies
    }

@router.get("/{country_code}/cost-of-living")
async def get_cost_of_living(country_code: str, db: Session = Depends(get_db)):
    """Get cost of living for a country"""
    search_term = get_country_search_term(country_code)
    guide = db.query(CountryMigration).filter(
        CountryMigration.country_name.ilike(f"%{search_term}%")
    ).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Info not found")
    return {
        "monthly_expenses": guide.monthly_expenses_estimate,
        "initial_settlement_cost": guide.initial_settlement_cost
    }

