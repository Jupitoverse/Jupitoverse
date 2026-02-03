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
        
        return render_template('feedback/skill_view.html', 
                             team_members=team_members,
                             all_skills=list(all_skills),
                             member_skills=member_skills,
                             total_members=len(team_members))
                             
    except Exception as e:
        logger.error(f"Skill page error: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('feedback/skill_view.html', 
                             team_members=[],
                             all_skills=[],
                             member_skills={},
                             error=str(e))


def get_people_data():
    """Helper function to get all team members with current load"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        team_members = db.get_all_people()
        
        # Sort team members alphabetically by name
        team_members = sorted(team_members, key=lambda x: x.get('name', '').lower())
        
        # Get team configuration for skills
        config = db.get_team_configuration()
        
        # ðŸ†• Calculate current load from today's SRs in ChromaDB
        today = datetime.now().strftime('%Y-%m-%d')
        assignment_counts = {}  # {member_name: count}
        
        try:
            from RAG.utils.history_db_manager import HistoryDatabaseManager
            hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
            if hist_manager.use_chromadb:
                all_records = hist_manager.chromadb_collection.get(include=['metadatas'])
                for metadata in all_records.get('metadatas', []):
                    if metadata:
                        sr_date = metadata.get('added_date', '') or metadata.get('opened_date', '')
                        if today in str(sr_date):
                            assigned_to = metadata.get('assigned_to', '')
                            if assigned_to:
                                # Normalize name (replace underscores with spaces for consistent matching)
                                normalized_name = assigned_to.replace('_', ' ')
                                assignment_counts[normalized_name] = assignment_counts.get(normalized_name, 0) + 1
                logger.info(f"Today's assignment counts: {assignment_counts}")
        except Exception as e:
            logger.warning(f"Could not calculate loads from ChromaDB: {e}")
        
        # Map field names for frontend compatibility
        for member in team_members:
            # Frontend expects 'availability_percent' but database returns 'current_availability'
            member['availability_percent'] = member.get('current_availability', 100)
            
            member_name = member.get('name', '')
            
            # ðŸ†• Add current load info
            member['current_load'] = assignment_counts.get(member_name, 0)
            member['max_load'] = 0  # Will be set from skills config (start at 0 so max() works)
            member['at_capacity'] = member['current_load'] >= member['max_load']
            member['display'] = f"{member_name} ({member['current_load']}/{member['max_load']})"
            
            # Add skills array for each member
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
            
            # Fallback to 10 if no skills configured
            if member['max_load'] == 0:
                member['max_load'] = 10
            
            # Recalculate display with actual max_load
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
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db = PeopleSkillsDatabase(os.path.join(DATABASE_DIR, 'people_skills.db'))
        
        if db.add_member_with_skills(member_name, application, skill_level, specializations, max_load):
            logger.info(f"Added new team member: {member_name} with {application} skill")
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
    """Update SR assignment in the database"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        # Support both field names (frontend uses assigned_to)
        new_assignee = data.get('new_assignee', '') or data.get('assigned_to', '')
        new_assignee = new_assignee.strip() if new_assignee else '' 
        
        if not sr_id or not new_assignee:
            return jsonify({'success': False, 'error': 'SR ID and assignee required'}), 400
        
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        if not hist_manager.use_chromadb:
            return jsonify({'success': False, 'error': 'Could not connect to ChromaDB'}), 500
        
        # Find and update SR
        metadata_list = hist_manager.db_data.get('metadata', [])
        sr_id_upper = sr_id.upper().strip()
        updated = False
        
        for sr in metadata_list:
            if str(sr.get('call_id', '')).upper().strip() == sr_id_upper:
                sr['current_assignee'] = new_assignee
                sr['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                updated = True
                break
        
        if not updated:
            return jsonify({'success': False, 'error': f'SR {sr_id} not found'}), 404
        
        hist_manager.save_database()
        
        logger.info(f"Updated assignment for {sr_id} to {new_assignee}")
        return jsonify({
            'success': True,
            'message': f'SR {sr_id} assigned to {new_assignee}'
        })
        
    except Exception as e:
        logger.error(f"Update assignment error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500






@team_bp.route('/admin/batch_reassign_unassigned', methods=['POST'])
@login_required
def batch_reassign_unassigned():
    """
    Re-assign ALL today's SRs using LLM CALL 5 (skill-based assignment)
    This reassigns every SR uploaded today, not just unassigned ones.
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
        
        # Get all SRs from ChromaDB
        try:
            all_records = hist_manager.chromadb_collection.get(include=['metadatas'])
            metadata_list = all_records.get('metadatas', [])
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return jsonify({'success': False, 'error': 'ChromaDB query failed'}), 500
        
        # Filter for ALL today's SRs (reassign all, not just unassigned)
        todays_srs = []
        for sr in metadata_list:
            if sr is None:
                continue
            sr_date = sr.get('added_date', '') or sr.get('opened_date', '') or sr.get('Reported Date', '')
            
            # Get ALL SRs from today for reassignment
            if sr_date and sr_date.startswith(today):
                todays_srs.append(sr)
        
        if not todays_srs:
            return jsonify({
                'success': True, 
                'message': 'No SRs found for today',
                'assigned_count': 0,
                'distribution': {}
            })
        
        # Initialize LLM for skill-based assignment
        try:
            from multi_model_rag_pipeline_chatgpt import MultiModelRAGPipeline
            pipeline = MultiModelRAGPipeline()
            logger.info(f"[BATCH] Initialized RAG pipeline for {len(todays_srs)} SRs")
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")
            # Fallback to simple round-robin if LLM unavailable
            return _fallback_batch_assignment(todays_srs, hist_manager)
        
        # Process each SR (reassign all)
        assigned_count = 0
        distribution = {}
        errors = []
        
        for sr in todays_srs:
            try:
                sr_id = sr.get('call_id', 'Unknown')
                
                # Build SR data for LLM
                sr_data = {
                    'SR ID': sr_id,
                    'Priority': sr.get('priority', 'P3'),
                    'Description': sr.get('description', ''),
                    'Notes': sr.get('notes', ''),
                    'Application': sr.get('application', 'Unknown')
                }
                
                # Determine if Java error (from stored data or default to False)
                is_java_error = sr.get('is_java_error', 'No') == 'Yes'
                issue_type = sr.get('issue_type', 'Unknown')
                
                # Call LLM CALL 5: Skill-based assignment
                assigned_to = pipeline._llm_skill_assignment(sr_data, is_java_error, issue_type)
                
                if assigned_to and assigned_to != 'UNASSIGNED':
                    # Update SR in ChromaDB
                    sr['current_assignee'] = assigned_to
                    sr['assigned_to'] = assigned_to
                    sr['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
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
        
        return jsonify({
            'success': True,
            'message': f'Reassigned {assigned_count} of {len(todays_srs)} SRs',
            'assigned_count': assigned_count,
            'total_srs': len(todays_srs),
            'distribution': distribution,
            'errors': errors if errors else None
        })
        
    except Exception as e:
        logger.error(f"Batch reassign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


def _fallback_batch_assignment(todays_srs, hist_manager):
    """Fallback round-robin assignment when LLM is unavailable"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        
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
        
        for i, sr in enumerate(todays_srs):
            assignee = available[i % len(available)]['name']
            sr['current_assignee'] = assignee
            sr['assigned_to'] = assignee
            sr['assigned_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            distribution[assignee] = distribution.get(assignee, 0) + 1
            assigned_count += 1
        
        hist_manager.save_database()
        
        return jsonify({
            'success': True,
            'message': f'[Fallback] Reassigned {assigned_count} SRs using round-robin',
            'assigned_count': assigned_count,
            'distribution': distribution,
            'note': 'LLM unavailable, used round-robin assignment'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Fallback failed: {str(e)}'}), 500
