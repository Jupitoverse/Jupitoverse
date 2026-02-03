#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Application Factory
Creates and configures the Flask application with blueprints
"""

import sys
import os

# SQLite fix for ChromaDB - MUST BE BEFORE ANY OTHER IMPORTS
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# Fix Windows console encoding issues
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'

# Add parent directory to path for imports
FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FLASK_APP_DIR)
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    errors='replace'
)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Application factory for creating the Flask app
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, 'templates'))
    
    # Load configuration
    app.config['SECRET_KEY'] = 'sr_feedback_secret_key_2024_change_in_production'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, 'input')
    app.config['OUTPUT_FOLDER'] = os.path.join(PROJECT_ROOT, 'output', 'reports')
    
    # Path configuration
    app.config['PROJECT_ROOT'] = PROJECT_ROOT
    app.config['DATABASE_DIR'] = os.path.join(PROJECT_ROOT, 'data', 'database')
    app.config['VECTORSTORE_DIR'] = os.path.join(PROJECT_ROOT, 'data', 'vectorstore')
    app.config['TOKENS_DIR'] = os.path.join(PROJECT_ROOT, 'tokens')
    app.config['INPUT_DIR'] = os.path.join(PROJECT_ROOT, 'input')
    app.config['OUTPUT_DIR'] = os.path.join(PROJECT_ROOT, 'output')
    app.config['REPORTS_DIR'] = os.path.join(PROJECT_ROOT, 'output', 'reports')
    
    # Apply custom config if provided
    if config:
        app.config.update(config)
    
    # Ensure folders exist
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    logger.info("Flask application created successfully")
    return app


# For backward compatibility - create default app instance
app = None

def get_app():
    """Get or create the Flask application"""
    global app
    if app is None:
        app = create_app()
    return app
