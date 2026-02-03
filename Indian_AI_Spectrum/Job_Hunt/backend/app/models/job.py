"""
Job Models - Job postings and applications
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class JobType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevel(enum.Enum):
    FRESHER = "fresher"
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"
    EXECUTIVE = "executive"

class WorkMode(enum.Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"

class Job(Base):
    """Job Posting Table"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(300), nullable=False, index=True)
    slug = Column(String(300), index=True)
    description = Column(Text)
    requirements = Column(Text)
    responsibilities = Column(Text)
    
    # Company
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String(255))  # Denormalized for quick access
    
    # Job Details
    job_type = Column(Enum(JobType), default=JobType.FULL_TIME)
    experience_level = Column(Enum(ExperienceLevel))
    experience_min = Column(Integer)
    experience_max = Column(Integer)
    
    # Location
    location_city = Column(String(100))
    location_country = Column(String(100))
    work_mode = Column(Enum(WorkMode), default=WorkMode.ONSITE)
    
    # Skills & Tech
    skills_required = Column(JSON)  # ["Python", "AWS", "Django"]
    skills_preferred = Column(JSON)
    education_required = Column(String(200))
    
    # Salary
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default="INR")
    salary_period = Column(String(20), default="yearly")  # "yearly", "monthly", "hourly"
    is_salary_disclosed = Column(Boolean, default=True)
    
    # Application
    application_url = Column(String(500))
    application_email = Column(String(200))
    application_deadline = Column(DateTime)
    
    # Source
    source = Column(String(100))  # "linkedin", "naukri", "direct", "referral"
    source_url = Column(String(500))
    source_job_id = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)
    
    # For Abroad Jobs
    is_abroad = Column(Boolean, default=False)
    visa_sponsorship = Column(Boolean, default=False)
    relocation_assistance = Column(Boolean, default=False)
    
    # Timestamps
    posted_at = Column(DateTime)
    scraped_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(Base):
    """Job Applications Table"""
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Application Status
    status = Column(String(50), default="applied")  # applied, screening, interview, offer, rejected
    applied_at = Column(DateTime, server_default=func.now())
    
    # Cover Letter & Resume
    cover_letter = Column(Text)
    resume_url = Column(String(500))
    
    # Notes
    notes = Column(Text)
    
    job = relationship("Job", back_populates="applications")




