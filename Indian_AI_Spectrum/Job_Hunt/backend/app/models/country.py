"""
Country Models - Country migration details for abroad jobs
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Country(Base):
    """Country Information Table"""
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(100), unique=True, index=True)
    code = Column(String(10), unique=True)  # ISO code
    flag_emoji = Column(String(10))
    continent = Column(String(50))
    
    # Job Market
    tech_hub_cities = Column(JSON)  # ["Berlin", "Munich", "Hamburg"]
    popular_industries = Column(JSON)
    avg_tech_salary_usd = Column(Integer)
    
    # For Indians
    indian_population_estimate = Column(Integer)
    indian_friendly_score = Column(Float)  # 1-10 based on community feedback
    
    # Metadata
    is_popular_destination = Column(Boolean, default=False)
    difficulty_score = Column(Float)  # 1-10, higher = more difficult
    
    created_at = Column(DateTime, server_default=func.now())

class CountryMigration(Base):
    """Detailed Migration Guide for each country"""
    __tablename__ = "country_migrations"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer)
    country_name = Column(String(100), index=True)
    
    # Visa Information
    visa_types = Column(JSON)  # [{"name": "Blue Card", "description": "...", "requirements": [...]}]
    visa_process_steps = Column(JSON)
    visa_processing_time_weeks = Column(Integer)
    visa_cost_usd = Column(Integer)
    
    # Work Permit
    work_permit_info = Column(Text)
    employer_sponsorship_required = Column(Boolean, default=True)
    
    # Job Search
    popular_job_portals = Column(JSON)  # [{"name": "Indeed Germany", "url": "...", "description": "..."}]
    recruitment_agencies = Column(JSON)
    linkedin_job_search_tips = Column(Text)
    
    # Resume/CV
    resume_format = Column(Text)  # Country-specific resume format
    resume_tips = Column(JSON)  # List of tips
    cover_letter_required = Column(Boolean)
    
    # Documents Required
    documents_required = Column(JSON)  # ["Degree certificates", "Experience letters", ...]
    document_attestation_required = Column(Boolean)
    
    # Cost of Living
    monthly_expenses_estimate = Column(JSON)  # {"single": 1500, "family": 3000}
    initial_settlement_cost = Column(Integer)  # In USD
    
    # Relocation
    relocation_checklist = Column(JSON)
    initial_accommodation_tips = Column(Text)
    banking_guide = Column(Text)
    mobile_sim_guide = Column(Text)
    
    # Language
    language_requirements = Column(JSON)  # {"work": "English B2", "residence": "German A1"}
    language_learning_resources = Column(JSON)
    
    # PR/Citizenship Path
    pr_eligibility_years = Column(Integer)
    pr_requirements = Column(JSON)
    citizenship_eligibility_years = Column(Integer)
    citizenship_requirements = Column(JSON)
    
    # Tax & Finance
    income_tax_rate = Column(String(100))  # "14% - 45% progressive"
    tax_treaties_with_india = Column(Boolean)
    tax_tips = Column(JSON)
    
    # Quality of Life
    healthcare_system = Column(Text)
    education_system = Column(Text)
    indian_community = Column(Text)
    indian_groceries_availability = Column(String(100))
    
    # Risks & Challenges
    common_challenges = Column(JSON)
    tips_for_indians = Column(JSON)
    things_to_avoid = Column(JSON)
    
    # Success Stories
    success_stories = Column(JSON)  # Links or embedded stories
    
    # Current Opportunities
    current_demand_sectors = Column(JSON)
    companies_hiring_indians = Column(JSON)
    
    # Community & Resources
    facebook_groups = Column(JSON)
    whatsapp_telegram_groups = Column(JSON)
    youtube_channels = Column(JSON)
    useful_websites = Column(JSON)
    
    # Additional Fields
    interview_process = Column(JSON)  # Interview process steps
    salary_negotiation_tips = Column(JSON)  # Salary negotiation advice
    
    # Extended Information
    top_hiring_companies = Column(JSON)  # List of companies with careers URLs
    attestation_process = Column(JSON)  # Document attestation steps
    initial_costs_breakdown = Column(JSON)  # Detailed initial costs
    work_culture = Column(JSON)  # Work culture notes
    tax_info = Column(JSON)  # Detailed tax info
    healthcare_info = Column(JSON)  # Healthcare system details
    salary_expectations = Column(JSON)  # Salary ranges by role
    pr_info = Column(Text)  # PR pathway summary
    citizenship_info = Column(Text)  # Citizenship pathway summary
    
    # New Enhanced Fields
    pros_cons = Column(JSON)  # {"pros": [...], "cons": [...]}
    verified_agencies = Column(JSON)  # List of verified recruitment agencies
    mail_templates = Column(JSON)  # Cold email templates for job applications
    expense_breakdown = Column(JSON)  # Detailed expense breakdown
    avg_salaries_by_role = Column(JSON)  # Role-wise salary data
    job_openings_urls = Column(JSON)  # URLs to scrape/show job openings
    indian_community_size = Column(String(100))  # Estimated Indian population
    best_cities_for_indians = Column(JSON)  # Cities ranked for Indians
    weather_info = Column(Text)  # Weather summary
    food_options = Column(JSON)  # Indian food availability
    flight_time_from_india = Column(String(50))  # Flight duration
    time_zone_diff = Column(String(50))  # Time difference from IST
    interview_tips = Column(JSON)  # Country-specific interview tips
    networking_tips = Column(JSON)  # Networking and referral tips
    work_life_balance_score = Column(Float)  # 1-10 score
    career_growth_score = Column(Float)  # 1-10 score
    safety_score = Column(Float)  # 1-10 score
    
    # Timestamps
    last_updated = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

