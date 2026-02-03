"""
Profile API Routes - Education, Experience, Projects, Skills, Portfolio
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models import (
    get_db,
    Education, Experience, Project, 
    Certification, Award, SocialLink, Resume,
    UserSkill, Skill, SkillCategory,
    UserPortfolio, PortfolioTemplate,
    CareerRoadmap, UserRoadmapProgress,
    SavedJob
)

router = APIRouter(prefix="/profile", tags=["Profile"])


# ==================== SCHEMAS ====================
class EducationCreate(BaseModel):
    institution_name: str
    degree_name: str
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool = False
    gpa: Optional[float] = None
    percentage: Optional[float] = None
    description: Optional[str] = None


class EducationResponse(EducationCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExperienceCreate(BaseModel):
    company_name: str
    job_title: str
    location: Optional[str] = None
    location_type: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    skills_used: Optional[List[str]] = None


class ExperienceResponse(ExperienceCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: str
    project_type: Optional[str] = "personal"
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    features: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectResponse(ProjectCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CertificationCreate(BaseModel):
    name: str
    issuing_organization: str
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class AwardCreate(BaseModel):
    title: str
    issuing_organization: Optional[str] = None
    date_received: Optional[datetime] = None
    description: Optional[str] = None
    url: Optional[str] = None


class SocialLinkCreate(BaseModel):
    platform: str
    url: str
    username: Optional[str] = None


class SkillsUpdate(BaseModel):
    skills: List[str]


class PortfolioCreate(BaseModel):
    template_id: int
    subdomain: str
    title: Optional[str] = None
    tagline: Optional[str] = None


class SavedJobCreate(BaseModel):
    job_title: str
    company_name: str
    external_job_url: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


# ==================== EDUCATION ROUTES ====================
@router.get("/education", response_model=List[EducationResponse])
async def get_educations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all education entries for a user"""
    return db.query(Education).filter(
        Education.user_id == user_id
    ).order_by(Education.start_date.desc()).all()


@router.post("/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def create_education(
    user_id: int,
    data: EducationCreate,
    db: Session = Depends(get_db)
):
    """Create a new education entry"""
    education = Education(user_id=user_id, **data.model_dump())
    db.add(education)
    db.commit()
    db.refresh(education)
    return education


@router.put("/education/{education_id}", response_model=EducationResponse)
async def update_education(
    education_id: int,
    data: EducationCreate,
    db: Session = Depends(get_db)
):
    """Update an education entry"""
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    for key, value in data.model_dump().items():
        setattr(education, key, value)
    
    db.commit()
    db.refresh(education)
    return education


@router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: int,
    db: Session = Depends(get_db)
):
    """Delete an education entry"""
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    db.delete(education)
    db.commit()


# ==================== EXPERIENCE ROUTES ====================
@router.get("/experience", response_model=List[ExperienceResponse])
async def get_experiences(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all experience entries for a user"""
    return db.query(Experience).filter(
        Experience.user_id == user_id
    ).order_by(Experience.start_date.desc()).all()


@router.post("/experience", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(
    user_id: int,
    data: ExperienceCreate,
    db: Session = Depends(get_db)
):
    """Create a new experience entry"""
    experience = Experience(user_id=user_id, **data.model_dump())
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return experience


@router.put("/experience/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: int,
    data: ExperienceCreate,
    db: Session = Depends(get_db)
):
    """Update an experience entry"""
    experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    for key, value in data.model_dump().items():
        setattr(experience, key, value)
    
    db.commit()
    db.refresh(experience)
    return experience


@router.delete("/experience/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db)
):
    """Delete an experience entry"""
    experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    db.delete(experience)
    db.commit()


# ==================== PROJECTS ROUTES ====================
@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all projects for a user"""
    return db.query(Project).filter(
        Project.user_id == user_id
    ).order_by(Project.display_order).all()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    user_id: int,
    data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project"""
    project = Project(user_id=user_id, **data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()


# ==================== SKILLS ROUTES ====================
@router.get("/skills/categories")
async def get_skill_categories(db: Session = Depends(get_db)):
    """Get all skill categories with skills"""
    categories = db.query(SkillCategory).order_by(SkillCategory.display_order).all()
    result = []
    for cat in categories:
        skills = db.query(Skill).filter(Skill.category_id == cat.id).all()
        result.append({
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "icon": cat.icon,
            "color": cat.color,
            "skills": [{"id": s.id, "name": s.name, "slug": s.slug} for s in skills]
        })
    return result


@router.get("/skills/user/{user_id}")
async def get_user_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all skills for a user"""
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    result = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            result.append({
                "id": us.id,
                "skill_id": skill.id,
                "name": skill.name,
                "level": us.level.value if us.level else None,
                "is_primary": us.is_primary
            })
        elif us.custom_skill_name:
            result.append({
                "id": us.id,
                "skill_id": None,
                "name": us.custom_skill_name,
                "level": us.level.value if us.level else None,
                "is_primary": us.is_primary
            })
    return result


@router.put("/skills/user/{user_id}")
async def update_user_skills(
    user_id: int,
    data: SkillsUpdate,
    db: Session = Depends(get_db)
):
    """Update user skills (replace all)"""
    # Delete existing skills
    db.query(UserSkill).filter(UserSkill.user_id == user_id).delete()
    
    # Add new skills
    for skill_name in data.skills:
        # Try to find skill in master list
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        
        user_skill = UserSkill(
            user_id=user_id,
            skill_id=skill.id if skill else None,
            custom_skill_name=skill_name if not skill else None
        )
        db.add(user_skill)
    
    db.commit()
    return {"message": "Skills updated successfully", "count": len(data.skills)}


# ==================== CERTIFICATIONS ROUTES ====================
@router.get("/certifications")
async def get_certifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(Certification).filter(Certification.user_id == user_id).all()


@router.post("/certifications", status_code=status.HTTP_201_CREATED)
async def create_certification(user_id: int, data: CertificationCreate, db: Session = Depends(get_db)):
    cert = Certification(user_id=user_id, **data.model_dump())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.delete("/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if cert:
        db.delete(cert)
        db.commit()


# ==================== AWARDS ROUTES ====================
@router.get("/awards")
async def get_awards(user_id: int, db: Session = Depends(get_db)):
    return db.query(Award).filter(Award.user_id == user_id).all()


@router.post("/awards", status_code=status.HTTP_201_CREATED)
async def create_award(user_id: int, data: AwardCreate, db: Session = Depends(get_db)):
    award = Award(user_id=user_id, **data.model_dump())
    db.add(award)
    db.commit()
    db.refresh(award)
    return award


@router.delete("/awards/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_award(award_id: int, db: Session = Depends(get_db)):
    award = db.query(Award).filter(Award.id == award_id).first()
    if award:
        db.delete(award)
        db.commit()


# ==================== SOCIAL LINKS ROUTES ====================
@router.get("/social-links")
async def get_social_links(user_id: int, db: Session = Depends(get_db)):
    return db.query(SocialLink).filter(SocialLink.user_id == user_id).all()


@router.post("/social-links", status_code=status.HTTP_201_CREATED)
async def create_social_link(user_id: int, data: SocialLinkCreate, db: Session = Depends(get_db)):
    link = SocialLink(user_id=user_id, **data.model_dump())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.put("/social-links/bulk")
async def update_social_links_bulk(
    user_id: int,
    links: List[SocialLinkCreate],
    db: Session = Depends(get_db)
):
    """Update all social links for a user"""
    # Delete existing
    db.query(SocialLink).filter(SocialLink.user_id == user_id).delete()
    
    # Add new
    for link_data in links:
        link = SocialLink(user_id=user_id, **link_data.model_dump())
        db.add(link)
    
    db.commit()
    return {"message": "Social links updated", "count": len(links)}


# ==================== PORTFOLIO ROUTES ====================
@router.get("/portfolio/templates")
async def get_portfolio_templates(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all available portfolio templates"""
    query = db.query(PortfolioTemplate).filter(PortfolioTemplate.is_active == True)
    
    if category:
        query = query.filter(PortfolioTemplate.category == category)
    
    return query.order_by(PortfolioTemplate.display_order).all()


@router.get("/portfolio/user/{user_id}")
async def get_user_portfolio(user_id: int, db: Session = Depends(get_db)):
    """Get user's portfolio"""
    return db.query(UserPortfolio).filter(UserPortfolio.user_id == user_id).first()


@router.post("/portfolio", status_code=status.HTTP_201_CREATED)
async def create_portfolio(user_id: int, data: PortfolioCreate, db: Session = Depends(get_db)):
    """Create or update user's portfolio"""
    # Check if subdomain is taken
    existing = db.query(UserPortfolio).filter(
        UserPortfolio.subdomain == data.subdomain,
        UserPortfolio.user_id != user_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Subdomain already taken")
    
    # Check if user already has a portfolio
    portfolio = db.query(UserPortfolio).filter(UserPortfolio.user_id == user_id).first()
    
    if portfolio:
        for key, value in data.model_dump().items():
            setattr(portfolio, key, value)
    else:
        portfolio = UserPortfolio(user_id=user_id, **data.model_dump())
        db.add(portfolio)
    
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.put("/portfolio/{portfolio_id}/publish")
async def publish_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Publish a portfolio"""
    portfolio = db.query(UserPortfolio).filter(UserPortfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio.is_published = True
    portfolio.published_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Portfolio published", "url": f"https://careerlaunch.io/{portfolio.subdomain}"}


# ==================== ROADMAPS ROUTES ====================
@router.get("/roadmaps")
async def get_roadmaps(
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all career roadmaps"""
    query = db.query(CareerRoadmap).filter(CareerRoadmap.is_active == True)
    
    if role:
        query = query.filter(CareerRoadmap.role.ilike(f"%{role}%"))
    
    return query.order_by(CareerRoadmap.display_order).all()


@router.get("/roadmaps/{roadmap_id}")
async def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """Get a specific roadmap"""
    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap


@router.get("/roadmaps/user/{user_id}/progress")
async def get_user_roadmap_progress(user_id: int, db: Session = Depends(get_db)):
    """Get user's progress on all roadmaps"""
    return db.query(UserRoadmapProgress).filter(UserRoadmapProgress.user_id == user_id).all()


@router.post("/roadmaps/{roadmap_id}/enroll")
async def enroll_in_roadmap(roadmap_id: int, user_id: int, db: Session = Depends(get_db)):
    """Enroll user in a roadmap"""
    # Check if already enrolled
    existing = db.query(UserRoadmapProgress).filter(
        UserRoadmapProgress.user_id == user_id,
        UserRoadmapProgress.roadmap_id == roadmap_id
    ).first()
    
    if existing:
        return existing
    
    progress = UserRoadmapProgress(
        user_id=user_id,
        roadmap_id=roadmap_id,
        status="in_progress"
    )
    db.add(progress)
    
    # Update roadmap enrollment count
    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.id == roadmap_id).first()
    if roadmap:
        roadmap.enrolled_count = (roadmap.enrolled_count or 0) + 1
    
    db.commit()
    db.refresh(progress)
    return progress


# ==================== SAVED JOBS ROUTES ====================
@router.get("/saved-jobs")
async def get_saved_jobs(user_id: int, db: Session = Depends(get_db)):
    """Get user's saved jobs"""
    return db.query(SavedJob).filter(SavedJob.user_id == user_id).order_by(SavedJob.created_at.desc()).all()


@router.post("/saved-jobs", status_code=status.HTTP_201_CREATED)
async def save_job(user_id: int, data: SavedJobCreate, db: Session = Depends(get_db)):
    """Save a job"""
    saved = SavedJob(user_id=user_id, **data.model_dump())
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


@router.delete("/saved-jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_job(job_id: int, db: Session = Depends(get_db)):
    """Remove a saved job"""
    job = db.query(SavedJob).filter(SavedJob.id == job_id).first()
    if job:
        db.delete(job)
        db.commit()
