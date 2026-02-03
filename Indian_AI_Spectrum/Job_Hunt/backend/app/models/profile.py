"""
Profile Models - Education, Experience, Projects, Skills, Awards, Portfolio
Separate tables for better scalability and data management
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey, Float, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base


# ==================== ENUMS ====================
class EducationLevel(enum.Enum):
    HIGH_SCHOOL = "high_school"
    DIPLOMA = "diploma"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    PHD = "phd"
    POSTDOC = "postdoc"
    CERTIFICATION = "certification"
    BOOTCAMP = "bootcamp"


class EmploymentType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    APPRENTICESHIP = "apprenticeship"


class SkillLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class PortfolioTemplateCategory(enum.Enum):
    DEVELOPER = "developer"
    DESIGNER = "designer"
    DATA_SCIENCE = "data_science"
    PRODUCT = "product"
    GENERAL = "general"


# ==================== EDUCATION ====================
class Education(Base):
    """User Education Details"""
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Institution Details
    institution_name = Column(String(500), nullable=False)
    institution_location = Column(String(255))
    institution_type = Column(String(100))  # "university", "college", "school", "online"
    institution_logo_url = Column(String(500))
    institution_website = Column(String(500))
    
    # Degree Details
    degree_type = Column(Enum(EducationLevel), default=EducationLevel.BACHELORS)
    degree_name = Column(String(300), nullable=False)  # "B.Tech", "M.Sc", "MBA"
    field_of_study = Column(String(300))  # "Computer Science", "Data Science"
    specialization = Column(String(300))  # "Machine Learning", "Cloud Computing"
    
    # Duration
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_current = Column(Boolean, default=False)
    
    # Performance
    grade = Column(String(50))  # "A+", "First Class"
    gpa = Column(Float)  # 3.8
    gpa_scale = Column(Float, default=4.0)  # 4.0, 10.0
    percentage = Column(Float)  # 85.5
    rank = Column(Integer)  # Class rank if applicable
    
    # Additional Details
    thesis_title = Column(String(500))  # For Masters/PhD
    thesis_url = Column(String(500))
    activities = Column(Text)  # Extra-curricular activities
    achievements = Column(Text)  # Dean's list, scholarships
    courses = Column(JSON)  # Relevant courses taken
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_document_url = Column(String(500))
    
    # Display Settings
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="educations")


# ==================== EXPERIENCE ====================
class Experience(Base):
    """User Work Experience"""
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))  # Link to company if exists
    
    # Company Details
    company_name = Column(String(500), nullable=False)
    company_logo_url = Column(String(500))
    company_website = Column(String(500))
    company_linkedin = Column(String(500))
    industry = Column(String(200))  # "Technology", "Finance", "Healthcare"
    company_size = Column(String(50))  # "1-50", "51-200", "201-500", "501-1000", "1000+"
    
    # Role Details
    job_title = Column(String(300), nullable=False)
    employment_type = Column(Enum(EmploymentType), default=EmploymentType.FULL_TIME)
    location = Column(String(255))
    location_type = Column(String(50))  # "onsite", "remote", "hybrid"
    department = Column(String(200))
    
    # Duration
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    is_current = Column(Boolean, default=False)
    
    # Compensation (optional, for tracking)
    salary_currency = Column(String(10), default="INR")
    salary_amount = Column(Integer)  # Monthly or annual
    salary_type = Column(String(20))  # "monthly", "annual"
    
    # Description
    description = Column(Text)  # Full job description
    responsibilities = Column(JSON)  # ["Led team of 5", "Designed architecture"]
    achievements = Column(JSON)  # ["Reduced costs by 40%", "Launched 3 products"]
    
    # Skills & Technologies
    skills_used = Column(JSON)  # ["Python", "AWS", "Docker"]
    tools_used = Column(JSON)  # ["JIRA", "Confluence", "Git"]
    
    # Projects at this job (brief mentions)
    key_projects = Column(JSON)  # [{"name": "", "description": "", "impact": ""}]
    
    # References
    manager_name = Column(String(255))
    manager_linkedin = Column(String(500))
    can_contact = Column(Boolean, default=False)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_type = Column(String(50))  # "linkedin", "email", "document"
    
    # Display Settings
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="experiences")


# ==================== PROJECTS ====================
class Project(Base):
    """User Projects - Personal, Open Source, Work"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    experience_id = Column(Integer, ForeignKey("experiences.id"))  # Link to work experience
    
    # Basic Info
    name = Column(String(300), nullable=False)
    tagline = Column(String(500))  # One-liner description
    description = Column(Text, nullable=False)
    
    # Project Type
    project_type = Column(String(50))  # "personal", "work", "open_source", "academic", "freelance"
    status = Column(String(50))  # "in_progress", "completed", "maintained", "archived"
    visibility = Column(String(20))  # "public", "private"
    
    # Links
    live_url = Column(String(500))
    demo_url = Column(String(500))
    github_url = Column(String(500))
    documentation_url = Column(String(500))
    video_url = Column(String(500))  # Demo video
    
    # Media
    thumbnail_url = Column(String(500))
    screenshots = Column(JSON)  # Array of image URLs
    
    # Technical Details
    tech_stack = Column(JSON)  # ["React", "Node.js", "MongoDB"]
    programming_languages = Column(JSON)  # ["JavaScript", "Python"]
    frameworks = Column(JSON)  # ["Next.js", "FastAPI"]
    databases = Column(JSON)  # ["PostgreSQL", "Redis"]
    cloud_services = Column(JSON)  # ["AWS Lambda", "S3"]
    tools = Column(JSON)  # ["Docker", "GitHub Actions"]
    
    # Features & Highlights
    features = Column(JSON)  # ["Real-time sync", "OAuth integration"]
    highlights = Column(JSON)  # ["10K users", "Featured on HN"]
    challenges = Column(Text)  # Technical challenges overcome
    learnings = Column(Text)  # What you learned
    
    # Metrics
    stars = Column(Integer, default=0)  # GitHub stars
    forks = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    users = Column(Integer, default=0)
    
    # Team
    is_solo = Column(Boolean, default=True)
    team_size = Column(Integer, default=1)
    your_role = Column(String(200))  # "Lead Developer", "Full Stack Developer"
    team_members = Column(JSON)  # [{"name": "", "role": "", "linkedin": ""}]
    
    # Duration
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Categories/Tags
    categories = Column(JSON)  # ["web_app", "ai_ml", "devtools"]
    tags = Column(JSON)  # ["saas", "b2b", "productivity"]
    
    # Display Settings
    is_featured = Column(Boolean, default=False)  # Show prominently
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="projects")


# ==================== SKILLS ====================
class SkillCategory(Base):
    """Skill Categories - Programming, Frontend, Backend, etc."""
    __tablename__ = "skill_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))  # Font awesome icon or emoji
    color = Column(String(20))  # Hex color
    display_order = Column(Integer, default=0)
    
    # Relationships
    skills = relationship("Skill", back_populates="category")


class Skill(Base):
    """Master Skill List"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.id"))
    
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Visual
    icon = Column(String(100))
    logo_url = Column(String(500))
    color = Column(String(20))
    
    # Metadata
    is_popular = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    related_skills = Column(JSON)  # ["React", "Redux"] for JavaScript
    
    # Stats
    user_count = Column(Integer, default=0)  # How many users have this skill
    job_count = Column(Integer, default=0)  # How many jobs require this
    
    # Relationships
    category = relationship("SkillCategory", back_populates="skills")


class UserSkill(Base):
    """User's Skills with proficiency"""
    __tablename__ = "user_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    
    # If skill not in master list
    custom_skill_name = Column(String(100))
    
    # Proficiency
    level = Column(Enum(SkillLevel), default=SkillLevel.INTERMEDIATE)
    years_of_experience = Column(Float)
    
    # Endorsements
    endorsement_count = Column(Integer, default=0)
    
    # Last used
    last_used_date = Column(DateTime)
    
    # Display
    is_primary = Column(Boolean, default=False)  # Top skills to highlight
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="user_skills")
    skill = relationship("Skill")


# ==================== CERTIFICATIONS ====================
class Certification(Base):
    """User Certifications"""
    __tablename__ = "certifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Certification Details
    name = Column(String(500), nullable=False)
    issuing_organization = Column(String(300), nullable=False)
    organization_logo_url = Column(String(500))
    organization_website = Column(String(500))
    
    # Credentials
    credential_id = Column(String(255))
    credential_url = Column(String(500))  # Verification URL
    
    # Dates
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    does_expire = Column(Boolean, default=False)
    
    # Skills
    skills_covered = Column(JSON)  # ["AWS", "Cloud Architecture"]
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))  # "url", "api", "manual"
    
    # Badge
    badge_url = Column(String(500))  # Digital badge image
    
    # Display
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="certifications")


# ==================== AWARDS & ACHIEVEMENTS ====================
class Award(Base):
    """User Awards and Achievements"""
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Award Details
    title = Column(String(500), nullable=False)
    award_type = Column(String(100))  # "hackathon", "competition", "recognition", "scholarship", "publication"
    
    # Issuer
    issuing_organization = Column(String(300))
    organization_logo_url = Column(String(500))
    organization_website = Column(String(500))
    
    # Details
    description = Column(Text)
    position = Column(String(50))  # "1st", "2nd", "Winner", "Finalist"
    category = Column(String(200))  # Category won in
    
    # Links
    url = Column(String(500))  # Link to award/certificate
    proof_url = Column(String(500))  # Certificate image
    news_url = Column(String(500))  # News article about it
    
    # Date
    date_received = Column(DateTime)
    
    # Prize (if applicable)
    prize_amount = Column(Integer)
    prize_currency = Column(String(10))
    prize_details = Column(Text)
    
    # Display
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="awards")


# ==================== SOCIAL LINKS ====================
class SocialLink(Base):
    """User Social and Professional Links"""
    __tablename__ = "social_links"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Platform
    platform = Column(String(50), nullable=False)  # "linkedin", "github", "twitter", etc.
    platform_icon = Column(String(100))
    platform_color = Column(String(20))
    
    # Link
    url = Column(String(500), nullable=False)
    username = Column(String(200))  # Extracted username
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    
    # Stats (scraped)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    posts_count = Column(Integer)
    repos_count = Column(Integer)  # For GitHub
    contributions_count = Column(Integer)  # For GitHub
    stars_count = Column(Integer)  # For GitHub
    
    # Last synced
    last_synced = Column(DateTime)
    
    # Display
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    show_in_portfolio = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="social_links")


# ==================== RESUME ====================
class Resume(Base):
    """User Resumes - Multiple versions"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # File Details
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500))
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer)  # In bytes
    file_type = Column(String(50))  # "pdf", "docx"
    
    # Metadata
    title = Column(String(300))  # "Software Engineer Resume", "Data Scientist Resume"
    description = Column(Text)
    version = Column(String(50))  # "v1", "v2"
    
    # Target
    target_role = Column(String(200))
    target_companies = Column(JSON)
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    
    # Analytics
    download_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="resumes")


# ==================== PORTFOLIO ====================
class PortfolioTemplate(Base):
    """Portfolio Templates available"""
    __tablename__ = "portfolio_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Template Info
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Category
    category = Column(Enum(PortfolioTemplateCategory), default=PortfolioTemplateCategory.GENERAL)
    tags = Column(JSON)  # ["minimal", "dark", "animated"]
    
    # Visuals
    thumbnail_url = Column(String(500))
    preview_url = Column(String(500))
    screenshots = Column(JSON)
    
    # Template Source
    template_html = Column(Text)  # HTML template
    template_css = Column(Text)  # CSS styles
    template_js = Column(Text)  # JavaScript
    
    # Features
    features = Column(JSON)  # ["dark_mode", "animations", "responsive"]
    color_schemes = Column(JSON)  # Available color schemes
    font_options = Column(JSON)  # Available fonts
    
    # Pricing
    is_free = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    price = Column(Integer, default=0)
    
    # Stats
    usage_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserPortfolio(Base):
    """User's Generated Portfolio"""
    __tablename__ = "user_portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("portfolio_templates.id"))
    
    # URL
    subdomain = Column(String(100), unique=True, index=True)  # username.careerlaunch.io
    custom_domain = Column(String(255))  # Custom domain if pro
    slug = Column(String(100), unique=True, index=True)  # careerlaunch.io/slug
    
    # Customization
    title = Column(String(300))
    tagline = Column(String(500))
    
    # Theme customization
    color_primary = Column(String(20))
    color_secondary = Column(String(20))
    color_background = Column(String(20))
    color_text = Column(String(20))
    font_heading = Column(String(100))
    font_body = Column(String(100))
    
    # Custom CSS/JS
    custom_css = Column(Text)
    custom_js = Column(Text)
    custom_head = Column(Text)  # Custom head tags
    
    # SEO
    meta_title = Column(String(300))
    meta_description = Column(String(500))
    meta_keywords = Column(JSON)
    og_image = Column(String(500))
    
    # Content Visibility
    show_education = Column(Boolean, default=True)
    show_experience = Column(Boolean, default=True)
    show_projects = Column(Boolean, default=True)
    show_skills = Column(Boolean, default=True)
    show_certifications = Column(Boolean, default=True)
    show_awards = Column(Boolean, default=True)
    show_contact = Column(Boolean, default=True)
    show_resume_download = Column(Boolean, default=True)
    show_social_links = Column(Boolean, default=True)
    
    # Section Order
    section_order = Column(JSON)  # ["about", "experience", "projects", "skills", "education"]
    
    # Status
    is_published = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    published_at = Column(DateTime)
    
    # Password Protection
    is_password_protected = Column(Boolean, default=False)
    password_hash = Column(String(255))
    
    # Analytics
    view_count = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    resume_downloads = Column(Integer, default=0)
    contact_clicks = Column(Integer, default=0)
    
    # Generated HTML (cached)
    generated_html = Column(Text)
    last_generated = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="portfolios")
    template = relationship("PortfolioTemplate")


class PortfolioAnalytics(Base):
    """Portfolio View Analytics"""
    __tablename__ = "portfolio_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("user_portfolios.id"), nullable=False)
    
    # Visitor Info
    visitor_ip = Column(String(45))
    visitor_country = Column(String(100))
    visitor_city = Column(String(100))
    device_type = Column(String(50))  # "desktop", "mobile", "tablet"
    browser = Column(String(100))
    os = Column(String(100))
    referrer = Column(String(500))
    
    # Session
    session_id = Column(String(255))
    page_views = Column(Integer, default=1)
    time_spent = Column(Integer)  # Seconds
    
    # Actions
    clicked_resume = Column(Boolean, default=False)
    clicked_contact = Column(Boolean, default=False)
    clicked_social = Column(JSON)  # ["github", "linkedin"]
    clicked_projects = Column(JSON)  # Project IDs clicked
    
    # Timestamps
    visited_at = Column(DateTime, server_default=func.now())


# ==================== CAREER ROADMAPS ====================
class CareerRoadmap(Base):
    """Career Roadmaps - Learning paths for different roles"""
    __tablename__ = "career_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(300), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Target
    role = Column(String(200))  # "Frontend Developer", "Data Scientist"
    experience_level = Column(String(50))  # "beginner", "intermediate", "advanced"
    
    # Visual
    icon = Column(String(100))
    color = Column(String(20))
    thumbnail_url = Column(String(500))
    banner_url = Column(String(500))
    
    # Content
    overview = Column(Text)  # Introduction
    prerequisites = Column(JSON)  # Required knowledge
    duration_weeks = Column(Integer)  # Estimated completion time
    
    # Steps/Milestones
    steps = Column(JSON)  # [{id, title, description, topics, resources, duration, order}]
    
    # Resources
    resources = Column(JSON)  # [{title, url, type, is_free}]
    tools = Column(JSON)  # Recommended tools
    projects = Column(JSON)  # Suggested projects
    
    # Stats
    enrolled_count = Column(Integer, default=0)
    completed_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    # Author
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserRoadmapProgress(Base):
    """Track user progress on roadmaps"""
    __tablename__ = "user_roadmap_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(Integer, ForeignKey("career_roadmaps.id"), nullable=False)
    
    # Progress
    current_step = Column(Integer, default=0)
    completed_steps = Column(JSON)  # [1, 2, 3] - completed step IDs
    progress_percentage = Column(Float, default=0.0)
    
    # Status
    status = Column(String(50))  # "in_progress", "completed", "paused"
    
    # Notes
    notes = Column(JSON)  # User notes per step
    
    # Timestamps
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    last_activity = Column(DateTime, onupdate=func.now())


# ==================== SAVED JOBS ====================
class SavedJob(Base):
    """Jobs saved/bookmarked by users"""
    __tablename__ = "saved_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    # If job not in our database
    external_job_url = Column(String(500))
    job_title = Column(String(300))
    company_name = Column(String(300))
    company_logo = Column(String(500))
    location = Column(String(200))
    salary_range = Column(String(100))
    job_type = Column(String(50))
    
    # Notes
    notes = Column(Text)
    tags = Column(JSON)  # User's custom tags
    
    # Status
    status = Column(String(50))  # "saved", "applied", "interviewing", "rejected", "offer"
    priority = Column(Integer, default=0)  # 1-5 priority
    
    # Reminder
    reminder_date = Column(DateTime)
    reminder_sent = Column(Boolean, default=False)
    
    # Application
    applied_date = Column(DateTime)
    application_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="saved_jobs")
