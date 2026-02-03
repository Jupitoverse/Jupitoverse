#!/usr/bin/env python3
"""
Authentication Routes Blueprint
Handles login/logout for admin and user portals
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from app.utils.decorators import (
    check_login_attempts, record_failed_login, reset_login_attempts,
    MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES, login_attempts
)

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# Admin credentials
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),
}

# User credentials
USER_CREDENTIALS = {
    'user1': generate_password_hash('user123'),
    'user2': generate_password_hash('pass123'),
    'john': generate_password_hash('john123'),
    'sarah': generate_password_hash('sarah123')
}


@auth_bp.route('/')
def index():
    """Main entry point - login selection page"""
    return render_template('feedback/login_select.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'GET':
        if 'admin_logged_in' in session:
            return redirect(url_for('admin.admin_page'))
        return render_template('feedback/admin_login.html')
    
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
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    logger.info(f"Admin logout: {username}")
    return redirect(url_for('auth.index'))


@auth_bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """User login page"""
    if request.method == 'GET':
        if 'user_logged_in' in session:
            return redirect(url_for('user.user_portal'))
        return render_template('feedback/user_login.html')
    
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
    session.pop('user_logged_in', None)
    session.pop('user_username', None)
    logger.info(f"User logout: {username}")
    return redirect(url_for('auth.index'))


