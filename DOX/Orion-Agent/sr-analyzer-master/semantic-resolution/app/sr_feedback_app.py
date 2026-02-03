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

# SQLite fix for ChromaDB - MUST BE BEFORE ANY OTHER IMPORTS
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

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
    import os
    
    # Check for SSL certificates
    ssl_cert = 'ssl/cert.pem'
    ssl_key = 'ssl/key.pem'
    use_ssl = os.path.exists(ssl_cert) and os.path.exists(ssl_key)
    
    # Fixed port 5000, use 0.0.0.0 to allow external connections
    port = 5000
    host = '0.0.0.0'  # Listen on all interfaces for external access
    protocol = "https" if use_ssl else "http"
    
    # Get hostname for display
    import socket
    hostname = os.environ.get('SERVER_HOSTNAME', socket.getfqdn())
    
    print("=" * 80)
    print("🌟 SR Feedback System Starting...")
    print("=" * 80)
    print(f"🌐 User Portal: {protocol}://{hostname}:{port}")
    print(f"🔐 Admin Portal: {protocol}://{hostname}:{port}/admin")
    if use_ssl:
        print("🔒 SSL/HTTPS: Enabled ✅")
    else:
        print("⚠️  SSL/HTTPS: Disabled (create ssl/cert.pem and ssl/key.pem for HTTPS)")
    print("=" * 80)
    
    if use_ssl:
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=False,
            ssl_context=(ssl_cert, ssl_key)
        )
    else:
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=False
        )


if __name__ == '__main__':
    main()
