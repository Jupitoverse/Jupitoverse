#!/usr/bin/env python3
"""
User Routes Blueprint
Handles user portal routes for SR search, feedback, etc.
"""

from flask import Blueprint, render_template, request, jsonify, send_file, current_app, session
import pandas as pd
import os
import pickle
import logging
import traceback
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from app.utils.decorators import user_login_required
from app.utils.helpers import safe_get, sanitize_for_json, concatenate_categorization_fields
from app.utils.state import (
    session_data, get_feedback_manager, get_analyzer, get_age_calculator,
    BASE_DIR, VECTOR_STORE_DIR, OUTPUT_DIR, REPORTS_DIR, CHROMADB_PATH
)
from app.utils.summarize_semantic_wa import summarize_semantic_workarounds
from app.utils.known_workaround_service import get_known_workaround_service

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)


def _build_no_wa_message(cas_ids: list) -> str:
    """Build message when no workarounds are available, showing CAS IDs if found"""
    if cas_ids:
        cas_ids_text = "Similar SRs Found:\n" + "\n".join([f"  • {cid}" for cid in cas_ids])
        return f"{cas_ids_text}\n\n--- No previous WA available ---"
    else:
        return "No similar SRs found. No previous WA available."


def _build_aging_reason(is_cat: bool, is_pri: bool, is_old: bool, age: int, priority: str, category: str) -> str:
    """Build aging reason string showing which condition(s) triggered aging"""
    reasons = []
    if is_cat:
        reasons.append(f"EOM/Ops: {category}")
    if is_pri:
        reasons.append(f"Priority: {priority}")
    if is_old:
        reasons.append(f"Age: {age} days (>3)")
    return " | ".join(reasons) if reasons else ""


@user_bp.route('/user')
@user_login_required
def user_portal():
    """User feedback interface page"""
    # Get username from session (Azure AD or local login)
    # Azure AD stores: user_username, user_email
    # Local login stores: user_username (or admin_username for admins)
    logged_in_user = session.get('user_username', session.get('admin_username', 'User'))
    logged_in_email = session.get('user_email', session.get('admin_email', ''))
    
    return render_template('user/feedback_main.html', 
                           logged_in_user=logged_in_user,
                           logged_in_email=logged_in_email)


@user_bp.route('/user/my_srs')
@user_login_required
def my_srs():
    """Page showing SRs assigned to the logged-in user"""
    logged_in_user = session.get('user_username', session.get('admin_username', 'User'))
    logged_in_email = session.get('user_email', session.get('admin_email', ''))
    
    return render_template('user/my_srs.html', 
                           logged_in_user=logged_in_user,
                           logged_in_email=logged_in_email)


@user_bp.route('/user/my_availability', methods=['GET'])
@user_login_required
def get_my_availability():
    """Get logged-in user's current availability"""
    from team.people_skills_database import PeopleSkillsDatabase
    
    logged_in_email = session.get('user_email', session.get('admin_email', ''))
    
    if not logged_in_email:
        return jsonify({'success': False, 'error': 'No email in session', 'is_team_member': False})
    
    try:
        db_path = os.path.join(BASE_DIR, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        # Get member by email
        member = db.get_member_by_email(logged_in_email)
        if not member:
            return jsonify({
                'success': False, 
                'error': 'User not found in team database',
                'is_team_member': False
            })
        
        # Get current availability
        availability = db.get_member_availability(member['name'])
        
        return jsonify({
            'success': True,
            'is_team_member': True,
            'member_name': member['name'],
            'availability_percent': availability.get('availability_percent', 100),
            'availability_type': availability.get('availability_type', 'full_day'),
            'reason': availability.get('reason', ''),
            'updated_at': availability.get('updated_at', '')
        })
        
    except Exception as e:
        logger.error(f"Get availability error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'is_team_member': False}), 500


@user_bp.route('/user/set_my_availability', methods=['POST'])
@user_login_required
def set_my_availability():
    """Set logged-in user's availability"""
    from team.people_skills_database import PeopleSkillsDatabase
    
    logged_in_email = session.get('user_email', session.get('admin_email', ''))
    
    if not logged_in_email:
        return jsonify({'success': False, 'error': 'No email in session'}), 400
    
    try:
        data = request.json
        availability_percent = int(data.get('availability_percent', 100))
        availability_type = data.get('availability_type', 'full_day')
        reason = data.get('reason', '')
        
        db_path = os.path.join(BASE_DIR, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        # Get member by email
        member = db.get_member_by_email(logged_in_email)
        if not member:
            return jsonify({
                'success': False, 
                'error': 'User not found in team database'
            }), 404
        
        # Set availability with user's name as updated_by
        success = db.set_member_availability(
            member_name=member['name'],
            availability_percent=availability_percent,
            availability_type=availability_type,
            reason=reason,
            updated_by=member['name']  # User updates their own availability
        )
        
        if success:
            logger.info(f"User {member['name']} set own availability to {availability_percent}%")
            return jsonify({
                'success': True,
                'message': f'Availability set to {availability_percent}%'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update availability'}), 500
        
    except Exception as e:
        logger.error(f"Set availability error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/api/my_srs', methods=['GET'])
@user_login_required
def get_my_srs():
    """API endpoint to get SRs assigned to the logged-in user - TODAY'S SRs ONLY"""
    from RAG.utils.history_db_manager import HistoryDatabaseManager
    from team.people_skills_database import PeopleSkillsDatabase
    from assignment.priority_age_calculator import PriorityAgeCalculator
    import os
    import pandas as pd
    
    # Initialize age calculator for aging SR detection
    age_calculator = None
    try:
        age_calculator = PriorityAgeCalculator()
    except Exception as e:
        logger.warning(f"Could not initialize age calculator: {e}")
    
    logged_in_email = session.get('user_email', session.get('admin_email', ''))
    logged_in_user = session.get('user_username', session.get('admin_username', ''))
    
    if not logged_in_email and not logged_in_user:
        return jsonify({'success': False, 'error': 'User not identified'}), 400
    
    try:
        # First, try to get the team member's name from their email
        member_name = logged_in_user  # Default to session username
        
        if logged_in_email:
            db_path = os.path.join(BASE_DIR, 'data', 'database', 'people_skills.db')
            if os.path.exists(db_path):
                db = PeopleSkillsDatabase(db_path)
                member_info = db.get_member_by_email(logged_in_email)
                if member_info:
                    member_name = member_info['name']
                    logger.info(f"Found team member: {member_name} for email: {logged_in_email}")
        
        # Get TODAY's SRs from the latest output file (most reliable source)
        today_str = datetime.now().strftime('%Y%m%d')
        today_display = datetime.now().strftime('%Y-%m-%d')
        output_dir = os.path.join(BASE_DIR, 'output', 'reports')
        input_dir = os.path.join(BASE_DIR, 'input')
        
        srs = []
        
        # First, load input Excel to get Submit Date, Last Date, and Category (not in output Excel)
        input_data_lookup = {}  # sr_id -> {submit_date, last_date, category}
        if os.path.exists(input_dir):
            input_files = [f for f in os.listdir(input_dir) 
                          if today_str in f and (f.endswith('.xlsx') or f.endswith('.xls'))]
            logger.info(f"[DEBUG] Looking for input files with date {today_str}, found: {[f for f in input_files]}")
            
            if input_files:
                input_files.sort(reverse=True)
                input_file = os.path.join(input_dir, input_files[0])
                logger.info(f"[DEBUG] Reading dates/category from input file: {input_files[0]}")
                try:
                    input_df = pd.read_excel(input_file)
                    logger.info(f"[DEBUG] Input Excel columns: {list(input_df.columns)}")
                    
                    # Find SR ID column
                    sr_col = None
                    for col in ['Call ID', 'SR ID', 'call_id', 'sr_id']:
                        if col in input_df.columns:
                            sr_col = col
                            break
                    
                    # Find date columns
                    submit_col = None
                    for col in ['Submit Date', 'submit_date', 'Reported Date', 'Created Date']:
                        if col in input_df.columns:
                            submit_col = col
                            break
                    
                    last_col = None
                    for col in ['Last Date Duration Calculated', 'Last Date', 'last_date']:
                        if col in input_df.columns:
                            last_col = col
                            break
                    
                    # Find Category column
                    cat_col = None
                    for col in ['Categorization Tier 3', 'Operational Categorization Tier 3', 'Categorization', 
                               'Resolution Categorization', 'Category', 'Op Cat Tier 3']:
                        if col in input_df.columns:
                            cat_col = col
                            break
                    
                    logger.info(f"[DEBUG] Input columns found - SR: {sr_col}, Submit: {submit_col}, Last: {last_col}, Category: {cat_col}")
                    
                    if sr_col:
                        for idx, row in input_df.iterrows():
                            sr_id = str(row.get(sr_col, '')).upper().strip()
                            if sr_id and sr_id != 'NAN':
                                input_data_lookup[sr_id] = {
                                    'submit_date': row.get(submit_col) if submit_col else None,
                                    'last_date': row.get(last_col) if last_col else None,
                                    'category': row.get(cat_col) if cat_col else None
                                }
                        
                        # Log sample data
                        if input_data_lookup:
                            first_sr = next(iter(input_data_lookup.keys()))
                            logger.info(f"[DEBUG] Sample input data for {first_sr}: {input_data_lookup[first_sr]}")
                            
                except Exception as e:
                    logger.warning(f"[DEBUG] Could not read input file: {e}")
                    import traceback
                    logger.warning(f"[DEBUG] Traceback: {traceback.format_exc()}")
        
        logger.info(f"[DEBUG] Loaded {len(input_data_lookup)} SR data entries from input file")
        
        # Find today's upload file
        if os.path.exists(output_dir):
            today_files = [f for f in os.listdir(output_dir) 
                          if f.startswith(f'Admin_Upload_{today_str}') and f.endswith('.xlsx')]
            
            if today_files:
                today_files.sort(reverse=True)  # Get most recent
                latest_file = os.path.join(output_dir, today_files[0])
                
                try:
                    df = pd.read_excel(latest_file)
                    
                    # Find the assignee column
                    assignee_col = None
                    for col in ['Assigned To', 'assigned_to', 'Assignee', 'Current Assignee']:
                        if col in df.columns:
                            assignee_col = col
                            break
                    
                    # Log all columns for debugging
                    all_cols = list(df.columns)
                    logger.info(f"Excel columns ({len(all_cols)}): {all_cols}")
                    
                    # Find SR ID column - try many variations
                    sr_id_col = None
                    for col in all_cols:
                        col_lower = col.lower().replace(' ', '').replace('_', '')
                        if col_lower in ['callid', 'srid', 'ticketid', 'caseid', 'id', 'srno', 'ticketno']:
                            sr_id_col = col
                            break
                    
                    # Find description column
                    desc_col = None
                    for col in all_cols:
                        col_lower = col.lower()
                        if 'description' in col_lower or 'summary' in col_lower or 'subject' in col_lower or 'issue' in col_lower:
                            desc_col = col
                            break
                    
                    logger.info(f"Detected columns - SR ID: '{sr_id_col}', Description: '{desc_col}', Assignee: '{assignee_col}'")
                    
                    # Filter for this user's SRs
                    for idx, row in df.iterrows():
                        sr_data = row.to_dict()
                        
                        # DEBUG: Log first row to see all values
                        if idx == 0 or idx == df.index[0]:
                            logger.info(f"DEBUG First row data: {sr_data}")
                        
                        # Get SR ID - try multiple approaches
                        sr_id = ''
                        
                        # Approach 1: Use detected column
                        if sr_id_col and sr_id_col in sr_data:
                            sr_id = str(sr_data[sr_id_col]).strip()
                            if idx == 0 or idx == df.index[0]:
                                logger.info(f"DEBUG SR ID from '{sr_id_col}': '{sr_id}'")
                        
                        # Approach 2: Try common column names
                        if not sr_id or sr_id.lower() in ['nan', 'none', '']:
                            for col in df.columns:
                                if 'sr' in col.lower() and 'id' in col.lower():
                                    sr_id = str(sr_data.get(col, '')).strip()
                                    if sr_id and sr_id.lower() not in ['nan', 'none', '']:
                                        if idx == 0:
                                            logger.info(f"DEBUG SR ID from fallback col '{col}': '{sr_id}'")
                                        break
                        
                        # Approach 3: Scan all values for CAS/SR pattern
                        if not sr_id or sr_id.lower() in ['nan', 'none', '']:
                            for col, val in sr_data.items():
                                val_str = str(val).strip()
                                if val_str.upper().startswith('CAS') or (val_str.upper().startswith('SR') and len(val_str) > 3):
                                    sr_id = val_str
                                    if idx == 0:
                                        logger.info(f"DEBUG SR ID from scan col '{col}': '{sr_id}'")
                                    break
                        
                        # Skip if no valid SR ID
                        if not sr_id or sr_id.lower() in ['nan', 'none', ''] or sr_id.strip() == '':
                            continue
                        
                        # Get description
                        description = ''
                        if desc_col and desc_col in sr_data:
                            description = str(sr_data[desc_col])
                        if not description or description.lower() in ['nan', 'none', '']:
                            # Try to find any text field
                            for col, val in sr_data.items():
                                val_str = str(val)
                                if len(val_str) > 50 and val_str.lower() not in ['nan', 'none']:
                                    description = val_str[:200]
                                    break
                        if not description or description.lower() in ['nan', 'none', '']:
                            description = f'SR {sr_id}'
                        
                        # Check if assigned to this user - flexible matching
                        assigned_to = str(sr_data.get(assignee_col, '')) if assignee_col else ''
                        assigned_lower = assigned_to.lower()
                        member_parts = member_name.lower().split()
                        # Match if any significant part (>2 chars) of member name is in assignee
                        if not any(part in assigned_lower for part in member_parts if len(part) > 2):
                            continue
                        
                        # Get priority and categorization for aging detection
                        priority = str(sr_data.get('Customer Priority', sr_data.get('Priority', 'P3'))).upper()
                        sr_id_upper = sr_id.upper().strip()
                        
                        # Get Operational Categorization Tier 3 - try output Excel first
                        ops_cat_tier3 = ''
                        for col in ['Operational Categorization Tier 3', 'Op Cat Tier 3', 'Ops Cat Tier 3', 
                                   'Operational Cat Tier 3', 'OpCatTier3', 'Resolution Categorization',
                                   'Categorization Tier 3', 'Category']:
                            if col in sr_data:
                                val = sr_data.get(col)
                                if pd.notna(val) and str(val).strip().lower() not in ['nan', 'none', '']:
                                    ops_cat_tier3 = str(val).lower()
                                    break
                        
                        # If category not in output, get from input lookup
                        if not ops_cat_tier3 and sr_id_upper in input_data_lookup:
                            input_cat = input_data_lookup[sr_id_upper].get('category')
                            if pd.notna(input_cat) and str(input_cat).strip().lower() not in ['nan', 'none', '']:
                                ops_cat_tier3 = str(input_cat).lower()
                                if idx == 0:
                                    logger.info(f"[DEBUG] Got category from input lookup: {ops_cat_tier3}")
                        
                        # Get Submit Date - try output Excel first
                        submit_date = None
                        for col in ['Submit Date', 'Reported Date', 'Created Date', 'Opened Date', 
                                   'submit_date', 'reported_date', 'created_date']:
                            if col in sr_data and pd.notna(sr_data.get(col)):
                                submit_date = sr_data.get(col)
                                break
                        
                        # If submit date not in output, get from input lookup
                        if (submit_date is None or pd.isna(submit_date)) and sr_id_upper in input_data_lookup:
                            submit_date = input_data_lookup[sr_id_upper].get('submit_date')
                            if idx == 0:
                                logger.info(f"[DEBUG] Got submit_date from input lookup: {submit_date}")
                        
                        # Get Last Date - try output Excel first
                        last_date = None
                        for col in ['Last Date', 'Last Date Duration Calculated', 'Last Activity Date', 
                                   'Modified Date', 'Last Updated', 'last_date', 'last_activity_date', 
                                   'modified_date', 'Last Modified Date', 'Last Modified', 'Updated Date']:
                            if col in sr_data and pd.notna(sr_data.get(col)):
                                last_date = sr_data.get(col)
                                break
                        
                        # If last date not in output, get from input lookup
                        if (last_date is None or pd.isna(last_date)) and sr_id_upper in input_data_lookup:
                            last_date = input_data_lookup[sr_id_upper].get('last_date')
                            if idx == 0:
                                logger.info(f"[DEBUG] Got last_date from input lookup: {last_date}")
                        
                        # Debug: Log final dates for first row
                        if idx == 0:
                            logger.info(f"[DEBUG] Final dates - Submit: {submit_date}, Last: {last_date}")
                        
                        # Calculate business days age: Last Date - Submit Date (excluding weekends & US holidays)
                        business_days_age = 0
                        if age_calculator and submit_date:
                            try:
                                if last_date and pd.notna(last_date):
                                    # Calculate between Submit Date and Last Date
                                    business_days_age = age_calculator.calculate_business_days(submit_date, last_date)
                                    if idx == 0:
                                        logger.info(f"[DEBUG] Calculated age (Last-Submit): {business_days_age} business days")
                                else:
                                    # Fallback: calculate from submit date to now
                                    business_days_age = age_calculator.calculate_business_days(submit_date)
                                    if idx == 0:
                                        logger.info(f"[DEBUG] Calculated age (Submit-Now): {business_days_age} business days")
                            except Exception as age_err:
                                logger.warning(f"[DEBUG] Age calculation failed for {sr_id}: {age_err}")
                        
                        # Format dates for display
                        submit_date_str = '-'
                        last_date_str = '-'
                        if pd.notna(submit_date):
                            try:
                                if hasattr(submit_date, 'strftime'):
                                    submit_date_str = submit_date.strftime('%m/%d/%Y')
                                else:
                                    submit_date_str = str(submit_date)[:10]
                            except:
                                submit_date_str = str(submit_date)[:10]
                        if pd.notna(last_date):
                            try:
                                if hasattr(last_date, 'strftime'):
                                    last_date_str = last_date.strftime('%m/%d/%Y')
                                else:
                                    last_date_str = str(last_date)[:10]
                            except:
                                last_date_str = str(last_date)[:10]
                        
                        # Aging SR conditions:
                        # 1. Ops Cat Tier 3 is one of: Ops EOM, Potential Ops EOM, Sales EOM, Potential Sales EOM
                        # 2. Priority is P2 or P3
                        # 3. Age > 3 business days
                        aging_categories = ['ops eom', 'potential ops eom', 'sales eom', 'potential sales eom']
                        is_aging_category = any(cat in ops_cat_tier3 for cat in aging_categories)
                        is_aging_priority = priority in ['P2', 'P3']
                        is_over_age_threshold = business_days_age > 3
                        
                        # OR condition - ANY of these makes it aging
                        is_aging = is_aging_category or is_aging_priority or is_over_age_threshold
                        
                        # Get category display value (capitalize for display)
                        category_display = ops_cat_tier3.title() if ops_cat_tier3 else '-'
                        
                        srs.append({
                            'call_id': sr_id,
                            'sr_id': sr_id,  # Frontend uses sr_id
                            'description': description[:200],
                            'priority': priority,
                            'application': str(sr_data.get('Assigned Group', sr_data.get('Application', '-'))),
                            'status': str(sr_data.get('Status', 'Open')),
                            'assigned_to': assigned_to,
                            'reported_date': today_display,
                            'submit_date': submit_date_str,
                            'last_date': last_date_str,
                            'has_ai_workaround': bool(sr_data.get('AI Workaround', sr_data.get('Semantic Workaround', ''))),
                            # Category field
                            'categorization_tier3': category_display,
                            'category': category_display,
                            # Aging SR fields
                            'is_aging': is_aging,
                            'business_days_age': business_days_age,
                            'ops_categorization': ops_cat_tier3,
                            'aging_reason': _build_aging_reason(is_aging_category, is_aging_priority, is_over_age_threshold, business_days_age, priority, ops_cat_tier3) if is_aging else ''
                        })
                        
                except Exception as e:
                    logger.error(f"Error reading today's file: {e}")
        
        # Group SRs by date for frontend display
        grouped_by_date = {}
        for sr in srs:
            date_key = sr.get('reported_date', today_display)
            if date_key not in grouped_by_date:
                grouped_by_date[date_key] = []
            grouped_by_date[date_key].append(sr)
        
        return jsonify({
            'success': True,
            'user': member_name,
            'email': logged_in_email,
            'total_count': len(srs),
            'date': today_display,
            'srs': srs,
            'grouped_by_date': grouped_by_date,
            'message': f"Showing {len(srs)} SRs assigned to you today ({today_display})"
        })
        
    except Exception as e:
        logger.error(f"Error fetching my SRs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/get_upload_info', methods=['GET'])
def get_upload_info():
    """Get info about admin uploads - uses ChromaDB and output files"""
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        from team.people_skills_database import PeopleSkillsDatabase
        import pandas as pd
        
        # Get logged-in user info for counting their assigned SRs
        logged_in_email = session.get('user_email', session.get('admin_email', ''))
        logged_in_user = session.get('user_username', session.get('admin_username', ''))
        member_name = logged_in_user
        
        # Try to get the team member's name from their email
        if logged_in_email:
            db_path = os.path.join(BASE_DIR, 'data', 'database', 'people_skills.db')
            if os.path.exists(db_path):
                try:
                    db = PeopleSkillsDatabase(db_path)
                    member_info = db.get_member_by_email(logged_in_email)
                    if member_info:
                        member_name = member_info['name']
                except:
                    pass
        
        # Get data from ChromaDB (the authoritative source)
        chromadb_count = 0
        today_count = 0
        user_today_count = 0  # Count for THIS user
        latest_date = None
        
        try:
            hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
            if hist_manager.use_chromadb and hist_manager.chromadb_collection:
                chromadb_count = hist_manager.chromadb_collection.count()
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
        
        # Count today's SRs from output files (most reliable source)
        today_str = datetime.now().strftime('%Y%m%d')  # Format: 20260116
        output_dir = os.path.join(BASE_DIR, 'output', 'reports')
        
        try:
            if os.path.exists(output_dir):
                today_files = [f for f in os.listdir(output_dir) 
                              if f.startswith(f'Admin_Upload_{today_str}') and f.endswith('.xlsx')]
                
                if today_files:
                    # Get the latest file from today
                    today_files.sort(reverse=True)
                    latest_file = today_files[0]
                    latest_path = os.path.join(output_dir, latest_file)
                    
                    # Count SRs in the latest today's file
                    try:
                        df = pd.read_excel(latest_path)
                        today_count = len(df)
                        
                        # Count SRs assigned to THIS user
                        if member_name:
                            assignee_col = None
                            for col in ['Assigned To', 'assigned_to', 'Assignee', 'Current Assignee']:
                                if col in df.columns:
                                    assignee_col = col
                                    break
                            if assignee_col:
                                # Flexible name matching
                                member_parts = member_name.lower().split()
                                for _, row in df.iterrows():
                                    assigned = str(row.get(assignee_col, '')).lower()
                                    # Match if any part of the member name is in the assignee field
                                    if any(part in assigned for part in member_parts if len(part) > 2):
                                        user_today_count += 1
                    except Exception as e:
                        logger.warning(f"Error reading today's file: {e}")
                        today_count = 0
                    
                    # Extract date from filename (Admin_Upload_20260116_154702.xlsx)
                    try:
                        date_part = latest_file.split('_')[2]  # 20260116
                        latest_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                    except:
                        latest_date = datetime.now().strftime('%Y-%m-%d')
                else:
                    # No files today, check for most recent file
                    all_files = [f for f in os.listdir(output_dir) 
                                if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
                    if all_files:
                        all_files.sort(reverse=True)
                        latest_file = all_files[0]
                        try:
                            date_part = latest_file.split('_')[2]
                            latest_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                        except:
                            pass
        except Exception as e:
            logger.error(f"Error checking output files: {e}")
        
        # Return appropriate response based on ChromaDB data
        if chromadb_count == 0:
            return jsonify({
                'has_upload': False,
                'historical_count': 0,
                'message': 'No data available. Please contact admin.'
            })
        
        # Format the latest date nicely
        upload_date_display = "Unknown"
        if latest_date:
            try:
                dt = datetime.strptime(latest_date, '%Y-%m-%d')
                upload_date_display = dt.strftime('%B %d, %Y')
            except:
                upload_date_display = latest_date
        
        return jsonify({
            'has_upload': True,
            'upload_date': upload_date_display,
            'sr_count': user_today_count,  # User's SRs today (for "Total Assigned SRs")
            'today_total': today_count,  # Total SRs today (all users)
            'historical_count': chromadb_count,  # For Knowledge Base display
            'filename': 'Today',
            'total_uploads': 1,
            'user_name': member_name,
            'message': f'Today: {user_today_count} SRs assigned to you (Last update: {upload_date_display})'
        })
        
    except Exception as e:
        logger.error(f"Error getting upload info: {str(e)}")
        return jsonify({
            'has_upload': False,
            'historical_count': 0,
            'message': 'Error loading data'
        })


def _get_valid_field(val):
    """Helper to get non-garbage value - enhanced to detect empty AI workarounds"""
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str.upper() in ['NA', 'N/A', 'NULL', 'NONE', '']:
        return None
    return val_str


def _is_valid_workaround(workaround: str) -> bool:
    """Check if workaround has actual content (not just headers/empty brackets)"""
    if not workaround or workaround.upper() in ['NA', 'N/A', 'NULL', 'NONE', '']:
        return False
    
    # Remove AI workaround headers
    cleaned = workaround
    for pattern in ['**AI WORKAROUND:**', '**AI WORKAROUND**', 'AI WORKAROUND:', 'AI WORKAROUND']:
        cleaned = cleaned.replace(pattern, '')
    
    # Remove empty brackets, bullets, numbers, and whitespace
    cleaned = re.sub(r'\[\s*\]', '', cleaned)  # Remove empty []
    cleaned = re.sub(r'^\s*[-*•]\s*$', '', cleaned, flags=re.MULTILINE)  # Empty bullet lines
    cleaned = re.sub(r'^\s*\d+\.\s*$', '', cleaned, flags=re.MULTILINE)  # Empty numbered lines
    cleaned = re.sub(r'\n+', '\n', cleaned).strip()  # Collapse newlines
    
    # If nothing meaningful remains (less than 15 chars of real content), it's garbage
    return len(cleaned) >= 15


def find_similar_srs(description: str, current_sr_id: str, top_k: int = 5) -> list:
    """Find similar SRs using semantic search (summary param removed - was redundant)"""
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        
        # Build query from description only (summary removed - was redundant)
        query_text = description.strip()
        
        if len(query_text) < 10:
            return []
        
        similar_srs = []
        
        # Use ChromaDB's query method for semantic search
        if hist_manager.use_chromadb and hist_manager.chromadb_collection:
            try:
                # Reuse model from hist_manager (already loaded with meta tensor fix)
                # This avoids loading a new model which can trigger meta tensor error
                model = hist_manager.model
                if model is None:
                    logger.warning("Model not loaded in hist_manager, skipping similar SR search")
                    return []
                
                query_embedding = model.encode(query_text).tolist()
                
                # Query ChromaDB
                results = hist_manager.chromadb_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k + 1,  # +1 to exclude current SR
                    include=['metadatas', 'distances']
                )
                
                if results and results.get('metadatas') and results['metadatas'][0]:
                    for i, metadata in enumerate(results['metadatas'][0]):
                        sr_id = metadata.get('call_id', '')
                        
                        # Skip current SR
                        if sr_id.upper() == current_sr_id.upper():
                            continue
                        
                        # Calculate similarity (ChromaDB returns L2 distance)
                        distance = results['distances'][0][i] if results.get('distances') else 0
                        similarity = max(0, 1 - (distance / 2))  # Convert L2 to similarity
                        
                        if similarity >= 0.3:  # Include matches with 30%+ similarity
                            # Get workaround - prioritize actual workaround field, then user corrected, then AI
                            # Also validate that workaround has actual content (not just empty headers)
                            workaround = 'N/A'
                            for wa_field in ['workaround', 'user_corrected_workaround', 'ai_generated_workaround']:
                                wa_val = _get_valid_field(metadata.get(wa_field))
                                if wa_val and _is_valid_workaround(wa_val):
                                    workaround = wa_val
                                    break
                            
                            # Get resolution info - check both field name variations
                            resolution = (_get_valid_field(metadata.get('resolution_categorization')) or
                                        _get_valid_field(metadata.get('Resolution Categorization')) or 'Unknown')
                            
                            sla_resolution = (_get_valid_field(metadata.get('sla_resolution_category')) or
                                            _get_valid_field(metadata.get('sla_resolution_categorization_t1')) or 'Unknown')
                            
                            logger.info(f"Similar SR {sr_id}: res={resolution}, sla={sla_resolution}, wa={workaround[:50] if workaround != 'N/A' else 'N/A'}...")
                            
                            similar_srs.append({
                                'sr_id': sr_id,
                                'summary': metadata.get('description', 'N/A')[:150],  # Use description (summary removed)
                                'similarity': round(similarity * 100, 1),
                                'workaround': workaround[:500] if workaround != 'N/A' else 'N/A',
                                'resolution': resolution,
                                'sla_resolution': sla_resolution,
                                'priority': metadata.get('priority', metadata.get('Customer Priority', 'N/A'))
                            })
                        
                        if len(similar_srs) >= top_k:
                            break
                
                logger.info(f"Found {len(similar_srs)} similar SRs for {current_sr_id}")
                            
            except Exception as e:
                logger.warning(f"ChromaDB semantic search error: {e}")
                import traceback
                traceback.print_exc()
        
        return similar_srs
        
    except Exception as e:
        logger.error(f"Error finding similar SRs: {e}")
        return []


def search_vectorstore_by_sr_id(sr_id: str) -> Optional[Dict]:
    """Search vector store for exact SR ID match using HistoryDatabaseManager"""
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        
        sr_id_upper = sr_id.upper().strip()
        
        # Check if using ChromaDB
        if hist_manager.use_chromadb and hist_manager.chromadb_collection:
            try:
                # Search ChromaDB by ID
                results = hist_manager.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    limit=1
                )
                
                if results and results.get('metadatas') and len(results['metadatas']) > 0:
                    metadata = results['metadatas'][0]
                    logger.info(f"✅ Found SR {sr_id} in ChromaDB")
                    # Debug: Log all fields in the metadata
                    logger.info(f"📊 Metadata keys: {list(metadata.keys())}")
                    logger.info(f"📊 Description: {str(metadata.get('description', 'N/A'))[:100]}")
                    logger.info(f"📊 Priority: {metadata.get('Customer Priority', metadata.get('priority', 'N/A'))}")
                    logger.info(f"📊 Assigned: {metadata.get('assigned_to', 'N/A')}")
                    return metadata
                
                # Also try case-insensitive search with all records
                all_results = hist_manager.chromadb_collection.get(
                    limit=50000,
                    include=['metadatas']
                )
                
                if all_results and all_results.get('metadatas'):
                    for metadata in all_results['metadatas']:
                        call_id = str(metadata.get('call_id', '')).upper().strip()
                        if call_id == sr_id_upper:
                            logger.info(f"✅ Found SR {sr_id} in ChromaDB (full scan)")
                            # Debug: Log all fields in the metadata
                            logger.info(f"📊 Metadata keys: {list(metadata.keys())}")
                            logger.info(f"📊 Description: {metadata.get('description', 'N/A')[:100]}")
                            logger.info(f"📊 Priority: {metadata.get('Customer Priority', metadata.get('priority', 'N/A'))}")
                            return metadata
                
            except Exception as e:
                logger.warning(f"ChromaDB search error: {e}, trying pickle fallback")
        
        # Fallback to pickle data
        if hist_manager.db_data:
            metadata_list = hist_manager.db_data.get('metadata', [])
            for metadata in metadata_list:
                call_id = str(metadata.get('call_id', '')).upper().strip()
                if call_id == sr_id_upper:
                    logger.info(f"✅ Found SR {sr_id} in vector store")
                    return metadata
        
        logger.info(f"📊 SR {sr_id} not found in vector store")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error searching vector store: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def search_latest_admin_upload_only(sr_id: str):
    """Search ONLY the latest Admin_Upload file"""
    try:
        output_dir = os.path.join(BASE_DIR, 'output', 'reports')
        if not os.path.exists(output_dir):
            return None, None
        
        files = [f for f in os.listdir(output_dir) 
                 if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
        
        if not files:
            return None, None
        
        files.sort(reverse=True)
        latest_file = files[0]
        filepath = os.path.join(output_dir, latest_file)
        
        df = pd.read_excel(filepath)
        
        sr_col = None
        for col in ['SR ID', 'Call ID', 'SR Number', 'Ticket ID']:
            if col in df.columns:
                sr_col = col
                break
        
        if not sr_col:
            return None, None
        
        sr_id_upper = sr_id.upper().strip()
        mask = df[sr_col].astype(str).str.upper().str.strip() == sr_id_upper
        
        if mask.any():
            logger.info(f"✅ Found SR {sr_id} in latest Excel: {latest_file}")
            return df[mask].iloc[0], latest_file
        
        return None, None
        
    except Exception as e:
        logger.error(f"❌ Error searching latest Excel: {str(e)}")
        return None, None


@user_bp.route('/search_sr', methods=['POST'])
def search_sr():
    """Search for an SR by ID"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'Please enter an SR ID'}), 400
        
        # Search vector store first
        vs_result = search_vectorstore_by_sr_id(sr_id)
        
        if vs_result:
            # Build response from vector store
            # ChromaDB uses different field names - map them correctly
            age_calculator = get_age_calculator()
            age_info = None
            
            # Try different date field names
            opened_date_str = (vs_result.get('Reported Date', '') or 
                             vs_result.get('opened_date', '') or
                             vs_result.get('reported_date', ''))
            if age_calculator and opened_date_str:
                age_days = age_calculator.calculate_business_days(opened_date_str)
                age_info = {
                    'business_days': age_days,
                    'display': f"{age_days} business day{'s' if age_days != 1 else ''}"
                }
            
            # Map ChromaDB fields to expected names
            # ChromaDB uses: Customer Priority, assigned_to, Status, etc.
            priority = (vs_result.get('Customer Priority', '') or 
                       vs_result.get('priority', '') or 'P3')
            
            status = (vs_result.get('Status', '') or 
                     vs_result.get('status', '') or 'N/A')
            
            assignee = (vs_result.get('assigned_to', '') or 
                       vs_result.get('current_assignee', '') or 
                       vs_result.get('Assigned To', '') or 'Not Assigned')
            
            description = (vs_result.get('description', '') or 
                          vs_result.get('document', '') or 'N/A')
            
            # summary field removed - use wl_summary or first 100 chars of description
            notes = (vs_result.get('wl_summary', '') or 
                    vs_result.get('description', '')[:100] or 'N/A')
            
            ai_workaround = vs_result.get('ai_generated_workaround', '')
            if ai_workaround in ['NA', 'N/A', '', None]:
                ai_workaround = ''
            
            user_corrected = vs_result.get('user_corrected_workaround', '')
            
            # Build SLA Resolution display
            sla_fields = []
            sla_t1 = vs_result.get('sla_resolution_categorization_t1', '')
            sla_cat = vs_result.get('sla_resolution_category', '')
            if sla_t1 and sla_t1 not in ['N/A', 'NA', '']:
                sla_fields.append(sla_t1)
            if sla_cat and sla_cat not in ['N/A', 'NA', '']:
                sla_fields.append(sla_cat)
            sla_resolution_display = ' > '.join(sla_fields) if sla_fields else 'N/A'
            
            # Find similar SRs (summary param removed - was redundant)
            similar_srs = find_similar_srs(description, sr_id, top_k=5)
            
            # Use similar_srs directly as semantic_workarounds_list 
            # (already contains all needed fields: sr_id, similarity, description, workaround, resolution, sla_resolution)
            semantic_workarounds_list = similar_srs
            
            # Search for known workaround from JSON knowledge base
            known_workaround = None
            try:
                known_wa_service = get_known_workaround_service()
                rca_text = vs_result.get('resolution_categorization', '') or vs_result.get('Resolution Categorization', '')
                known_workaround = known_wa_service.find_known_workaround(
                    description=description,
                    rca=rca_text,
                    threshold=0.35  # 35% match threshold
                )
                if known_workaround:
                    logger.info(f"✅ Found known workaround for {sr_id}: {known_workaround.get('sr_id', 'N/A')} "
                               f"(score: {known_workaround.get('match_score', 0):.1%})")
            except Exception as e:
                logger.warning(f"Known workaround search failed for {sr_id}: {e}")
            
            # Get all user feedback entries for this SR (supports multiple corrections per SR)
            all_user_feedback = []
            try:
                from RAG.utils.history_db_manager import HistoryDatabaseManager
                feedback_hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
                if feedback_hist_manager and hasattr(feedback_hist_manager, 'get_all_user_feedback_for_sr'):
                    all_user_feedback = feedback_hist_manager.get_all_user_feedback_for_sr(sr_id)
                    if all_user_feedback:
                        logger.info(f"Found {len(all_user_feedback)} user feedback entries for SR {sr_id}")
            except Exception as e:
                logger.warning(f"Error getting user feedback: {e}")
            
            # Summarize semantic workarounds using LLM for cleaner display
            summarized_result = {'success': False, 'summary': '', 'similar_count': 0}
            if similar_srs:
                try:
                    summarized_result = summarize_semantic_workarounds(
                        sr_id=sr_id,
                        description=description,
                        priority=priority,
                        similar_srs=similar_srs
                    )
                    logger.info(f"Summarized workarounds for {sr_id}: success={summarized_result.get('success')}")
                except Exception as e:
                    logger.warning(f"Failed to summarize workarounds for {sr_id}: {e}")
            
            response = {
                'success': True,
                'source': 'vector_store',
                'sr': {
                    'sr_id': vs_result.get('call_id', sr_id),
                    'description': sanitize_for_json(description),
                    # 'summary' field removed - using notes from wl_summary
                    'notes': sanitize_for_json(notes),  # Frontend expects 'notes'
                    'priority': sanitize_for_json(priority),
                    'status': sanitize_for_json(status),
                    'current_assignee': sanitize_for_json(assignee),
                    'assigned_to': sanitize_for_json(assignee),  # Frontend expects 'assigned_to'
                    'Assigned To': sanitize_for_json(assignee),  # Also with capital case
                    
                    # AI Workaround fields
                    'ai_workaround': sanitize_for_json(ai_workaround) if ai_workaround else None,
                    'ai_workaround_available': bool(ai_workaround),
                    
                    # User corrected workaround (latest)
                    'corrected_workaround': sanitize_for_json(user_corrected) if user_corrected else None,
                    'is_user_corrected': bool(user_corrected) or len(all_user_feedback) > 0,
                    'user_corrected_workaround': sanitize_for_json(user_corrected),
                    
                    # All user feedback entries (multiple user workarounds supported)
                    'all_user_feedback': all_user_feedback,
                    'user_feedback_count': len(all_user_feedback),
                    
                    # Semantic matches - USE SUMMARIZED TEXT instead of raw
                    # When summarization fails, show CAS IDs with "No previous WA available"
                    'semantic_workaround': sanitize_for_json(
                        summarized_result.get('summary', '') if summarized_result.get('success') 
                        else _build_no_wa_message(summarized_result.get('cas_ids', []))
                    ),
                    'semantic_workarounds_list': semantic_workarounds_list if semantic_workarounds_list else 'No semantic matches found',
                    'similar_srs': similar_srs,
                    
                    # Summarized semantic workaround (for UI display)
                    'summarized_semantic_workaround': sanitize_for_json(
                        summarized_result.get('summary', '') if summarized_result.get('success')
                        else _build_no_wa_message(summarized_result.get('cas_ids', []))
                    ),
                    'has_summarized_workaround': summarized_result.get('success', False),
                    'no_recorded_workarounds': summarized_result.get('no_recorded_workarounds', False),
                    'similar_sr_count': summarized_result.get('similar_count', 0),
                    'similar_cas_ids': summarized_result.get('cas_ids', []),
                    
                    # Known workaround from JSON knowledge base (high priority)
                    'known_workaround': sanitize_for_json(known_workaround.get('workaround', '')) if known_workaround else None,
                    'known_workaround_sr': known_workaround.get('sr_id', '') if known_workaround else None,
                    'known_workaround_match_score': round(known_workaround.get('match_score', 0) * 100, 1) if known_workaround else None,
                    'known_workaround_category': known_workaround.get('category', '') if known_workaround else None,
                    'known_workaround_rca': sanitize_for_json(known_workaround.get('rca', '')) if known_workaround else None,
                    'has_known_workaround': bool(known_workaround),
                    
                    # Resolution categorization
                    'resolution_categorization': concatenate_categorization_fields(vs_result, 'vector_store'),
                    'resolution_categorization_display': concatenate_categorization_fields(vs_result, 'vector_store'),
                    'sla_resolution_display': sla_resolution_display,
                    
                    'age_info': age_info
                }
            }
            return jsonify(response)
        
        # Fallback to Excel search
        excel_result, filename = search_latest_admin_upload_only(sr_id)
        
        if excel_result is not None:
            response = {
                'success': True,
                'source': 'excel_temp',
                'filename': filename,
                'sr': {
                    'sr_id': safe_get(excel_result, ['SR ID', 'Call ID'], sr_id),
                    'description': sanitize_for_json(safe_get(excel_result, ['Description', 'Problem Description'], 'N/A')),
                    # 'summary' field removed - using notes from wl_summary
                    'notes': sanitize_for_json(safe_get(excel_result, ['WL_Summary', 'Notes'], 'N/A')),
                    'priority': sanitize_for_json(safe_get(excel_result, ['Priority', 'Customer Priority'], 'P3')),
                    'status': sanitize_for_json(safe_get(excel_result, ['Status', 'SR Status'], 'N/A')),
                    'current_assignee': sanitize_for_json(safe_get(excel_result, ['Current Assignee', 'Assignee'], 'N/A')),
                    'ai_workaround': sanitize_for_json(safe_get(excel_result, ['AI Generated Workaround', 'AI Workaround'], 'N/A')),
                    'semantic_workaround': sanitize_for_json(safe_get(excel_result, ['Semantic Workaround', 'Similar SR Workaround'], 'N/A')),
                    'user_corrected_workaround': '',
                    'resolution_categorization': concatenate_categorization_fields(dict(excel_result), 'excel_temp')
                }
            }
            return jsonify(response)
        
        return jsonify({
            'success': False,
            'error': f'SR {sr_id} not found in system. Please verify the SR ID.'
        }), 404
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': f'Search error: {str(e)}'}), 500


@user_bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback on workaround"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        is_correct = data.get('is_satisfied', data.get('is_correct', True))
        # Support both 'corrected_workaround' (from frontend) and 'correction' (legacy)
        correction = data.get('corrected_workaround', data.get('correction', '')).strip()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        feedback_manager = get_feedback_manager()
        if feedback_manager:
            # Pass correct parameters to add_feedback
            feedback_manager.add_feedback(
                sr_id=sr_id,
                original_description=data.get('original_description', data.get('description', '')),
                original_notes=data.get('original_notes', data.get('notes', '')),
                original_workaround=data.get('original_workaround', ''),
                user_corrected_workaround=correction,
                corrected_by=data.get('corrected_by', 'user')
            )
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully!'
        })
        
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@user_bp.route('/feedback_stats', methods=['GET'])
def feedback_stats():
    """Get feedback statistics"""
    feedback_manager = get_feedback_manager()
    if feedback_manager:
        stats = feedback_manager.get_statistics()
        return jsonify(stats)
    return jsonify({'total_feedback': 0, 'corrected': 0})


@user_bp.route('/api/mark_sr_done', methods=['POST'])
@user_login_required
def mark_sr_done():
    """
    Mark an SR as Done/Resolved.
    Updates both ChromaDB and Excel file so load calculations are updated.
    """
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip().upper()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        # Get logged-in user for audit
        logged_in_user = session.get('user_username', session.get('admin_username', 'User'))
        
        updated_chromadb = False
        updated_excel = False
        
        # 1. Update ChromaDB
        try:
            from RAG.utils.history_db_manager import HistoryDatabaseManager
            import chromadb
            
            hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
            
            if hist_manager.use_chromadb and hist_manager.chromadb_collection:
                results = hist_manager.chromadb_collection.get(
                    where={"call_id": sr_id},
                    include=["metadatas", "documents", "embeddings"]
                )
                
                if results and results['ids']:
                    record_id = results['ids'][0]
                    old_doc = results['documents'][0] if results['documents'] else ''
                    old_embedding = results['embeddings'][0] if results.get('embeddings') else None
                    
                    # Update metadata with Resolved status
                    updated_metadata = results['metadatas'][0].copy()
                    updated_metadata['status'] = 'Resolved'
                    updated_metadata['Status'] = 'Resolved'
                    updated_metadata['marked_done_by'] = logged_in_user
                    updated_metadata['marked_done_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Delete and re-add (ChromaDB update pattern)
                    hist_manager.chromadb_collection.delete(ids=[record_id])
                    hist_manager.chromadb_collection.add(
                        ids=[record_id],
                        embeddings=[old_embedding] if old_embedding else None,
                        documents=[old_doc],
                        metadatas=[updated_metadata]
                    )
                    updated_chromadb = True
                    logger.info(f"Marked SR {sr_id} as Done in ChromaDB by {logged_in_user}")
        except Exception as e:
            logger.warning(f"ChromaDB update failed for {sr_id}: {e}")
        
        # 2. Update Excel file (today's output file)
        try:
            today_str = datetime.now().strftime('%Y%m%d')
            output_dir = Path(REPORTS_DIR)
            
            if output_dir.exists():
                matching_files = [f for f in output_dir.iterdir() 
                                if f.name.startswith(f'Admin_Upload_{today_str}') and f.suffix == '.xlsx']
                
                for excel_file in matching_files:
                    try:
                        df = pd.read_excel(excel_file)
                        
                        # Find SR ID column
                        sr_id_col = None
                        for col in ['SR ID', 'Call ID', 'call_id', 'sr_id']:
                            if col in df.columns:
                                sr_id_col = col
                                break
                        
                        # Find Status column
                        status_col = None
                        for col in ['Status', 'status', 'SR Status']:
                            if col in df.columns:
                                status_col = col
                                break
                        
                        if sr_id_col:
                            mask = df[sr_id_col].astype(str).str.upper().str.strip() == sr_id
                            if mask.any():
                                # Update status if column exists, otherwise add it
                                if status_col:
                                    df.loc[mask, status_col] = 'Resolved'
                                else:
                                    df.loc[mask, 'Status'] = 'Resolved'
                                
                                df.to_excel(excel_file, index=False, engine='openpyxl')
                                updated_excel = True
                                logger.info(f"Marked SR {sr_id} as Done in Excel: {excel_file.name}")
                    except Exception as e:
                        logger.warning(f"Error updating {excel_file.name}: {e}")
        except Exception as e:
            logger.warning(f"Excel update failed for {sr_id}: {e}")
        
        if not updated_chromadb and not updated_excel:
            return jsonify({'success': False, 'error': f'SR {sr_id} not found'}), 404
        
        return jsonify({
            'success': True,
            'message': f'SR {sr_id} marked as Done',
            'sr_id': sr_id,
            'updated_chromadb': updated_chromadb,
            'updated_excel': updated_excel
        })
        
    except Exception as e:
        logger.error(f"Mark SR done error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


