#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SR Feedback Web Application - Entry Point
Web interface for collecting user feedback on AI-generated workarounds

This file serves as the entry point for the Flask application.
The application is now modularized using Flask Blueprints:

- app/__init__.py         - Flask app factory
- app/routes/auth.py      - Authentication routes (login/logout)
- app/routes/user.py      - User portal routes
- app/routes/admin.py     - Admin portal routes
- app/routes/team.py      - Team management routes
- app/routes/api.py       - API routes (voting, AI generation)
- app/utils/helpers.py    - Utility functions
- app/utils/decorators.py - Route decorators
- app/utils/state.py      - Shared application state
"""

import sys
import os

# Fix Windows console encoding issues - MUST BE FIRST
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

from app import create_app

# Create the Flask application
app = create_app()


def main():
    """Run the Flask application"""
    print("=" * 80)
    print("🌟 SR Feedback System Starting...")
    print("=" * 80)
    print("🌐 User Portal: http://localhost:5000")
    print("🔐 Admin Portal: http://localhost:5000/admin")
    print("=" * 80)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disabled to prevent constant restarts
    )


if __name__ == '__main__':
    main()
