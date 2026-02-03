"""
Application Settings
Configuration settings for the SR Feedback application
"""

import os

# Flask settings
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
SECRET_KEY = os.environ.get('SECRET_KEY', 'sr-feedback-secret-key-2024')

# Session settings
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

# Upload settings
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}

# Model settings
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# LLM API settings
LLM_API_URL = 'https://ai-framework1:8085/api/v1/call_llm'

# Search settings
DEFAULT_TOP_K = 5
SEMANTIC_SEARCH_THRESHOLD = 0.3

