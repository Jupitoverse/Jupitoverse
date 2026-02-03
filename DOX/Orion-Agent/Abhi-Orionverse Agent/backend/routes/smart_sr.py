# backend/routes/smart_sr.py
"""
Smart SR Assignment Routes
Integrates RAG-based SR Analysis functionality into Orionverse
"""

from flask import Blueprint, jsonify, request, render_template, send_file
import sys
import os
import json
import traceback

# Add rag_module to path for imports
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
RAG_MODULE_PATH = os.path.join(PROJECT_ROOT, 'rag_module')
sys.path.insert(0, RAG_MODULE_PATH)

smart_sr_bp = Blueprint('smart_sr', __name__)

# Global variable for RAG pipeline (lazy loading)
_rag_pipeline = None
_pipeline_error = None

def get_rag_pipeline():
    """Lazy load the RAG pipeline"""
    global _rag_pipeline, _pipeline_error
    
    if _rag_pipeline is not None:
        return _rag_pipeline
    
    if _pipeline_error:
        raise _pipeline_error
    
    try:
        from RAG.pipeline.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
        _rag_pipeline = MultiModelSRPipeline()
        print("[OK] RAG Pipeline initialized successfully")
        return _rag_pipeline
    except Exception as e:
        _pipeline_error = e
        print(f"[ERROR] Failed to initialize RAG pipeline: {e}")
        raise e


@smart_sr_bp.route('/status', methods=['GET'])
def get_status():
    """Check RAG system status"""
    status = {
        "rag_module_path": RAG_MODULE_PATH,
        "rag_module_exists": os.path.exists(RAG_MODULE_PATH),
        "pipeline_status": "not_initialized",
        "vectorstore_status": "unknown",
        "database_status": "unknown"
    }
    
    # Check vectorstore
    vectorstore_path = os.path.join(RAG_MODULE_PATH, 'data', 'vectorstore', 'chromadb_store')
    status["vectorstore_status"] = "available" if os.path.exists(vectorstore_path) else "not_found"
    
    # Check database
    database_path = os.path.join(RAG_MODULE_PATH, 'data', 'database')
    status["database_status"] = "available" if os.path.exists(database_path) else "not_found"
    
    # Try to load pipeline
    try:
        get_rag_pipeline()
        status["pipeline_status"] = "ready"
    except Exception as e:
        status["pipeline_status"] = f"error: {str(e)}"
    
    return jsonify(status)


@smart_sr_bp.route('/analyze', methods=['POST'])
def analyze_sr():
    """
    Analyze a single SR using the RAG pipeline
    
    Expected JSON body:
    {
        "sr_id": "SR-12345",
        "description": "SR description text...",
        "customer_id": "CUST001",
        "category": "Billing"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        sr_id = data.get('sr_id', 'UNKNOWN')
        description = data.get('description', '')
        
        if not description:
            return jsonify({"error": "SR description is required"}), 400
        
        print(f"[ANALYZE] Processing SR: {sr_id}")
        
        # Get RAG pipeline
        pipeline = get_rag_pipeline()
        
        # Process the SR
        result = pipeline.process_sr({
            'SR_ID': sr_id,
            'DETAILS': description,
            'CUSTOMER_ID': data.get('customer_id', ''),
            'LBGUPS_Subcategory': data.get('category', ''),
            'UPDATE_DETAILS': data.get('update_details', '')
        })
        
        return jsonify({
            "success": True,
            "sr_id": sr_id,
            "analysis": result
        })
        
    except Exception as e:
        print(f"[ERROR] SR analysis failed: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@smart_sr_bp.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Analyze multiple SRs in batch
    
    Expected JSON body:
    {
        "srs": [
            {"sr_id": "SR-1", "description": "..."},
            {"sr_id": "SR-2", "description": "..."}
        ]
    }
    """
    try:
        data = request.get_json()
        srs = data.get('srs', [])
        
        if not srs:
            return jsonify({"error": "No SRs provided"}), 400
        
        print(f"[BATCH] Processing {len(srs)} SRs")
        
        pipeline = get_rag_pipeline()
        results = []
        
        for sr_data in srs:
            try:
                result = pipeline.process_sr({
                    'SR_ID': sr_data.get('sr_id', 'UNKNOWN'),
                    'DETAILS': sr_data.get('description', ''),
                    'CUSTOMER_ID': sr_data.get('customer_id', ''),
                    'LBGUPS_Subcategory': sr_data.get('category', ''),
                    'UPDATE_DETAILS': sr_data.get('update_details', '')
                })
                results.append({
                    "sr_id": sr_data.get('sr_id'),
                    "success": True,
                    "analysis": result
                })
            except Exception as e:
                results.append({
                    "sr_id": sr_data.get('sr_id'),
                    "success": False,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "total": len(srs),
            "processed": len([r for r in results if r['success']]),
            "results": results
        })
        
    except Exception as e:
        print(f"[ERROR] Batch analysis failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@smart_sr_bp.route('/team-assignment', methods=['POST'])
def get_team_assignment():
    """
    Get team assignment recommendation for an SR
    """
    try:
        data = request.get_json()
        sr_id = data.get('sr_id', 'UNKNOWN')
        category = data.get('category', '')
        complexity = data.get('complexity', 'medium')
        
        # Load team skills database
        from team.people_skills_database import PeopleSkillsDatabase
        team_db = PeopleSkillsDatabase()
        
        # Get assignment recommendation
        recommendation = team_db.get_assignment_recommendation(
            category=category,
            complexity=complexity
        )
        
        return jsonify({
            "success": True,
            "sr_id": sr_id,
            "recommendation": recommendation
        })
        
    except Exception as e:
        print(f"[ERROR] Team assignment failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@smart_sr_bp.route('/semantic-search', methods=['POST'])
def semantic_search():
    """
    Search for similar historical SRs using semantic search
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Use the RAG semantic search
        from RAG.extract_semantic_workarounds import SemanticWorkaroundExtractor
        extractor = SemanticWorkaroundExtractor()
        
        results = extractor.search_similar(query, k=limit)
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results
        })
        
    except Exception as e:
        print(f"[ERROR] Semantic search failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@smart_sr_bp.route('/workaround-suggestions', methods=['POST'])
def get_workaround_suggestions():
    """
    Get workaround suggestions based on SR description
    """
    try:
        data = request.get_json()
        description = data.get('description', '')
        category = data.get('category', '')
        
        if not description:
            return jsonify({"error": "Description is required"}), 400
        
        pipeline = get_rag_pipeline()
        
        # Get semantic workarounds
        suggestions = pipeline.find_semantic_workarounds(description, category)
        
        return jsonify({
            "success": True,
            "suggestions": suggestions
        })
        
    except Exception as e:
        print(f"[ERROR] Workaround suggestions failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@smart_sr_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get RAG system statistics"""
    try:
        stats = {
            "vectorstore_records": 0,
            "total_srs_processed": 0,
            "team_members": 0,
            "categories": []
        }
        
        # Count vectorstore records
        try:
            import chromadb
            client = chromadb.PersistentClient(
                path=os.path.join(RAG_MODULE_PATH, 'data', 'vectorstore', 'chromadb_store')
            )
            collections = client.list_collections()
            for col in collections:
                stats["vectorstore_records"] += col.count()
        except:
            pass
        
        # Get LLM usage stats
        stats_file = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'llm_usage_stats.json')
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                usage_stats = json.load(f)
                stats["total_srs_processed"] = usage_stats.get('total_calls', 0)
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# TEAM MANAGEMENT ROUTES (Smart Team)
# ============================================================

@smart_sr_bp.route('/team/members', methods=['GET'])
def get_team_members():
    """Get all team members with skills and availability"""
    try:
        from team.people_skills_database import PeopleSkillsDatabase
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        team_members = db.get_all_people()
        team_members = sorted(team_members, key=lambda x: x.get('name', '').lower())
        
        # Get skills configuration
        config = db.get_team_configuration()
        
        # Build member skills
        for member in team_members:
            member['availability_percent'] = member.get('current_availability', 100)
            member['skills'] = []
            member_name = member.get('name', '')
            
            if member_name in config:
                member_data = config[member_name]
                for app, app_data in member_data.get('applications', {}).items():
                    member['skills'].append({
                        'application': app,
                        'skill_level': app_data.get('skill_level', 3.0),
                        'max_load': app_data.get('max_load', 10)
                    })
            
            member['max_load'] = max([s.get('max_load', 10) for s in member['skills']], default=10)
            member['current_load'] = 0  # TODO: Calculate from today's assignments
        
        return jsonify({
            'success': True,
            'people': team_members,
            'total_members': len(team_members)
        })
        
    except Exception as e:
        print(f"[ERROR] Get team members failed: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/add-member', methods=['POST'])
def add_team_member():
    """Add a new team member"""
    try:
        data = request.get_json()
        member_name = data.get('member_name', '').strip()
        application = data.get('application', 'SOM_MM')
        skill_level = float(data.get('skill_level', 3.0))
        specializations = data.get('specializations', '')
        max_load = int(data.get('max_load', 10))
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        if db.add_member_with_skills(member_name, application, skill_level, specializations, max_load):
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
        print(f"[ERROR] Add member failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/remove-member', methods=['POST'])
def remove_team_member():
    """Remove a team member"""
    try:
        data = request.get_json()
        member_name = data.get('member_name', '').strip()
        
        if not member_name:
            return jsonify({'success': False, 'error': 'Member name is required'}), 400
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        if db.remove_member(member_name):
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
        print(f"[ERROR] Remove member failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/member-skills', methods=['GET'])
def get_member_skills():
    """Get skills for a specific team member"""
    try:
        member_name = request.args.get('member_name', '')
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        config = db.get_team_configuration()
        
        skills = []
        if member_name in config:
            member_data = config[member_name]
            for app, app_data in member_data.get('applications', {}).items():
                skills.append({
                    'application': app,
                    'skill_level': app_data.get('skill_level', 3.0),
                    'max_load': app_data.get('max_load', 10),
                    'specializations': app_data.get('specializations', [])
                })
        
        return jsonify({
            'success': True,
            'skills': skills
        })
        
    except Exception as e:
        print(f"[ERROR] Get member skills failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/save-skill', methods=['POST'])
def save_skill():
    """Save or update a skill for a team member"""
    try:
        data = request.get_json()
        member_name = data.get('member_name', '')
        application = data.get('application', 'SOM_MM')
        skill_level = float(data.get('skill_level', 3.0))
        specializations = data.get('specializations', '')
        max_load = int(data.get('max_load', 10))
        
        from team.people_skills_database import PeopleSkillsDatabase
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        db = PeopleSkillsDatabase(db_path)
        
        updates = {
            'application': application,
            'skill_level': skill_level,
            'specializations': specializations,
            'max_load': max_load
        }
        
        success = db.update_member_config_via_chat(member_name, updates, changed_by='ADMIN')
        
        if success:
            return jsonify({'success': True, 'message': 'Skill saved'})
        else:
            return jsonify({'success': False, 'error': 'Failed to save skill'}), 500
        
    except Exception as e:
        print(f"[ERROR] Save skill failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/remove-skill', methods=['POST'])
def remove_skill():
    """Remove a skill from a team member"""
    try:
        data = request.get_json()
        member_name = data.get('member_name', '')
        application = data.get('application', '')
        
        if not member_name or not application:
            return jsonify({'success': False, 'error': 'Member name and application required'}), 400
        
        import sqlite3
        
        db_path = os.path.join(RAG_MODULE_PATH, 'data', 'database', 'people_skills.db')
        conn = sqlite3.connect(db_path)
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
            return jsonify({'success': True, 'message': f'Skill {application} removed from {member_name}'})
        else:
            return jsonify({'success': False, 'error': f'Skill {application} not found for {member_name}'}), 404
        
    except Exception as e:
        print(f"[ERROR] Remove skill failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/team/batch-reassign', methods=['POST'])
def batch_reassign():
    """Reassign all today's SRs using AI"""
    try:
        # This requires the full RAG pipeline
        return jsonify({
            'success': True,
            'assigned_count': 0,
            'message': 'Batch reassignment feature requires RAG pipeline initialization'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# MY DASHBOARD ROUTES (User Portal)
# ============================================================

@smart_sr_bp.route('/database-info', methods=['GET'])
def get_database_info():
    """Get database info for My Dashboard"""
    try:
        chromadb_path = os.path.join(RAG_MODULE_PATH, 'data', 'vectorstore', 'chromadb_store')
        
        chromadb_count = 0
        if os.path.exists(chromadb_path):
            try:
                import chromadb
                client = chromadb.PersistentClient(path=chromadb_path)
                collections = client.list_collections()
                for col in collections:
                    chromadb_count += col.count()
            except:
                pass
        
        if chromadb_count == 0:
            return jsonify({
                'has_upload': False,
                'historical_count': 0,
                'message': 'No data available. Please contact admin.'
            })
        
        return jsonify({
            'has_upload': True,
            'historical_count': chromadb_count,
            'upload_date': 'ChromaDB',
            'message': f'Database: {chromadb_count} total SRs available'
        })
        
    except Exception as e:
        return jsonify({'has_upload': False, 'historical_count': 0, 'message': 'Error loading data'})


@smart_sr_bp.route('/search-sr', methods=['POST'])
def search_sr():
    """Search for an SR by ID"""
    try:
        data = request.get_json()
        sr_id = data.get('sr_id', '').strip()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'Please enter an SR ID'}), 400
        
        chromadb_path = os.path.join(RAG_MODULE_PATH, 'data', 'vectorstore', 'chromadb_store')
        
        try:
            import chromadb
            client = chromadb.PersistentClient(path=chromadb_path)
            
            # Try to get the main collection
            try:
                collection = client.get_collection("sr_history")
            except:
                collection = client.get_or_create_collection("sr_history")
            
            # Search by SR ID
            results = collection.get(
                where={"call_id": sr_id.upper()},
                limit=1
            )
            
            if results and results.get('metadatas') and len(results['metadatas']) > 0:
                metadata = results['metadatas'][0]
                
                sr_data = {
                    'sr_id': metadata.get('call_id', sr_id),
                    'description': metadata.get('description', metadata.get('document', 'N/A')),
                    'priority': metadata.get('Customer Priority', metadata.get('priority', 'P3')),
                    'status': metadata.get('Status', metadata.get('status', 'N/A')),
                    'assigned_to': metadata.get('assigned_to', 'Not Assigned'),
                    'ai_workaround': metadata.get('ai_generated_workaround', ''),
                    'user_corrected_workaround': metadata.get('user_corrected_workaround', ''),
                    'semantic_workaround': metadata.get('semantic_workaround', ''),
                    'summarized_semantic_workaround': metadata.get('semantic_workaround', ''),
                    'resolution_categorization': metadata.get('resolution_categorization', 'N/A'),
                    'sla_resolution_display': metadata.get('sla_resolution_category', 'N/A'),
                    'similar_srs': []
                }
                
                return jsonify({
                    'success': True,
                    'source': 'chromadb',
                    'sr': sr_data
                })
            
            return jsonify({
                'success': False,
                'error': f'SR {sr_id} not found in database'
            }), 404
            
        except Exception as e:
            print(f"[ERROR] ChromaDB search failed: {e}")
            traceback.print_exc()
            return jsonify({'success': False, 'error': f'Database search error: {str(e)}'}), 500
        
    except Exception as e:
        print(f"[ERROR] Search SR failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@smart_sr_bp.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback/workaround"""
    try:
        data = request.get_json()
        sr_id = data.get('sr_id', '').strip()
        workaround = data.get('corrected_workaround', '').strip()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        # Store feedback - simplified version
        print(f"[FEEDBACK] SR: {sr_id}, Workaround: {workaround[:100]}...")
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully!'
        })
        
    except Exception as e:
        print(f"[ERROR] Submit feedback failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

