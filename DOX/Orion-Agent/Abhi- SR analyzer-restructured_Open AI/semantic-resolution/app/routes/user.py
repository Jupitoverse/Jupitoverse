#!/usr/bin/env python3
"""
User Routes Blueprint
Handles user portal routes for SR search, feedback, etc.
"""

from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import pandas as pd
import os
import pickle
import logging
import traceback
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

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)


@user_bp.route('/user')
@user_login_required
def user_portal():
    """User feedback interface page"""
    return render_template('feedback/feedback_main.html')


@user_bp.route('/get_upload_info', methods=['GET'])
def get_upload_info():
    """Get info about admin uploads - uses ChromaDB directly (no Excel files needed)"""
    try:
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        # Get data from ChromaDB (the authoritative source)
        chromadb_count = 0
        today_count = 0
        latest_date = None
        
        try:
            hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
            if hist_manager.use_chromadb and hist_manager.chromadb_collection:
                chromadb_count = hist_manager.chromadb_collection.count()
                
                if chromadb_count > 0:
                    # Get today's date
                    today_str = datetime.now().strftime('%Y-%m-%d')
                    
                    # Query for SRs added today
                    try:
                        today_results = hist_manager.chromadb_collection.get(
                            where={"added_date": today_str},
                            include=["metadatas"]
                        )
                        today_count = len(today_results.get('ids', []))
                    except Exception:
                        today_count = 0
                    
                    # Get most recent added_date by sampling recent records
                    try:
                        sample_results = hist_manager.chromadb_collection.get(
                            limit=100,
                            include=["metadatas"]
                        )
                        dates = []
                        for meta in sample_results.get('metadatas', []):
                            if meta and 'added_date' in meta:
                                dates.append(meta['added_date'])
                        if dates:
                            dates.sort(reverse=True)
                            latest_date = dates[0]
                    except Exception:
                        pass
                        
        except Exception as e:
            logger.warning(f"ChromaDB query error: {e}")
        
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
            'sr_count': today_count,  # Today's SRs
            'historical_count': chromadb_count,  # Total in database
            'filename': 'ChromaDB',  # No file, using database
            'total_uploads': 1,
            'message': f'Database: {chromadb_count} total SRs | Today: {today_count} SRs (Last update: {upload_date_display})'
        })
        
    except Exception as e:
        logger.error(f"Error getting upload info: {str(e)}")
        return jsonify({
            'has_upload': False,
            'historical_count': 0,
            'message': 'Error loading data'
        })


def _get_valid_field(val):
    """Helper to get non-garbage value"""
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str.upper() in ['NA', 'N/A', 'NULL', 'NONE', '']:
        return None
    return val_str


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
                            workaround = (_get_valid_field(metadata.get('workaround')) or 
                                         _get_valid_field(metadata.get('user_corrected_workaround')) or
                                         _get_valid_field(metadata.get('ai_generated_workaround')) or 'N/A')
                            
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
            
            # 🆕 Get ALL user feedback entries for this SR (supports multiple user WAs)
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
            
            # 🆕 Summarize semantic workarounds using LLM
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
                    
                    # 🆕 ALL user feedback entries (multiple user WAs supported)
                    'all_user_feedback': all_user_feedback,
                    'user_feedback_count': len(all_user_feedback),
                    
                    # Semantic matches - USE SUMMARIZED TEXT instead of raw
                    'semantic_workaround': sanitize_for_json(
                        summarized_result.get('summary', '') if summarized_result.get('success') 
                        else vs_result.get('semantic_workaround', '')
                    ),
                    'semantic_workarounds_list': semantic_workarounds_list if semantic_workarounds_list else 'No semantic matches found',
                    'similar_srs': similar_srs,
                    
                    # Summarized semantic workaround (for UI display)
                    'summarized_semantic_workaround': sanitize_for_json(summarized_result.get('summary', '')),
                    'has_summarized_workaround': summarized_result.get('success', False),
                    'similar_sr_count': summarized_result.get('similar_count', 0),
                    
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


