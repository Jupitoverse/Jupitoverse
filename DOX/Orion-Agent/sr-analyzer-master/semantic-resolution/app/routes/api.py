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
    """Regenerate AI workaround for an SR with optional user context"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        description = data.get('description', '')
        notes = data.get('notes', '')
        user_context = data.get('user_context', '').strip()  # Optional user-provided context
        semantic_workaround = data.get('semantic_workaround', '')  # Existing semantic workaround
        resolution_category = data.get('resolution_category', '')
        application = data.get('application', '')
        
        # DEBUG: Log what we received
        logger.info(f"[REGENERATE] SR ID: {sr_id}")
        logger.info(f"[REGENERATE] Description length: {len(description) if description else 0}")
        logger.info(f"[REGENERATE] Description preview: {description[:200] if description else 'EMPTY'}...")
        logger.info(f"[REGENERATE] Notes length: {len(notes) if notes else 0}")
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        if user_context:
            logger.info(f"[REGENERATE] User context: {user_context[:100]}...")
        
        import sys
        sys.path.insert(0, os.path.join(BASE_DIR, 'RAG', 'pipeline'))
        
        try:
            from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
            
            pipeline = MultiModelSRPipeline()
            
            result = pipeline.analyze_single_sr({
                'call_id': sr_id,
                'SR ID': sr_id,
                'Description': description,
                'description': description,
                'Notes': notes,
                'notes': notes,
                'user_context': user_context,
                'existing_semantic_workaround': semantic_workaround,  # Pass existing workaround
                'Resolution Category': resolution_category,
                'Application': application
            })
            
            if result:
                ai_workaround = result.get('AI Workaround', '')
                # Return success even if workaround is minimal - let user decide if it's helpful
                return jsonify({
                    'success': True,
                    'ai_workaround': ai_workaround if ai_workaround else 'No specific workaround found. Please provide more context or try manual resolution.',
                    'java_info': result.get('Is Java Error', ''),
                    'activity_name': result.get('Activity Names', ''),
                    'similar_workarounds': result.get('Similar Workarounds', []),
                    'has_similar': bool(result.get('Similar Workarounds')),
                    'message': 'AI workaround generated successfully' if ai_workaround else 'Generated with limited context'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not generate workaround - pipeline returned no result'
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
    """Update AI workaround in the database - directly in ChromaDB"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        # Accept both 'workaround' and 'ai_workaround' field names
        workaround = data.get('workaround', '') or data.get('ai_workaround', '')
        if isinstance(workaround, str):
            workaround = workaround.strip()
        
        if not sr_id or not workaround:
            return jsonify({'success': False, 'error': 'SR ID and workaround required'}), 400
        
        import chromadb
        
        # Connect directly to ChromaDB
        client = chromadb.PersistentClient(path=CHROMADB_PATH)
        
        # Try to find and update in the history collection
        updated = False
        sr_id_upper = sr_id.upper().strip()
        
        # Prioritize clean_history_data - this is what search_vectorstore_by_sr_id uses
        for coll_name in ['clean_history_data', 'sr_history', 'historical_srs']:
            try:
                collection = client.get_collection(coll_name)
                
                # Search for the SR
                results = collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas', 'documents']
                )
                
                if results and results['ids']:
                    # Found it - update the metadata
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i] if results['metadatas'] else {}
                        metadata['ai_generated_workaround'] = workaround[:10000]  # Increased limit
                        metadata['ai_workaround_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Update in ChromaDB
                        collection.update(
                            ids=[doc_id],
                            metadatas=[metadata]
                        )
                        updated = True
                        logger.info(f"✅ Updated AI workaround for {sr_id} in collection {coll_name}")
                        break
                
                if updated:
                    break
                    
            except Exception as coll_err:
                logger.debug(f"Collection {coll_name} error: {coll_err}")
                continue
        
        if not updated:
            # Try lowercase sr_id - prioritize clean_history_data
            for coll_name in ['clean_history_data', 'sr_history']:
                try:
                    collection = client.get_collection(coll_name)
                    results = collection.get(
                        where={"call_id": sr_id},
                        include=['metadatas']
                    )
                    if results and results['ids']:
                        for i, doc_id in enumerate(results['ids']):
                            metadata = results['metadatas'][i] if results['metadatas'] else {}
                            metadata['ai_generated_workaround'] = workaround[:10000]  # Increased limit
                            metadata['ai_workaround_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            collection.update(ids=[doc_id], metadatas=[metadata])
                            updated = True
                            logger.info(f"✅ Updated AI workaround for {sr_id} in {coll_name}")
                            break
                    if updated:
                        break
                except:
                    continue
        
        if updated:
            return jsonify({
                'success': True,
                'message': f'Workaround saved to database for {sr_id}'
            })
        else:
            logger.warning(f"SR {sr_id} not found in any ChromaDB collection")
            return jsonify({
                'success': True,
                'message': f'Workaround saved (SR {sr_id} not in database yet)'
            })
        
    except Exception as e:
        logger.error(f"Update workaround error: {str(e)}")
        import traceback
        traceback.print_exc()
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


