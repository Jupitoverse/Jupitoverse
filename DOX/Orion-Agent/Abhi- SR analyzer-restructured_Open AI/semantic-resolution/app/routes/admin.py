#!/usr/bin/env python3
"""
Admin Routes Blueprint
Handles admin portal routes for uploads, stats, etc.
"""

from flask import Blueprint, render_template, request, jsonify, send_file, Response
import pandas as pd
import os
import logging
import traceback
import uuid
from pathlib import Path
from datetime import datetime

from app.utils.decorators import login_required
from app.utils.helpers import safe_get, sanitize_for_json
from app.utils.state import (
    session_data, BASE_DIR, VECTOR_STORE_DIR, OUTPUT_DIR, REPORTS_DIR, INPUT_DIR,
    CHROMADB_PATH, DATABASE_DIR
)

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def admin_page():
    """Admin upload portal"""
    return render_template('feedback/admin_upload.html')


@admin_bp.route('/admin/stats')
@login_required
def admin_stats():
    """Get admin statistics"""
    try:
        import json
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        # Get historical SR count - use ChromaDB
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        historical_count = 0
        user_corrections = 0
        
        # Check ChromaDB first
        if hist_manager.use_chromadb and hist_manager.chromadb_collection:
            try:
                historical_count = hist_manager.chromadb_collection.count()
                # Count user corrections from ChromaDB
                all_metadata = hist_manager.chromadb_collection.get(include=['metadatas'])
                metadata_list = all_metadata.get('metadatas', [])
                user_corrections = sum(
                    1 for m in metadata_list 
                    if m and m.get('user_corrected_workaround', '').strip()
                )
            except Exception as e:
                logger.warning(f"ChromaDB count error: {e}")
        
        # Fallback to pickle
        if historical_count == 0:
            if hist_manager.db_data:
                metadata_list = hist_manager.db_data.get('metadata', [])
                historical_count = len(metadata_list)
                # Count user corrections
                user_corrections = sum(
                    1 for m in metadata_list 
                    if m.get('user_corrected_workaround', '').strip()
                )
        
        # Get upload stats
        output_dir = os.path.join(BASE_DIR, 'output', 'reports')
        upload_count = 0
        latest_upload = 'None'
        
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
            upload_count = len(files)
            if files:
                files.sort(reverse=True)
                latest_upload = files[0]
        
        # Get LLM usage stats
        llm_stats = {
            'last_run_cost': 0,
            'last_run_tokens': 0,
            'last_run_calls': 0,
            'cumulative_cost': 0,
            'cumulative_tokens': 0
        }
        
        llm_stats_file = os.path.join(DATABASE_DIR, 'llm_usage_stats.json')
        if os.path.exists(llm_stats_file):
            try:
                with open(llm_stats_file, 'r') as f:
                    llm_data = json.load(f)
                
                last_run = llm_data.get('last_run', {})
                cumulative = llm_data.get('cumulative', {})
                
                llm_stats = {
                    'last_run_cost': last_run.get('cost', 0),
                    'last_run_tokens': last_run.get('input_tokens', 0) + last_run.get('output_tokens', 0),
                    'last_run_calls': last_run.get('total_calls', 0),
                    'cumulative_cost': cumulative.get('total_cost', 0),
                    'cumulative_tokens': cumulative.get('total_tokens', 0)
                }
            except Exception as e:
                logger.warning(f"Error reading LLM stats: {e}")
        
        # Read LLM usage JSON file directly for proper structure
        llm_usage = None
        llm_stats_file = os.path.join(DATABASE_DIR, 'llm_usage_stats.json')
        if os.path.exists(llm_stats_file):
            try:
                with open(llm_stats_file, 'r') as f:
                    llm_usage = json.load(f)
            except Exception as e:
                logger.warning(f"Error reading LLM usage file: {e}")
        
        return jsonify({
            'success': True,
            # Frontend expects these names:
            'total_historical': historical_count,
            'last_upload_date': latest_upload if latest_upload != 'None' else None,
            'total_feedback': user_corrections,
            'llm_usage': llm_usage,  # Pass the whole structure
            # Also include original names for compatibility
            'historical_srs': historical_count,
            'total_uploads': upload_count,
            'latest_upload': latest_upload,
            'user_corrections': user_corrections,
            'llm_stats': llm_stats
        })
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/upload_and_process', methods=['POST'])
@login_required
def upload_and_process():
    """Handle file upload and processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"upload_{timestamp}_{file.filename}"
        filepath = os.path.join(INPUT_DIR, filename)
        file.save(filepath)
        
        # Generate upload ID for tracking
        upload_id = str(uuid.uuid4())[:8]
        
        return jsonify({
            'success': True,
            'upload_id': upload_id,
            'filepath': filepath,
            'message': 'File uploaded. Processing started...'
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/process_stream/<upload_id>/<path:filepath>')
@login_required
def process_stream(upload_id, filepath):
    """Stream processing progress using Server-Sent Events"""
    import queue
    import threading
    import json
    
    progress_queue = queue.Queue()
    result_holder = {'success': None, 'output_file': None, 'error': None}
    
    def progress_callback(pct, msg):
        progress_queue.put({'progress': pct, 'message': msg})
    
    def run_processing():
        try:
            import sys
            sys.path.insert(0, BASE_DIR)
            from admin.upload.admin_upload_and_merge_with_rag import upload_and_merge_with_rag
            
            success, output_file, log_messages = upload_and_merge_with_rag(
                filepath,
                progress_callback=progress_callback
            )
            result_holder['success'] = success
            result_holder['output_file'] = output_file
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            result_holder['error'] = str(e)
        finally:
            progress_queue.put(None)  # Signal completion
    
    def generate():
        # Start processing in background thread
        thread = threading.Thread(target=run_processing)
        thread.start()
        
        yield f"data: {json.dumps({'progress': 5, 'message': 'Starting processing...'})}\n\n"
        
        # Stream progress updates
        while True:
            try:
                update = progress_queue.get(timeout=0.5)
                if update is None:  # Processing complete
                    break
                yield f"data: {json.dumps(update)}\n\n"
            except queue.Empty:
                # Keep connection alive with heartbeat
                yield f"data: {json.dumps({'heartbeat': True})}\n\n"
        
        thread.join()
        
        # Final result - MUST include 'complete' and 'success' flags for frontend
        if result_holder['error']:
            yield f"data: {json.dumps({'progress': 100, 'error': result_holder['error'], 'complete': True, 'success': False})}\n\n"
        elif result_holder['success']:
            yield f"data: {json.dumps({'progress': 100, 'message': 'Processing complete!', 'output_file': result_holder['output_file'], 'complete': True, 'success': True})}\n\n"
        else:
            yield f"data: {json.dumps({'progress': 100, 'error': 'Processing failed', 'complete': True, 'success': False})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@admin_bp.route('/admin/download_latest_report', methods=['GET'])
@login_required
def download_latest_report():
    """Download the latest admin upload report"""
    try:
        output_dir = os.path.join(BASE_DIR, 'output', 'reports')
        
        if not os.path.exists(output_dir):
            return jsonify({'success': False, 'error': 'No reports available'}), 404
        
        files = [f for f in os.listdir(output_dir) if f.startswith('Admin_Upload_') and f.endswith('.xlsx')]
        
        if not files:
            return jsonify({'success': False, 'error': 'No reports available'}), 404
        
        files.sort(reverse=True)
        latest_file = os.path.join(output_dir, files[0])
        
        return send_file(
            latest_file,
            as_attachment=True,
            download_name=files[0]
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/today_upload')
@login_required
def today_upload():
    """Today's upload page"""
    return render_template('feedback/today_upload.html')


@admin_bp.route('/admin/remove_sr')
@login_required
def remove_sr_page():
    """SR removal page"""
    return render_template('feedback/admin_remove_sr.html')


@admin_bp.route('/admin/get_srs_by_date', methods=['GET'])
@login_required
def get_srs_by_date():
    """Get SRs by date for today's page"""
    try:
        target_date = request.args.get('date')  # Support single date param
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        if not hist_manager.use_chromadb:
            return jsonify({'success': False, 'error': 'Could not connect to ChromaDB'}), 500
        
        # Query ChromaDB directly
        try:
            all_records = hist_manager.chromadb_collection.get(include=['metadatas'])
            metadata_list = all_records.get('metadatas', [])
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return jsonify({'success': False, 'error': 'ChromaDB query failed'}), 500
        
        filtered_srs = []
        
        for sr in metadata_list:
            if sr is None:
                continue
            sr_date = sr.get('added_date', '') or sr.get('opened_date', '') or sr.get('Reported Date', '')
            sr_id = sr.get('call_id', 'Unknown')
            
            # Filter by target_date if provided
            if target_date and sr_date:
                if target_date in str(sr_date):
                    desc_text = str(sr.get('description', '') or sr.get('summary', '') or 'N/A')
                    filtered_srs.append({
                        'sr_id': sr_id,
                        'description': desc_text[:100] + '...' if len(desc_text) > 100 else desc_text,
                        'opened_date': sr_date,
                        'priority': sr.get('priority', ''),
                        'assigned_to': sr.get('assigned_to', 'Not Assigned'),
                        'application': sr.get('application', ''),
                        'ai_workaround': sr.get('ai_generated_workaround', '')
                    })
            elif not target_date:
                # No date filter - return all (limited)
                desc_text = str(sr.get('description', '') or sr.get('summary', '') or 'N/A')
                filtered_srs.append({
                    'sr_id': sr_id,
                    'description': desc_text[:100],
                    'opened_date': sr_date
                })
        
        return jsonify({
            'success': True,
            'srs': filtered_srs[:100],  # Limit to 100
            'count': len(filtered_srs[:100])  # Count for frontend display
        })
        
    except Exception as e:
        logger.error(f"Error getting SRs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/delete_sr', methods=['POST'])
@login_required
def delete_sr():
    """Delete a single SR from the database"""
    try:
        data = request.json
        sr_id = data.get('sr_id', '').strip()
        
        if not sr_id:
            return jsonify({'success': False, 'error': 'SR ID required'}), 400
        
        from RAG.utils.history_db_manager import HistoryDatabaseManager
        import numpy as np
        
        hist_manager = HistoryDatabaseManager(chromadb_path=CHROMADB_PATH)
        if not hist_manager.use_chromadb:
            return jsonify({'success': False, 'error': 'Could not connect to ChromaDB'}), 500
        
        metadata_list = hist_manager.db_data.get('metadata', [])
        embeddings = hist_manager.db_data.get('embeddings')
        
        # Find and remove SR
        sr_id_upper = sr_id.upper().strip()
        indices_to_remove = []
        
        for i, sr in enumerate(metadata_list):
            if str(sr.get('call_id', '')).upper().strip() == sr_id_upper:
                indices_to_remove.append(i)
        
        if not indices_to_remove:
            return jsonify({'success': False, 'error': f'SR {sr_id} not found'}), 404
        
        # Remove from metadata
        for i in sorted(indices_to_remove, reverse=True):
            del metadata_list[i]
        
        # Remove from embeddings
        if embeddings is not None:
            embeddings = np.delete(embeddings, indices_to_remove, axis=0)
            hist_manager.db_data['embeddings'] = embeddings
        
        # Save
        hist_manager.save_database()
        
        logger.info(f"Deleted SR {sr_id}")
        return jsonify({
            'success': True,
            'message': f'SR {sr_id} deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/fetch_from_email', methods=['POST'])
@login_required
def fetch_from_email():
    """Fetch SR data from Outlook email"""
    import traceback
    try:
        data = request.json
        days_back = data.get('days_back', 3)
        
        from admin.email.email_fetcher import OutlookEmailFetcher, OUTLOOK_COM_AVAILABLE
        
        if not OUTLOOK_COM_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'pywin32 not installed. Run: pip install pywin32'
            }), 500
        
        fetcher = OutlookEmailFetcher()
        
        # Try to connect first
        if not fetcher.connect():
            return jsonify({
                'success': False,
                'error': 'Failed to connect to Outlook. Make sure Outlook desktop app is running.'
            }), 500
        
        result = fetcher.fetch_latest_report(days_back=days_back)
        
        if result:
            filepath, email_date = result
            return jsonify({
                'success': True,
                'message': f'Fetched report from email dated {email_date.strftime("%Y-%m-%d %H:%M")}',
                'filepath': filepath
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No SR report found in recent emails'
            }), 404
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Email fetch error: {error_msg}")
        logger.error(traceback.format_exc())
        
        # Provide helpful error messages
        if 'CoInitialize' in error_msg:
            error_msg = 'COM initialization failed. Make sure Outlook is running.'
        elif 'Dispatch' in error_msg or 'MAPI' in error_msg:
            error_msg = 'Cannot connect to Outlook. Make sure Outlook desktop app is open and logged in.'
        
        return jsonify({'success': False, 'error': error_msg}), 500


