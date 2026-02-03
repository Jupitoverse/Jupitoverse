# backend/app.py
"""
Orionverse Agent - Combined Web + RAG Application
Integrates Orionverse Hub with Smart SR Assignment (RAG-based analysis)
"""
import sys
import os

# Fix Windows console encoding issues
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask
from flask_cors import CORS

# Enable more explicit CORS for cross-port communication
CORS_CONFIG = {
    "origins": ["*"],  # Allow all origins for development
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}

# Import all blueprints
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.billing_csv import billing_csv_bp
from routes.search import search_bp
from routes.workarounds import workarounds_bp
from routes.bulk_handling import bulk_handling_bp
from routes.excel_loader import excel_loader_bp
from routes.smart_sr import smart_sr_bp  # NEW: Smart SR Assignment

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": CORS_CONFIG})

    # Register all blueprints with the main app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(billing_csv_bp, url_prefix='/api/billing-csv')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(workarounds_bp, url_prefix='/api/workarounds')
    app.register_blueprint(bulk_handling_bp, url_prefix='/api/bulk-handling')
    app.register_blueprint(excel_loader_bp, url_prefix='/api/excel')
    
    # NEW: Smart SR Assignment (RAG-based analysis)
    app.register_blueprint(smart_sr_bp, url_prefix='/api/smart-sr')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Network deployment configuration
    # host='0.0.0.0' makes the app accessible from other machines on the network
    # Change debug=False for production deployment
    app.run(
        host='0.0.0.0',        # Listen on all network interfaces
        port=5002,             # Port number (different from original Orionverse)
        debug=True,            # Debug mode (set to False for production)
        threaded=True          # Handle multiple requests simultaneously
    )