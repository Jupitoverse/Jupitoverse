# backend/app.py
# Deployment-Ready Flask Application for ONI-SQO-Bulk Demo
# Author: Abhishek Sharma

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import blueprints
from routes.sqo_api import sqo_api_bp
from routes.oni_api import oni_api_bp
from routes.bulk_handling import bulk_handling_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    
    # CORS configuration - Allow all origins for demo
    # In production, restrict to specific domains
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(sqo_api_bp, url_prefix='/api/sqo')
    app.register_blueprint(oni_api_bp, url_prefix='/api/oni')
    app.register_blueprint(bulk_handling_bp, url_prefix='/api/bulk-handling')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ONI-SQO-Bulk API'}
    
    # Serve static files
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)
    
    return app

# Configuration
CONFIG = {
    'host': '0.0.0.0',      # Listen on all interfaces (required for remote access)
    'port': 5003,           # Backend port (use 5003 to avoid conflicts)
    'debug': False,         # Set to False for production
    'threaded': True        # Handle multiple requests
}

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("ONI-SQO-Bulk API Server")
    print("=" * 60)
    print(f"Local:   http://localhost:{CONFIG['port']}")
    print(f"Network: http://0.0.0.0:{CONFIG['port']}")
    print("=" * 60)
    print("Available Endpoints:")
    print("   /api/sqo/*           - SQO Operations")
    print("   /api/oni/*           - ONI Search")
    print("   /api/bulk-handling/* - Bulk Handling")
    print("   /api/health          - Health Check")
    print("=" * 60)
    
    app.run(
        host=CONFIG['host'],
        port=CONFIG['port'],
        debug=CONFIG['debug'],
        threaded=CONFIG['threaded']
    )
