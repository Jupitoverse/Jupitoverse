"""
User Models - User profiles, subscriptions, and preferences
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base


class UserRole(enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    PRO = "pro"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class SubscriptionPlan(enum.Enum):
    FREE = "free"  # Basic access
    PREMIUM = "premium"  # ₹499/month - More features
    PRO = "pro"  # ₹999/month - Full access including HR contacts


class User(Base):
    """User Table with Authentication and Subscription"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Auth Info
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Email verified
    
    # Role & Subscription
    role = Column(Enum(UserRole), default=UserRole.USER)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_start = Column(DateTime)
    subscription_end = Column(DateTime)
    subscription_active = Column(Boolean, default=False)
    
    # Company Verification (for verified badge)
    is_verified_employee = Column(Boolean, default=False)
    verified_company_id = Column(Integer, ForeignKey("companies.id"))
    verified_company_email = Column(String(255))
    verification_code = Column(String(100))
    verification_expires = Column(DateTime)
    
    # Basic Info
    full_name = Column(String(255))
    username = Column(String(100), unique=True, index=True)
    avatar_url = Column(String(500))
    bio = Column(Text)
    phone = Column(String(20))
    
    # Professional Info
    current_company_id = Column(Integer, ForeignKey("companies.id"))
    current_company_name = Column(String(255))  # For non-listed companies
    current_title = Column(String(200))
    years_of_experience = Column(Float)
    
    # Social
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    portfolio_url = Column(String(500))
    twitter_url = Column(String(500))
    
    # Referral System
    referral_code = Column(String(20), unique=True, index=True)
    referred_by = Column(Integer, ForeignKey("users.id"))
    referral_earnings = Column(Float, default=0.0)  # ₹146 per referral
    total_referrals = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    referrals_given = relationship("Referral", foreign_keys="Referral.referrer_id", back_populates="referrer")
    referrals_received = relationship("Referral", foreign_keys="Referral.requester_id", back_populates="requester")
    reviews = relationship("Review", back_populates="user")
    interviews = relationship("InterviewTracker", back_populates="user")
    questions = relationship("InterviewQuestion", back_populates="user")
    posts = relationship("CommunityPost", back_populates="author")
    comments = relationship("CommunityComment", back_populates="author")


class UserProfile(Base):
    """User Profile with preferences for personalized suggestions"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Personal Info
    headline = Column(String(500))  # Professional headline like LinkedIn
    date_of_birth = Column(DateTime)
    gender = Column(String(20))
    
    # Career Info
    experience_years = Column(Float)
    current_ctc = Column(Integer)  # In INR lakhs
    expected_ctc = Column(Integer)
    notice_period_days = Column(Integer)
    notice_period_type = Column(String(50))  # "immediate", "15", "30", "45", "60", "90", "serving"
    last_working_day = Column(DateTime)  # If serving notice
    
    # Skills & Expertise
    primary_skills = Column(JSON)  # ["Python", "Machine Learning", "AWS"]
    secondary_skills = Column(JSON)
    certifications = Column(JSON)  # [{"name": "", "issuer": "", "date": "", "url": ""}]
    languages_known = Column(JSON)  # ["English", "Hindi"]
    
    # Education (JSON array for multiple entries)
    education = Column(JSON)  # [{"degree": "", "field": "", "university": "", "start": "", "end": "", "grade": ""}]
    highest_education = Column(String(100))
    degree = Column(String(200))
    university = Column(String(200))
    graduation_year = Column(Integer)
    
    # Work History (JSON array)
    work_history = Column(JSON)  # [{"company": "", "role": "", "type": "", "location": "", "from": "", "to": "", "current": false, "description": "", "skills": ""}]
    
    # Job Search Preferences
    is_looking_for_change = Column(Boolean, default=False)  # Toggle for looking for job change
    preferred_roles = Column(JSON)  # ["software_engineer", "senior_swe", "lead_swe", ...]
    preferred_job_types = Column(JSON)  # ["full_time", "contract"]
    preferred_work_modes = Column(JSON)  # ["remote", "hybrid", "onsite"]
    preferred_company_types = Column(JSON)  # ["product", "service", "startup", "mnc", "remote_first", "faang"]
    preferred_company_sizes = Column(JSON)  # ["startup", "mid", "large"]
    minimum_salary = Column(Integer)  # In INR lakhs
    
    # Location Preferences
    current_city = Column(String(100))
    preferred_cities = Column(JSON)  # ["bangalore", "hyderabad", "pune", ...]
    open_to_relocate = Column(Boolean, default=False)
    preferred_countries = Column(JSON)  # For abroad jobs
    
    # Abroad Job Preferences
    interested_in_abroad = Column(Boolean, default=False)
    target_countries = Column(JSON)
    visa_status = Column(String(100))  # "need_sponsorship", "valid_work_permit", "citizen"
    passport_valid = Column(Boolean)
    
    # Interested Roadmaps
    interested_roadmaps = Column(JSON)  # ["system_design", "dsa", "devops", "ml_ai", ...]
    
    # Job Search Status
    job_search_status = Column(String(50))  # "actively_looking", "open", "not_looking"
    available_from = Column(DateTime)
    
    # Social Links
    portfolio_url = Column(String(500))
    twitter_url = Column(String(500))
    
    # Notification Preferences
    job_alerts = Column(Boolean, default=True)
    referral_alerts = Column(Boolean, default=True)
    newsletter = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    
    # Resume
    resume_url = Column(String(500))
    resume_filename = Column(String(255))
    resume_updated_at = Column(DateTime)
    
    user = relationship("User", back_populates="profile")


class InterviewTracker(Base):
    """Track user's interview progress with detailed round tracking"""
    __tablename__ = "interview_trackers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String(255))  # For non-listed companies
    
    # Job Details
    job_title = Column(String(255))
    job_url = Column(String(500))
    job_description = Column(Text)
    applied_via = Column(String(100))  # "linkedin", "naukri", "company_website", "referral", "recruiter", "indeed", "other"
    referrer_name = Column(String(255))
    expected_ctc = Column(Integer)  # Expected CTC in LPA
    
    # Status - Enhanced statuses
    status = Column(String(50))  # "applied", "screening", "in_progress", "final_round", "offer", "accepted", "rejected", "declined", "on_hold"
    applied_date = Column(DateTime)
    last_updated = Column(DateTime, onupdate=func.now())
    
    # Rounds (JSON array) - Enhanced structure
    # [{"roundNumber": 1, "type": "hr_screening|technical|coding|system_design|lld|hld|behavioral|managerial|bar_raiser|culture_fit|case_study|assignment|final", 
    #   "datetime": "", "duration": 60, "status": "scheduled|completed|passed|failed|pending_feedback|cancelled|rescheduled",
    #   "interviewer": "", "questions": "", "notes": ""}]
    rounds = Column(JSON)
    total_rounds = Column(Integer, default=0)  # Total rounds in process
    current_round = Column(Integer, default=0)  # Current round number
    
    # Offer Details
    offer_ctc = Column(Integer)  # Offered CTC in LPA
    offer_joining_date = Column(DateTime)
    offer_location = Column(String(200))
    offer_received_date = Column(DateTime)
    offer_deadline = Column(DateTime)  # Deadline to respond
    
    # HR/Recruiter Contact
    hr_contact = Column(String(255))
    hr_email = Column(String(255))
    hr_phone = Column(String(20))
    
    # Notes
    notes = Column(Text)
    
    # Outcome
    final_outcome = Column(String(50))  # "accepted", "rejected", "declined", "pending"
    rejection_reason = Column(Text)
    feedback = Column(Text)
    
    # Privacy Settings - NEW
    is_public = Column(Boolean, default=False)  # If true, visible to community
    is_anonymous = Column(Boolean, default=True)  # If public, hide user identity
    share_questions = Column(Boolean, default=True)  # Share questions asked
    share_salary = Column(Boolean, default=False)  # Share salary details
    
    # Engagement (if public)
    views = Column(Integer, default=0)
    upvotes = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="interviews")


class StudyTask(Base):
    """Track study/preparation tasks for interviews"""
    __tablename__ = "study_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interview_trackers.id"))  # Optional link to interview
    
    # Task Details
    title = Column(String(500), nullable=False)
    description = Column(Text)
    task_type = Column(String(50))  # "study", "practice", "mock", "revision", "research"
    
    # Scheduling
    scheduled_date = Column(DateTime)
    duration_minutes = Column(Integer)
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    
    # Topics/Tags
    topics = Column(JSON)  # ["DSA", "System Design", "Behavioral"]
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class InterviewQuestion(Base):
    """Interview questions shared by users (anonymously)"""
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String(255))
    
    # Question Details
    role = Column(String(200))
    experience_level = Column(String(50))  # "fresher", "1-3", "3-5", "5-10", "10+"
    round_type = Column(String(100))  # "Technical", "HR", "Managerial", "System Design"
    
    # Content
    question = Column(Text, nullable=False)
    answer = Column(Text)  # Optional answer
    difficulty = Column(String(20))  # "easy", "medium", "hard"
    topics = Column(JSON)  # ["DSA", "System Design", "Behavioral"]
    
    # Privacy
    is_anonymous = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=True)  # Admin approval
    
    # Engagement
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    
    # Timestamps
    interview_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="questions")


class CommunityPost(Base):
    """Community posts (like Fishbowl/Blind)"""
    __tablename__ = "community_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Post Details
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(50))  # "question", "discussion", "review", "referral_request"
    
    # Targeting
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String(255))
    tags = Column(JSON)  # ["salary", "wlb", "interview"]
    
    # Privacy
    is_anonymous = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=True)
    
    # Only verified employees can see author
    show_verified_badge = Column(Boolean, default=False)
    
    # Engagement
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("CommunityComment", back_populates="post")


class CommunityComment(Base):
    """Comments on community posts"""
    __tablename__ = "community_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("community_comments.id"))  # For nested comments
    
    # Content
    content = Column(Text, nullable=False)
    
    # Privacy
    is_anonymous = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=True)
    show_verified_badge = Column(Boolean, default=False)
    
    # Engagement
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    post = relationship("CommunityPost", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Subscription(Base):
    """Subscription/Payment records"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Plan Details
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    amount = Column(Integer)  # In INR (499 or 999)
    currency = Column(String(10), default="INR")
    
    # Duration
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Payment
    payment_id = Column(String(255))  # Razorpay payment ID
    payment_status = Column(String(50))  # "pending", "completed", "failed", "refunded"
    payment_method = Column(String(50))  # "upi", "card", "netbanking"
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class ReferralReward(Base):
    """Track referral rewards"""
    __tablename__ = "referral_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who referred
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who signed up
    
    # Reward
    amount = Column(Float, default=146.0)  # ₹146 per referral
    status = Column(String(50))  # "pending", "credited", "paid"
    
    # Conditions
    referred_subscribed = Column(Boolean, default=False)  # Did referred user subscribe?
    subscription_plan = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    credited_at = Column(DateTime)
