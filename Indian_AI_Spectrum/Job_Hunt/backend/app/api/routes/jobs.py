"""
Jobs API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.job import Job, JobType, ExperienceLevel, WorkMode

router = APIRouter()

@router.get("/")
async def get_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    work_mode: Optional[str] = None,
    location_city: Optional[str] = None,
    location_country: Optional[str] = None,
    is_abroad: Optional[bool] = None,
    visa_sponsorship: Optional[bool] = None,
    is_active: bool = True,
    search: Optional[str] = None
):
    """Get list of jobs with filters"""
    query = db.query(Job).filter(Job.is_active == is_active)
    
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if experience_level:
        query = query.filter(Job.experience_level == experience_level)
    if work_mode:
        query = query.filter(Job.work_mode == work_mode)
    if location_city:
        query = query.filter(Job.location_city.ilike(f"%{location_city}%"))
    if location_country:
        query = query.filter(Job.location_country == location_country)
    if is_abroad is not None:
        query = query.filter(Job.is_abroad == is_abroad)
    if visa_sponsorship is not None:
        query = query.filter(Job.visa_sponsorship == visa_sponsorship)
    if search:
        query = query.filter(
            (Job.title.ilike(f"%{search}%")) | 
            (Job.company_name.ilike(f"%{search}%"))
        )
    
    total = query.count()
    jobs = query.order_by(Job.posted_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "jobs": jobs
    }

@router.get("/remote")
async def get_remote_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get remote jobs"""
    return db.query(Job).filter(
        Job.work_mode == WorkMode.REMOTE,
        Job.is_active == True
    ).offset(skip).limit(limit).all()

@router.get("/abroad")
async def get_abroad_jobs(
    db: Session = Depends(get_db),
    country: Optional[str] = None,
    visa_sponsorship: bool = True,
    skip: int = 0,
    limit: int = 50
):
    """Get abroad jobs with visa sponsorship"""
    query = db.query(Job).filter(
        Job.is_abroad == True,
        Job.is_active == True
    )
    if country:
        query = query.filter(Job.location_country == country)
    if visa_sponsorship:
        query = query.filter(Job.visa_sponsorship == True)
    return query.offset(skip).limit(limit).all()

@router.get("/fresher")
async def get_fresher_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get jobs for freshers"""
    return db.query(Job).filter(
        Job.experience_level == ExperienceLevel.FRESHER,
        Job.is_active == True
    ).offset(skip).limit(limit).all()

@router.get("/by-skill")
async def get_jobs_by_skill(
    skill: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get jobs by required skill"""
    return db.query(Job).filter(
        Job.skills_required.contains([skill]),
        Job.is_active == True
    ).offset(skip).limit(limit).all()

@router.get("/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job by ID"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Increment view count
    job.views_count += 1
    db.commit()
    
    return job




