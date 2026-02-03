"""
Content API Routes - AI Tools, Git Repos, YouTube Channels, Courses, etc.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from pydantic import BaseModel

from app.models import (
    get_db,
    AITool, AIToolCategory, PricingModel,
    GitRepository,
    YouTubeChannel,
    OnlineCourse,
    TechNewsletter,
    TechPodcast,
    TechBook,
    PublicInterviewExperience
)

router = APIRouter(prefix="/content", tags=["Content"])


# ==================== SCHEMAS ====================
class AIToolResponse(BaseModel):
    id: int
    name: str
    slug: str
    tagline: Optional[str]
    description: Optional[str]
    category: str
    tags: Optional[List[str]]
    website_url: Optional[str]
    logo_url: Optional[str]
    pricing_model: str
    starting_price: Optional[str]
    features: Optional[List[str]]
    is_featured: bool
    views: int
    
    class Config:
        from_attributes = True


class GitRepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str]
    owner_name: Optional[str]
    html_url: str
    homepage: Optional[str]
    stars: int
    language: Optional[str]
    topics: Optional[List[str]]
    category: Optional[str]
    skill_level: Optional[str]
    is_featured: bool
    
    class Config:
        from_attributes = True


# ==================== AI TOOLS ====================
@router.get("/ai-tools")
async def get_ai_tools(
    category: Optional[str] = None,
    pricing: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get AI tools with filtering and pagination"""
    query = db.query(AITool).filter(AITool.is_active == True)
    
    # Filters
    if category:
        try:
            cat_enum = AIToolCategory[category.upper()]
            query = query.filter(AITool.category == cat_enum)
        except KeyError:
            pass
    
    if pricing:
        try:
            pricing_enum = PricingModel[pricing.upper()]
            query = query.filter(AITool.pricing_model == pricing_enum)
        except KeyError:
            pass
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                AITool.name.ilike(search_filter),
                AITool.description.ilike(search_filter),
                AITool.tagline.ilike(search_filter)
            )
        )
    
    if featured_only:
        query = query.filter(AITool.is_featured == True)
    
    # Count total
    total = query.count()
    
    # Pagination
    offset = (page - 1) * limit
    tools = query.order_by(AITool.is_featured.desc(), AITool.views.desc()).offset(offset).limit(limit).all()
    
    return {
        "items": tools,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/ai-tools/categories")
async def get_ai_tool_categories(db: Session = Depends(get_db)):
    """Get all AI tool categories with counts"""
    categories = []
    for cat in AIToolCategory:
        count = db.query(AITool).filter(
            AITool.category == cat,
            AITool.is_active == True
        ).count()
        if count > 0:
            categories.append({
                "name": cat.name,
                "value": cat.value,
                "count": count
            })
    return categories


@router.get("/ai-tools/featured")
async def get_featured_ai_tools(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured AI tools"""
    return db.query(AITool).filter(
        AITool.is_featured == True,
        AITool.is_active == True
    ).limit(limit).all()


@router.get("/ai-tools/{slug}")
async def get_ai_tool(slug: str, db: Session = Depends(get_db)):
    """Get a specific AI tool by slug"""
    tool = db.query(AITool).filter(
        AITool.slug == slug,
        AITool.is_active == True
    ).first()
    
    if not tool:
        raise HTTPException(status_code=404, detail="AI Tool not found")
    
    # Increment views
    tool.views = (tool.views or 0) + 1
    db.commit()
    
    return tool


# ==================== GIT REPOSITORIES ====================
@router.get("/git-repos")
async def get_git_repos(
    category: Optional[str] = None,
    language: Optional[str] = None,
    skill_level: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get Git repositories with filtering"""
    query = db.query(GitRepository).filter(GitRepository.is_active == True)
    
    if category:
        query = query.filter(GitRepository.category == category)
    
    if language:
        query = query.filter(GitRepository.language.ilike(f"%{language}%"))
    
    if skill_level:
        query = query.filter(GitRepository.skill_level == skill_level)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                GitRepository.name.ilike(search_filter),
                GitRepository.description.ilike(search_filter),
                GitRepository.full_name.ilike(search_filter)
            )
        )
    
    if featured_only:
        query = query.filter(GitRepository.is_featured == True)
    
    total = query.count()
    offset = (page - 1) * limit
    repos = query.order_by(GitRepository.stars.desc()).offset(offset).limit(limit).all()
    
    return {
        "items": repos,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/git-repos/categories")
async def get_git_repo_categories(db: Session = Depends(get_db)):
    """Get repository categories"""
    result = db.query(
        GitRepository.category,
        func.count(GitRepository.id).label('count')
    ).filter(
        GitRepository.is_active == True,
        GitRepository.category.isnot(None)
    ).group_by(GitRepository.category).all()
    
    return [{"name": r[0], "count": r[1]} for r in result]


@router.get("/git-repos/languages")
async def get_git_repo_languages(db: Session = Depends(get_db)):
    """Get repository languages"""
    result = db.query(
        GitRepository.language,
        func.count(GitRepository.id).label('count')
    ).filter(
        GitRepository.is_active == True,
        GitRepository.language.isnot(None)
    ).group_by(GitRepository.language).order_by(func.count(GitRepository.id).desc()).limit(20).all()
    
    return [{"name": r[0], "count": r[1]} for r in result]


@router.get("/git-repos/featured")
async def get_featured_git_repos(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured repositories"""
    return db.query(GitRepository).filter(
        GitRepository.is_featured == True,
        GitRepository.is_active == True
    ).order_by(GitRepository.stars.desc()).limit(limit).all()


@router.get("/git-repos/{full_name:path}")
async def get_git_repo(full_name: str, db: Session = Depends(get_db)):
    """Get a specific repository"""
    repo = db.query(GitRepository).filter(
        GitRepository.full_name == full_name,
        GitRepository.is_active == True
    ).first()
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    repo.views = (repo.views or 0) + 1
    db.commit()
    
    return repo


# ==================== YOUTUBE CHANNELS ====================
@router.get("/youtube-channels")
async def get_youtube_channels(
    category: Optional[str] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get YouTube channels"""
    query = db.query(YouTubeChannel).filter(YouTubeChannel.is_active == True)
    
    if category:
        query = query.filter(YouTubeChannel.category == category)
    
    return query.order_by(YouTubeChannel.subscriber_count.desc()).all()


@router.get("/youtube-channels/featured")
async def get_featured_youtube_channels(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured YouTube channels"""
    return db.query(YouTubeChannel).filter(
        YouTubeChannel.is_featured == True,
        YouTubeChannel.is_active == True
    ).limit(limit).all()


# ==================== COURSES ====================
@router.get("/courses")
async def get_courses(
    category: Optional[str] = None,
    provider: Optional[str] = None,
    free_only: bool = False,
    skill_level: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get online courses"""
    query = db.query(OnlineCourse).filter(OnlineCourse.is_active == True)
    
    if category:
        query = query.filter(OnlineCourse.category == category)
    
    if provider:
        query = query.filter(OnlineCourse.provider_name.ilike(f"%{provider}%"))
    
    if free_only:
        query = query.filter(OnlineCourse.is_free == True)
    
    if skill_level:
        query = query.filter(OnlineCourse.skill_level == skill_level)
    
    if search:
        query = query.filter(OnlineCourse.title.ilike(f"%{search}%"))
    
    total = query.count()
    offset = (page - 1) * limit
    courses = query.order_by(OnlineCourse.rating.desc()).offset(offset).limit(limit).all()
    
    return {"items": courses, "total": total, "page": page}


# ==================== NEWSLETTERS ====================
@router.get("/newsletters")
async def get_newsletters(
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get tech newsletters"""
    query = db.query(TechNewsletter).filter(TechNewsletter.is_active == True)
    return query.order_by(TechNewsletter.is_featured.desc()).all()


# ==================== PODCASTS ====================
@router.get("/podcasts")
async def get_podcasts(
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get tech podcasts"""
    query = db.query(TechPodcast).filter(TechPodcast.is_active == True)
    return query.order_by(TechPodcast.rating.desc()).all()


# ==================== BOOKS ====================
@router.get("/books")
async def get_books(
    category: Optional[str] = None,
    skill_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get tech books"""
    query = db.query(TechBook).filter(TechBook.is_active == True)
    
    if category:
        query = query.filter(TechBook.category == category)
    
    if skill_level:
        query = query.filter(TechBook.skill_level == skill_level)
    
    return query.order_by(TechBook.rating.desc()).all()


# ==================== INTERVIEW EXPERIENCES ====================
@router.get("/interview-experiences")
async def get_interview_experiences(
    company: Optional[str] = None,
    role: Optional[str] = None,
    result: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get public interview experiences"""
    query = db.query(PublicInterviewExperience).filter(
        PublicInterviewExperience.is_approved == True
    )
    
    if company:
        query = query.filter(PublicInterviewExperience.company_name.ilike(f"%{company}%"))
    
    if role:
        query = query.filter(PublicInterviewExperience.role.ilike(f"%{role}%"))
    
    if result:
        query = query.filter(PublicInterviewExperience.result == result)
    
    total = query.count()
    offset = (page - 1) * limit
    experiences = query.order_by(PublicInterviewExperience.created_at.desc()).offset(offset).limit(limit).all()
    
    return {"items": experiences, "total": total, "page": page}


@router.get("/interview-experiences/company/{company_name}")
async def get_company_interviews(
    company_name: str,
    db: Session = Depends(get_db)
):
    """Get all interview experiences for a company"""
    return db.query(PublicInterviewExperience).filter(
        PublicInterviewExperience.company_name.ilike(f"%{company_name}%"),
        PublicInterviewExperience.is_approved == True
    ).order_by(PublicInterviewExperience.created_at.desc()).all()


# ==================== SEARCH ALL ====================
@router.get("/search")
async def search_all_content(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search across all content types"""
    search_filter = f"%{q}%"
    
    results = {
        "ai_tools": db.query(AITool).filter(
            AITool.is_active == True,
            or_(AITool.name.ilike(search_filter), AITool.description.ilike(search_filter))
        ).limit(limit).all(),
        
        "git_repos": db.query(GitRepository).filter(
            GitRepository.is_active == True,
            or_(GitRepository.name.ilike(search_filter), GitRepository.description.ilike(search_filter))
        ).limit(limit).all(),
        
        "courses": db.query(OnlineCourse).filter(
            OnlineCourse.is_active == True,
            OnlineCourse.title.ilike(search_filter)
        ).limit(limit).all()
    }
    
    return results
