"""
Content Models - AI Tools, Git Repositories, YouTube Channels, Courses, etc.
Scraped and curated content for the platform
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base


# ==================== ENUMS ====================
class AIToolCategory(enum.Enum):
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    CODE_ASSISTANT = "code_assistant"
    VIDEO_GENERATION = "video_generation"
    AUDIO_MUSIC = "audio_music"
    CHATBOT = "chatbot"
    WRITING = "writing"
    PRODUCTIVITY = "productivity"
    DATA_ANALYSIS = "data_analysis"
    DESIGN = "design"
    MARKETING = "marketing"
    RESEARCH = "research"
    AUTOMATION = "automation"
    OTHER = "other"


class PricingModel(enum.Enum):
    FREE = "free"
    FREEMIUM = "freemium"
    PAID = "paid"
    OPEN_SOURCE = "open_source"
    ENTERPRISE = "enterprise"


class CourseProvider(enum.Enum):
    UDEMY = "udemy"
    COURSERA = "coursera"
    EDEX = "edx"
    PLURALSIGHT = "pluralsight"
    LINKEDIN_LEARNING = "linkedin_learning"
    YOUTUBE = "youtube"
    SKILLSHARE = "skillshare"
    FREECODECAMP = "freecodecamp"
    CODECADEMY = "codecademy"
    UDACITY = "udacity"
    OTHER = "other"


# ==================== AI TOOLS ====================
class AITool(Base):
    """AI Tools Directory"""
    __tablename__ = "ai_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True)
    tagline = Column(String(500))
    description = Column(Text)
    
    # Categorization
    category = Column(Enum(AIToolCategory), default=AIToolCategory.OTHER)
    subcategories = Column(JSON)  # ["chatbot", "customer_support"]
    tags = Column(JSON)  # ["gpt", "nlp", "free"]
    
    # Links
    website_url = Column(String(500))
    demo_url = Column(String(500))
    documentation_url = Column(String(500))
    api_url = Column(String(500))
    github_url = Column(String(500))
    
    # Visual
    logo_url = Column(String(500))
    screenshot_url = Column(String(500))
    screenshots = Column(JSON)  # Array of screenshot URLs
    
    # Pricing
    pricing_model = Column(Enum(PricingModel), default=PricingModel.FREEMIUM)
    pricing_details = Column(Text)
    free_tier_limits = Column(String(500))
    starting_price = Column(String(100))  # "$20/month", "Free"
    
    # Features
    features = Column(JSON)  # ["API access", "Bulk processing", "Export"]
    use_cases = Column(JSON)  # ["Content writing", "Code review"]
    integrations = Column(JSON)  # ["Slack", "Notion", "VS Code"]
    
    # Technical
    api_available = Column(Boolean, default=False)
    open_source = Column(Boolean, default=False)
    self_hosted = Column(Boolean, default=False)
    supported_languages = Column(JSON)  # Programming languages supported
    platforms = Column(JSON)  # ["web", "ios", "android", "desktop"]
    
    # Company Info
    company_name = Column(String(255))
    company_website = Column(String(500))
    founded_year = Column(Integer)
    headquarters = Column(String(255))
    
    # Stats (can be updated via scraping)
    monthly_visits = Column(Integer)
    user_count = Column(String(100))  # "1M+", "500K+"
    rating = Column(Float)  # 4.5
    review_count = Column(Integer)
    
    # Popularity on our platform
    views = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_verified = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ==================== GIT REPOSITORIES ====================
class GitRepository(Base):
    """Popular GitHub/GitLab Repositories"""
    __tablename__ = "git_repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(500), unique=True, index=True)  # owner/repo
    description = Column(Text)
    
    # Owner
    owner_name = Column(String(255))
    owner_type = Column(String(50))  # "user", "organization"
    owner_avatar = Column(String(500))
    owner_url = Column(String(500))
    
    # Links
    html_url = Column(String(500), nullable=False)
    clone_url = Column(String(500))
    homepage = Column(String(500))
    
    # Stats (scraped from GitHub API)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    watchers = Column(Integer, default=0)
    open_issues = Column(Integer, default=0)
    
    # Technical
    language = Column(String(100))
    languages = Column(JSON)  # {"JavaScript": 50, "Python": 30}
    topics = Column(JSON)  # ["machine-learning", "python"]
    license = Column(String(100))
    
    # Categorization (our own)
    category = Column(String(100))  # "frameworks", "tools", "learning"
    subcategory = Column(String(100))
    tags = Column(JSON)
    skill_level = Column(String(50))  # "beginner", "intermediate", "advanced"
    
    # Dates
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    pushed_date = Column(DateTime)
    
    # Additional Info
    readme_content = Column(Text)
    contributing_guide = Column(Text)
    has_wiki = Column(Boolean, default=False)
    has_issues = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    is_fork = Column(Boolean, default=False)
    
    # Platform engagement
    views = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ==================== YOUTUBE CHANNELS ====================
class YouTubeChannel(Base):
    """Tech YouTube Channels for Learning"""
    __tablename__ = "youtube_channels"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    channel_id = Column(String(100), unique=True, index=True)
    custom_url = Column(String(255))  # @channelname
    description = Column(Text)
    
    # Links
    channel_url = Column(String(500))
    
    # Visual
    thumbnail_url = Column(String(500))
    banner_url = Column(String(500))
    
    # Stats
    subscriber_count = Column(Integer)
    video_count = Column(Integer)
    view_count = Column(Integer)  # Total views
    
    # Categorization
    category = Column(String(100))  # "programming", "devops", "career"
    topics = Column(JSON)  # ["python", "javascript", "career_advice"]
    languages = Column(JSON)  # Content languages ["english", "hindi"]
    
    # Content Quality
    avg_video_length = Column(Integer)  # In minutes
    upload_frequency = Column(String(100))  # "weekly", "daily"
    content_type = Column(JSON)  # ["tutorials", "courses", "live"]
    
    # Target Audience
    skill_level = Column(String(50))  # "beginner", "intermediate", "advanced"
    target_roles = Column(JSON)  # ["frontend", "backend", "data_science"]
    
    # Featured Playlists
    playlists = Column(JSON)  # [{"name": "", "url": "", "videos": 10}]
    
    # Platform engagement
    views = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    rating = Column(Float)
    rating_count = Column(Integer, default=0)
    
    # Status
    is_verified = Column(Boolean, default=False)  # YouTube verified
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ==================== ONLINE COURSES ====================
class OnlineCourse(Base):
    """Online Courses from Various Platforms"""
    __tablename__ = "online_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(500), nullable=False)
    slug = Column(String(500), index=True)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Provider
    provider = Column(Enum(CourseProvider), default=CourseProvider.OTHER)
    provider_name = Column(String(255))  # For custom providers
    course_url = Column(String(500), nullable=False)
    
    # Instructor
    instructor_name = Column(String(255))
    instructor_title = Column(String(255))
    instructor_image = Column(String(500))
    instructor_bio = Column(Text)
    
    # Visual
    thumbnail_url = Column(String(500))
    preview_video_url = Column(String(500))
    
    # Course Details
    duration_hours = Column(Float)
    video_count = Column(Integer)
    article_count = Column(Integer)
    resource_count = Column(Integer)
    
    # Pricing
    is_free = Column(Boolean, default=False)
    original_price = Column(Float)
    current_price = Column(Float)
    currency = Column(String(10), default="USD")
    discount_percentage = Column(Integer)
    
    # Ratings
    rating = Column(Float)
    rating_count = Column(Integer)
    enrollment_count = Column(Integer)
    
    # Categorization
    category = Column(String(100))
    subcategory = Column(String(100))
    topics = Column(JSON)  # ["python", "django", "rest_api"]
    skills_covered = Column(JSON)
    
    # Target Audience
    skill_level = Column(String(50))  # "beginner", "intermediate", "advanced"
    prerequisites = Column(JSON)
    target_roles = Column(JSON)
    
    # Content
    syllabus = Column(JSON)  # [{"section": "", "lectures": []}]
    what_you_learn = Column(JSON)
    requirements = Column(JSON)
    
    # Certification
    has_certificate = Column(Boolean, default=False)
    certificate_type = Column(String(100))  # "completion", "professional"
    
    # Language
    language = Column(String(50), default="English")
    subtitles = Column(JSON)  # ["English", "Hindi", "Spanish"]
    
    # Dates
    created_date = Column(DateTime)
    last_updated = Column(DateTime)
    
    # Platform engagement
    views = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_synced = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ==================== TECH NEWS ====================
class TechNews(Base):
    """Tech News and Articles"""
    __tablename__ = "tech_news"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(500), nullable=False)
    slug = Column(String(500), index=True)
    summary = Column(Text)
    content = Column(Text)
    
    # Source
    source_name = Column(String(255))
    source_url = Column(String(500))
    author = Column(String(255))
    
    # Links
    article_url = Column(String(500), nullable=False)
    
    # Visual
    image_url = Column(String(500))
    
    # Categorization
    category = Column(String(100))  # "ai", "startups", "career", "tech"
    tags = Column(JSON)
    
    # Dates
    published_date = Column(DateTime)
    
    # Engagement
    views = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())


# ==================== TECH EVENTS ====================
class TechEvent(Base):
    """Tech Events, Conferences, Meetups"""
    __tablename__ = "tech_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(500), nullable=False)
    slug = Column(String(500), index=True)
    description = Column(Text)
    
    # Event Type
    event_type = Column(String(100))  # "conference", "meetup", "hackathon", "webinar"
    format = Column(String(50))  # "in_person", "virtual", "hybrid"
    
    # Links
    event_url = Column(String(500))
    registration_url = Column(String(500))
    
    # Visual
    banner_url = Column(String(500))
    logo_url = Column(String(500))
    
    # Location
    venue_name = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    address = Column(Text)
    
    # Dates
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    registration_deadline = Column(DateTime)
    
    # Pricing
    is_free = Column(Boolean, default=False)
    ticket_price = Column(String(100))
    
    # Categorization
    topics = Column(JSON)  # ["ai", "cloud", "devops"]
    target_audience = Column(JSON)
    
    # Organizer
    organizer_name = Column(String(255))
    organizer_url = Column(String(500))
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ==================== NEWSLETTERS ====================
class TechNewsletter(Base):
    """Tech Newsletters to Subscribe"""
    __tablename__ = "tech_newsletters"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    tagline = Column(String(500))
    
    # Links
    website_url = Column(String(500))
    subscribe_url = Column(String(500))
    archive_url = Column(String(500))
    
    # Visual
    logo_url = Column(String(500))
    
    # Details
    author_name = Column(String(255))
    frequency = Column(String(50))  # "daily", "weekly", "monthly"
    subscriber_count = Column(String(100))  # "50K+", "100K+"
    
    # Categorization
    topics = Column(JSON)  # ["ai", "startups", "programming"]
    
    # Pricing
    is_free = Column(Boolean, default=True)
    paid_tier_price = Column(String(100))
    
    # Platform engagement
    rating = Column(Float)
    saves = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())


# ==================== PODCASTS ====================
class TechPodcast(Base):
    """Tech Podcasts"""
    __tablename__ = "tech_podcasts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    
    # Host
    host_name = Column(String(255))
    host_bio = Column(Text)
    
    # Links
    website_url = Column(String(500))
    spotify_url = Column(String(500))
    apple_url = Column(String(500))
    youtube_url = Column(String(500))
    rss_url = Column(String(500))
    
    # Visual
    cover_url = Column(String(500))
    
    # Details
    episode_count = Column(Integer)
    avg_duration = Column(Integer)  # Minutes
    frequency = Column(String(50))
    
    # Categorization
    topics = Column(JSON)
    language = Column(String(50), default="English")
    
    # Stats
    rating = Column(Float)
    review_count = Column(Integer)
    
    # Platform engagement
    saves = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())


# ==================== BOOKS ====================
class TechBook(Base):
    """Tech Books Recommendations"""
    __tablename__ = "tech_books"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String(500), nullable=False)
    slug = Column(String(500), index=True)
    subtitle = Column(String(500))
    description = Column(Text)
    
    # Author
    author_name = Column(String(255))
    author_bio = Column(Text)
    
    # Publisher
    publisher = Column(String(255))
    published_date = Column(DateTime)
    edition = Column(String(50))
    pages = Column(Integer)
    isbn = Column(String(20))
    
    # Links
    amazon_url = Column(String(500))
    goodreads_url = Column(String(500))
    official_url = Column(String(500))
    
    # Visual
    cover_url = Column(String(500))
    
    # Categorization
    category = Column(String(100))
    topics = Column(JSON)
    skill_level = Column(String(50))
    
    # Ratings
    rating = Column(Float)
    rating_count = Column(Integer)
    
    # Pricing
    price = Column(String(50))
    
    # Platform engagement
    saves = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())


# ==================== INTERVIEW EXPERIENCES (PUBLIC) ====================
class PublicInterviewExperience(Base):
    """Public interview experiences shared by users"""
    __tablename__ = "public_interview_experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # Company Info (for non-linked)
    company_name = Column(String(255), nullable=False)
    company_logo = Column(String(500))
    
    # Position
    role = Column(String(255), nullable=False)
    experience_level = Column(String(50))  # "fresher", "1-3", "3-5", etc.
    location = Column(String(255))
    
    # Interview Details
    interview_date = Column(DateTime)
    difficulty = Column(String(50))  # "easy", "medium", "hard"
    result = Column(String(50))  # "selected", "rejected", "pending"
    duration_days = Column(Integer)  # Total process duration
    
    # Rounds
    total_rounds = Column(Integer)
    rounds = Column(JSON)  # [{"type": "", "questions": [], "tips": ""}]
    
    # Content
    overall_experience = Column(Text)
    tips = Column(Text)
    questions_asked = Column(JSON)
    
    # Salary (optional)
    offered_ctc = Column(Integer)
    share_salary = Column(Boolean, default=False)
    
    # Privacy
    is_anonymous = Column(Boolean, default=True)
    
    # Engagement
    views = Column(Integer, default=0)
    upvotes = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Moderation
    is_approved = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
