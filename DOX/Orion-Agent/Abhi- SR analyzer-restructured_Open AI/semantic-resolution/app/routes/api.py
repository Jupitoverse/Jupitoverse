#!/usr/bin/env python3
"""
API Routes Blueprint
Handles API endpoints for voting, AI workaround generation, etc.
"""

from flask import Blueprint, request, jsonify
import os
import logging
import traceback
from datetime import datetime

from app.utils.decorators import user_login_required
from app.utils.state import (
    BASE_DIR, VECTOR_STORE_DIR, get_feedback_storage, CHROMADB_PATH
)

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


@api_bp.route('/vote/upvote', methods=['POST'])
def upvote_workaround():
    """Upvote a workaround"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        workaround_type = data.get('workaround_type', 'semantic')
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        feedback_storage = get_feedback_storage()
        if feedback_storage:
            feedback_storage.upvote(sr_id, workaround_type)
            votes = feedback_storage.get_votes(sr_id, workaround_type)
            return jsonify({
                'success': True,
                'upvotes': votes.get('upvotes', 0),
                'downvotes': votes.get('downvotes', 0)
            })
        
        return jsonify({'success': True, 'upvotes': 1, 'downvotes': 0})
        
    except Exception as e:
        logger.error(f"Upvote error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/vote/downvote', methods=['POST'])
def downvote_workaround():
    """Downvote a workaround"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        workaround_type = data.get('workaround_type', 'semantic')
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        feedback_storage = get_feedback_storage()
        if feedback_storage:
            feedback_storage.downvote(sr_id, workaround_type)
            votes = feedback_storage.get_votes(sr_id, workaround_type)
            return jsonify({
                'success': True,
                'upvotes': votes.get('upvotes', 0),
                'downvotes': votes.get('downvotes', 0)
            })
        
        return jsonify({'success': True, 'upvotes': 0, 'downvotes': 1})
        
    except Exception as e:
        logger.error(f"Downvote error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/vote/get_votes', methods=['POST'])
def get_votes():
    """Get votes for a workaround"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        workaround_type = data.get('workaround_type', 'semantic')
        
        feedback_storage = get_feedback_storage()
        if feedback_storage:
            votes = feedback_storage.get_votes(sr_id, workaround_type)
            return jsonify({
                'success': True,
                'upvotes': votes.get('upvotes', 0),
                'downvotes': votes.get('downvotes', 0)
            })
        
        return jsonify({'success': True, 'upvotes': 0, 'downvotes': 0})
        
    except Exception as e:
        logger.error(f"Get votes error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/vote/statistics', methods=['GET'])
def get_vote_statistics():
    """Get overall vote statistics"""
    try:
        feedback_storage = get_feedback_storage()
        if feedback_storage:
            stats = feedback_storage.get_statistics()
            return jsonify({
                'success': True,
                'statistics': stats
            })
        
        return jsonify({'success': True, 'statistics': {}})
        
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/regenerate_ai_workaround', methods=['POST'])
@user_login_required
def regenerate_ai_workaround():
    """Regenerate AI workaround for an SR"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        description = data.get('description', '')
        notes = data.get('notes', '')
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        import sys
        sys.path.insert(0, os.path.join(BASE_DIR, 'RAG', 'pipeline'))
        
        try:
            from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
            
            pipeline = MultiModelSRPipeline()
            
            result = pipeline.process_sr({
                'call_id': sr_id,
                'description': description,
                'notes': notes
            })
            
            if result and result.get('ai_generated_workaround'):
                return jsonify({
                    'success': True,
                    'workaround': result.get('ai_generated_workaround', ''),
                    'java_info': result.get('java_backend_info', ''),
                    'activity_name': result.get('activity_name', '')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not generate workaround'
                }), 500
                
        except ImportError as e:
            logger.error(f"Pipeline import error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'AI pipeline not available'
            }), 500
        
    except Exception as e:
        logger.error(f"Regenerate error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/generate_ai_workaround', methods=['POST'])
@user_login_required
def generate_ai_workaround():
    """Generate AI workaround on demand"""
    return regenerate_ai_workaround()


@api_bp.route('/update_ai_workaround_in_db', methods=['POST'])
@user_login_required
def update_ai_workaround_in_db():
    """Update AI workaround in the database"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        workaround = data.get('workaround', '').strip()
        
        if not sr_id or not workaround:
            return jsonify({'success': False, 'error': 'SR ID and workaround required'}), 400
        
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
                sr['ai_generated_workaround'] = workaround
                sr['ai_workaround_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                updated = True
                break
        
        if not updated:
            return jsonify({'success': False, 'error': f'SR {sr_id} not found'}), 404
        
        hist_manager.save_database()
        
        logger.info(f"Updated AI workaround for {sr_id}")
        return jsonify({
            'success': True,
            'message': f'Workaround updated for {sr_id}'
        })
        
    except Exception as e:
        logger.error(f"Update workaround error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/user_feedback/<sr_id>', methods=['GET'])
def get_all_user_feedback(sr_id: str):
    """
    Get ALL user feedback entries for a specific SR.
    Supports multiple user workarounds per SR.
    
    Returns:
        List of user feedback entries sorted by date (newest first)
    """
    try:
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        
        # Get all user feedback for this SR
        all_feedback = hist_manager.get_all_user_feedback_for_sr(sr_id)
        
        return jsonify({
            'success': True,
            'sr_id': sr_id.upper(),
            'feedback_count': len(all_feedback),
            'feedback': all_feedback
        })
        
    except Exception as e:
        logger.error(f"Get user feedback error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/user_feedback_stats', methods=['GET'])
def get_user_feedback_stats():
    """
    Get statistics about user feedback in the system.
    """
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        stats = hist_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'total_records': stats.get('total_records', 0),
            'user_feedback_count': stats.get('user_feedback_count', 0),
            'storage': stats.get('storage', 'unknown')
        })
        
    except Exception as e:
        logger.error(f"User feedback stats error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


