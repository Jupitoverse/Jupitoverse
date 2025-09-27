# backend/app.py
from flask import Flask
from flask_cors import CORS
from routes.search import search_bp # <-- Add this import

# backend/app.py
# ... other imports ...
#search engine logic

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # ... other blueprints ...
    app.register_blueprint(search_bp, url_prefix='/api/search') # <-- Add this line
    
    return app

# ... rest of the file ...



# This line should now work correctly
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.workarounds import workarounds_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register the blueprints with the main app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(workarounds_bp, url_prefix='/api/workarounds')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)