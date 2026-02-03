"""
Referral Models - Internal referral system
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class ReferralStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REFERRED = "referred"
    CLOSED = "closed"
    EXPIRED = "expired"

class Referral(Base):
    """Referral Requests Table"""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Requester
    requester_id = Column(Integer, ForeignKey("users.id"))
    
    # Target Company
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String(255), nullable=False)  # Denormalized
    
    # Job Details
    job_title = Column(String(300))
    job_url = Column(String(500))
    job_id = Column(String(100))  # External job ID if any
    
    # Requester Profile Summary
    requester_experience_years = Column(Integer)
    requester_skills = Column(Text)
    requester_current_company = Column(String(200))
    requester_linkedin = Column(String(500))
    resume_url = Column(String(500))
    
    # Message
    message = Column(Text)
    
    # Status
    status = Column(Enum(ReferralStatus), default=ReferralStatus.OPEN)
    
    # Referrer (company employee who refers)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_at = Column(DateTime)
    referrer_notes = Column(Text)
    
    # Visibility
    is_public = Column(Boolean, default=True)  # Visible to all company employees
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)  # Auto-expire after 30 days
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="referrals_received")
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_given")
    company = relationship("Company", back_populates="referrals")




