# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import all blueprints
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.billing_csv import billing_csv_bp
from routes.search import search_bp
from routes.workarounds import workarounds_bp
from routes.bulk_handling import bulk_handling_bp
from routes.excel_loader import excel_loader_bp
from routes.sqo_api import sqo_api_bp
from routes.oni_api import oni_api_bp
from routes.activity_data import activity_data_bp

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    CORS(app)

    # Register all blueprints with the main app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(billing_csv_bp, url_prefix='/api/billing-csv')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(workarounds_bp, url_prefix='/api/workarounds')
    app.register_blueprint(bulk_handling_bp, url_prefix='/api/bulk-handling')
    app.register_blueprint(excel_loader_bp, url_prefix='/api/excel')
    app.register_blueprint(sqo_api_bp, url_prefix='/api/sqo')
    app.register_blueprint(oni_api_bp, url_prefix='/api/oni')
    app.register_blueprint(activity_data_bp, url_prefix='/api/activity')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Network deployment configuration
    # host='0.0.0.0' makes the app accessible from other machines on the network
    # Change debug=False for production deployment
    app.run(
        host='0.0.0.0',        # Listen on all network interfaces
        port=5001,             # Port number
        debug=False,           # Disabled to avoid Werkzeug DebuggedApplication compatibility issue
        threaded=True          # Handle multiple requests simultaneously
    )