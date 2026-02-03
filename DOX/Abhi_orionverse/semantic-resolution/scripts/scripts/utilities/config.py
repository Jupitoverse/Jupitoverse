"""
Configuration settings for SR Assignment Web Application
"""

import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sr_analyzer_secret_key_2024'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
    # Directories
    UPLOAD_FOLDER = 'web_uploads'
    RESULTS_FOLDER = 'web_results'
    TEMPLATES_FOLDER = 'templates'
    
    # File settings
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Server settings
    HOST = '0.0.0.0'  # Allow external access
    PORT = 5000
    DEBUG = False
    THREADED = True
    
    # Analysis settings
    DEFAULT_ANALYSIS_TYPE = 'complexity'
    MAX_PROCESSING_TIME = 300  # 5 minutes
    
    # Team configuration - Updated based on provided table
    TEAM_CONFIG = {
        "prateek_jain": {
            "name": "Prateek Jain",
            "areas": ["SOM_MM", "SQO_MM"],
            "som_mm_skill": 5,
            "sqo_mm_skill": 3,
            "max_workload": 15,  # SOM_MM max
            "max_workload_sqo": 2,  # SQO_MM max
            "specializations": ["Decomposition", "Scheduling", "ONI", "Shipping", "CPM Assignment", "Construction", "Dashboard", "Billing", "Pre-Sales"],
            "notes": "Expert in SOM_MM (5/5), Mid-level SQO_MM (3/5)"
        },
        "akshit_kaushik": {
            "name": "Akshit Kaushik",
            "areas": ["SOM_MM"],
            "som_mm_skill": 3,
            "max_workload": 10,
            "specializations": ["Decomposition", "Construction", "Dashboard", "Provisioning", "Pre-Sales"],
            "notes": "SOM_MM specialist (3/5)"
        },
        "abhishek_agrahari": {
            "name": "Abhishek Agrahari",
            "areas": ["SOM_MM"],
            "som_mm_skill": 4,
            "max_workload": 8,
            "specializations": ["Scheduling", "Shipping", "CPM Assignment", "Construction", "Dashboard", "Provisioning", "Billing"],
            "notes": "Strong SOM_MM performer (4/5)"
        },
        "sagar_ranjan": {
            "name": "Sagar Ranjan",
            "areas": ["SOM_MM"],
            "som_mm_skill": 1,
            "max_workload": 5,
            "specializations": ["Scheduling", "Shipping", "CPM Assignment", "Construction", "Provisioning", "Pre-Sales"],
            "notes": "Entry level SOM_MM (1/5)"
        },
        "smitesh_kadia": {
            "name": "Smitesh Kadia",
            "areas": ["SOM_MM"],
            "som_mm_skill": 4,
            "max_workload": 8,
            "specializations": ["Scheduling", "ONI", "Shipping", "CPM Assignment", "Construction", "Dashboard", "Provisioning", "Sync Point"],
            "notes": "Experienced SOM_MM (4/5)"
        },
        "anamika_thakur": {
            "name": "Anamika Thakur",
            "areas": ["SOM_MM"],
            "som_mm_skill": 3,
            "max_workload": 8,
            "specializations": ["Construction", "Dashboard", "Provisioning", "CPM Assignment", "Scheduling", "Pre-Sales"],
            "notes": "Mid-level SOM_MM (3/5)"
        },
        "dhulipalla_divya": {
            "name": "Dhulipalla Divya",
            "areas": ["SOM_MM"],
            "som_mm_skill": 2,
            "max_workload": 5,
            "specializations": ["Scheduling", "Shipping", "CPM Assignment", "Decomposition", "Construction", "Provisioning", "Pre-Sales"],
            "notes": "Basic SOM_MM (2/5)"
        },
        "kiran_jadhav": {
            "name": "Kiran Jadhav",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 5,
            "max_workload": 15,
            "specializations": ["NB Failure", "PreOPE or FABA", "Contract Terms", "Package", "Customer-Site", "Finalize-Screen", "Initiate Amend", "Serviceability", "ADH", "Offnet Quote", "Disconnect-Restore", "IRR"],
            "notes": "Expert SQO_MM (5/5)"
        },
        "aditya_sahore": {
            "name": "Aditya Sahore",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 5,
            "max_workload": 12,
            "specializations": ["NB Failure", "PreOPE or FABA", "Contract Terms", "Package", "Customer-Site", "Finalize-Screen", "Initiate Amend", "Serviceability", "ADH", "Offnet Quote", "Disconnect-Restore", "IRR"],
            "notes": "Expert SQO_MM (5/5)"
        },
        "krishna_tayade": {
            "name": "Krishna Tayade",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 4,
            "max_workload": 12,
            "specializations": ["Initiate Amend", "Proposal Validation", "Offnet Quote", "Serviceability", "ADH", "Offnet Quote", "Disconnect-Restore", "Customer-Site", "Finalize-Screen", "Merge Failure"],
            "notes": "Strong SQO_MM (4/5)"
        },
        "satyam_gupta": {
            "name": "Satyam Gupta",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 4,
            "max_workload": 10,
            "specializations": ["Merge Failure", "Proposal Validation", "Address Validation", "Initiate Amend", "Proposal Validation", "Offnet Quote", "PreOPE or FABA", "Contract Terms", "Serviceability", "Disconnect-Restore", "Customer-Site", "Finalize-Screen"],
            "notes": "Strong SQO_MM (4/5)"
        },
        "vishal_kasat": {
            "name": "Vishal Kasat",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 3,
            "max_workload": 5,
            "specializations": ["Initiate Amend", "Proposal Validation", "Offnet Quote", "Contract Terms", "Address Validation", "Serviceability", "Customer-Site", "Finalize-Screen"],
            "notes": "Mid-level SQO_MM (3/5)"
        },
        "aashika_mehrotra": {
            "name": "Aashika Mehrotra",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 3,
            "max_workload": 4,
            "specializations": ["Initiate Amend", "Proposal Validation", "Offnet Quote", "Contract Terms", "Address Validation", "Serviceability", "Customer-Site", "Finalize-Screen", "Merge Failure"],
            "notes": "Mid-level SQO_MM (3/5)"
        },
        "sunny_panghal": {
            "name": "Sunny Panghal",
            "areas": ["SQO_MM"],
            "sqo_mm_skill": 2,
            "max_workload": 2,
            "specializations": ["Offnet Quote", "Address Validation", "Serviceability", "Customer-Site", "Merge Failure"],
            "notes": "Entry level SQO_MM (2/5)"
        }
    }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
