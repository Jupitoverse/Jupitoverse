# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import database

# ✅ FIX: This line creates the 'auth_bp' Blueprint that app.py needs to import.
auth_bp = Blueprint('auth', __name__)

# ✅ FIX: The route decorator now uses '@auth_bp.route' instead of '@app.route'.
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')

    if not all([fullname, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = database.create_user(fullname, email, password)
    
    if new_user is None:
        return jsonify({"error": "Email already exists"}), 409

    return jsonify(new_user), 201

# ✅ FIX: This route also uses '@auth_bp.route'.
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = database.find_user_by_email(email)

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    if user['status'] != 'approved':
        return jsonify({"error": "Account not approved by admin"}), 403
    
    return jsonify({
        "message": "Login successful",
        "user": {"fullname": user['fullname'], "email": user['email'], "role": user['role']}
    })
    
    # You can add more authentication-related routes here if needed.
    # For now, there is nothing else to add.