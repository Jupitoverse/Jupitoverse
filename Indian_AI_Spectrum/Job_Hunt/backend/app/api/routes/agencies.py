"""
Agencies API Routes - Recruitment agencies
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models.database import get_db
from app.models.agency import Agency

router = APIRouter()

@router.get("/")
async def get_agencies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    agency_type: Optional[str] = None,
    country: Optional[str] = None,
    is_verified: Optional[bool] = None,
    search: Optional[str] = None
):
    """Get list of recruitment agencies"""
    query = db.query(Agency)
    
    if agency_type:
        query = query.filter(Agency.agency_type == agency_type)
    if country:
        query = query.filter(Agency.countries_served.contains([country]))
    if is_verified is not None:
        query = query.filter(Agency.is_verified == is_verified)
    if search:
        query = query.filter(Agency.name.ilike(f"%{search}%"))
    
    total = query.count()
    agencies = query.offset(skip).limit(limit).all()
    
    return {"total": total, "agencies": agencies}

@router.get("/abroad-jobs")
async def get_abroad_agencies(
    db: Session = Depends(get_db),
    target_country: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get agencies for abroad job placement"""
    query = db.query(Agency).filter(Agency.agency_type == "abroad_placement")
    if target_country:
        query = query.filter(Agency.countries_served.contains([target_country]))
    return query.offset(skip).limit(limit).all()

@router.get("/remote-jobs")
async def get_remote_agencies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get agencies for remote job placement"""
    return db.query(Agency).filter(
        Agency.agency_type == "remote_jobs"
    ).offset(skip).limit(limit).all()

@router.get("/verified")
async def get_verified_agencies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get verified agencies only"""
    return db.query(Agency).filter(
        Agency.is_verified == True
    ).order_by(Agency.rating.desc()).offset(skip).limit(limit).all()

@router.get("/{agency_id}")
async def get_agency(agency_id: int, db: Session = Depends(get_db)):
    """Get agency details"""
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency




