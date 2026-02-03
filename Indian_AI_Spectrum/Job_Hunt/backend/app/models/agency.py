"""
Agency Models - Recruitment agencies for abroad/remote jobs
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Agency(Base):
    """Recruitment Agencies Table"""
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True)
    logo_url = Column(String(500))
    website = Column(String(500))
    description = Column(Text)
    
    # Classification
    agency_type = Column(String(50))  # "abroad_placement", "remote_jobs", "general", "specialized"
    specializations = Column(JSON)  # ["IT", "Healthcare", "Engineering"]
    
    # Location
    headquarters_city = Column(String(100))
    headquarters_country = Column(String(100))
    office_locations = Column(JSON)  # List of cities
    
    # Service Details
    countries_served = Column(JSON)  # ["Germany", "Canada", "Australia"]
    industries_served = Column(JSON)
    experience_levels = Column(JSON)  # ["fresher", "experienced"]
    
    # For Abroad Jobs
    visa_assistance = Column(Boolean, default=False)
    relocation_support = Column(Boolean, default=False)
    
    # Fees
    fee_structure = Column(Text)
    is_free_for_candidates = Column(Boolean, default=True)
    
    # Contact
    contact_email = Column(String(200))
    contact_phone = Column(String(50))
    linkedin_url = Column(String(500))
    
    # Ratings & Reviews
    rating = Column(Float)
    reviews_count = Column(Integer, default=0)
    success_stories_count = Column(Integer, default=0)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    is_government_registered = Column(Boolean, default=False)
    registration_number = Column(String(100))
    
    # Warnings
    has_complaints = Column(Boolean, default=False)
    complaint_details = Column(Text)
    
    # Metadata
    is_recommended = Column(Boolean, default=False)
    last_verified = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())




