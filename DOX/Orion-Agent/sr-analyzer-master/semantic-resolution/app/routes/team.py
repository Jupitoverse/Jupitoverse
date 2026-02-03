#!/usr/bin/env python3
"""
Team Routes Blueprint
Handles team management, skills, and assignments
"""

from flask import Blueprint, render_template, request, jsonify
import os
import logging
import sqlite3
from datetime import datetime

from app.utils.decorators import login_required
from app.utils.state import BASE_DIR, VECTOR_STORE_DIR, CHROMADB_PATH, DATABASE_DIR

logger = logging.getLogger(__name__)

team_bp = Blueprint('team', __name__)


@team_bp.route('/skill', methods=['GET'])
def skill_page():
    """Team skills management page"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        # Get all team members using correct method
        team_members = db.get_all_people()
        
        # Sort team members alphabetically by name
        team_members = sorted(team_members, key=lambda x: x.get('name', '').lower())
        
        # Get team configuration for skills
        config = db.get_team_configuration()
        
        # Build member skills from configuration
        member_skills = {}
        all_skills = set()
        for member_name, member_data in config.items():
            member_skills[member_name] = []
            for app, app_data in member_data.get('applications', {}).items():
                skill_info = {
                    'application': app,
                    'skill_level': app_data.get('skill_level', 3.0),
                    'max_load': app_data.get('max_load', 10),
                    'specializations': app_data.get('specializations', [])
                }
                member_skills[member_name].append(skill_info)
                all_skills.add(app)
        
        return render_template('team/skill_view.html', 
                             team_members=team_members,
                             all_skills=list(all_skills),
                             member_skills=member_skills,
                             total_members=len(team_members))
                             
    except Exception as e:
        logger.error(f"Skill page error: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('team/skill_view.html', 
                             team_members=[],
                             all_skills=[],
                             member_skills={},
                             error=str(e))


def get_people_data():
    """Helper function to get all team members with current load"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        import pandas as pd
        from pathlib import Path
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        team_members = db.get_all_people()
        
        # Sort team members alphabetically by name
        team_members = sorted(team_members, key=lambda x: x.get('name', '').lower())
        
        # Get team configuration for skills
        config = db.get_team_configuration()
        
        # Calculate current load from today's Excel file (same source as Today page)
        today = datetime.now().strftime('%Y-%m-%d')
        date_for_file = datetime.now().strftime('%Y%m%d')
        assignment_counts = {}  # {member_name: count}
        
        try:
            output_dir = Path(BASE_DIR) / 'output' / 'reports'
            if output_dir.exists():
                # Find files matching today's date
                matching_files = [f for f in output_dir.iterdir() 
                                if f.name.startswith(f'Admin_Upload_{date_for_file}') and f.suffix == '.xlsx']
                
                if matching_files:
                    # Get the most recent file for today
                    matching_files.sort(key=lambda x: x.name, reverse=True)
                    latest_file = matching_files[0]
                    
                    logger.info(f"Counting assignments from: {latest_file.name}")
                    
                    df = pd.read_excel(latest_file)
                    
                    # Find status column
                    status_col = None
                    for col in ['Status', 'status', 'SR Status']:
                        if col in df.columns:
                            status_col = col
                            break
                    
                    for _, row in df.iterrows():
                        assigned_to = str(row.get('Assigned To', '')).strip()
                        # Skip empty, 'nan', 'Not Assigned' values
                        if assigned_to and assigned_to.lower() not in ['nan', 'not assigned', 'none', '']:
                            # Skip Done/Resolved/Closed SRs - they don't count toward load
                            if status_col:
                                status = str(row.get(status_col, '')).strip().lower()
                                if status in ['done', 'resolved', 'closed', 'completed']:
                                    continue
                            assignment_counts[assigned_to] = assignment_counts.get(assigned_to, 0) + 1
                    
                    logger.info(f"Today's assignment counts from Excel (excluding Done): {assignment_counts}")
                else:
                    logger.warning(f"No files found for today: {date_for_file}")
        except Exception as e:
            logger.warning(f"Could not calculate loads from Excel: {e}")
            import traceback
            traceback.print_exc()
        
        # Map field names for frontend compatibility
        for member in team_members:
            # Frontend expects 'availability_percent' but database returns 'current_availability'
            member['availability_percent'] = member.get('current_availability', 100)
            
            member_name = member.get('name', '')
            
            # Include current load for capacity display
            member['current_load'] = assignment_counts.get(member_name, 0)
            
            # Get max_load from member data (already fetched from skills table) or default to 10
            member['max_load'] = member.get('max_load', 10)
            
            # Add skills array for each member and update max_load from config if higher
            member['skills'] = []
            if member_name in config:
                member_data = config[member_name]
                for app, app_data in member_data.get('applications', {}).items():
                    app_max_load = app_data.get('max_load', 10)
                    member['max_load'] = max(member['max_load'], app_max_load)  # Use highest max_load
                    member['skills'].append({
                        'application': app,
                        'skill_level': app_data.get('skill_level', 3.0),
                        'max_load': app_max_load
                    })
            
            # Calculate capacity status
            member['at_capacity'] = member['current_load'] >= member['max_load']
            member['display'] = f"{member_name} ({member['current_load']}/{member['max_load']})"
        
        return jsonify({
            'success': True,
            'people': team_members,
            'total_members': len(team_members)
        })
        
    except Exception as e:
        logger.error(f"Get people error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/api/get_people', methods=['GET'])
def get_people_api():
    """Get all team members - public API for team page"""
    return get_people_data()


@team_bp.route('/admin/get_people', methods=['GET'])
@login_required
def get_people():
    """Get all team members (admin route - requires login)"""
    return get_people_data()


@team_bp.route('/admin/get_team_members', methods=['GET'])
@login_required
def get_team_members():
    """Get active team members for assignment"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        # get_all_people returns only active members by default
        team_members = db.get_all_people()
        
        # Sort team members alphabetically by name
        team_members = sorted(team_members, key=lambda x: x.get('name', '').lower())
        
        return jsonify({
            'success': True,
            'members': team_members
        })
        
    except Exception as e:
        logger.error(f"Get team members error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/set_availability', methods=['POST'])
@login_required
def set_availability():
    """Set team member availability"""
    try:
        data = request.json
        member_name = data.get('member_name', '')
        
        # Get availability_percent directly from request (not boolean 'available')
        availability_percent = int(data.get('availability_percent', 100))
        availability_type = data.get('availability_type', 'full_day')
        reason = data.get('reason', '')
        end_date = data.get('end_date')
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        db.set_member_availability(
            member_name=member_name,
            availability_percent=availability_percent,
            availability_type=availability_type,
            reason=reason,
            end_date=end_date
        )
        
        logger.info(f"Set availability for {member_name}: {availability_percent}% ({availability_type})")
        
        return jsonify({
            'success': True,
            'message': f'Availability set to {availability_percent}%'
        })
        
    except Exception as e:
        logger.error(f"Set availability error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/add_member', methods=['POST'])
@login_required
def add_member():
    """Add a new team member with skills"""
    try:
        data = request.json
        member_name = data.get('member_name', '').strip()
        application = data.get('application', 'SOM_MM')
        skill_level = float(data.get('skill_level', 3.0))
        specializations = data.get('specializations', '')
        max_load = int(data.get('max_load', 10))
        email = data.get('email', '').strip()
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        # Validate email format
        if email and not email.lower().endswith('@amdocs.com'):
            return jsonify({'success': False, 'error': 'Email must end with @amdocs.com'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        if db.add_member_with_skills(member_name, application, skill_level, specializations, max_load, email):
            logger.info(f"Added new team member: {member_name} with email: {email} and {application} skill")
            return jsonify({
                'success': True,
                'message': f'Team member "{member_name}" added successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Member "{member_name}" already exists or could not be added'
            }), 400
        
    except Exception as e:
        logger.error(f"Add member error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/update_email', methods=['POST'])
@login_required
def update_email():
    """Update a team member's email address"""
    try:
        data = request.json
        member_name = data.get('member_name', '').strip()
        new_email = data.get('email', '').strip()
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        if not new_email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Validate email format
        if not new_email.lower().endswith('@amdocs.com'):
            return jsonify({'success': False, 'error': 'Email must end with @amdocs.com'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        if db.update_member_email(member_name, new_email):
            logger.info(f"Updated email for {member_name} to {new_email}")
            return jsonify({
                'success': True,
                'message': f'Email updated to "{new_email}"'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Could not update email for "{member_name}"'
            }), 400
        
    except Exception as e:
        logger.error(f"Update email error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/remove_member', methods=['POST'])
@login_required
def remove_member():
    """Remove a team member (set to inactive)"""
    try:
        data = request.json
        member_name = data.get('member_name', '').strip()
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        if db.remove_member(member_name):
            logger.info(f"Removed team member: {member_name}")
            return jsonify({
                'success': True,
                'message': f'Team member "{member_name}" removed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Member "{member_name}" not found'
            }), 404
        
    except Exception as e:
        logger.error(f"Remove member error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/delete_member', methods=['POST'])
@login_required
def delete_member():
    """Alias for remove_member - frontend uses delete_member"""
    return remove_member()


@team_bp.route('/admin/get_member_skills', methods=['GET'])
@login_required
def get_member_skills():
    """Get skills for a specific team member"""
    try:
        member_name = request.args.get('member_name', '')
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        # Get team configuration and extract skills for this member
        config = db.get_team_configuration()
        
        skills = []
        if member_name in config:
            member_data = config[member_name]
            for app, app_data in member_data.get('applications', {}).items():
                skills.append({
                    'application': app,
                    'skill_level': app_data.get('skill_level', 3.0),
                    'max_load': app_data.get('max_load', 10),
                    'specializations': app_data.get('specializations', []),
                    'confidence_score': app_data.get('confidence_score', 0.5)
                })
        
        return jsonify({
            'success': True,
            'skills': skills
        })
        
    except Exception as e:
        logger.error(f"Get member skills error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/save_skill', methods=['POST'])
@login_required
def save_skill():
    """Save or update a skill for a team member"""
    try:
        data = request.json
        member_name = data.get('member_name', '')
        application = data.get('application', 'SOM_MM')
        skill_level = float(data.get('skill_level', 3.0))
        specializations = data.get('specializations', '')
        max_load = int(data.get('max_load', 10))
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        # Use update_member_config_via_chat to update skill
        updates = {
            'application': application,
            'skill_level': skill_level,
            'specializations': specializations,
            'max_load': max_load
        }
        
        success = db.update_member_config_via_chat(member_name, updates, changed_by='ADMIN')
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Skill saved'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save skill'
            }), 500
        
    except Exception as e:
        logger.error(f"Save skill error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/remove_skill', methods=['POST'])
@login_required
def remove_skill():
    """Remove a skill from a team member"""
    try:
        data = request.json
        member_name = data.get('member_name', '')
        application = data.get('application', '')
        
        if not member_name or not application:
            return jsonify({'success': False, 'error': 'Member name and application required'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        import sqlite3
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        # Direct SQL delete since there's no remove method
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM skills 
            WHERE member_id = (SELECT id FROM team_members WHERE name = ?) 
            AND application = ?
        ''', (member_name, application))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if deleted:
            return jsonify({
                'success': True,
                'message': f'Skill {application} removed from {member_name}'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Skill {application} not found for {member_name}'
            }), 404
        
    except Exception as e:
        logger.error(f"Remove skill error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/update_sr_assignment', methods=['POST'])
@login_required
def update_sr_assignment():
    """Update SR assignment in the database AND Excel file"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        # Accept both 'new_assignee' and 'assigned_to' field names
        new_assignee = data.get('new_assignee', data.get('assigned_to', '')).strip()
        
        if not sr_id or not new_assignee:
            return jsonify({'success': False, 'error': 'SR ID and assignee required'}), 400
        
        import chromadb
        import pandas as pd
        from pathlib import Path
        
        sr_id_upper = sr_id.upper().strip()
        updated_chromadb = False
        updated_excel = False
        
        # 1. Update ChromaDB
        try:
            client = chromadb.PersistentClient(path=str(CHROMADB_PATH))
            
            for collection_name in ['clean_history_data', 'sr_history', 'history_data']:
                try:
                    collection = client.get_collection(collection_name)
                    results = collection.get(
                        where={"call_id": sr_id_upper},
                        include=["metadatas", "documents"]
                    )
                    
                    if results and results['ids']:
                        doc_id = results['ids'][0]
                        old_metadata = results['metadatas'][0] if results['metadatas'] else {}
                        old_metadata['assigned_to'] = new_assignee
                        old_metadata['current_assignee'] = new_assignee
                        old_metadata['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        collection.update(ids=[doc_id], metadatas=[old_metadata])
                        updated_chromadb = True
                        logger.info(f"Updated {sr_id} in ChromaDB collection {collection_name}")
                        break
                except:
                    continue
        except Exception as e:
            logger.warning(f"ChromaDB update failed: {e}")
        
        # 2. Update Excel file (today's output file)
        try:
            output_dir = Path(BASE_DIR) / 'output' / 'reports'
            today_str = datetime.now().strftime('%Y%m%d')
            
            if output_dir.exists():
                # Find today's Excel files
                matching_files = [f for f in output_dir.iterdir() 
                                if f.name.startswith(f'Admin_Upload_{today_str}') and f.suffix == '.xlsx']
                
                for excel_file in matching_files:
                    try:
                        df = pd.read_excel(excel_file)
                        
                        # Find the SR ID column
                        sr_id_col = None
                        for col in ['SR ID', 'Call ID', 'call_id', 'sr_id']:
                            if col in df.columns:
                                sr_id_col = col
                                break
                        
                        # Find the Assigned To column
                        assigned_col = None
                        for col in ['Assigned To', 'assigned_to', 'Assignee', 'Current Assignee']:
                            if col in df.columns:
                                assigned_col = col
                                break
                        
                        if sr_id_col and assigned_col:
                            # Update the assignment
                            mask = df[sr_id_col].astype(str).str.upper().str.strip() == sr_id_upper
                            if mask.any():
                                df.loc[mask, assigned_col] = new_assignee
                                df.to_excel(excel_file, index=False)
                                updated_excel = True
                                logger.info(f"Updated {sr_id} in Excel file {excel_file.name}")
                    except Exception as e:
                        logger.warning(f"Error updating {excel_file.name}: {e}")
        except Exception as e:
            logger.warning(f"Excel update failed: {e}")
        
        if not updated_chromadb and not updated_excel:
            return jsonify({'success': False, 'error': f'SR {sr_id} not found'}), 404
        
        return jsonify({
            'success': True,
            'message': f'SR {sr_id} assigned to {new_assignee}',
            'new_assignee': new_assignee,
            'updated_chromadb': updated_chromadb,
            'updated_excel': updated_excel
        })
        
    except Exception as e:
        logger.error(f"Update assignment error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@team_bp.route('/admin/batch_reassign_unassigned', methods=['POST'])
@login_required
def batch_reassign_unassigned():
    """
    Re-assign ALL SRs uploaded today using LLM CALL 5 (skill-based assignment).
    This will reassign ALL today's SRs, not just unassigned ones.
    """
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        from team.people_skills_database import PeopleSkillsDatabase
        import sys
        from pathlib import Path
        
        # Add RAG path for imports
        rag_path = Path(BASE_DIR) / 'RAG' / 'rag'
        if str(rag_path) not in sys.path:
            sys.path.insert(0, str(rag_path))
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Connect to ChromaDB
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        if not hist_manager.use_chromadb:
            return jsonify({'success': False, 'error': 'Could not connect to ChromaDB'}), 500
        
        # Get all SRs from ChromaDB with IDs for later update
        try:
            all_records = hist_manager.chromadb_collection.get(include=['metadatas', 'documents', 'embeddings'])
            metadata_list = all_records.get('metadatas', [])
            ids_list = all_records.get('ids', [])
            docs_list = all_records.get('documents', [])
            embeddings_list = all_records.get('embeddings', [])
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return jsonify({'success': False, 'error': 'ChromaDB query failed'}), 500
        
        # Filter for ALL today's SRs (not just unassigned - reassign everything)
        # Store record_id, document, embedding along with metadata for updates
        todays_srs = []
        for i, sr in enumerate(metadata_list):
            if sr is None:
                continue
            sr_date = sr.get('added_date', '') or sr.get('opened_date', '') or sr.get('Reported Date', '')
            
            # Check if it's today - include ALL SRs regardless of current assignment
            if sr_date and sr_date.startswith(today):
                # Store the ChromaDB record ID, document, and embedding for later update
                sr['_chromadb_id'] = ids_list[i] if i < len(ids_list) else None
                sr['_chromadb_doc'] = docs_list[i] if docs_list and i < len(docs_list) else ''
                sr['_chromadb_embedding'] = embeddings_list[i] if embeddings_list and i < len(embeddings_list) else None
                todays_srs.append(sr)
        
        if not todays_srs:
            return jsonify({
                'success': True, 
                'message': 'No SRs found for today',
                'assigned_count': 0,
                'distribution': {}
            })
        
        # SORT BY: 1) Aging SRs first, 2) Priority (P1 first)
        # Aging SR conditions: Category is EOM-related, or Priority P2/P3, or Age > 3 days
        def get_sr_sort_key(sr):
            # Check if aging
            is_aging = sr.get('is_aging', False)
            if not is_aging:
                # Calculate aging if not already set
                priority = str(sr.get('priority', 'P3')).upper()
                age_days = sr.get('age_days', 0) or 0
                category = str(sr.get('categorization_tier3', '') or sr.get('category', '')).lower()
                aging_categories = ['ops eom', 'potential ops eom', 'sales eom', 'potential sales eom']
                is_aging_category = any(cat in category for cat in aging_categories)
                is_aging_priority = priority in ['P2', 'P3']
                is_over_age = age_days > 3 if isinstance(age_days, (int, float)) else False
                is_aging = is_aging_category or is_aging_priority or is_over_age
            
            # Priority order
            priority_order = {'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4, '': 5}
            priority_rank = priority_order.get(str(sr.get('priority', 'P3')).upper(), 5)
            
            # Sort key: (not aging=1/aging=0, priority rank) - aging first, then by priority
            return (0 if is_aging else 1, priority_rank)
        
        todays_srs.sort(key=get_sr_sort_key)
        
        # Count aging vs non-aging for logging
        aging_count = sum(1 for sr in todays_srs if get_sr_sort_key(sr)[0] == 0)
        logger.info(f"[BATCH] Sorted {len(todays_srs)} SRs: {aging_count} AGING first, then by priority (P1→P4)")
        
        # Initialize LLM for skill-based assignment
        try:
            from RAG.pipeline.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
            pipeline = MultiModelSRPipeline()
            logger.info(f"[BATCH] Initialized RAG pipeline for {len(todays_srs)} today's SRs (reassigning all)")
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")
            # Fallback to simple round-robin if LLM unavailable
            return _fallback_batch_assignment(todays_srs, hist_manager)
        
        # Process each SR (reassign all today's SRs)
        assigned_count = 0
        distribution = {}
        errors = []
        
        for idx, sr in enumerate(todays_srs, 1):
            try:
                sr_id = sr.get('call_id', 'Unknown')
                priority = sr.get('priority', 'P3')
                application = sr.get('application', 'Unknown')
                is_aging = sr.get('is_aging', False)
                age_days = sr.get('age_days', 0)
                
                # Log SR details before assignment
                aging_tag = "🔴 AGING" if is_aging else "🟢 Normal"
                logger.info(f"[BATCH] [{idx}/{len(todays_srs)}] Processing {sr_id}: {aging_tag} | Priority={priority} | App={application} | Age={age_days}d")
                
                # Build SR data for LLM
                sr_data = {
                    'SR ID': sr_id,
                    'Priority': priority,
                    'Description': sr.get('description', ''),
                    'Notes': sr.get('notes', ''),
                    'Application': application
                }
                
                # Determine if Java error (from stored data or default to False)
                is_java_error = sr.get('is_java_error', 'No') == 'Yes'
                issue_type = sr.get('issue_type', 'Unknown')
                
                # Call LLM CALL 5: Skill-based assignment
                assigned_to = pipeline._llm_skill_assignment(sr_data, is_java_error, issue_type)
                
                if assigned_to and assigned_to != 'UNASSIGNED':
                    # Update SR dict for Excel update later
                    sr['current_assignee'] = assigned_to
                    sr['assigned_to'] = assigned_to
                    sr['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Update SR in ChromaDB - use stored IDs from initial query
                    record_id = sr.get('_chromadb_id')
                    old_doc = sr.get('_chromadb_doc', '')
                    old_embedding = sr.get('_chromadb_embedding')
                    
                    if record_id:
                        # Actually persist to ChromaDB using stored ID
                        try:
                            # Update metadata (remove our internal fields first)
                            updated_metadata = {k: v for k, v in sr.items() if not k.startswith('_chromadb_')}
                            
                            # Delete and re-add (ChromaDB update pattern)
                            hist_manager.chromadb_collection.delete(ids=[record_id])
                            hist_manager.chromadb_collection.add(
                                ids=[record_id],
                                embeddings=[old_embedding] if old_embedding else None,
                                documents=[old_doc],
                                metadatas=[updated_metadata]
                            )
                            logger.info(f"[BATCH] ChromaDB updated for {sr_id}")
                        except Exception as chroma_err:
                            logger.warning(f"[BATCH] ChromaDB update failed for {sr_id}: {chroma_err}")
                    else:
                        logger.warning(f"[BATCH] No ChromaDB record ID found for {sr_id} - Excel will be updated")
                    
                    assigned_count += 1
                    distribution[assigned_to] = distribution.get(assigned_to, 0) + 1
                    logger.info(f"[BATCH] Assigned {sr_id} to {assigned_to}")
                else:
                    errors.append(f"{sr_id}: No suitable assignee found")
                    
            except Exception as e:
                logger.error(f"Error assigning SR {sr.get('call_id', 'Unknown')}: {e}")
                errors.append(f"{sr.get('call_id', 'Unknown')}: {str(e)}")
        
        # Save all updates to ChromaDB
        if assigned_count > 0:
            hist_manager.save_database()
            
            # Also update the Excel file so UI shows updated assignments
            try:
                import pandas as pd
                today_str = datetime.now().strftime('%Y%m%d')
                output_dir = Path(BASE_DIR) / 'output' / 'reports'
                
                if output_dir.exists():
                    # Find today's output file
                    today_files = [f for f in output_dir.iterdir() 
                                  if f.name.startswith(f'Admin_Upload_{today_str}') and f.suffix == '.xlsx']
                    
                    if today_files:
                        today_files.sort(key=lambda x: x.name, reverse=True)
                        excel_path = today_files[0]
                        
                        # Read the Excel file
                        df = pd.read_excel(excel_path)
                        
                        # Find SR ID and Assigned To columns
                        sr_col = None
                        for col in ['SR ID', 'Call ID', 'call_id', 'sr_id']:
                            if col in df.columns:
                                sr_col = col
                                break
                        
                        assign_col = None
                        for col in ['Assigned To', 'assigned_to', 'Assignee']:
                            if col in df.columns:
                                assign_col = col
                                break
                        
                        if sr_col and assign_col:
                            # Update assignments in DataFrame
                            updates_made = 0
                            for sr in todays_srs:
                                sr_id = sr.get('call_id', '')
                                new_assignee = sr.get('assigned_to', sr.get('current_assignee', ''))
                                
                                if sr_id and new_assignee:
                                    mask = df[sr_col].astype(str).str.upper() == str(sr_id).upper()
                                    if mask.any():
                                        df.loc[mask, assign_col] = new_assignee
                                        updates_made += 1
                            
                            # Save updated Excel
                            df.to_excel(excel_path, index=False, engine='openpyxl')
                            logger.info(f"[BATCH] Updated {updates_made} assignments in Excel: {excel_path.name}")
                        else:
                            logger.warning(f"[BATCH] Could not find SR ID or Assigned To column in Excel")
                    else:
                        logger.warning(f"[BATCH] No Excel file found for today ({today_str})")
            except Exception as excel_err:
                logger.error(f"[BATCH] Error updating Excel file: {excel_err}")
                # Don't fail the request - ChromaDB was updated successfully
        
        return jsonify({
            'success': True,
            'message': f'Reassigned {assigned_count} of {len(todays_srs)} today\'s SRs',
            'assigned_count': assigned_count,
            'total_today': len(todays_srs),
            'distribution': distribution,
            'errors': errors if errors else None
        })
        
    except Exception as e:
        logger.error(f"Batch reassign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


def _fallback_batch_assignment(unassigned_srs, hist_manager):
    """Fallback round-robin assignment when LLM is unavailable"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        import pandas as pd
        from pathlib import Path
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        team_members = db.get_all_people()
        
        # Filter active members with availability
        available = [m for m in team_members if m.get('status') == 'active']
        
        if not available:
            return jsonify({
                'success': False, 
                'error': 'No available team members for assignment'
            }), 400
        
        # Simple round-robin
        distribution = {}
        assigned_count = 0
        
        for i, sr in enumerate(unassigned_srs):
            assignee = available[i % len(available)]['name']
            sr_id = sr.get('call_id', '')
            
            sr['current_assignee'] = assignee
            sr['assigned_to'] = assignee
            sr['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Actually persist to ChromaDB using stored IDs from initial query
            record_id = sr.get('_chromadb_id')
            old_doc = sr.get('_chromadb_doc', '')
            old_embedding = sr.get('_chromadb_embedding')
            
            if record_id and hist_manager.chromadb_collection:
                try:
                    # Update metadata (remove our internal fields first)
                    updated_metadata = {k: v for k, v in sr.items() if not k.startswith('_chromadb_')}
                    
                    # Delete and re-add (ChromaDB update pattern)
                    hist_manager.chromadb_collection.delete(ids=[record_id])
                    hist_manager.chromadb_collection.add(
                        ids=[record_id],
                        embeddings=[old_embedding] if old_embedding else None,
                        documents=[old_doc],
                        metadatas=[updated_metadata]
                    )
                    logger.info(f"[FALLBACK] ChromaDB updated for {sr_id}")
                except Exception as chroma_err:
                    logger.warning(f"[FALLBACK] ChromaDB update failed for {sr_id}: {chroma_err}")
            else:
                logger.warning(f"[FALLBACK] No ChromaDB record ID found for {sr_id} - Excel will be updated")
            
            distribution[assignee] = distribution.get(assignee, 0) + 1
            assigned_count += 1
        
        hist_manager.save_database()
        
        # Also update Excel file so UI shows updated assignments
        try:
            today_str = datetime.now().strftime('%Y%m%d')
            output_dir = Path(BASE_DIR) / 'output' / 'reports'
            
            if output_dir.exists():
                today_files = [f for f in output_dir.iterdir() 
                              if f.name.startswith(f'Admin_Upload_{today_str}') and f.suffix == '.xlsx']
                
                if today_files:
                    today_files.sort(key=lambda x: x.name, reverse=True)
                    excel_path = today_files[0]
                    
                    df = pd.read_excel(excel_path)
                    
                    # Find SR ID and Assigned To columns
                    sr_col = None
                    for col in ['SR ID', 'Call ID', 'call_id', 'sr_id']:
                        if col in df.columns:
                            sr_col = col
                            break
                    
                    assign_col = None
                    for col in ['Assigned To', 'assigned_to', 'Assignee']:
                        if col in df.columns:
                            assign_col = col
                            break
                    
                    if sr_col and assign_col:
                        updates_made = 0
                        for sr in unassigned_srs:
                            sr_id = sr.get('call_id', '')
                            new_assignee = sr.get('assigned_to', sr.get('current_assignee', ''))
                            
                            if sr_id and new_assignee:
                                mask = df[sr_col].astype(str).str.upper() == str(sr_id).upper()
                                if mask.any():
                                    df.loc[mask, assign_col] = new_assignee
                                    updates_made += 1
                        
                        df.to_excel(excel_path, index=False, engine='openpyxl')
                        logger.info(f"[FALLBACK] Updated {updates_made} assignments in Excel: {excel_path.name}")
        except Exception as excel_err:
            logger.error(f"[FALLBACK] Error updating Excel file: {excel_err}")
        
        return jsonify({
            'success': True,
            'message': f'[Fallback] Assigned {assigned_count} SRs using round-robin',
            'assigned_count': assigned_count,
            'distribution': distribution,
            'note': 'LLM unavailable, used round-robin assignment'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Fallback failed: {str(e)}'}), 500

