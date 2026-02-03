"""
Resources API Routes - Courses, tutorials, roadmaps
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.resource import Resource, Roadmap, ResourceType, ResourcePricing

router = APIRouter()

@router.get("/")
async def get_resources(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    resource_type: Optional[str] = None,
    pricing: Optional[str] = None,
    category: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    is_free: Optional[bool] = None,
    search: Optional[str] = None
):
    """Get list of learning resources"""
    query = db.query(Resource)
    
    if resource_type:
        query = query.filter(Resource.resource_type == resource_type)
    if pricing:
        query = query.filter(Resource.pricing == pricing)
    if category:
        query = query.filter(Resource.category == category)
    if difficulty_level:
        query = query.filter(Resource.difficulty_level == difficulty_level)
    if is_free:
        query = query.filter(Resource.pricing == ResourcePricing.FREE)
    if search:
        query = query.filter(Resource.title.ilike(f"%{search}%"))
    
    total = query.count()
    resources = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "resources": resources
    }

@router.get("/types")
async def get_resource_types():
    """Get all resource types"""
    return {
        "types": [t.value for t in ResourceType],
        "pricing_options": [p.value for p in ResourcePricing]
    }

@router.get("/free")
async def get_free_resources(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get free learning resources"""
    query = db.query(Resource).filter(Resource.pricing == ResourcePricing.FREE)
    if category:
        query = query.filter(Resource.category == category)
    return query.offset(skip).limit(limit).all()

@router.get("/youtube")
async def get_youtube_resources(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    is_indian_creator: bool = False,
    skip: int = 0,
    limit: int = 50
):
    """Get YouTube channels and playlists"""
    query = db.query(Resource).filter(
        Resource.resource_type.in_([
            ResourceType.YOUTUBE_CHANNEL,
            ResourceType.YOUTUBE_PLAYLIST,
            ResourceType.YOUTUBE_VIDEO
        ])
    )
    if category:
        query = query.filter(Resource.category == category)
    if is_indian_creator:
        query = query.filter(Resource.is_indian_creator == True)
    return query.offset(skip).limit(limit).all()

@router.get("/roadmaps")
async def get_roadmaps(
    db: Session = Depends(get_db),
    role: Optional[str] = None,
    experience_level: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    """Get career roadmaps"""
    query = db.query(Roadmap)
    if role:
        query = query.filter(Roadmap.role.ilike(f"%{role}%"))
    if experience_level:
        query = query.filter(Roadmap.experience_level == experience_level)
    return query.offset(skip).limit(limit).all()

@router.get("/roadmaps/{roadmap_id}")
async def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """Get roadmap with all steps"""
    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    roadmap.views_count += 1
    db.commit()
    
    return roadmap

@router.get("/by-role/{role}")
async def get_resources_by_role(
    role: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get resources relevant to a specific role"""
    return db.query(Resource).filter(
        Resource.relevant_roles.contains([role])
    ).offset(skip).limit(limit).all()

@router.get("/{resource_id}")
async def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get resource by ID"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource




