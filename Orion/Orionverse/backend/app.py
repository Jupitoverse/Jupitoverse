# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import all blueprints
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.search import search_bp
from routes.workarounds import workarounds_bp

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    CORS(app)

    # Register all blueprints with the main app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(workarounds_bp, url_prefix='/api/workarounds')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)