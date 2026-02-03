"""
Company Models - Comprehensive company data storage
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, JSON, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class CompanyType(enum.Enum):
    PRODUCT = "product"
    SERVICE = "service"
    STARTUP = "startup"
    CONSULTING = "consulting"
    HYBRID = "hybrid"
    GOVERNMENT = "government"
    NGO = "ngo"

class CompanyCategory(enum.Enum):
    FAANG = "faang"
    MAANG = "maang"
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    MNC = "mnc"
    INDIAN_UNICORN = "indian_unicorn"
    STARTUP = "startup"
    PSU = "psu"

# Many-to-many relationship tables
company_tech_stack = Table(
    'company_tech_stack',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('technology_id', Integer, ForeignKey('technologies.id'))
)

company_locations = Table(
    'company_locations',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)

class Company(Base):
    """Main Company Table with comprehensive metadata"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True)
    logo_url = Column(String(500))
    website = Column(String(500))
    description = Column(Text)
    tagline = Column(String(500))
    
    # Company Classification
    company_type = Column(Enum(CompanyType), default=CompanyType.PRODUCT)
    category = Column(Enum(CompanyCategory))
    industry = Column(String(100))
    sub_industry = Column(String(100))
    
    # Size & Revenue
    employee_count = Column(Integer)
    employee_count_range = Column(String(50))  # e.g., "1000-5000"
    revenue_range = Column(String(100))
    founded_year = Column(Integer)
    
    # Location
    headquarters_city = Column(String(100))
    headquarters_country = Column(String(100))
    has_indian_office = Column(Boolean, default=False)
    indian_cities = Column(JSON)  # List of cities
    
    # Remote Work
    is_remote_friendly = Column(Boolean, default=False)
    remote_policy = Column(String(50))  # "full", "hybrid", "no"
    hires_from_india = Column(Boolean, default=False)
    
    # Interview & Culture
    interview_difficulty = Column(Float)  # 1-5 scale
    interview_experience = Column(Float)  # 1-5 scale
    interview_process = Column(JSON)  # List of rounds
    work_life_balance = Column(Float)  # 1-5 scale
    culture_rating = Column(Float)  # 1-5 scale
    
    # Salary Info
    avg_salary_india = Column(JSON)  # {"entry": 800000, "mid": 2000000, "senior": 5000000}
    salary_currency = Column(String(10), default="INR")
    
    # Social Links
    linkedin_url = Column(String(500))
    glassdoor_url = Column(String(500))
    ambitionbox_url = Column(String(500))
    github_url = Column(String(500))
    careers_page = Column(String(500))
    
    # Metadata
    is_verified = Column(Boolean, default=False)
    is_actively_hiring = Column(Boolean, default=True)
    last_scraped = Column(DateTime)
    data_source = Column(JSON)  # ["linkedin", "glassdoor", "manual"]
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    technologies = relationship("Technology", secondary=company_tech_stack, back_populates="companies")
    locations = relationship("Location", secondary=company_locations, back_populates="companies")
    jobs = relationship("Job", back_populates="company")
    reviews = relationship("Review", back_populates="company")
    referrals = relationship("Referral", back_populates="company")
    interview_experiences = relationship("InterviewExperience", back_populates="company")

class Technology(Base):
    """Technology/Skills Table"""
    __tablename__ = "technologies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    category = Column(String(50))  # "language", "framework", "database", "cloud"
    icon_url = Column(String(500))
    
    companies = relationship("Company", secondary=company_tech_stack, back_populates="technologies")

class Location(Base):
    """Location Table"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    state = Column(String(100))
    country = Column(String(100), index=True)
    country_code = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    
    companies = relationship("Company", secondary=company_locations, back_populates="locations")

class InterviewExperience(Base):
    """Interview Experiences Table"""
    __tablename__ = "interview_experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    role = Column(String(200))
    experience_level = Column(String(50))  # "fresher", "2-5 years", "5-10 years", "10+ years"
    interview_date = Column(DateTime)
    
    # Process Details
    total_rounds = Column(Integer)
    round_details = Column(JSON)  # [{"type": "coding", "duration": 60, "description": "..."}]
    questions = Column(JSON)  # List of questions asked
    
    # Outcome
    got_offer = Column(Boolean)
    difficulty_rating = Column(Integer)  # 1-5
    experience_rating = Column(Integer)  # 1-5
    
    # Content
    description = Column(Text)
    tips = Column(Text)
    
    # Metadata
    is_verified = Column(Boolean, default=False)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    company = relationship("Company", back_populates="interview_experiences")




