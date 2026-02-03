#!/usr/bin/env python3
"""
Route Decorators for SR Feedback Application
Authentication and authorization decorators
"""

from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Brute force protection - track failed login attempts
login_attempts = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def user_login_required(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect(url_for('auth.user_login'))
        return f(*args, **kwargs)
    return decorated_function


def check_login_attempts(ip_address):
    """Check if IP is locked out due to too many failed attempts"""
    if ip_address in login_attempts:
        attempt_data = login_attempts[ip_address]
        lockout_until = attempt_data.get('lockout_until')
        
        if lockout_until and datetime.now() < lockout_until:
            remaining = int((lockout_until - datetime.now()).total_seconds() / 60)
            return False, f"Too many failed attempts. Try again in {remaining} minutes."
        elif lockout_until and datetime.now() >= lockout_until:
            login_attempts[ip_address] = {'count': 0, 'lockout_until': None}
    
    return True, None


def record_failed_login(ip_address):
    """Record a failed login attempt"""
    if ip_address not in login_attempts:
        login_attempts[ip_address] = {'count': 0, 'lockout_until': None}
    
    login_attempts[ip_address]['count'] += 1
    
    if login_attempts[ip_address]['count'] >= MAX_LOGIN_ATTEMPTS:
        login_attempts[ip_address]['lockout_until'] = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        logger.warning(f"IP {ip_address} locked out after {MAX_LOGIN_ATTEMPTS} failed attempts")


def reset_login_attempts(ip_address):
    """Reset login attempts after successful login"""
    if ip_address in login_attempts:
        login_attempts[ip_address] = {'count': 0, 'lockout_until': None}
