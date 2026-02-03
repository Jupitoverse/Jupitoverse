#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SR Feedback Web Application
Web interface for collecting user feedback on AI-generated workarounds
"""

# Fix Windows console encoding issues - MUST BE FIRST
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    
    # Set environment variables for subprocesses
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'  # Disable Python buffering

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import traceback
import pickle
from typing import Optional, Dict

# Import our modules
from scripts.core.user_feedback_manager import UserFeedbackManager
from comprehensive_sr_analyzer import ComprehensiveSRAnalyzer

# 🆕 Import feedback storage system
try:
    from feedback_storage import WorkaroundFeedbackStorage
    feedback_storage = WorkaroundFeedbackStorage()
    print("[OK] Workaround feedback storage initialized")
except Exception as e:
    feedback_storage = None
    print(f"[WARN] Could not initialize feedback storage: {e}")


# ============================================================================
# UTILITY FUNCTIONS - Data Helpers
# ============================================================================

def safe_get(d, keys, default='NA'):
    """
    Safely get values from dict and handle NaN/None values
    
    Args:
        d: Dictionary to search
        keys: Key or list of keys to try
        default: Default value if not found
    
    Returns:
        Value from dict or default
    """
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        val = d.get(key, default)
        # Check if value is NaN or None
        if pd.isna(val) or val is None or str(val).strip() == '':
            continue
        return str(val)
    return default


def concatenate_categorization_fields(sr_dict: Dict, source: str = 'excel_temp') -> str:
    """
    Concatenate the new SLA categorization fields into a single display string
    
    Args:
        sr_dict: SR dictionary containing categorization fields
        source: Source of the SR ('vector_store' or 'excel_temp')
    
    Returns:
        Concatenated categorization string
    """
    fields = []
    
    if source == 'vector_store':
        # Direct access from vector store metadata
        field_names = [
            'resolution_categorization',
            'resolution_categorization_tier3',
            'sla_resolution_categorization_t1',
            'sla_resolution_category'
        ]
    else:
        # From processed Excel with "Similar SRs" suffix
        field_names = [
            'Resolution Categorization',
            'Resolution Categorization Tier 3',
            'SLA Resolution Categorization T1',
            'SLA Resolution Category'
        ]
    
    for field in field_names:
        value = safe_get(sr_dict, [field], '')
        if value and str(value).strip() and str(value).strip().lower() not in ['nan', 'none', 'n/a', 'na', '']:
            fields.append(str(value).strip())
    
    if fields:
        return ' > '.join(fields)
    else:
        return 'N/A'

# Configure logging with UTF-8 support
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    errors='replace'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output/reports'
app.secret_key = 'sr_feedback_secret_key_2024_change_in_production'  # Secret key for sessions

# Admin credentials (can be moved to config file or database later)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),  # Username: admin, Password: admin123
    'bishala': generate_password_hash('bishala@123')  # Username: bishala, Password: bishala@123
}

# User credentials (can be moved to config file or database later)
USER_CREDENTIALS = {
    'user1': generate_password_hash('user123'),  # Username: user1, Password: user123
    'user2': generate_password_hash('pass123'),  # Username: user2, Password: pass123
    'john': generate_password_hash('john123'),  # Username: john, Password: john123
    'sarah': generate_password_hash('sarah123')  # Username: sarah, Password: sarah123
}

# Ensure folders exist
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

# Initialize managers
feedback_manager = UserFeedbackManager()
analyzer = ComprehensiveSRAnalyzer()

# Store current session data
session_data = {
    'uploaded_file': None,
    'analyzed_data': None,
    'original_df': None
}

# Brute force protection - track failed login attempts
login_attempts = {}  # {ip_address: {'count': 0, 'lockout_until': None}}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


def check_login_attempts(ip_address):
    """Check if IP is locked out due to too many failed attempts"""
    if ip_address in login_attempts:
        attempt_data = login_attempts[ip_address]
        lockout_until = attempt_data.get('lockout_until')
        
        if lockout_until and datetime.now() < lockout_until:
            remaining = int((lockout_until - datetime.now()).total_seconds() / 60)
            return False, f"Too many failed attempts. Try again in {remaining} minutes."
        elif lockout_until and datetime.now() >= lockout_until:
            # Lockout expired, reset
            login_attempts[ip_address] = {'count': 0, 'lockout_until': None}
    
    return True, None


def record_failed_login(ip_address):
    """Record a failed login attempt"""
    if ip_address not in login_attempts:
        login_attempts[ip_address] = {'count': 0, 'lockout_until': None}
    
    login_attempts[ip_address]['count'] += 1
    
    if login_attempts[ip_address]['count'] >= MAX_LOGIN_ATTEMPTS:
        from datetime import timedelta
        login_attempts[ip_address]['lockout_until'] = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        logger.warning(f"IP {ip_address} locked out after {MAX_LOGIN_ATTEMPTS} failed attempts")


def reset_login_attempts(ip_address):
    """Reset login attempts after successful login"""
    if ip_address in login_attempts:
        login_attempts[ip_address] = {'count': 0, 'lockout_until': None}


# Admin login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# User login required decorator
def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'GET':
        # Check if already logged in
        if 'admin_logged_in' in session:
            return redirect(url_for('admin_page'))
        return render_template('feedback/admin_login.html')
    
    # POST - handle login
    try:
        # Get client IP address
        ip_address = request.remote_addr or 'unknown'
        
        # Check if IP is locked out
        allowed, error_msg = check_login_attempts(ip_address)
        if not allowed:
            return jsonify({'success': False, 'error': error_msg}), 429  # Too Many Requests
        
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not username or not password:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        if len(username) > 50 or len(password) > 100:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 400
        
        # Check credentials
        if username in ADMIN_CREDENTIALS and check_password_hash(ADMIN_CREDENTIALS[username], password):
            # Successful login
            reset_login_attempts(ip_address)
            session['admin_logged_in'] = True
            session['admin_username'] = username
            logger.info(f"Admin login successful: {username} from {ip_address}")
            return jsonify({
                'success': True,
                'message': f'Welcome, {username}!',
                'redirect': url_for('admin_page')
            })
        else:
            # Failed login
            record_failed_login(ip_address)
            attempts_left = MAX_LOGIN_ATTEMPTS - login_attempts.get(ip_address, {}).get('count', 0)
            logger.warning(f"Failed login attempt for username: {username} from {ip_address} ({attempts_left} attempts remaining)")
            
            if attempts_left > 0:
                return jsonify({'success': False, 'error': f'Invalid username or password. {attempts_left} attempts remaining.'}), 401
            else:
                return jsonify({'success': False, 'error': f'Too many failed attempts. Account locked for {LOCKOUT_DURATION_MINUTES} minutes.'}), 429
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@app.route('/admin/logout')
def admin_logout():
    """Admin logout - redirect to login selection"""
    username = session.get('admin_username', 'Unknown')
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    logger.info(f"Admin logout: {username}")
    return redirect(url_for('index'))  # Goes back to login selection page


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """User login page"""
    if request.method == 'GET':
        # Check if already logged in
        if 'user_logged_in' in session:
            return redirect(url_for('user_portal'))
        return render_template('feedback/user_login.html')
    
    # POST - handle login
    try:
        # Get client IP address
        ip_address = request.remote_addr or 'unknown'
        
        # Check if IP is locked out
        allowed, error_msg = check_login_attempts(ip_address)
        if not allowed:
            return jsonify({'success': False, 'error': error_msg}), 429  # Too Many Requests
        
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not username or not password:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        if len(username) > 50 or len(password) > 100:
            record_failed_login(ip_address)
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 400
        
        # Check credentials
        if username in USER_CREDENTIALS and check_password_hash(USER_CREDENTIALS[username], password):
            # Successful login
            reset_login_attempts(ip_address)
            session['user_logged_in'] = True
            session['user_username'] = username
            logger.info(f"User login successful: {username} from {ip_address}")
            return jsonify({
                'success': True,
                'message': f'Welcome, {username}!',
                'redirect': url_for('user_portal')
            })
        else:
            # Failed login
            record_failed_login(ip_address)
            attempts_left = MAX_LOGIN_ATTEMPTS - login_attempts.get(ip_address, {}).get('count', 0)
            logger.warning(f"Failed user login attempt for username: {username} from {ip_address} ({attempts_left} attempts remaining)")
            
            if attempts_left > 0:
                return jsonify({'success': False, 'error': f'Invalid username or password. {attempts_left} attempts remaining.'}), 401
            else:
                return jsonify({'success': False, 'error': f'Too many failed attempts. Account locked for {LOCKOUT_DURATION_MINUTES} minutes.'}), 429
    
    except Exception as e:
        logger.error(f"User login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@app.route('/user/logout')
def user_logout():
    """User logout - redirect to login selection"""
    username = session.get('user_username', 'Unknown')
    session.pop('user_logged_in', None)
    session.pop('user_username', None)
    logger.info(f"User logout: {username}")
    return redirect(url_for('index'))  # Goes back to login selection page


@app.route('/')
def index():
    """Login selection page - Choose between User or Admin portal"""
    return render_template('feedback/login_select.html')


@app.route('/user')
@user_login_required
def user_portal():
    """User feedback interface page"""
    return render_template('feedback/feedback_main.html')


@app.route('/admin')
@login_required
def admin_page():
    """Admin upload portal"""
    return render_template('feedback/admin_upload.html')


def search_vectorstore_by_sr_id(sr_id: str) -> Optional[Dict]:
    """
    Search vector store for exact SR ID match (primary search method)
    
    Args:
        sr_id: SR ID to search for (case-insensitive)
    
    Returns:
        Dict with all SR metadata if found, None if not found
    """
    try:
        db_path = Path('vector store/clean_history_data.db')
        
        if not db_path.exists():
            logger.warning(f"Vector store not found at {db_path}")
            return None
        
        # Load vector store
        with open(db_path, 'rb') as f:
            db_data = pickle.load(f)
        
        metadata_list = db_data.get('metadata', [])
        sr_id_upper = sr_id.upper().strip()
        
        # Search by call_id (exact match)
        for metadata in metadata_list:
            call_id = str(metadata.get('call_id', '')).upper().strip()
            if call_id == sr_id_upper:
                logger.info(f"✅ Found SR {sr_id} in vector store")
                return metadata
        
        logger.info(f"📊 SR {sr_id} not found in vector store")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error searching vector store: {str(e)}")
        return None


def get_similar_srs_from_vectorstore(sr_metadata: Dict, top_k: int = 5) -> Dict[str, str]:
    """
    Get similar SRs from vector store and extract their AI workarounds
    
    Args:
        sr_metadata: Metadata of the current SR
        top_k: Number of similar SRs to retrieve
    
    Returns:
        Dict with 'ai_workarounds_list', 'semantic_workarounds_list', 'user_corrections_list'
    """
    try:
        db_path = Path('vector store/clean_history_data.db')
        
        if not db_path.exists():
            return {
                'ai_workarounds_list': 'No AI workarounds found',
                'semantic_workarounds_list': 'No semantic matches found',
                'user_corrections_list': 'No user corrections found'
            }
        
        # Load vector store
        with open(db_path, 'rb') as f:
            db_data = pickle.load(f)
        
        metadata_list = db_data.get('metadata', [])
        embeddings = db_data.get('embeddings')
        
        if embeddings is None or len(metadata_list) == 0:
            return {
                'ai_workarounds_list': 'No AI workarounds found',
                'semantic_workarounds_list': 'No semantic matches found',
                'user_corrections_list': 'No user corrections found'
            }
        
        # Get current SR's embedding (combine description and summary)
        current_description = sr_metadata.get('description', '')
        current_summary = sr_metadata.get('summary', '')
        current_text = f"{current_description} {current_summary}"
        current_call_id = sr_metadata.get('call_id', '').upper().strip()
        
        # Use sentence transformers to get embedding
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('models/sentence-transformers_all-MiniLM-L6-v2')
        current_embedding = model.encode([current_text])[0]
        
        # Calculate cosine similarity with all other SRs
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        similarities = cosine_similarity([current_embedding], embeddings)[0]
        
        # Get top_k similar SRs (excluding self)
        similar_indices = []
        for idx in np.argsort(similarities)[::-1]:
            if len(similar_indices) >= top_k:
                break
            # Exclude self
            other_call_id = str(metadata_list[idx].get('call_id', '')).upper().strip()
            if other_call_id != current_call_id:
                similar_indices.append(idx)
        
        # Helper function to validate values and filter out nan/NA
        def is_valid_value(val):
            if not val or pd.isna(val):
                return False
            val_str = str(val).strip().lower()
            return val_str not in ['nan', 'none', 'n/a', 'na', '']
        
        # Build formatted lists
        ai_workarounds_parts = []
        semantic_workarounds_parts = []
        user_corrections_parts = []
        
        for idx in similar_indices:
            similar_sr = metadata_list[idx]
            similarity_score = similarities[idx]
            similarity_pct = f"{similarity_score * 100:.1f}%"
            
            sr_id = similar_sr.get('call_id', 'Unknown')
            
            # Get all three types of workarounds
            workaround = similar_sr.get('workaround', '')
            ai_workaround = similar_sr.get('ai_generated_workaround', 'NA')
            user_correction = similar_sr.get('user_corrected_workaround', None)
            
            # Only include SR if at least one workaround exists
            if is_valid_value(workaround) or is_valid_value(ai_workaround) or is_valid_value(user_correction):
                # Get Resolution Categorization and SLA Resolution for each SR
                resolution_cat = similar_sr.get('resolution_categorization', 'Unknown')
                status_reason = similar_sr.get('status_reason', 'Unknown')
                
                # Build combined workaround entry with ALL three types
                combined_entry = (
                    f"SR ID: {sr_id}\n"
                    f"Similarity: {similarity_pct}\n"
                    f"Resolution Categorization: {resolution_cat}\n"
                    f"SLA Resolution: {status_reason}\n"
                )
                
                # Add Original Workaround if exists
                if is_valid_value(workaround):
                    combined_entry += f"Original Workaround: {workaround}\n"
                
                # Add AI Workaround if exists
                if is_valid_value(ai_workaround):
                    combined_entry += f"AI Workaround: {ai_workaround}\n"
                
                # Add User Correction if exists
                if is_valid_value(user_correction):
                    combined_entry += f"User Correction: {user_correction}\n"
                
                semantic_workarounds_parts.append(combined_entry)
            
            # Keep separate lists for backward compatibility (legacy sections)
            # AI Workaround
            if is_valid_value(ai_workaround):
                ai_workarounds_parts.append(
                    f"SR ID: {sr_id}\n"
                    f"Similarity: {similarity_pct}\n"
                    f"AI Workaround: {ai_workaround}\n"
                )
            
            # User Correction (from user_corrected_workaround field)
            if is_valid_value(user_correction):
                user_corrections_parts.append(
                    f"SR ID: {sr_id}\n"
                    f"Similarity: {similarity_pct}\n"
                    f"User Correction: {user_correction}\n"
                )
        
        # Combine results
        ai_workarounds_result = '\n\n'.join(ai_workarounds_parts) if ai_workarounds_parts else 'No AI workarounds found'
        semantic_workarounds_result = '\n\n'.join(semantic_workarounds_parts) if semantic_workarounds_parts else 'No semantic matches found'
        user_corrections_result = '\n\n'.join(user_corrections_parts) if user_corrections_parts else 'No user corrections found'
        
        logger.info(f"✅ Found {len(ai_workarounds_parts)} AI workarounds, {len(semantic_workarounds_parts)} semantic workarounds, {len(user_corrections_parts)} user corrections from similar SRs")
        
        return {
            'ai_workarounds_list': ai_workarounds_result,
            'semantic_workarounds_list': semantic_workarounds_result,
            'user_corrections_list': user_corrections_result
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting similar SRs from vector store: {str(e)}\n{traceback.format_exc()}")
        return {
            'ai_workarounds_list': 'No AI workarounds found',
            'semantic_workarounds_list': 'No semantic matches found',
            'user_corrections_list': 'No user corrections found'
        }


def search_latest_admin_upload_only(sr_id: str):
    """
    Search ONLY the latest Admin_Upload file (fallback method)
    
    Returns:
        Tuple of (sr_row, filename) or (None, None)
    """
    try:
        output_dir = 'output/reports'
        if not os.path.exists(output_dir):
            return None, None
        
        # Get ONLY the latest file
        files = [f for f in os.listdir(output_dir) 
                 if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
        
        if not files:
            return None, None
        
        files.sort(reverse=True)
        latest_file = files[0]
        filepath = os.path.join(output_dir, latest_file)
        
        # Read Excel
        df = pd.read_excel(filepath)
        
        # Find SR ID column
        sr_col = None
        for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
            if col in df.columns:
                sr_col = col
                break
        
        if not sr_col:
            return None, None
        
        # Search for SR
        sr_id_upper = sr_id.upper().strip()
        mask = df[sr_col].astype(str).str.upper().str.strip() == sr_id_upper
        
        if mask.any():
            logger.info(f"✅ Found SR {sr_id} in latest Excel: {latest_file}")
            return df[mask].iloc[0], latest_file
        
        return None, None
        
    except Exception as e:
        logger.error(f"❌ Error searching latest Excel: {str(e)}")
        return None, None


def load_latest_admin_upload():
    """Load the latest admin upload Excel for user review"""
    output_dir = 'output/reports'
    if not os.path.exists(output_dir):
        return None
    
    # Find latest Admin_Upload_*.xlsx file
    files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
    if not files:
        return None
    
    # Sort by timestamp (newest first)
    files.sort(reverse=True)
    latest_file = os.path.join(output_dir, files[0])
    
    return latest_file


@app.route('/get_upload_info', methods=['GET'])
def get_upload_info():
    """Get info about admin uploads"""
    try:
        output_dir = 'output/reports'
        
        if not os.path.exists(output_dir):
            return jsonify({
                'has_upload': False,
                'message': 'No data available. Please contact admin.'
            })
        
        # Get ALL Admin_Upload files
        files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
        
        if not files:
            return jsonify({
                'has_upload': False,
                'message': 'No data available. Please contact admin.'
            })
        
        # Sort and get latest
        files.sort(reverse=True)
        latest_file = os.path.join(output_dir, files[0])
        
        # Extract timestamp from latest filename
        filename = os.path.basename(latest_file)
        timestamp_str = filename.replace('Admin_Upload_', '').replace('.xlsx', '')
        
        # Parse timestamp
        try:
            dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            upload_date = dt.strftime('%B %d, %Y at %I:%M %p')
        except:
            upload_date = timestamp_str
        
        # Count SRs in latest file
        df = pd.read_excel(latest_file)
        sr_count = len(df)
        
        # 🆕 Show how many upload files are available
        total_uploads = len(files)
        
        return jsonify({
            'has_upload': True,
            'upload_date': upload_date,
            'sr_count': sr_count,
            'total_uploads': total_uploads,
            'message': f'{sr_count} Tickets in latest upload | Searching across 21k+ Tickets'
        })
    
    except Exception as e:
        logger.error(f"Error getting upload info: {str(e)}")
        return jsonify({
            'has_upload': False,
            'message': 'Error loading data'
        })


def search_sr_across_all_uploads(sr_id):
    """Search for SR across ALL admin upload files (newest to oldest)"""
    output_dir = 'output/reports'
    if not os.path.exists(output_dir):
        return None, None
    
    # Get all Admin_Upload files sorted by date (newest first)
    files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
    if not files:
        return None, None
    
    # Sort by filename (which contains timestamp)
    files.sort(reverse=True)
    
    sr_id_upper = sr_id.upper()
    
    # Search through each file
    for filename in files:
        filepath = os.path.join(output_dir, filename)
        
        try:
            # Read Excel
            df = pd.read_excel(filepath)
            
            # Try multiple column names for SR ID
            sr_col = None
            for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
                if col in df.columns:
                    sr_col = col
                    break
            
            if not sr_col:
                continue  # Skip this file if no SR column found
            
            # Search for SR
            mask = df[sr_col].astype(str).str.upper() == sr_id_upper
            
            if mask.any():
                # Found it!
                logger.info(f"✅ Found SR {sr_id} in {filename}")
                return df[mask].iloc[0], filename
                
        except Exception as e:
            logger.warning(f"Error reading {filename}: {e}")
            continue
    
    # Not found in any file
    return None, None


def search_rag_output_files(sr_id):
    """
    Search for SR in all RAG output Excel files in llm output folder
    Returns AI Workaround if found
    """
    llm_output_dir = 'RAG/llm output'
    if not os.path.exists(llm_output_dir):
        return None
    
    # Get all Excel files in llm output directory
    rag_files = [f for f in os.listdir(llm_output_dir) if f.endswith('.xlsx')]
    if not rag_files:
        return None
    
    # Sort by modification time (newest first)
    rag_files.sort(key=lambda f: os.path.getmtime(os.path.join(llm_output_dir, f)), reverse=True)
    
    sr_id_upper = sr_id.upper()
    
    # Search through each RAG output file
    for filename in rag_files:
        filepath = os.path.join(llm_output_dir, filename)
        
        try:
            df = pd.read_excel(filepath)
            
            # Try multiple column names for SR ID
            sr_col = None
            for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
                if col in df.columns:
                    sr_col = col
                    break
            
            if not sr_col:
                continue
            
            # Search for SR
            mask = df[sr_col].astype(str).str.upper() == sr_id_upper
            
            if mask.any():
                # Found it! Extract AI Workaround
                row = df[mask].iloc[0]
                ai_workaround = row.get('AI Workaround', row.get('AI Generated Workaround', None))
                
                if pd.notna(ai_workaround) and str(ai_workaround).strip() != '':
                    logger.info(f"✅ Found AI workaround for SR {sr_id} in {filename}")
                    return {
                        'ai_workaround': str(ai_workaround),
                        'source_file': filename,
                        'found': True
                    }
        
        except Exception as e:
            logger.warning(f"Error reading RAG file {filename}: {e}")
            continue
    
    # Not found in any RAG output file
    return None


@app.route('/search_sr', methods=['POST'])
def search_sr():
    """
    Search for SR - Vector Store first (primary), then Excel fallback (temporary)
    """
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        
        # Validation
        if not sr_id:
            return jsonify({'error': 'Please enter an SR ID'}), 400
        
        if len(sr_id) > 100:
            return jsonify({'error': 'SR ID too long. Please enter a valid SR ID (max 100 characters).'}), 400
        
        # Basic sanitization - remove dangerous characters
        if any(char in sr_id for char in ['<', '>', '"', "'", '\\', ';']):
            return jsonify({'error': 'SR ID contains invalid characters. Please use only alphanumeric characters, dashes, and underscores.'}), 400
        
        # STEP 1: Try Vector Store first (primary source)
        logger.info(f"🔍 Step 1: Searching vector store for SR {sr_id}...")
        sr_metadata = search_vectorstore_by_sr_id(sr_id)
        
        sr_dict = None
        source = None
        found_in_file = None
        
        if sr_metadata:
            # Found in vector store!
            sr_dict = sr_metadata
            source = 'vector_store'
            logger.info(f"✅ Found SR {sr_id} in vector store (primary source)")
        else:
            # STEP 2: Fallback to latest Excel (if still processing)
            logger.info(f"📊 Step 2: Not in vector store, checking latest Excel (fallback)...")
            sr_row, found_in_file = search_latest_admin_upload_only(sr_id)
            
            if sr_row is None:
                return jsonify({
                    'error': f'SR {sr_id} not found',
                    'suggestion': 'Please check the SR ID or wait for processing to complete'
                }), 404
            
            sr_dict = sr_row.to_dict()
            source = 'excel_temp'
            logger.info(f"✅ Found SR {sr_id} in latest Excel (temporary): {found_in_file}")
        
        # Check if user feedback exists for this SR
        existing_feedback = feedback_manager.get_feedback_by_sr_id(sr_id)
        
        # ✨ Intelligent Team Assignment from people_skills.db
        # Features: Persist to vectorstore, respect max_load, equal distribution
        existing_assignee = safe_get(sr_dict, ['Assigned Group*', 'Assignee Name', 'Assigned Group', 'Assigned To', 'ASSIGNED TO', 'assigned_to', 'Assignee'], None)
        
        # Check if existing assignment is a VALID PERSON NAME from people_skills.db
        has_valid_assignment = False
        if existing_assignee and str(existing_assignee).strip() not in ['', 'Not Assigned', 'NA', 'N/A', 'None', 'nan', 'null', 'Not Assigned - No available members', 'Not Assigned - Error', 'Not Assigned - All at max capacity']:
            # Verify it's a real person name, not a category like SOM_MM/BILLING_MM
            try:
                import sqlite3
                conn = sqlite3.connect('vector store/people_skills.db')
                cursor = conn.cursor()
                cursor.execute('SELECT name FROM team_members WHERE status = "active" AND name = ?', (str(existing_assignee).strip(),))
                result = cursor.fetchone()
                conn.close()
                if result:
                    has_valid_assignment = True
                else:
                    logger.warning(f"⚠️ Invalid assignee '{existing_assignee}' - not a team member, will re-assign")
            except Exception as e:
                logger.warning(f"⚠️ Could not verify assignee: {e}")
        
        if has_valid_assignment:
            # ✅ USE EXISTING ASSIGNMENT from vectorstore - don't change it
            assigned_to = str(existing_assignee).strip()
            logger.info(f"📌 Using existing assignment from vectorstore: {sr_id} → {assigned_to}")
            sr_dict['assigned_to'] = assigned_to
        else:
            # 🆕 NO VALID ASSIGNMENT - perform intelligent assignment with load balancing
            try:
                import sys
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'scripts', 'utilities'))
                from people_skills_database import PeopleSkillsDatabase
                import sqlite3
                from datetime import datetime, timedelta
                import json
                
                # Get SR details for assignment
                priority = safe_get(sr_dict, ['priority', 'Priority', 'Customer Priority'], 'P3')
                description = safe_get(sr_dict, ['Original Description', 'Description', 'description'], '')
                notes = safe_get(sr_dict, ['Original Notes/Summary', 'Notes', 'Additional Notes', 'summary'], '')
                application = safe_get(sr_dict, ['Application', 'App', 'application'], 'SOM_MM')
                java_failure = safe_get(sr_dict, ['Java Failure Detected', 'java_failure'], 'No')
                
                # Initialize database
                db = PeopleSkillsDatabase('vector store/people_skills.db')
                
                # Get members with current_load AND max_load (for capacity check)
                conn = sqlite3.connect('vector store/people_skills.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        tm.name,
                        s.application,
                        s.skill_level,
                        s.specializations,
                        s.max_load,
                        COALESCE(ah.availability_percent, 100) as availability,
                        (SELECT COUNT(*) FROM assignment_history ah2 
                         WHERE ah2.member_id = tm.id 
                         AND ah2.assigned_date >= datetime('now', '-7 days')) as current_load
                    FROM team_members tm
                    JOIN skills s ON tm.id = s.member_id
                    LEFT JOIN (
                        SELECT member_id, availability_percent
                        FROM availability_history
                        WHERE (end_date IS NULL OR end_date >= datetime('now'))
                        GROUP BY member_id
                        HAVING id = MAX(id)
                    ) ah ON tm.id = ah.member_id
                    WHERE tm.status = 'active' AND s.application = ?
                    ORDER BY s.skill_level DESC
                ''', (application,))
                
                candidates = cursor.fetchall()
                
                if not candidates:
                    # Fallback: get members from any application
                    logger.warning(f"⚠️ No members found for {application}, using all available members")
                    cursor.execute('''
                        SELECT 
                            tm.name,
                            s.application,
                            s.skill_level,
                            s.specializations,
                            s.max_load,
                            COALESCE(ah.availability_percent, 100) as availability,
                            (SELECT COUNT(*) FROM assignment_history ah2 
                             WHERE ah2.member_id = tm.id 
                             AND ah2.assigned_date >= datetime('now', '-7 days')) as current_load
                        FROM team_members tm
                        JOIN skills s ON tm.id = s.member_id
                        LEFT JOIN (
                            SELECT member_id, availability_percent
                            FROM availability_history
                            WHERE (end_date IS NULL OR end_date >= datetime('now'))
                            GROUP BY member_id
                            HAVING id = MAX(id)
                        ) ah ON tm.id = ah.member_id
                        WHERE tm.status = 'active'
                        GROUP BY tm.name
                        HAVING MAX(s.skill_level)
                        ORDER BY s.skill_level DESC
                    ''')
                    candidates = cursor.fetchall()
                
                conn.close()
                
                # Filter and score candidates
                scored_candidates = []
                
                for candidate in candidates:
                    name, app, skill_level, specializations_json, max_load, availability, current_load = candidate
                    
                    # ❌ Skip if unavailable
                    if availability <= 0:
                        continue
                    
                    # ❌ Skip if at max capacity (RESPECT max_load!)
                    if current_load >= max_load:
                        logger.debug(f"   Skipping {name}: at max capacity ({current_load}/{max_load})")
                        continue
                    
                    # Parse specializations
                    try:
                        specializations = json.loads(specializations_json) if specializations_json else []
                    except:
                        specializations = []
                    
                    # Calculate capacity remaining (for load balancing)
                    capacity_remaining = max_load - current_load
                    capacity_percent = capacity_remaining / max_load if max_load > 0 else 0
                    
                    # ===== SCORING ALGORITHM (Equal Distribution) =====
                    skill_score = float(skill_level)
                    availability_factor = float(availability) / 100.0
                    
                    # Load balancing: FAVOR those with more capacity remaining
                    # This ensures equal distribution (6, 6, 7 instead of 20, 0, 0)
                    load_balance_bonus = capacity_percent * 5.0
                    
                    # Priority bonus for experts on high-priority tickets
                    priority_bonus = 0
                    if priority in ['P0', 'P1', 'P2'] and skill_level >= 4.0:
                        priority_bonus = 2.0
                    
                    # Java failure bonus
                    java_bonus = 0
                    if java_failure == 'Yes' and any('java' in str(s).lower() for s in specializations):
                        java_bonus = 1.5
                    
                    # Specialization match bonus
                    spec_bonus = 0
                    description_lower = (description + ' ' + notes).lower()
                    for spec in specializations:
                        if str(spec).lower() in description_lower:
                            spec_bonus += 0.5
                    
                    # ===== TOTAL SCORE =====
                    total_score = (
                        skill_score * 2.0 +
                        load_balance_bonus +
                        priority_bonus +
                        java_bonus +
                        spec_bonus +
                        (availability_factor * 2.0)
                    )
                    
                    scored_candidates.append({
                        'name': name,
                        'score': total_score,
                        'skill_level': skill_level,
                        'current_load': current_load,
                        'max_load': max_load,
                        'capacity_remaining': capacity_remaining,
                        'availability': availability
                    })
                
                # Sort by score (highest first) - ensures equal distribution
                scored_candidates.sort(key=lambda x: x['score'], reverse=True)
                
                if scored_candidates:
                    best = scored_candidates[0]
                    assigned_to = best['name']
                    
                    logger.info(f"✅ Intelligent assignment: {sr_id} → {assigned_to}")
                    logger.info(f"   Priority: {priority}, Application: {application}")
                    logger.info(f"   Score: {best['score']:.2f} | Skill: {best['skill_level']} | "
                               f"Load: {best['current_load']}/{best['max_load']} | Avail: {best['availability']}%")
                    
                    # Record assignment in history (for future load balancing)
                    try:
                        assignment_data = {
                            'sr_id': sr_id,
                            'application': application,
                            'area': 'Auto-assigned',
                            'complexity_score': 0.5 if priority in ['P3', 'P4'] else 0.8,
                            'success_rate': 1.0,
                            'resolution_time_hours': 0,
                            'feedback_score': 0.8,
                            'keywords': []
                        }
                        db.record_assignment(assigned_to, assignment_data)
                        logger.info(f"   ✅ Recorded in assignment_history")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Could not record in history: {e}")
                    
                    # 💾 PERSIST TO VECTORSTORE - assignment won't change on reload
                    try:
                        from history_db_manager import HistoryDatabaseManager
                        hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
                        if hist_manager.load_database():
                            success = hist_manager.update_sr_from_admin(
                                sr_id=sr_id,
                                assigned_to=assigned_to,
                                preserve_user_feedback=True
                            )
                            if success:
                                logger.info(f"   💾 Saved to vectorstore (persistent)")
                            else:
                                logger.warning(f"   ⚠️ Could not save to vectorstore")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Vectorstore save error: {e}")
                else:
                    assigned_to = 'Not Assigned - All at max capacity'
                    logger.warning(f"⚠️ No available members (all at max capacity)")
                
                # Update sr_dict with assignment
                sr_dict['Assigned To'] = assigned_to
                sr_dict['assigned_to'] = assigned_to
                
            except Exception as e:
                logger.error(f"❌ Could not perform intelligent assignment: {e}")
                import traceback
                logger.error(traceback.format_exc())
                assigned_to = 'Not Assigned - Error'
                sr_dict['Assigned To'] = assigned_to
                sr_dict['assigned_to'] = assigned_to
        
        # Get workarounds based on source
        if source == 'vector_store':
            # From vector store - metadata has all fields
            semantic_workaround = safe_get(sr_dict, ['workaround', 'Suggested Workaround', 'Semantic Workaround'], 'NA')
            ai_workaround = safe_get(sr_dict, ['ai_generated_workaround', 'AI Workaround'], None)
            
            # 🔍 DEBUG: Log what we got from vectorstore
            logger.info(f"🔍 DEBUG - Vectorstore data for SR {sr_id}:")
            logger.info(f"   ai_generated_workaround raw value: {repr(ai_workaround)}")
            logger.info(f"   ai_generated_workaround type: {type(ai_workaround)}")
            logger.info(f"   ai_generated_workaround length: {len(str(ai_workaround)) if ai_workaround else 0}")
            
            # Better validation for AI workaround
            ai_workaround_available = (
                ai_workaround and 
                str(ai_workaround).strip() not in ['', 'NA', 'N/A', 'None', 'nan', 'null'] and
                len(str(ai_workaround).strip()) > 10  # At least 10 chars to be valid
            )
            
            logger.info(f"   ai_workaround_available: {ai_workaround_available}")
        else:
            # From Excel - use old column names
            semantic_workaround = safe_get(sr_dict, ['Suggested Workaround', 'Semantic Workaround', 'Workaround'], 'NA')
            # Search for AI workaround in RAG output files
            rag_result = search_rag_output_files(sr_id)
            ai_workaround = rag_result.get('ai_workaround') if rag_result and rag_result.get('found') else None
            ai_workaround_available = bool(ai_workaround) and len(str(ai_workaround).strip()) > 10
        
        # User-corrected workaround (if exists)
        # PRIORITY 1: Check vectorstore directly (updated via update_workaround)
        is_user_corrected = False
        user_corrected_workaround = None
        
        if source == 'vector_store':
            vectorstore_user_wa = sr_dict.get('user_corrected_workaround', '')
            
            # 🔍 DEBUG: Log what we got
            logger.info(f"🔍 DEBUG - User workaround from vectorstore:")
            logger.info(f"   user_corrected_workaround raw value: {repr(vectorstore_user_wa)}")
            logger.info(f"   user_corrected_workaround type: {type(vectorstore_user_wa)}")
            
            if vectorstore_user_wa and str(vectorstore_user_wa).strip() not in ['', 'NA', 'N/A', 'None', 'nan', 'null']:
                user_corrected_workaround = str(vectorstore_user_wa).strip()
                is_user_corrected = True
                logger.info(f"✅ Found user-corrected workaround in VECTORSTORE for SR {sr_id}")
        
        # PRIORITY 2: Fallback to feedback_manager (for legacy entries with source='user_feedback')
        if not is_user_corrected and existing_feedback and existing_feedback.get('user_corrected_workaround'):
            feedback_user_wa = existing_feedback.get('user_corrected_workaround', '')
            if feedback_user_wa and str(feedback_user_wa).strip() not in ['', 'NA', 'N/A', 'None', 'nan', 'null']:
                user_corrected_workaround = str(feedback_user_wa).strip()
                is_user_corrected = True
                logger.info(f"✅ Found user-corrected workaround in FEEDBACK_MANAGER for SR {sr_id}")
        
        # Get interface (with user correction if exists)
        ai_interface = safe_get(sr_dict, ['Interface', 'function_category'], 'Unknown')
        is_interface_corrected = False
        interface_to_display = ai_interface
        
        if existing_feedback and existing_feedback.get('user_corrected_interface'):
            interface_to_display = existing_feedback['user_corrected_interface']
            is_interface_corrected = True
        
        # Get additional fields based on source
        if source == 'vector_store':
            # 🆕 Get similar SRs from vector store
            similar_srs_data = get_similar_srs_from_vectorstore(sr_dict, top_k=5)
            semantic_workarounds_list = similar_srs_data['semantic_workarounds_list']
            ai_workarounds_list = similar_srs_data['ai_workarounds_list']
            user_corrections_list = similar_srs_data['user_corrections_list']
            
            # 🆕 TWO SEPARATE categorization fields - Use full concatenated strings
            # These fields already contain the full concatenated path from all similar SRs
            # Example: "Interface > Interface | Service Request > User Service Request | TBD > Customer Info"
            resolution_categorization_display = sr_dict.get('resolution_categorization', '')
            sla_resolution_display = sr_dict.get('sla_resolution_categorization_t1', '')
            
            # Clean up empty/invalid values
            if not resolution_categorization_display or str(resolution_categorization_display).strip() in ['', 'nan', 'None', 'N/A']:
                resolution_categorization_display = 'N/A'
            else:
                resolution_categorization_display = str(resolution_categorization_display).strip()
                
            if not sla_resolution_display or str(sla_resolution_display).strip() in ['', 'nan', 'None', 'N/A']:
                sla_resolution_display = 'N/A'
            else:
                sla_resolution_display = str(sla_resolution_display).strip()
            
            # Debug logging for categorization fields
            logger.info(f"🔍 Vector Store categorization fields for SR {sr_id}:")
            logger.info(f"   resolution_categorization (full concatenated string): {resolution_categorization_display}")
            logger.info(f"   sla_resolution_categorization_t1 (full concatenated string): {sla_resolution_display}")
        else:
            semantic_workarounds_list = safe_get(sr_dict, ['Semantic Workarounds'], 'No semantic matches found')
            ai_workarounds_list = safe_get(sr_dict, ['Previous AI Workarounds (Similar SRs)'], 'No AI workarounds found')
            user_corrections_list = safe_get(sr_dict, ['User Corrections (Similar SRs)'], 'No user corrections found')
            # 🆕 TWO SEPARATE categorization fields
            resolution_categorization_display = safe_get(sr_dict, ['Resolution Categorization'], 'N/A')
            sla_resolution_display = safe_get(sr_dict, ['SLA Resolution', 'SLA Resolution Categorization T1'], 'N/A')
            # Debug logging
            logger.info(f"🔍 Excel fields for SR {sr_id}:")
            logger.info(f"   Resolution Categorization: {sr_dict.get('Resolution Categorization', 'MISSING')}")
            logger.info(f"   SLA Resolution: {sr_dict.get('SLA Resolution', 'MISSING')}")
            logger.info(f"   SLA Resolution Categorization T1: {sr_dict.get('SLA Resolution Categorization T1', 'MISSING')}")
            logger.info(f"   Final resolution_categorization_display: {resolution_categorization_display}")
            logger.info(f"   Final sla_resolution_display: {sla_resolution_display}")
        
        # Extract upload date from filename or source
        upload_date_str = 'Unknown'
        if source == 'vector_store':
            upload_date_str = 'Historical Data (Vector Store)'
        elif found_in_file:
            try:
                timestamp_part = found_in_file.replace('Admin_Upload_', '').replace('.xlsx', '')
                upload_datetime = datetime.strptime(timestamp_part, '%Y%m%d_%H%M%S')
                upload_date_str = upload_datetime.strftime('%B %d, %Y at %I:%M %p') + ' (Processing)'
            except:
                upload_date_str = f'{found_in_file} (Processing)'
        
        response = {
            'success': True,
            'sr_id': sr_id,
            'source': source,  # 'vector_store' or 'excel_temp'
            'description': safe_get(sr_dict, ['Original Description', 'Description', 'description'], ''),
            'notes': safe_get(sr_dict, ['Original Notes/Summary', 'Notes', 'Additional Notes', 'summary'], ''),
            'priority': safe_get(sr_dict, ['priority', 'Priority', 'Customer Priority'], 'P3'),
            'assigned_to': sr_dict.get('assigned_to', 'Not Assigned'),  # Use intelligent assignment from people_skills.db
            
            # Workarounds
            'semantic_workaround': semantic_workaround,
            'ai_workaround': ai_workaround,
            'ai_workaround_available': ai_workaround_available,
            
            # Keep old field for backward compatibility
            'workaround': semantic_workaround,
            
            'corrected_workaround': user_corrected_workaround,
            'is_user_corrected': is_user_corrected,
            
            'interface': interface_to_display,
            'is_interface_corrected': is_interface_corrected,
            'classification': safe_get(sr_dict, ['Classification'], 'Unknown'),
            'confidence': safe_get(sr_dict, ['Confidence'], '0%'),
            'java_failure': safe_get(sr_dict, ['Java Failure Detected'], 'No'),
            'troubleshooting': safe_get(sr_dict, ['Troubleshooting Steps'], 'NA'),
            'expected_path': safe_get(sr_dict, ['Expected Path'], 'NA'),
            'has_feedback': existing_feedback is not None,
            'feedback_data': existing_feedback if existing_feedback else None,
            'found_in_upload': upload_date_str,
            
            # Semantic workarounds and categories
            'semantic_workarounds_list': semantic_workarounds_list,
            'ai_workarounds_list': ai_workarounds_list,
            'user_corrections_list': user_corrections_list,
            # 🆕 TWO SEPARATE categorization fields
            'resolution_categorization_display': resolution_categorization_display,
            'sla_resolution_display': sla_resolution_display,
            # Keep old fields for backward compatibility (deprecated)
            'categorization_display': resolution_categorization_display,
            'resolution_categories': resolution_categorization_display,
            'status_reasons': sla_resolution_display
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"❌ Search error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle Excel file upload - DEPRECATED, kept for compatibility"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Only Excel files (.xlsx, .xls) are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)
        
        logger.info(f"📁 File uploaded: {saved_filename}")
        
        # Read Excel file
        df = pd.read_excel(filepath)
        
        # Standardize column names
        column_mapping = {
            'Call ID': ['SR ID', 'Service Request ID', 'ID', 'Inc Call ID'],
            'Description': ['Issue Description', 'Problem Description', 'Details', 'Inc Description'],
            'Customer Priority': ['Priority', 'UTS Priority'],
            'STATUS': ['Status', 'Inc Current EIR - Status'],
            'Notes': ['Additional Notes', 'Resolution', 'Inc Resolution'],
            'Categorization Tier 3': ['Category', 'Categorization'],
            'Assigned Group': ['Application', 'Assignee Support Group', 'Owner Support Group'],
            'Submit Date': ['Created Date', 'Inc Created Date']
        }
        
        for standard_col, alternatives in column_mapping.items():
            if standard_col not in df.columns:
                for alt_col in alternatives:
                    if alt_col in df.columns:
                        df.rename(columns={alt_col: standard_col}, inplace=True)
                        break
        
        # Store in session
        session_data['uploaded_file'] = filepath
        session_data['original_df'] = df
        
        # Extract SR list for display
        sr_list = []
        for idx, row in df.iterrows():
            sr_list.append({
                'index': idx,
                'sr_id': str(row.get('Call ID', row.get('SR ID', f'Unknown_{idx}'))),
                'description': str(row.get('Description', 'No description'))[:200] + '...',
                'priority': str(row.get('Customer Priority', row.get('Priority', 'P3'))),
                'assigned_to': str(row.get('Assigned Group*', row.get('Assignee Name', row.get('Assigned Group', row.get('Assigned To', row.get('ASSIGNED TO', row.get('assigned_to', row.get('Assignee', 'Not Assigned'))))))))
            })
        
        return jsonify({
            'success': True,
            'message': f'Uploaded {len(sr_list)} SRs',
            'sr_count': len(sr_list),
            'sr_list': sr_list
        })
    
    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze_sr/<int:sr_index>', methods=['GET'])
def analyze_sr(sr_index):
    """Analyze a specific SR and return the workaround"""
    try:
        if session_data['original_df'] is None:
            return jsonify({'error': 'No file uploaded'}), 400
        
        df = session_data['original_df']
        if sr_index >= len(df):
            return jsonify({'error': 'Invalid SR index'}), 400
        
        # Get SR data
        sr_row = df.iloc[sr_index]
        sr_dict = sr_row.to_dict()
        
        logger.info(f"🔍 Analyzing SR at index {sr_index}")
        
        # Analyze the SR
        results = analyzer.analyze_sr_batch([sr_dict])
        
        if not results:
            return jsonify({'error': 'Analysis failed'}), 500
        
        result = results[0]
        
        # Check if user feedback exists for this SR
        sr_id = result.get('SR ID', 'Unknown')
        existing_feedback = feedback_manager.get_feedback_by_sr_id(sr_id)
        
        # Prioritize user-corrected workaround if it exists
        workaround_to_display = result.get('Suggested Workaround', 'NA')
        is_user_corrected = False
        
        if existing_feedback and existing_feedback.get('user_corrected_workaround'):
            workaround_to_display = existing_feedback['user_corrected_workaround']
            is_user_corrected = True
            logger.info(f"✅ Using user-corrected workaround for SR {sr_id}")
        
        # ✨ Intelligent Team Assignment from people_skills.db
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'scripts', 'utilities'))
            from people_skills_database import PeopleSkillsDatabase
            import sqlite3
            
            priority = result.get('Priority', result.get('Customer Priority', 'P3'))
            application = result.get('Application', result.get('App', 'SOM_MM'))
            
            # Get best available member for this application
            conn = sqlite3.connect('vector store/people_skills.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT tm.name, s.skill_level
                FROM team_members tm
                JOIN skills s ON tm.id = s.member_id
                LEFT JOIN (
                    SELECT member_id, availability_percent
                    FROM availability_history
                    WHERE (end_date IS NULL OR end_date >= datetime('now'))
                    GROUP BY member_id HAVING id = MAX(id)
                ) ah ON tm.id = ah.member_id
                WHERE tm.status = 'active' AND s.application = ?
                    AND COALESCE(ah.availability_percent, 100) > 0
                ORDER BY s.skill_level DESC
                LIMIT 1
            ''', (application,))
            
            best_match = cursor.fetchone()
            conn.close()
            
            if best_match:
                assigned_to = best_match[0]
                logger.info(f"✅ Intelligent assignment: {sr_id} → {assigned_to}")
            else:
                assigned_to = 'Not Assigned'
        except Exception as e:
            logger.warning(f"⚠️ Assignment error: {e}")
            assigned_to = 'Not Assigned'
        
        response = {
            'sr_id': sr_id,
            'description': result.get('Original Description', ''),
            'notes': result.get('Original Notes/Summary', result.get('Notes', result.get('Additional Notes', ''))),
            'priority': result.get('Priority', result.get('Customer Priority', 'P3')),
            'assigned_to': assigned_to,  # Use intelligent assignment from people_skills.db
            'workaround': workaround_to_display,  # Use user-corrected if available
            'is_user_corrected': is_user_corrected,  # Flag to show in UI
            'interface': result.get('Interface', 'Unknown'),
            'classification': result.get('Classification', 'Unknown'),
            'confidence': result.get('Confidence', '0%'),
            'java_failure': result.get('Java Failure Detected', 'No'),
            'troubleshooting': result.get('Troubleshooting Steps', 'NA'),
            'expected_path': result.get('Expected Path', 'NA'),
            'has_feedback': existing_feedback is not None,
            'feedback_data': existing_feedback if existing_feedback else None
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"❌ Analysis error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for a workaround"""
    try:
        data = request.json
        
        sr_id = data.get('sr_id', '').strip()
        is_satisfied = data.get('is_satisfied', False)
        corrected_workaround = data.get('corrected_workaround', '').strip()
        corrected_by = data.get('corrected_by', 'user').strip()
        
        # Validation: SR ID
        if not sr_id:
            return jsonify({'error': 'SR ID is required'}), 400
        
        if len(sr_id) > 100:
            return jsonify({'error': 'SR ID too long (max 100 characters)'}), 400
        
        if is_satisfied:
            # User is satisfied - just log it
            logger.info(f"✅ User satisfied with workaround for SR {sr_id}")
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
        else:
            # User provided correction
            # Validation: Workaround (after stripping whitespace)
            if not corrected_workaround:
                return jsonify({'error': 'Corrected workaround is required. Please provide a valid workaround.'}), 400
            
            if len(corrected_workaround) < 10:
                return jsonify({'error': 'Corrected workaround too short. Please provide at least 10 characters.'}), 400
            
            if len(corrected_workaround) > 5000:
                return jsonify({'error': 'Corrected workaround too long (max 5000 characters)'}), 400
            
            # Get original data
            original_description = data.get('original_description', '')
            original_notes = data.get('original_notes', '')
            original_workaround = data.get('original_workaround', '')
            
            # Add to feedback manager
            success = feedback_manager.add_feedback(
                sr_id=sr_id,
                original_description=original_description,
                original_notes=original_notes,
                original_workaround=original_workaround,
                user_corrected_workaround=corrected_workaround,
                corrected_by=corrected_by
            )
            
            if success:
                logger.info(f"✅ Feedback added for SR {sr_id}")
                
                # 🆕 UPDATE HISTORY_DATA.DB WITH USER CORRECTION
                try:
                    from history_db_manager import HistoryDatabaseManager
                    
                    hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
                    if hist_manager.load_database():
                        # Update the workaround in history database
                        hist_manager.update_workaround(sr_id, corrected_workaround)
                        logger.info(f"✅ Updated clean_history_data.db with user correction for {sr_id}")
                    else:
                        logger.warning("⚠️ Could not load clean_history_data.db for update")
                except Exception as hist_error:
                    logger.error(f"⚠️ Could not update clean_history_data.db: {str(hist_error)}")
                    # Don't fail the whole operation if historical update fails
                
                # Update the Excel file with corrected workaround
                if session_data['original_df'] is not None:
                    df = session_data['original_df']
                    
                    # Find SR ID column (flexible naming)
                    sr_col = None
                    for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
                        if col in df.columns:
                            sr_col = col
                            break
                    
                    if sr_col:
                        sr_mask = df[sr_col].astype(str) == str(sr_id)
                        if sr_mask.any():
                            # Add a new column for user-corrected workaround
                            if 'User Corrected Workaround' not in df.columns:
                                df['User Corrected Workaround'] = ''
                            df.loc[sr_mask, 'User Corrected Workaround'] = corrected_workaround
                            session_data['original_df'] = df
                            logger.info(f"✅ Updated Excel with user correction for SR {sr_id}")
                
                return jsonify({
                    'success': True,
                    'message': 'Feedback saved successfully! The historical database has been updated and similar SRs will now use your correction.'
                })
            else:
                return jsonify({'error': 'Failed to save feedback'}), 500
    
    except Exception as e:
        logger.error(f"❌ Feedback submission error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/download_corrected', methods=['GET'])
def download_corrected():
    """Download the Excel file with user corrections"""
    try:
        if session_data['original_df'] is None:
            return jsonify({'error': 'No file to download'}), 400
        
        df = session_data['original_df']
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"SR_Analysis_With_Feedback_{timestamp}.xlsx"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Save to Excel
        df.to_excel(output_path, index=False)
        
        logger.info(f"📥 Downloading corrected file: {output_filename}")
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"❌ Download error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/feedback_stats', methods=['GET'])
def feedback_stats():
    """Get feedback statistics"""
    try:
        stats = feedback_manager.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"❌ Stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/submit_interface_correction', methods=['POST'])
def submit_interface_correction():
    """Submit user correction for interface field"""
    try:
        data = request.json
        
        sr_id = data.get('sr_id', '').strip()
        corrected_interface = data.get('corrected_interface', '').strip()
        original_interface = data.get('original_interface', '').strip()
        original_description = data.get('original_description', '')
        original_notes = data.get('original_notes', '')
        corrected_by = data.get('corrected_by', 'user').strip()
        
        # Validation: SR ID
        if not sr_id:
            return jsonify({'error': 'SR ID is required'}), 400
        
        if len(sr_id) > 100:
            return jsonify({'error': 'SR ID too long'}), 400
        
        # Validation: Interface
        if not corrected_interface:
            return jsonify({'error': 'Corrected interface is required. Please enter a valid interface.'}), 400
        
        if len(corrected_interface) < 2:
            return jsonify({'error': 'Interface too short. Please provide at least 2 characters.'}), 400
        
        if len(corrected_interface) > 200:
            return jsonify({'error': 'Interface too long (max 200 characters)'}), 400
        
        # Check if actually changed (case-insensitive comparison)
        if corrected_interface.upper() == original_interface.upper():
            return jsonify({'error': 'Interface is the same, no changes needed'}), 400
        
        # Add to feedback manager (will merge with existing feedback if present)
        success = feedback_manager.add_feedback(
            sr_id=sr_id,
            original_description=original_description,
            original_notes=original_notes,
            original_workaround='',  # Not updating workaround, just interface
            user_corrected_workaround='',  # Keep existing if present
            user_corrected_interface=corrected_interface,
            corrected_by=corrected_by
        )
        
        if success:
            logger.info(f"Interface correction added for SR {sr_id}: {original_interface} -> {corrected_interface}")
            
            # 🆕 UPDATE HISTORY_DATA.DB WITH INTERFACE CORRECTION
            try:
                from history_db_manager import HistoryDatabaseManager
                
                hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
                if hist_manager.load_database() and hist_manager.db_data:
                    # Find and update the SR entry
                    metadata_list = hist_manager.db_data.get('metadata', [])
                    for metadata in metadata_list:
                        if metadata.get('call_id') == sr_id:
                            # Update interface field
                            metadata['interface'] = corrected_interface
                            logger.info(f"✅ Updated clean_history_data.db interface for {sr_id}")
                            hist_manager.save_database()
                            break
                else:
                    logger.warning("⚠️ Could not load clean_history_data.db for interface update")
            except Exception as hist_error:
                logger.error(f"⚠️ Could not update clean_history_data.db: {str(hist_error)}")
                # Don't fail the whole operation if historical update fails
            
            return jsonify({
                'success': True,
                'message': f'Interface correction saved! Changed from "{original_interface}" to "{corrected_interface}". The historical database has been updated.'
            })
        else:
            return jsonify({'error': 'Failed to save interface correction'}), 500
    
    except Exception as e:
        logger.error(f"Interface correction error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


# Global dictionary to store upload progress
upload_progress = {}

@app.route('/admin/upload_and_process', methods=['POST'])
@login_required
def admin_upload_and_process():
    """Handle admin Excel upload and save file - returns upload_id for streaming"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file extension
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'success': False, 'error': 'Only Excel files (.xlsx, .xls) are allowed'}), 400
        
        # Check file content type
        if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                                     'application/vnd.ms-excel', 
                                     'application/octet-stream']:
            logger.warning(f"Suspicious file upload attempt: {file.content_type}")
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload a valid Excel file.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        if not filename:  # secure_filename might return empty string for malicious filenames
            return jsonify({'success': False, 'error': 'Invalid filename'}), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        
        # Save file
        file.save(filepath)
        
        # Check if file is empty or too small (minimum 100 bytes for a valid Excel)
        file_size = os.path.getsize(filepath)
        if file_size < 100:
            os.remove(filepath)  # Clean up
            return jsonify({'success': False, 'error': 'File is empty or corrupted. Please upload a valid Excel file.'}), 400
        
        if file_size > 50 * 1024 * 1024:  # Additional server-side check
            os.remove(filepath)
            return jsonify({'success': False, 'error': 'File too large (max 50MB)'}), 400
        
        logger.info(f"Admin uploaded file: {saved_filename} ({file_size} bytes)")
        
        # Validate that it's actually a readable Excel file
        try:
            test_df = pd.read_excel(filepath, nrows=1)  # Try to read just first row
            if test_df.empty:
                os.remove(filepath)
                return jsonify({'success': False, 'error': 'Excel file is empty (no data rows)'}), 400
        except Exception as e:
            os.remove(filepath)
            logger.error(f"Invalid Excel file: {str(e)}")
            return jsonify({'success': False, 'error': f'Invalid or corrupted Excel file: {str(e)}'}), 400
        
        # Generate upload_id for tracking
        upload_id = timestamp
        
        # Return immediately with upload_id - processing will happen via SSE
        return jsonify({
            'success': True,
            'upload_id': upload_id,
            'filepath': filepath,
            'message': 'File uploaded successfully. Starting processing...'
        })
    
    except Exception as e:
        logger.error(f"Admin upload error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/process_stream/<upload_id>/<path:filepath>')
@login_required
def admin_process_stream(upload_id, filepath):
    """Stream processing progress using Server-Sent Events"""
    from flask import Response, stream_with_context
    import json
    
    def generate():
        """Generator function that yields progress updates"""
        try:
            # Progress callback that yields SSE events
            progress_queue = []
            
            def progress_callback(percent, message):
                data = {
                    'percent': percent if percent is not None else 0,
                    'message': message
                }
                progress_queue.append(f"data: {json.dumps(data)}\n\n")
            
            # Import and run upload_and_merge with callback
            import sys
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from admin_upload_and_merge_with_rag import upload_and_merge_with_rag
            
            # We need to run this in a way that yields progress
            # Use a custom approach - modify upload_and_merge to be a generator
            # For now, let's use a different approach with threading
            import threading
            import time
            
            result = {'success': False}
            
            def run_processing():
                result['success'] = upload_and_merge_with_rag(filepath, progress_callback=progress_callback)
            
            # Start processing in background thread
            thread = threading.Thread(target=run_processing)
            thread.start()
            
            # Yield progress updates as they come in
            last_keepalive = time.time()
            keepalive_interval = 2  # Send keepalive every 2 seconds
            
            while thread.is_alive() or progress_queue:
                if progress_queue:
                    # Pop and yield all available messages
                    while progress_queue:
                        message = progress_queue.pop(0)
                        yield message
                        sys.stdout.flush()  # Force immediate flush
                    last_keepalive = time.time()  # Reset keepalive timer on real message
                else:
                    # Send keepalive comment to prevent timeout
                    current_time = time.time()
                    if current_time - last_keepalive >= keepalive_interval:
                        yield ": keepalive\n\n"  # SSE comment (keeps connection alive)
                        sys.stdout.flush()
                        last_keepalive = current_time
                    time.sleep(0.05)  # Reduced delay for faster response
            
            # Wait for thread to complete
            thread.join()
            success = result['success']
            
            if success:
                # Get final stats from clean_history_data.db
                from history_db_manager import HistoryDatabaseManager
                hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
                if hist_manager.load_database() and hist_manager.db_data:
                    total_historical = len(hist_manager.db_data.get('metadata', []))
                else:
                    total_historical = 0
                
                # Find the latest Admin_Upload file
                output_dir = app.config['OUTPUT_FOLDER']
                admin_files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
                admin_files.sort(reverse=True)
                latest_file = admin_files[0] if admin_files else 'Unknown'
                
                # Read SR count from original file
                df = pd.read_excel(filepath)
                analyzed_count = len(df)
                
                # Send final success message
                final_data = {
                    'percent': 100,
                    'message': '[SUCCESS] Processing complete!',
                    'complete': True,
                    'success': True,
                    'analyzed_count': analyzed_count,
                    'total_historical': total_historical,
                    'output_file': latest_file
                }
                yield f"data: {json.dumps(final_data)}\n\n"
            else:
                # Send error message
                error_data = {
                    'percent': 0,
                    'message': '[ERROR] Processing failed',
                    'complete': True,
                    'success': False
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        except Exception as e:
            logger.error(f"Stream processing error: {str(e)}\n{traceback.format_exc()}")
            error_data = {
                'percent': 0,
                'message': f'[ERROR] {str(e)}',
                'complete': True,
                'success': False
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    response = Response(stream_with_context(generate()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx (if used)
    return response


@app.route('/admin/stats')
@login_required
def admin_stats():
    """Get admin statistics"""
    try:
        from history_db_manager import HistoryDatabaseManager
        
        # Get historical count from clean_history_data.db
        total_historical = 0
        try:
            hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
            if hist_manager.load_database() and hist_manager.db_data:
                total_historical = len(hist_manager.db_data.get('metadata', []))
        except (ImportError, ModuleNotFoundError, Exception) as e:
            # clean_history_data.db not available - count from Admin_Upload files
            logger.warning(f"Cannot load clean_history_data.db: {str(e)}")
            # Count actual unique SRs from all Admin_Upload files
            output_dir = app.config['OUTPUT_FOLDER']
            if os.path.exists(output_dir):
                admin_files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
                unique_sr_ids = set()
                for admin_file in admin_files:
                    try:
                        file_path = os.path.join(output_dir, admin_file)
                        df = pd.read_excel(file_path)
                        # Find SR ID column
                        sr_col = None
                        for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
                            if col in df.columns:
                                sr_col = col
                                break
                        if sr_col:
                            sr_ids = df[sr_col].dropna().astype(str).unique()
                            unique_sr_ids.update(sr_ids)
                    except Exception as file_error:
                        logger.warning(f"Could not read {admin_file}: {str(file_error)}")
                        continue
                total_historical = len(unique_sr_ids)
                logger.info(f"Counted {total_historical} unique SRs from {len(admin_files)} Admin_Upload files")
        
        # Get last upload date from Admin_Upload files
        output_dir = app.config['OUTPUT_FOLDER']
        last_upload_date = '-'
        if os.path.exists(output_dir):
            admin_files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
            if admin_files:
                admin_files.sort(reverse=True)
                latest_file = admin_files[0]
                # Extract timestamp from filename (Admin_Upload_20241114_105058.xlsx)
                timestamp_str = latest_file.replace('Admin_Upload_', '').replace('.xlsx', '')
                try:
                    dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    last_upload_date = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    last_upload_date = timestamp_str
        
        # Get user feedback count
        total_feedback = feedback_manager.total_feedback_count
        
        return jsonify({
            'success': True,
            'total_historical': total_historical,
            'last_upload_date': last_upload_date,
            'total_feedback': total_feedback
        })
    
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/get_people', methods=['GET'])
@login_required
def admin_get_people():
    """Get all people with their availability status"""
    try:
        # Import the people skills database
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'scripts', 'utilities'))
        from people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase('vector store/people_skills.db')
        members = db.get_all_members_availability()
        
        return jsonify({
            'success': True,
            'people': members
        })
    
    except Exception as e:
        logger.error(f"Error getting people: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/set_availability', methods=['POST'])
@login_required
def admin_set_availability():
    """Set availability for a team member"""
    try:
        data = request.json
        
        member_name = data.get('member_name', '').strip()
        availability_percent = data.get('availability_percent', 100)
        availability_type = data.get('availability_type', 'full_day')
        reason = data.get('reason', '').strip()
        end_date = data.get('end_date', None)
        
        # Validation
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        if not isinstance(availability_percent, int) or availability_percent < 0 or availability_percent > 100:
            return jsonify({'success': False, 'error': 'Availability must be between 0 and 100'}), 400
        
        # Import the people skills database
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'scripts', 'utilities'))
        from people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase('vector store/people_skills.db')
        
        admin_username = session.get('admin_username', 'admin')
        success = db.set_member_availability(
            member_name=member_name,
            availability_percent=availability_percent,
            availability_type=availability_type,
            reason=reason,
            end_date=end_date,
            updated_by=admin_username
        )
        
        if success:
            logger.info(f"Admin {admin_username} set availability for {member_name}: {availability_percent}%")
            return jsonify({
                'success': True,
                'message': f'Availability set for {member_name}: {availability_percent}%'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to set availability'
            }), 500
    
    except Exception as e:
        logger.error(f"Error setting availability: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/get_member_skills', methods=['GET'])
@login_required
def get_member_skills():
    """Get skills for a specific team member"""
    try:
        member_name = request.args.get('member_name')
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name required'}), 400
        
        import sqlite3
        import json
        conn = sqlite3.connect('vector store/people_skills.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.application, s.skill_level, s.specializations, s.max_load
            FROM skills s
            JOIN team_members tm ON s.member_id = tm.id
            WHERE tm.name = ? AND tm.status = 'active'
            ORDER BY s.skill_level DESC
        ''', (member_name,))
        
        skills = []
        for row in cursor.fetchall():
            specializations = json.loads(row[2]) if row[2] else []
            skills.append({
                'application': row[0],
                'skill_level': row[1],
                'specializations': specializations,
                'max_load': row[3]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'skills': skills
        })
        
    except Exception as e:
        logger.error(f"Error getting member skills: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/save_skill', methods=['POST'])
@login_required
def save_skill():
    """Add or update a skill for a team member"""
    try:
        data = request.json
        member_name = data.get('member_name')
        application = data.get('application')
        skill_level = float(data.get('skill_level', 3.0))
        specializations = data.get('specializations', [])
        max_load = int(data.get('max_load', 10))
        
        if not member_name or not application:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        import sqlite3
        import json
        conn = sqlite3.connect('vector store/people_skills.db')
        cursor = conn.cursor()
        
        # Get member ID
        cursor.execute('SELECT id FROM team_members WHERE name = ? AND status = "active"', (member_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        
        member_id = result[0]
        spec_json = json.dumps(specializations)
        
        # Insert or update skill
        cursor.execute('''
            INSERT OR REPLACE INTO skills 
            (member_id, application, skill_level, specializations, max_load, confidence_score, last_updated)
            VALUES (?, ?, ?, ?, ?, 0.8, CURRENT_TIMESTAMP)
        ''', (member_id, application, skill_level, spec_json, max_load))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved skill for {member_name}: {application} (Level {skill_level})")
        return jsonify({
            'success': True,
            'message': f'Skill saved: {member_name} - {application} (Level {skill_level})'
        })
        
    except Exception as e:
        logger.error(f"Error saving skill: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/remove_skill', methods=['POST'])
@login_required
def remove_skill():
    """Remove a skill from a team member"""
    try:
        data = request.json
        member_name = data.get('member_name')
        application = data.get('application')
        
        if not member_name or not application:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        import sqlite3
        conn = sqlite3.connect('vector store/people_skills.db')
        cursor = conn.cursor()
        
        # Delete skill
        cursor.execute('''
            DELETE FROM skills 
            WHERE member_id = (SELECT id FROM team_members WHERE name = ?)
            AND application = ?
        ''', (member_name, application))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Removed skill: {member_name} - {application}")
        return jsonify({
            'success': True,
            'message': f'Removed {application} skill for {member_name}'
        })
        
    except Exception as e:
        logger.error(f"Error removing skill: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/regenerate_ai_workaround', methods=['POST'])
@user_login_required
def regenerate_ai_workaround():
    """
    Regenerate AI workaround for a specific SR using single SR RAG pipeline
    This button is shown when user is not satisfied with current AI workaround
    """
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        sr_description = data.get('description', '')
        sr_notes = data.get('notes', '')
        
        if not sr_id:
            return jsonify({'error': 'SR ID is required'}), 400
        
        logger.info(f"🔄 Regenerating AI workaround for SR {sr_id}")
        
        # Import single SR RAG pipeline
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG', 'rag'))
        
        try:
            # Try Ollama version first
            from single_sr_rag_pipeline_ollama import SingleSRAnalysisPipeline
            logger.info("Using Ollama pipeline for regeneration")
            
            # Initialize pipeline (components load automatically in __init__)
            pipeline = SingleSRAnalysisPipeline()
            
            # Prepare SR data
            sr_data = {
                'SR ID': sr_id,
                'Call ID': sr_id,
                'Description': sr_description,
                'Notes': sr_notes
            }
            
            # Call analyze_single_sr method
            result = pipeline.analyze_single_sr(sr_data)
            
        except ImportError as e:
            logger.error(f"single_sr_rag_pipeline_ollama not found: {e}")
            return jsonify({
                'success': False,
                'error': 'RAG pipeline not available. Please ensure the RAG module is installed.'
            }), 500
        except Exception as e:
            logger.error(f"Error initializing pipeline: {e}")
            return jsonify({
                'success': False,
                'error': f'RAG pipeline error: {str(e)}'
            }), 500
        
        # Pipeline returns 'AI Workaround' (capital), normalize to lowercase
        ai_workaround = result.get('AI Workaround') if result else None
        
        if result and ai_workaround:
            logger.info(f"✅ Generated new AI workaround for SR {sr_id}")
            
            # Save the regenerated workaround to llm output folder
            llm_output_dir = 'RAG/llm output'
            os.makedirs(llm_output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            regenerated_filename = f"Regenerated_{sr_id}_{timestamp}.xlsx"
            regenerated_path = os.path.join(llm_output_dir, regenerated_filename)
            
            # Create DataFrame and save
            regenerated_df = pd.DataFrame([result])
            regenerated_df.to_excel(regenerated_path, index=False)
            
            logger.info(f"Saved regenerated workaround to: {regenerated_path}")
            
            return jsonify({
                'success': True,
                'ai_workaround': ai_workaround,
                'message': 'AI workaround regenerated successfully',
                'saved_to': regenerated_filename
            })
        else:
            logger.error(f"❌ Failed to generate AI workaround for SR {sr_id}")
            return jsonify({
                'success': False,
                'error': 'Failed to generate AI workaround. Please try again or check if Ollama is running.'
            }), 500
    
    except Exception as e:
        logger.error(f"❌ Regenerate error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/generate_ai_workaround', methods=['POST'])
@user_login_required
def generate_ai_workaround():
    """
    Generate AI workaround for a specific SR that doesn't have one yet
    This is shown as a 'Generate' button when no AI workaround exists
    """
    # Same logic as regenerate
    return regenerate_ai_workaround()


@app.route('/update_ai_workaround_in_db', methods=['POST'])
@user_login_required
def update_ai_workaround_in_db():
    """
    Update AI workaround in database when user approves a regenerated version.
    This ONLY happens when user clicks "This is helpful" on a regenerated version.
    """
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        new_ai_workaround = data.get('ai_workaround', '')
        version_number = data.get('version_number', 1)
        original_workaround = data.get('original_workaround', '')
        
        if not sr_id:
            return jsonify({'error': 'SR ID is required'}), 400
        
        if not new_ai_workaround:
            return jsonify({'error': 'AI workaround is required'}), 400
        
        logger.info(f"🔄 Updating AI workaround in database for SR {sr_id} (v{version_number} approved by user)")
        
        # Update in clean_history_data.db
        try:
            from history_db_manager import HistoryDatabaseManager
            
            hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
            if hist_manager.load_database():
                # Update the AI workaround in history database
                success = hist_manager.update_ai_workaround(sr_id, new_ai_workaround)
                
                if success:
                    logger.info(f"✅ Updated clean_history_data.db with new AI workaround for {sr_id}")
                    
                    # Also update the Excel file if in session
                    if session_data['original_df'] is not None:
                        df = session_data['original_df']
                        
                        # Find SR ID column
                        sr_col = None
                        for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
                            if col in df.columns:
                                sr_col = col
                                break
                        
                        if sr_col:
                            sr_mask = df[sr_col].astype(str) == str(sr_id)
                            if sr_mask.any():
                                # Update AI Generated Workaround column
                                if 'AI Generated Workaround' not in df.columns:
                                    df['AI Generated Workaround'] = ''
                                df.loc[sr_mask, 'AI Generated Workaround'] = new_ai_workaround
                                
                                # Add version tracking column
                                if 'AI Workaround Version' not in df.columns:
                                    df['AI Workaround Version'] = 1
                                df.loc[sr_mask, 'AI Workaround Version'] = version_number
                                
                                session_data['original_df'] = df
                                logger.info(f"✅ Updated Excel with new AI workaround for SR {sr_id}")
                    
                    return jsonify({
                        'success': True,
                        'message': f'Database updated with AI workaround v{version_number}',
                        'updated_sr': sr_id
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to update database - SR not found'
                    }), 404
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not load history database'
                }), 500
                
        except Exception as hist_error:
            logger.error(f"⚠️ Could not update clean_history_data.db: {str(hist_error)}")
            return jsonify({
                'success': False,
                'error': f'Database error: {str(hist_error)}'
            }), 500
    
    except Exception as e:
        logger.error(f"❌ Error updating AI workaround: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/admin/download_latest_report', methods=['GET'])
@login_required
def admin_download_latest_report():
    """Download the latest generated Excel report"""
    try:
        output_dir = app.config['OUTPUT_FOLDER']
        
        if not os.path.exists(output_dir):
            return jsonify({'success': False, 'error': 'No reports available'}), 404
        
        # Find latest Admin_Upload file
        admin_files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
        
        if not admin_files:
            return jsonify({'success': False, 'error': 'No reports available'}), 404
        
        # Sort by filename (timestamp) to get latest
        admin_files.sort(reverse=True)
        latest_file = admin_files[0]
        latest_file_path = os.path.join(output_dir, latest_file)
        
        logger.info(f"Admin downloading report: {latest_file}")
        
        return send_file(
            latest_file_path,
            as_attachment=True,
            download_name=latest_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"Error downloading report: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# UTILITY FUNCTIONS - Vector Store Management & Cleanup
# ============================================================================

def inject_to_vectorstore(new_df, rag_results=None):
    """
    Add new SRs to vector store with full metadata
    
    Args:
        new_df: DataFrame with new SRs
        rag_results: List of RAG analysis results (optional)
    
    Returns:
        int: Number of SRs injected
    """
    try:
        from history_db_manager import HistoryDatabaseManager
        
        logger.info("📥 Starting vector store injection...")
        
        hist_manager = HistoryDatabaseManager('vector store/clean_history_data.db')
        
        if not hist_manager.load_database():
            logger.error("❌ Failed to load vector store")
            return 0
        
        # Map RAG results by SR ID
        rag_map = {}
        if rag_results:
            for result in rag_results:
                sr_id = result.get('SR ID', result.get('Call ID'))
                ai_workaround = result.get('AI Workaround', result.get('AI Generated Workaround'))
                if sr_id and ai_workaround:
                    rag_map[str(sr_id).upper()] = ai_workaround
            logger.info(f"   Mapped {len(rag_map)} AI workarounds from RAG")
        
        # Add each new SR using the existing add_user_feedback_entry method
        injected_count = 0
        for idx, row in new_df.iterrows():
            sr_id = row.get('SR ID', row.get('Call ID'))
            if not sr_id or pd.isna(sr_id):
                continue
            
            sr_id_str = str(sr_id).strip()
            
            # Get AI workaround from RAG or use semantic workaround as fallback
            ai_workaround = rag_map.get(sr_id_str.upper(), 'NA')
            semantic_workaround = str(row.get('Suggested Workaround', row.get('Workaround', '')))
            
            # Use add_user_feedback_entry which handles everything
            success = hist_manager.add_user_feedback_entry(
                sr_id=sr_id_str,
                description=str(row.get('Original Description', row.get('Description', ''))),
                notes=str(row.get('Original Notes/Summary', row.get('Notes', row.get('Summary', '')))),
                user_corrected_workaround='',  # Empty initially
                ai_generated_workaround=ai_workaround if ai_workaround != 'NA' else semantic_workaround,
                priority=str(row.get('Priority', row.get('Customer Priority', 'P3'))),
                function_category=str(row.get('Functional Category', row.get('Interface', ''))),
                resolution_categorization=str(row.get('Resolution Categorization', row.get('Resolution Category', row.get('Classification', '')))),
                sla_resolution_categorization_t1=str(row.get('SLA Resolution Categorization T1', row.get('SLA Resolution', ''))),
                sla_resolution_category=str(row.get('SLA Resolution Category', '')),
                resolution=semantic_workaround,
                workaround=semantic_workaround,
                status=str(row.get('Status', 'Resolved')),
                application=str(row.get('Application', 'Unknown')),
                assigned_to=str(row.get('Assigned Group*', row.get('Assignee Name', row.get('Assigned Group', row.get('Assigned To', row.get('ASSIGNED TO', row.get('assigned_to', row.get('Assignee', 'Not Assigned'))))))))
            )
            
            if success:
                injected_count += 1
                if injected_count % 10 == 0:
                    logger.info(f"   Injected {injected_count} SRs...")
        
        logger.info(f"✅ Vector store updated with {injected_count} new SRs")
        return injected_count
        
    except Exception as e:
        logger.error(f"❌ Error injecting to vector store: {str(e)}\n{traceback.format_exc()}")
        return 0


def cleanup_old_excel_files(keep_latest=1):
    """
    Delete old Excel files, keep only the latest N files
    
    Args:
        keep_latest: Number of latest files to keep (default: 1)
    
    Returns:
        int: Number of files deleted
    """
    try:
        deleted_count = 0
        logger.info(f"🗑️ Starting cleanup (keeping latest {keep_latest} files)...")
        
        # Cleanup output/reports
        output_dir = 'output/reports'
        if os.path.exists(output_dir):
            files = sorted([f for f in os.listdir(output_dir) 
                           if f.startswith('Admin_Upload_') and f.endswith('.xlsx')], 
                          reverse=True)
            
            for old_file in files[keep_latest:]:
                try:
                    os.remove(os.path.join(output_dir, old_file))
                    logger.info(f"   🗑️ Deleted: {old_file}")
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"   ⚠️ Could not delete {old_file}: {e}")
        
        # Cleanup RAG/llm output
        llm_dir = 'RAG/llm output'
        if os.path.exists(llm_dir):
            files = sorted([f for f in os.listdir(llm_dir) 
                           if f.endswith('.xlsx')], 
                          reverse=True)
            
            for old_file in files[keep_latest:]:
                try:
                    os.remove(os.path.join(llm_dir, old_file))
                    logger.info(f"   🗑️ Deleted: {old_file}")
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"   ⚠️ Could not delete {old_file}: {e}")
        
        # Cleanup uploads
        uploads_dir = 'uploads'
        if os.path.exists(uploads_dir):
            files = sorted([f for f in os.listdir(uploads_dir)
                           if f.endswith(('.xls', '.xlsx'))], 
                          reverse=True)
            
            for old_file in files[keep_latest:]:
                try:
                    os.remove(os.path.join(uploads_dir, old_file))
                    logger.info(f"   🗑️ Deleted: {old_file}")
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"   ⚠️ Could not delete {old_file}: {e}")
        
        logger.info(f"✅ Cleanup complete - deleted {deleted_count} old files")
        return deleted_count
        
    except Exception as e:
        logger.error(f"❌ Error during cleanup: {str(e)}\n{traceback.format_exc()}")
        return 0


# ============================================================================
# 🆕 WORKAROUND VOTING ENDPOINTS - Feedback System
# ============================================================================

@app.route('/api/vote/upvote', methods=['POST'])
def upvote_workaround():
    """Record an upvote for a workaround"""
    try:
        if not feedback_storage:
            return jsonify({'success': False, 'error': 'Feedback storage not available'}), 500
        
        data = request.json
        sr_id = data.get('sr_id')
        workaround_type = data.get('workaround_type')  # 'original', 'ai', 'user_corrected'
        workaround_text = data.get('workaround_text', '')
        
        if not sr_id or not workaround_type:
            return jsonify({'success': False, 'error': 'Missing sr_id or workaround_type'}), 400
        
        # Record upvote
        feedback_storage.upvote(sr_id, workaround_type, workaround_text)
        
        # Get updated votes
        votes = feedback_storage.get_votes(sr_id, workaround_type)
        
        return jsonify({
            'success': True,
            'votes': votes,
            'message': 'Upvote recorded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error recording upvote: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vote/downvote', methods=['POST'])
def downvote_workaround():
    """Record a downvote for a workaround"""
    try:
        if not feedback_storage:
            return jsonify({'success': False, 'error': 'Feedback storage not available'}), 500
        
        data = request.json
        sr_id = data.get('sr_id')
        workaround_type = data.get('workaround_type')  # 'original', 'ai', 'user_corrected'
        workaround_text = data.get('workaround_text', '')
        
        if not sr_id or not workaround_type:
            return jsonify({'success': False, 'error': 'Missing sr_id or workaround_type'}), 400
        
        # Record downvote
        feedback_storage.downvote(sr_id, workaround_type, workaround_text)
        
        # Get updated votes
        votes = feedback_storage.get_votes(sr_id, workaround_type)
        
        return jsonify({
            'success': False,
            'votes': votes,
            'message': 'Downvote recorded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error recording downvote: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vote/get_votes', methods=['POST'])
def get_votes():
    """Get current vote counts for a workaround"""
    try:
        if not feedback_storage:
            return jsonify({'success': False, 'error': 'Feedback storage not available'}), 500
        
        data = request.json
        sr_id = data.get('sr_id')
        workaround_type = data.get('workaround_type')
        
        if not sr_id or not workaround_type:
            return jsonify({'success': False, 'error': 'Missing sr_id or workaround_type'}), 400
        
        votes = feedback_storage.get_votes(sr_id, workaround_type)
        
        return jsonify({
            'success': True,
            'votes': votes
        })
        
    except Exception as e:
        logger.error(f"Error getting votes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vote/statistics', methods=['GET'])
def get_vote_statistics():
    """Get overall voting statistics"""
    try:
        if not feedback_storage:
            return jsonify({'success': False, 'error': 'Feedback storage not available'}), 500
        
        stats = feedback_storage.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/skill', methods=['GET'])
def skill_page():
    """
    Display all team members with their skills from people_skills.db
    Accessible without authentication for viewing team capabilities
    """
    try:
        import sqlite3
        import json
        from pathlib import Path
        
        # Connect to people_skills database
        db_path = Path('vector store/people_skills.db')
        
        if not db_path.exists():
            return render_template('feedback/skill_view.html', 
                                   error="People skills database not found",
                                   skills_data=[],
                                   total_members=0)
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Query to get all team members with their skills
        query = """
        SELECT 
            tm.name,
            tm.employee_id,
            tm.status,
            s.application,
            s.skill_level,
            s.specializations,
            s.max_load,
            s.confidence_score,
            s.last_updated
        FROM team_members tm
        LEFT JOIN skills s ON tm.id = s.member_id
        WHERE tm.status = 'active'
        ORDER BY tm.name, s.skill_level DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get assignment statistics
        stats_query = """
        SELECT 
            tm.name,
            COUNT(ah.id) as total_assignments,
            AVG(ah.success_rate) as avg_success_rate,
            AVG(ah.resolution_time_hours) as avg_resolution_time
        FROM team_members tm
        LEFT JOIN assignment_history ah ON tm.id = ah.member_id
        WHERE tm.status = 'active'
        GROUP BY tm.id, tm.name
        """
        
        cursor.execute(stats_query)
        stats_results = cursor.fetchall()
        stats_dict = {row[0]: {
            'total_assignments': row[1],
            'avg_success_rate': row[2],
            'avg_resolution_time': row[3]
        } for row in stats_results}
        
        conn.close()
        
        # Organize data by team member
        skills_data = {}
        for row in results:
            name = row[0]
            if name not in skills_data:
                skills_data[name] = {
                    'employee_id': row[1],
                    'status': row[2],
                    'skills': [],
                    'stats': stats_dict.get(name, {
                        'total_assignments': 0,
                        'avg_success_rate': 0,
                        'avg_resolution_time': 0
                    })
                }
            
            # Add skill if exists
            if row[3]:  # application exists
                specializations = json.loads(row[5]) if row[5] else []
                skills_data[name]['skills'].append({
                    'application': row[3],
                    'skill_level': row[4],
                    'specializations': specializations,
                    'max_load': row[6],
                    'confidence_score': row[7],
                    'last_updated': row[8]
                })
        
        # Convert to list for template
        team_members = []
        for name, data in skills_data.items():
            team_members.append({
                'name': name,
                'employee_id': data['employee_id'],
                'status': data['status'],
                'skills': data['skills'],
                'total_assignments': data['stats']['total_assignments'],
                'avg_success_rate': round(data['stats']['avg_success_rate'] * 100, 1) if data['stats']['avg_success_rate'] else 0,
                'avg_resolution_time': round(data['stats']['avg_resolution_time'], 1) if data['stats']['avg_resolution_time'] else 0
            })
        
        logger.info(f"Loaded {len(team_members)} team members with skills data")
        
        # Calculate total skills
        total_skills = sum(len(member['skills']) for member in team_members)
        
        return render_template('feedback/skill_view.html', 
                               skills_data=team_members,
                               total_members=len(team_members),
                               total_skills=total_skills,
                               error=None)
    
    except Exception as e:
        logger.error(f"Error loading skills page: {str(e)}")
        logger.error(traceback.format_exc())
        return render_template('feedback/skill_view.html', 
                               error=f"Error loading skills data: {str(e)}",
                               skills_data=[],
                               total_members=0,
                               total_skills=0)


if __name__ == '__main__':
    print("=" * 80)
    print("🌟 SR Feedback System Starting...")
    print("=" * 80)
    print(f"📊 Loaded {feedback_manager.total_feedback_count} existing feedback records")
    print("🌐 User Portal: http://localhost:5000")
    print("🔐 Admin Portal: http://localhost:5000/admin")
    print("=" * 80)
    
    # Disable auto-reload to prevent mid-request restarts during AI generation
    # This fixes "Failed to fetch" errors when generating AI workarounds
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

