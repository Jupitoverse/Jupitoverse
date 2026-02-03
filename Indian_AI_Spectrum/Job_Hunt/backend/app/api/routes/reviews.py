"""
Reviews API Routes - Company reviews
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models.database import get_db
from app.models.review import Review

router = APIRouter()

@router.get("/")
async def get_reviews(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    company_id: Optional[int] = None,
    min_rating: Optional[float] = None,
    employment_status: Optional[str] = None
):
    """Get list of company reviews"""
    query = db.query(Review).filter(Review.is_approved == True)
    
    if company_id:
        query = query.filter(Review.company_id == company_id)
    if min_rating:
        query = query.filter(Review.overall_rating >= min_rating)
    if employment_status:
        query = query.filter(Review.employment_status == employment_status)
    
    total = query.count()
    reviews = query.order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "reviews": reviews}

@router.get("/company/{company_id}")
async def get_company_reviews(
    company_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get reviews for a specific company"""
    reviews = db.query(Review).filter(
        Review.company_id == company_id,
        Review.is_approved == True
    ).order_by(Review.helpful_count.desc()).offset(skip).limit(limit).all()
    
    # Calculate averages
    all_reviews = db.query(Review).filter(
        Review.company_id == company_id,
        Review.is_approved == True
    ).all()
    
    if all_reviews:
        avg_rating = sum(r.overall_rating for r in all_reviews) / len(all_reviews)
        avg_wlb = sum(r.work_life_balance or 0 for r in all_reviews if r.work_life_balance) / len([r for r in all_reviews if r.work_life_balance]) if any(r.work_life_balance for r in all_reviews) else None
    else:
        avg_rating = None
        avg_wlb = None
    
    return {
        "total": len(all_reviews),
        "average_rating": avg_rating,
        "average_work_life_balance": avg_wlb,
        "reviews": reviews
    }

@router.get("/top-rated")
async def get_top_rated_companies(
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get companies with highest ratings"""
    from sqlalchemy import func
    from app.models.company import Company
    
    return db.query(
        Company.id,
        Company.name,
        func.avg(Review.overall_rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).join(Review).filter(
        Review.is_approved == True
    ).group_by(Company.id).order_by(
        func.avg(Review.overall_rating).desc()
    ).limit(limit).all()

@router.get("/{review_id}")
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get review by ID"""
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.is_approved == True
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/{review_id}/helpful")
async def mark_review_helpful(review_id: int, db: Session = Depends(get_db)):
    """Mark review as helpful"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.helpful_count += 1
    db.commit()
    return {"message": "Marked as helpful", "helpful_count": review.helpful_count}




