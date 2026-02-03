"""
Resource Models - Learning resources, roadmaps, courses
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class ResourceType(enum.Enum):
    COURSE = "course"
    YOUTUBE_CHANNEL = "youtube_channel"
    YOUTUBE_PLAYLIST = "youtube_playlist"
    YOUTUBE_VIDEO = "youtube_video"
    BOOK = "book"
    ARTICLE = "article"
    DOCUMENTATION = "documentation"
    GITHUB_REPO = "github_repo"
    WEBSITE = "website"
    PODCAST = "podcast"
    COMMUNITY = "community"

class ResourcePricing(enum.Enum):
    FREE = "free"
    FREEMIUM = "freemium"
    PAID = "paid"
    SUBSCRIPTION = "subscription"

class Resource(Base):
    """Learning Resources Table"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    
    # Classification
    resource_type = Column(Enum(ResourceType))
    pricing = Column(Enum(ResourcePricing), default=ResourcePricing.FREE)
    price_inr = Column(Integer)  # Price in INR if paid
    price_usd = Column(Float)
    
    # Content Details
    author = Column(String(200))
    platform = Column(String(100))  # "Udemy", "Coursera", "YouTube", etc.
    language = Column(String(50), default="English")
    duration_hours = Column(Float)
    
    # Categorization
    category = Column(String(100))  # "Programming", "AI/ML", "DevOps"
    subcategory = Column(String(100))
    skills_covered = Column(JSON)  # ["Python", "TensorFlow", "Deep Learning"]
    difficulty_level = Column(String(50))  # "beginner", "intermediate", "advanced"
    
    # For Job Roles
    relevant_roles = Column(JSON)  # ["Data Scientist", "ML Engineer"]
    
    # Ratings
    rating = Column(Float)
    reviews_count = Column(Integer)
    students_count = Column(Integer)
    
    # Indian Specific
    is_indian_creator = Column(Boolean, default=False)
    is_india_focused = Column(Boolean, default=False)
    
    # Metadata
    is_verified = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)
    last_updated = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class Roadmap(Base):
    """Career Roadmaps Table"""
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    description = Column(Text)
    thumbnail_url = Column(String(500))
    
    # Classification
    role = Column(String(100), index=True)  # "Software Engineer", "Data Scientist"
    experience_level = Column(String(50))  # "fresher", "experienced", "career_switch"
    
    # Content
    overview = Column(Text)
    estimated_duration_months = Column(Integer)
    
    # Metadata
    author_id = Column(Integer, ForeignKey("users.id"))
    is_official = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    steps = relationship("RoadmapStep", back_populates="roadmap", order_by="RoadmapStep.order")

class RoadmapStep(Base):
    """Roadmap Steps/Phases"""
    __tablename__ = "roadmap_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"))
    
    # Step Info
    order = Column(Integer)
    title = Column(String(200))
    description = Column(Text)
    duration_weeks = Column(Integer)
    
    # Content
    skills_to_learn = Column(JSON)  # ["Python basics", "OOP", "Data structures"]
    projects = Column(JSON)  # List of project ideas
    resources = Column(JSON)  # List of resource IDs or URLs
    
    # Milestones
    milestones = Column(JSON)  # ["Complete 50 LeetCode problems", "Build a portfolio project"]
    
    roadmap = relationship("Roadmap", back_populates="steps")




