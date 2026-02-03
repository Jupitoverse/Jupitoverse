#!/usr/bin/env python3
"""
Authentication Routes Blueprint
Handles login/logout for admin and user portals
Supports Azure AD SSO authentication
"""

import os
import uuid
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from app.utils.decorators import (
    check_login_attempts, record_failed_login, reset_login_attempts,
    MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES, login_attempts
)

# Import Azure AD configuration
try:
    from config.azure_ad import (
        get_auth_url, get_token_from_code, get_user_info, 
        AZURE_AD_CONFIG, is_azure_ad_configured
    )
    AZURE_AD_ENABLED = is_azure_ad_configured()
except ImportError:
    AZURE_AD_ENABLED = False

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# Admin credentials (fallback for local authentication)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),
}

# User credentials (fallback for local authentication)
USER_CREDENTIALS = {
    'user1': generate_password_hash('user123'),
    'user2': generate_password_hash('pass123'),
    'john': generate_password_hash('john123'),
    'sarah': generate_password_hash('sarah123')
}

# Admin email addresses (users with these emails get admin access)
# Can be configured via ADMIN_EMAILS environment variable (comma-separated)
# Example: ADMIN_EMAILS=user1@amdocs.com,user2@amdocs.com
_admin_emails_env = os.environ.get('ADMIN_EMAILS', '')
ADMIN_EMAILS = [
    email.strip().lower() 
    for email in _admin_emails_env.split(',') 
    if email.strip()
]

# Add your admin NT Net IDs here (or use environment variable)
# Format: firstname.lastname@amdocs.com or ntnetid@amdocs.com
if not ADMIN_EMAILS:
    ADMIN_EMAILS = [
        # Add your admin emails here:
        'mrituinjay.shahi@amdocs.com',  
        'mukul.bhasin@amdocs.com',
        'praveerd@amdocs.com',
        'nikhilesh.srivastava@amdocs.com',
        'abhisha3@amdocs.com',
        'prateek.jain5@amdocs.com',
        'jprateek@amdocs.com',
        'bishal.agrawal@amdocs.com'
    ]


@auth_bp.route('/')
def index():
    """Main entry point - login selection page"""
    return render_template('auth/login_select.html', azure_ad_enabled=AZURE_AD_ENABLED)


# ============================================
# Azure AD Authentication Routes
# ============================================

@auth_bp.route('/auth/login')
def azure_login():
    """Initiate Azure AD login flow"""
    if not AZURE_AD_ENABLED:
        return redirect(url_for('auth.user_login'))
    
    # Generate a unique state to prevent CSRF
    state = str(uuid.uuid4())
    session['auth_state'] = state
    
    # Store the portal type (user or admin) if specified
    portal = request.args.get('portal', 'user')
    session['auth_portal'] = portal
    
    # Get the Azure AD authorization URL
    auth_url = get_auth_url(state=state)
    
    logger.info(f"Initiating Azure AD login for portal: {portal}")
    return redirect(auth_url)


@auth_bp.route('/auth/microsoft/callback')
def azure_callback():
    """Handle Azure AD callback after authentication"""
    if not AZURE_AD_ENABLED:
        return redirect(url_for('auth.index'))
    
    # Check for errors from Azure AD
    error = request.args.get('error')
    if error:
        error_description = request.args.get('error_description', 'Unknown error')
        logger.error(f"Azure AD error: {error} - {error_description}")
        return render_template('auth/login_error.html', 
                             error=error, 
                             error_description=error_description)
    
    # Verify state to prevent CSRF
    state = request.args.get('state')
    stored_state = session.pop('auth_state', None)
    
    if state != stored_state:
        logger.warning("State mismatch in Azure AD callback - possible CSRF attack")
        return render_template('auth/login_error.html', 
                             error="Security Error", 
                             error_description="Invalid state parameter. Please try again.")
    
    # Get the authorization code
    auth_code = request.args.get('code')
    if not auth_code:
        return render_template('auth/login_error.html', 
                             error="No Code", 
                             error_description="No authorization code received.")
    
    try:
        # Exchange code for token
        token_result = get_token_from_code(auth_code)
        
        if 'error' in token_result:
            logger.error(f"Token error: {token_result.get('error_description', token_result.get('error'))}")
            return render_template('auth/login_error.html', 
                                 error=token_result.get('error', 'Token Error'),
                                 error_description=token_result.get('error_description', 'Failed to get access token'))
        
        # Get user info from Microsoft Graph
        access_token = token_result.get('access_token')
        user_info = get_user_info(access_token)
        
        if not user_info:
            return render_template('auth/login_error.html', 
                                 error="User Info Error",
                                 error_description="Failed to get user information from Microsoft.")
        
        # Extract user details
        user_email = user_info.get('mail') or user_info.get('userPrincipalName', '')
        user_name = user_info.get('displayName', user_email.split('@')[0])
        user_id = user_info.get('id')
        
        # Determine portal type and set session
        portal = session.pop('auth_portal', 'user')
        
        # Check if user should have admin access
        is_admin = user_email.lower() in [email.lower() for email in ADMIN_EMAILS]
        
        if portal == 'admin':
            if is_admin or not ADMIN_EMAILS:  # If ADMIN_EMAILS is empty, allow all authenticated users
                session['admin_logged_in'] = True
                session['admin_username'] = user_name
                session['admin_email'] = user_email
                session['admin_azure_id'] = user_id
                session['auth_method'] = 'azure_ad'
                
                logger.info(f"Azure AD admin login successful: {user_email}")
                return redirect(url_for('admin.admin_page'))
            else:
                logger.warning(f"Unauthorized admin access attempt: {user_email}")
                return render_template('auth/login_error.html', 
                                     error="Access Denied",
                                     error_description=f"Your account ({user_email}) doesn't have admin access. Please contact your administrator to add your email to the admin list.")
        else:
            # User portal login
            session['user_logged_in'] = True
            session['user_username'] = user_name
            session['user_email'] = user_email
            session['user_azure_id'] = user_id
            session['auth_method'] = 'azure_ad'
            
            logger.info(f"Azure AD user login successful: {user_email}")
            return redirect(url_for('user.user_portal'))
    
    except Exception as e:
        logger.error(f"Azure AD callback error: {str(e)}")
        return render_template('auth/login_error.html', 
                             error="Authentication Error",
                             error_description=f"An error occurred during authentication: {str(e)}")


@auth_bp.route('/auth/logout')
def azure_logout():
    """Logout from Azure AD and clear session"""
    # Get user info for logging
    user_email = session.get('user_email') or session.get('admin_email', 'Unknown')
    
    # Clear all session data
    session.clear()
    
    logger.info(f"User logged out: {user_email}")
    
    # Redirect to Azure AD logout (optional - signs out from Microsoft too)
    # If you want to just logout from your app, redirect to index instead
    if AZURE_AD_ENABLED:
        logout_url = f"https://login.microsoftonline.com/{AZURE_AD_CONFIG['tenant_id']}/oauth2/v2.0/logout"
        post_logout_redirect = url_for('auth.index', _external=True)
        return redirect(f"{logout_url}?post_logout_redirect_uri={post_logout_redirect}")
    
    return redirect(url_for('auth.index'))


# ============================================
# Local Authentication Routes (Fallback)
# ============================================

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'GET':
        if 'admin_logged_in' in session:
            return redirect(url_for('admin.admin_page'))
        return render_template('auth/admin_login.html', azure_ad_enabled=AZURE_AD_ENABLED)
    
    try:
        ip_address = request.remote_addr or 'unknown'
        
        allowed, error_msg = check_login_attempts(ip_address)
        if not allowed:
            return jsonify({'success': False, 'error': error_msg}), 429
        
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        if len(username) > 50 or len(password) > 100:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 400
        
        if username in ADMIN_CREDENTIALS and check_password_hash(ADMIN_CREDENTIALS[username], password):
            reset_login_attempts(ip_address)
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['auth_method'] = 'local'
            logger.info(f"Admin login successful: {username} from {ip_address}")
            return jsonify({
                'success': True,
                'message': f'Welcome, {username}!',
                'redirect': url_for('admin.admin_page')
            })
        else:
            record_failed_login(ip_address)
            attempts_left = MAX_LOGIN_ATTEMPTS - login_attempts.get(ip_address, {}).get('count', 0)
            logger.warning(f"Failed login attempt for username: {username} from {ip_address}")
            
            if attempts_left > 0:
                return jsonify({'success': False, 'error': f'Invalid username or password. {attempts_left} attempts remaining.'}), 401
            else:
                return jsonify({'success': False, 'error': f'Too many failed attempts. Account locked for {LOCKOUT_DURATION_MINUTES} minutes.'}), 429
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@auth_bp.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    username = session.get('admin_username', 'Unknown')
    auth_method = session.get('auth_method', 'local')
    
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    session.pop('admin_email', None)
    session.pop('admin_azure_id', None)
    session.pop('auth_method', None)
    
    logger.info(f"Admin logout: {username} (method: {auth_method})")
    
    # If Azure AD, do full logout
    if auth_method == 'azure_ad' and AZURE_AD_ENABLED:
        return redirect(url_for('auth.azure_logout'))
    
    return redirect(url_for('auth.index'))


@auth_bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """User login page"""
    if request.method == 'GET':
        if 'user_logged_in' in session:
            return redirect(url_for('user.user_portal'))
        return render_template('auth/user_login.html', azure_ad_enabled=AZURE_AD_ENABLED)
    
    try:
        ip_address = request.remote_addr or 'unknown'
        
        allowed, error_msg = check_login_attempts(ip_address)
        if not allowed:
            return jsonify({'success': False, 'error': error_msg}), 429
        
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        if len(username) > 50 or len(password) > 100:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 400
        
        if username in USER_CREDENTIALS and check_password_hash(USER_CREDENTIALS[username], password):
            reset_login_attempts(ip_address)
            session['user_logged_in'] = True
            session['user_username'] = username
            session['auth_method'] = 'local'
            logger.info(f"User login successful: {username} from {ip_address}")
            return jsonify({
                'success': True,
                'message': f'Welcome, {username}!',
                'redirect': url_for('user.user_portal')
            })
        else:
            record_failed_login(ip_address)
            attempts_left = MAX_LOGIN_ATTEMPTS - login_attempts.get(ip_address, {}).get('count', 0)
            logger.warning(f"Failed user login attempt for username: {username} from {ip_address}")
            
            if attempts_left > 0:
                return jsonify({'success': False, 'error': f'Invalid username or password. {attempts_left} attempts remaining.'}), 401
            else:
                return jsonify({'success': False, 'error': f'Too many failed attempts. Account locked for {LOCKOUT_DURATION_MINUTES} minutes.'}), 429
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@auth_bp.route('/user/logout')
def user_logout():
    """User logout"""
    username = session.get('user_username', 'Unknown')
    auth_method = session.get('auth_method', 'local')
    
    session.pop('user_logged_in', None)
    session.pop('user_username', None)
    session.pop('user_email', None)
    session.pop('user_azure_id', None)
    session.pop('auth_method', None)
    
    logger.info(f"User logout: {username} (method: {auth_method})")
    
    # If Azure AD, do full logout
    if auth_method == 'azure_ad' and AZURE_AD_ENABLED:
        return redirect(url_for('auth.azure_logout'))
    
    return redirect(url_for('auth.index'))
