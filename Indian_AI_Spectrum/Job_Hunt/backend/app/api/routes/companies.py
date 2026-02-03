"""
Companies API Routes - Comprehensive company directory
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, or_
from typing import List, Optional
from app.models.database import get_db
from app.models.company import Company, CompanyType, CompanyCategory

router = APIRouter()

@router.get("/")
async def get_companies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    company_type: Optional[str] = None,
    category: Optional[str] = None,
    industry: Optional[str] = None,
    country: Optional[str] = None,
    is_remote_friendly: Optional[bool] = None,
    has_indian_office: Optional[bool] = None,
    is_actively_hiring: Optional[bool] = None,
    search: Optional[str] = None
):
    """Get list of companies with filters"""
    query = db.query(Company)
    
    if company_type:
        query = query.filter(Company.company_type == company_type)
    if category:
        query = query.filter(Company.category == category)
    if industry:
        query = query.filter(Company.industry.ilike(f"%{industry}%"))
    if country:
        query = query.filter(Company.headquarters_country.ilike(f"%{country}%"))
    if is_remote_friendly is not None:
        query = query.filter(Company.is_remote_friendly == is_remote_friendly)
    if has_indian_office is not None:
        query = query.filter(Company.has_indian_office == has_indian_office)
    if is_actively_hiring is not None:
        query = query.filter(Company.is_actively_hiring == is_actively_hiring)
    if search:
        query = query.filter(
            or_(
                Company.name.ilike(f"%{search}%"),
                Company.description.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%"),
                Company.tagline.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    companies = query.order_by(Company.name).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "companies": companies
    }

@router.get("/filters")
async def get_filter_options(db: Session = Depends(get_db)):
    """Get all available filter options"""
    industries = db.query(distinct(Company.industry)).filter(Company.industry.isnot(None)).all()
    countries = db.query(distinct(Company.headquarters_country)).filter(Company.headquarters_country.isnot(None)).all()
    
    return {
        "company_types": [t.value for t in CompanyType],
        "categories": [c.value for c in CompanyCategory],
        "industries": sorted([i[0] for i in industries if i[0]]),
        "countries": sorted([c[0] for c in countries if c[0]])
    }

@router.get("/stats")
async def get_company_stats(db: Session = Depends(get_db)):
    """Get company statistics by type and category"""
    total = db.query(Company).count()
    by_type = db.query(Company.company_type, func.count(Company.id)).group_by(Company.company_type).all()
    by_category = db.query(Company.category, func.count(Company.id)).group_by(Company.category).all()
    by_country = db.query(Company.headquarters_country, func.count(Company.id)).group_by(Company.headquarters_country).all()
    indian_offices = db.query(Company).filter(Company.has_indian_office == True).count()
    remote_friendly = db.query(Company).filter(Company.is_remote_friendly == True).count()
    actively_hiring = db.query(Company).filter(Company.is_actively_hiring == True).count()
    
    return {
        "total": total,
        "by_type": {str(t[0].value) if t[0] else "unknown": t[1] for t in by_type},
        "by_category": {str(c[0].value) if c[0] else "unknown": c[1] for c in by_category},
        "by_country": {c[0] or "unknown": c[1] for c in by_country},
        "with_indian_offices": indian_offices,
        "remote_friendly": remote_friendly,
        "actively_hiring": actively_hiring
    }

@router.get("/types")
async def get_company_types():
    """Get all company types"""
    return {
        "types": [t.value for t in CompanyType],
        "categories": [c.value for c in CompanyCategory]
    }

@router.get("/product-based")
async def get_product_companies(
    db: Session = Depends(get_db),
    country: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get product-based companies"""
    query = db.query(Company).filter(Company.company_type == CompanyType.PRODUCT)
    if country:
        query = query.filter(Company.headquarters_country == country)
    return query.offset(skip).limit(limit).all()

@router.get("/service-based")
async def get_service_companies(
    db: Session = Depends(get_db),
    country: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get service-based companies"""
    query = db.query(Company).filter(Company.company_type == CompanyType.SERVICE)
    if country:
        query = query.filter(Company.headquarters_country == country)
    return query.offset(skip).limit(limit).all()

@router.get("/remote-friendly")
async def get_remote_companies(
    db: Session = Depends(get_db),
    hires_from_india: bool = True,
    skip: int = 0,
    limit: int = 50
):
    """Get remote-friendly companies"""
    query = db.query(Company).filter(Company.is_remote_friendly == True)
    if hires_from_india:
        query = query.filter(Company.hires_from_india == True)
    return query.offset(skip).limit(limit).all()

@router.get("/faang")
async def get_faang_companies(db: Session = Depends(get_db)):
    """Get FAANG/MAANG companies"""
    return db.query(Company).filter(
        Company.category.in_([CompanyCategory.FAANG, CompanyCategory.MAANG])
    ).all()

@router.get("/{company_id}")
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company by ID with full details"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/slug/{slug}")
async def get_company_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get company by slug"""
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

