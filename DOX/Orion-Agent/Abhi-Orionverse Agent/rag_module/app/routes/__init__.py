#!/usr/bin/env python3
"""
Blueprint Registration
Registers all route blueprints with the Flask application
"""


def register_blueprints(app):
    """Register all blueprints with the Flask application"""
    
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.team import team_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
