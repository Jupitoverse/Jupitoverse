"""
Referrals API Routes - Internal referral system
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models.database import get_db
from app.models.referral import Referral, ReferralStatus

router = APIRouter()

@router.get("/")
async def get_referrals(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    company_id: Optional[int] = None
):
    """Get list of referral requests"""
    query = db.query(Referral).filter(Referral.is_public == True)
    
    if status:
        query = query.filter(Referral.status == status)
    if company_id:
        query = query.filter(Referral.company_id == company_id)
    
    total = query.count()
    referrals = query.order_by(Referral.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "referrals": referrals}

@router.get("/open")
async def get_open_referrals(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get open referral requests"""
    return db.query(Referral).filter(
        Referral.status == ReferralStatus.OPEN,
        Referral.is_public == True
    ).order_by(Referral.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/company/{company_id}")
async def get_company_referrals(
    company_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get referral requests for a specific company"""
    return db.query(Referral).filter(
        Referral.company_id == company_id,
        Referral.status == ReferralStatus.OPEN,
        Referral.is_public == True
    ).order_by(Referral.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{referral_id}")
async def get_referral(referral_id: int, db: Session = Depends(get_db)):
    """Get referral request details"""
    referral = db.query(Referral).filter(Referral.id == referral_id).first()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    return referral

# TODO: Add POST, PUT endpoints for creating and updating referrals
# These would require authentication




