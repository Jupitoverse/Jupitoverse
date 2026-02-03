# Job Hunt Portal - Database Models
from .database import Base, engine, get_db, init_db, get_database_info
from .company import Company, CompanyCategory, CompanyType
from .job import Job, JobApplication
from .user import (
    User, UserProfile, UserRole, SubscriptionPlan,
    InterviewTracker, InterviewQuestion, StudyTask,
    CommunityPost, CommunityComment,
    Subscription, ReferralReward
)
from .resource import Resource, Roadmap, RoadmapStep
from .country import Country, CountryMigration
from .referral import Referral
from .review import Review
from .agency import Agency
from .hr_contact import HRContact, HRContactVisibility
from .profile import (
    Education, EducationLevel,
    Experience, EmploymentType,
    Project,
    SkillCategory, Skill, UserSkill, SkillLevel,
    Certification,
    Award,
    SocialLink,
    Resume,
    PortfolioTemplate, UserPortfolio, PortfolioAnalytics, PortfolioTemplateCategory,
    CareerRoadmap, UserRoadmapProgress,
    SavedJob
)
from .content import (
    AITool, AIToolCategory, PricingModel,
    GitRepository,
    YouTubeChannel,
    OnlineCourse, CourseProvider,
    TechNews,
    TechEvent,
    TechNewsletter,
    TechPodcast,
    TechBook,
    PublicInterviewExperience
)

__all__ = [
    # Database
    "Base", "engine", "get_db", "init_db", "get_database_info",
    # Company
    "Company", "CompanyCategory", "CompanyType",
    # Jobs
    "Job", "JobApplication", "SavedJob",
    # User & Auth
    "User", "UserProfile", "UserRole", "SubscriptionPlan",
    "Subscription", "ReferralReward",
    # Interview
    "InterviewTracker", "InterviewQuestion", "StudyTask",
    # Community
    "CommunityPost", "CommunityComment",
    # Profile
    "Education", "EducationLevel",
    "Experience", "EmploymentType",
    "Project",
    "SkillCategory", "Skill", "UserSkill", "SkillLevel",
    "Certification",
    "Award",
    "SocialLink",
    "Resume",
    # Portfolio
    "PortfolioTemplate", "UserPortfolio", "PortfolioAnalytics", "PortfolioTemplateCategory",
    # Roadmaps
    "CareerRoadmap", "UserRoadmapProgress",
    "Resource", "Roadmap", "RoadmapStep",
    # Content
    "AITool", "AIToolCategory", "PricingModel",
    "GitRepository",
    "YouTubeChannel",
    "OnlineCourse", "CourseProvider",
    "TechNews",
    "TechEvent",
    "TechNewsletter",
    "TechPodcast",
    "TechBook",
    "PublicInterviewExperience",
    # Other
    "Country", "CountryMigration",
    "Referral", "Review", "Agency",
    "HRContact", "HRContactVisibility"
]
