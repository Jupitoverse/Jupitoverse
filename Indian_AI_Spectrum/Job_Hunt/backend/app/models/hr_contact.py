"""
HR Contact Models - Premium feature for Pro users
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum
from .database import Base


class HRContactVisibility(enum.Enum):
    ALL = "all"  # Visible to all authenticated users
    PREMIUM = "premium"  # Visible to Premium and Pro users
    PRO = "pro"  # Visible only to Pro users
    HIDDEN = "hidden"  # Hidden from all users (admin only)


class HRContact(Base):
    """HR Contact Directory - Premium Feature"""
    __tablename__ = "hr_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Contact Info
    name = Column(String(200), nullable=False, index=True)
    email = Column(String(200), nullable=False, index=True)
    title = Column(String(300))
    company_name = Column(String(300), index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    
    # Additional Info
    linkedin_url = Column(String(500))
    phone = Column(String(50))
    location = Column(String(200))
    
    # Classification
    seniority_level = Column(String(50))  # "Director", "VP", "Head", "Manager"
    department = Column(String(100))  # "HR", "Talent Acquisition", "People"
    
    # Visibility Control (Admin Feature)
    visibility = Column(Enum(HRContactVisibility), default=HRContactVisibility.PRO)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    source = Column(String(100))  # "pdf_import", "excel_import", "manual"
    imported_at = Column(DateTime, server_default=func.now())
    last_verified = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


