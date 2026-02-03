"""
Review Models - User reviews for companies
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Review(Base):
    """Company Reviews Table"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Company & User
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Employment Details
    job_title = Column(String(200))
    department = Column(String(100))
    employment_status = Column(String(50))  # "current", "former"
    employment_type = Column(String(50))  # "full_time", "intern", "contract"
    years_at_company = Column(Integer)
    location = Column(String(100))
    
    # Ratings (1-5 scale)
    overall_rating = Column(Float, nullable=False)
    work_life_balance = Column(Float)
    salary_benefits = Column(Float)
    job_security = Column(Float)
    career_growth = Column(Float)
    management = Column(Float)
    culture = Column(Float)
    
    # Review Content
    title = Column(String(200))
    pros = Column(Text)
    cons = Column(Text)
    advice_to_management = Column(Text)
    
    # Salary Info (anonymous)
    salary_disclosed = Column(Boolean, default=False)
    salary_range = Column(String(100))  # "15-20 LPA"
    
    # Interview Experience (optional link)
    includes_interview = Column(Boolean, default=False)
    
    # Recommendations
    recommend_to_friend = Column(Boolean)
    ceo_approval = Column(Boolean)
    business_outlook = Column(String(50))  # "positive", "neutral", "negative"
    
    # Verification & Moderation
    is_verified = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=True)
    
    # Engagement
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="reviews")
    user = relationship("User", back_populates="reviews")




