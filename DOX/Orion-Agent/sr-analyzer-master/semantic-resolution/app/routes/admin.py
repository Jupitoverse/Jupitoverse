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
    return render_template('admin/admin_upload.html')


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
    
    # Fix for absolute Linux paths - restore leading slash if stripped
    if not filepath.startswith('/') and not filepath.startswith('C:') and not filepath.startswith('c:'):
        # Check if it looks like an absolute Linux path (starts with common root dirs)
        if filepath.startswith('ossusers') or filepath.startswith('home') or filepath.startswith('opt') or filepath.startswith('var') or filepath.startswith('tmp'):
            filepath = '/' + filepath
    
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
    return render_template('admin/today_upload.html')


@admin_bp.route('/admin/remove_sr')
@login_required
def remove_sr_page():
    """SR removal page"""
    return render_template('admin/admin_remove_sr.html')


@admin_bp.route('/admin/get_srs_by_date', methods=['GET'])
@login_required
def get_srs_by_date():
    """Get SRs by date for today's page - reads from output Excel files + input for dates"""
    try:
        import pandas as pd
        from pathlib import Path
        from assignment.priority_age_calculator import PriorityAgeCalculator
        
        age_calculator = PriorityAgeCalculator()
        
        target_date = request.args.get('date')  # Format: 2026-01-19
        
        # Convert date format for filename matching (2026-01-19 -> 20260119)
        if target_date:
            date_for_file = target_date.replace('-', '')
        else:
            date_for_file = datetime.now().strftime('%Y%m%d')
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        output_dir = Path(BASE_DIR) / 'output' / 'reports'
        input_dir = Path(BASE_DIR) / 'input'
        filtered_srs = []
        
        # First, load input Excel to get Submit Date and Last Date (these are not in output Excel)
        input_dates = {}  # sr_id -> {submit_date, last_date}
        if input_dir.exists():
            # Match any Excel file containing today's date (flexible matching)
            input_files = [f for f in input_dir.iterdir() 
                          if (date_for_file in f.name or f.name.startswith(f'upload_{date_for_file}')) 
                          and (f.suffix == '.xlsx' or f.suffix == '.xls')]
            logger.info(f"[DEBUG] Looking for input files with date {date_for_file}, found: {[f.name for f in input_files]}")
            if input_files:
                input_files.sort(key=lambda x: x.name, reverse=True)
                input_file = input_files[0]
                logger.info(f"Reading dates from input file: {input_file.name}")
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
                    
                    logger.info(f"Input columns found - SR: {sr_col}, Submit: {submit_col}, Last: {last_col}")
                    
                    # Find Category column
                    cat_col = None
                    for col in ['Categorization Tier 3', 'Categorization', 'Resolution Categorization', 'Category']:
                        if col in input_df.columns:
                            cat_col = col
                            break
                    
                    # Find Defect ID column
                    defect_col = None
                    for col in ['Defect ID(QC Defect ID)', 'QC Defect ID', 'Defect ID', 'defect_id', 'DefectID']:
                        if col in input_df.columns:
                            defect_col = col
                            break
                    
                    logger.info(f"Input columns found - SR: {sr_col}, Submit: {submit_col}, Last: {last_col}, Category: {cat_col}, Defect: {defect_col}")
                    
                    if sr_col:
                        for _, row in input_df.iterrows():
                            sr_id = str(row.get(sr_col, '')).upper().strip()
                            if sr_id and sr_id != 'NAN':
                                input_dates[sr_id] = {
                                    'submit_date': row.get(submit_col) if submit_col else None,
                                    'last_date': row.get(last_col) if last_col else None,
                                    'category': row.get(cat_col) if cat_col else None,
                                    'defect_id': row.get(defect_col) if defect_col else None
                                }
                    # Log first entry for debugging
                    if input_dates:
                        first_sr = next(iter(input_dates.keys()))
                        logger.info(f"[DEBUG] Sample input data for {first_sr}: {input_dates[first_sr]}")
                        
                except Exception as e:
                    logger.warning(f"Could not read input file for dates: {e}")
                    import traceback
                    logger.warning(f"[DEBUG] Traceback: {traceback.format_exc()}")
        
        logger.info(f"Loaded {len(input_dates)} SR dates from input file")
        
        if output_dir.exists():
            # Find files matching the date
            matching_files = [f for f in output_dir.iterdir() 
                            if f.name.startswith(f'Admin_Upload_{date_for_file}') and f.suffix == '.xlsx']
            
            if matching_files:
                # Get the most recent file for that date
                matching_files.sort(key=lambda x: x.name, reverse=True)
                latest_file = matching_files[0]
                
                logger.info(f"Reading SRs from: {latest_file.name}")
                
                try:
                    df = pd.read_excel(latest_file)
                    
                    # Log columns for debugging
                    logger.info(f"Excel columns: {list(df.columns)}")
                    
                    # Find Submit Date column
                    submit_date_col = None
                    for col in ['Submit Date', 'Reported Date', 'Created Date', 'Opened Date',
                               'submit_date', 'reported_date', 'created_date', 'opened_date']:
                        if col in df.columns:
                            submit_date_col = col
                            break
                    
                    # Find Last Date column
                    last_date_col = None
                    for col in ['Last Date Duration Calculated', 'Last Date', 'Last Activity Date', 
                               'Modified Date', 'Last Updated', 'last_date', 'last_activity_date', 
                               'modified_date', 'Last Modified Date', 'Last Modified', 'Updated Date',
                               'Last Duration Calculated']:
                        if col in df.columns:
                            last_date_col = col
                            break
                    
                    # Find categorization column
                    cat_col_found = None
                    for cat_col in ['Categorization Tier 3', 'Categorization', 'Resolution Categorization', 
                                   'Category', 'Type', 'Issue Type', 'categorization_tier3']:
                        if cat_col in df.columns:
                            cat_col_found = cat_col
                            break
                    
                    logger.info(f"Using Submit Date column: {submit_date_col}, Last Date column: {last_date_col}, Category column: {cat_col_found}")
                    
                    # Debug: Log first row to see structure
                    first_row_logged = False
                    
                    for idx, row in df.iterrows():
                        sr_id = str(row.get('SR ID', row.get('Call ID', 'Unknown')))
                        sr_id_upper = sr_id.upper().strip()
                        desc_text = str(row.get('Original Description', row.get('Description', 'N/A')))
                        
                        # Debug: Log first row data
                        if not first_row_logged:
                            logger.info(f"[DEBUG] First row keys: {list(row.keys())}")
                            logger.info(f"[DEBUG] First row SR ID: {sr_id}")
                            first_row_logged = True
                        
                        # Get Submit Date and Last Date - first from output Excel, then from input lookup
                        submit_date = row.get(submit_date_col) if submit_date_col else None
                        last_date = row.get(last_date_col) if last_date_col else None
                        
                        # Debug: Log if dates found in output
                        if idx == 0:
                            logger.info(f"[DEBUG] Output Excel - Submit: {submit_date}, Last: {last_date}")
                        
                        # If dates not in output, get from input lookup
                        if pd.isna(submit_date) or submit_date is None:
                            if sr_id_upper in input_dates:
                                submit_date = input_dates[sr_id_upper].get('submit_date')
                                if idx == 0:
                                    logger.info(f"[DEBUG] Got submit_date from input lookup: {submit_date}")
                        if pd.isna(last_date) or last_date is None:
                            if sr_id_upper in input_dates:
                                last_date = input_dates[sr_id_upper].get('last_date')
                                if idx == 0:
                                    logger.info(f"[DEBUG] Got last_date from input lookup: {last_date}")
                        
                        # Debug: Final dates used
                        if idx == 0:
                            logger.info(f"[DEBUG] Final dates - Submit: {submit_date}, Last: {last_date}")
                        
                        # Calculate age in business days: Last Date - Submit Date (excluding weekends & US holidays)
                        age_days = 0
                        if pd.notna(submit_date) and pd.notna(last_date):
                            # Calculate business days between Submit Date and Last Date
                            age_days = age_calculator.calculate_business_days(submit_date, last_date)
                            if idx == 0:
                                logger.info(f"[DEBUG] Calculated age (Last-Submit): {age_days} business days")
                        elif pd.notna(submit_date):
                            # Fallback: calculate from submit date to now
                            age_days = age_calculator.calculate_business_days(submit_date)
                            if idx == 0:
                                logger.info(f"[DEBUG] Calculated age (Submit-Now): {age_days} business days")
                        
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
                        
                        # Get categorization - check output Excel first, then input lookup
                        cat_tier3 = '-'
                        for cat_col_name in ['Categorization Tier 3', 'Categorization', 'Resolution Categorization', 
                                       'Category', 'Type', 'Issue Type', 'categorization_tier3']:
                            if cat_col_name in df.columns:
                                val = row.get(cat_col_name)
                                if pd.notna(val) and str(val).strip() and str(val).strip().lower() != 'nan':
                                    cat_tier3 = str(val).strip()
                                    break
                        
                        # If category not in output, get from input lookup
                        if cat_tier3 == '-' and sr_id_upper in input_dates:
                            input_cat = input_dates[sr_id_upper].get('category')
                            if pd.notna(input_cat) and str(input_cat).strip() and str(input_cat).strip().lower() != 'nan':
                                cat_tier3 = str(input_cat).strip()
                                if idx == 0:
                                    logger.info(f"[DEBUG] Got category from input lookup: {cat_tier3}")
                        
                        # Get priority for aging calculation
                        priority = str(row.get('Priority', row.get('Customer Priority', 'P3'))).upper()
                        
                        # Aging SR conditions (OR logic - any condition triggers aging):
                        # 1. Category is Ops EOM, Potential Ops EOM, Sales EOM, Potential Sales EOM
                        # 2. Priority is P2 or P3
                        # 3. Age > 3 business days
                        aging_categories = ['ops eom', 'potential ops eom', 'sales eom', 'potential sales eom']
                        cat_lower = cat_tier3.lower() if cat_tier3 else ''
                        is_aging_category = any(cat in cat_lower for cat in aging_categories)
                        is_aging_priority = priority in ['P2', 'P3']
                        is_over_age_threshold = age_days > 3
                        
                        # OR condition - ANY of these makes it aging
                        is_aging = is_aging_category or is_aging_priority or is_over_age_threshold
                        
                        # Build aging reason
                        aging_reasons = []
                        if is_aging_category:
                            aging_reasons.append(f"Category: {cat_tier3}")
                        if is_aging_priority:
                            aging_reasons.append(f"Priority: {priority}")
                        if is_over_age_threshold:
                            aging_reasons.append(f"Age: {age_days} days (>3)")
                        aging_reason = " | ".join(aging_reasons) if aging_reasons else ""
                        
                        # Get Status - check output Excel first
                        sr_status = 'Open'  # Default to Open
                        for status_col_name in ['Status', 'status', 'SR Status']:
                            if status_col_name in df.columns:
                                val = row.get(status_col_name)
                                if pd.notna(val) and str(val).strip() and str(val).strip().lower() != 'nan':
                                    sr_status = str(val).strip()
                                    break
                        
                        # Get Defect ID from input lookup
                        defect_id = '-'
                        if sr_id_upper in input_dates:
                            input_defect = input_dates[sr_id_upper].get('defect_id')
                            if pd.notna(input_defect) and str(input_defect).strip() and str(input_defect).strip().lower() != 'nan':
                                # Convert to int first to remove decimal (Excel reads numbers as float)
                                try:
                                    defect_id = str(int(float(input_defect)))
                                except (ValueError, TypeError):
                                    defect_id = str(input_defect).strip()
                        
                        filtered_srs.append({
                            'sr_id': sr_id,
                            'description': desc_text[:100] + '...' if len(desc_text) > 100 else desc_text,
                            'submit_date': submit_date_str,
                            'last_date': last_date_str,
                            'priority': priority,
                            'status': sr_status,
                            'defect_id': defect_id,
                            'assigned_to': str(row.get('Assigned To', 'Not Assigned')),
                            'application': str(row.get('Application', row.get('Assigned Group', ''))),
                            'ai_workaround': str(row.get('AI Workaround', row.get('Suggested Workaround', '')))[:200],
                            'age_days': age_days,  # Age in business days (Last Date - Submit Date)
                            'categorization_tier3': cat_tier3,
                            'is_aging': is_aging,
                            'aging_reason': aging_reason
                        })
                except Exception as e:
                    logger.error(f"Error reading Excel: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                logger.warning(f"No files found for date: {date_for_file}")
        
        return jsonify({
            'success': True,
            'srs': filtered_srs,
            'count': len(filtered_srs),
            'date': target_date
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


@admin_bp.route('/admin/get_input_files')
@login_required
def get_input_files():
    """Get list of Excel files in the input folder"""
    try:
        files = []
        input_path = Path(INPUT_DIR)
        if input_path.exists():
            for f in sorted(input_path.glob('*.xls*'), key=lambda x: x.stat().st_mtime, reverse=True):
                stat = f.stat()
                files.append({
                    'name': f.name,
                    'path': str(f),
                    'size': stat.st_size,
                    'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        logger.error(f"Error getting input files: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/process_latest_input', methods=['POST'])
@login_required
def process_latest_input():
    """Process the latest file from the input folder"""
    try:
        # Find latest Excel file in input folder
        input_path = Path(INPUT_DIR)
        if not input_path.exists():
            return jsonify({
                'success': False,
                'error': 'Input folder does not exist'
            }), 404
        
        # Get all Excel files sorted by modification time (newest first)
        excel_files = sorted(
            list(input_path.glob('*.xls')) + list(input_path.glob('*.xlsx')),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if not excel_files:
            return jsonify({
                'success': False,
                'error': 'No Excel files found in input folder. Run the Windows batch file first.'
            }), 404
        
        # Get the latest file
        latest_file = excel_files[0]
        
        # Generate upload ID for tracking
        upload_id = str(uuid.uuid4())[:8]
        
        logger.info(f"Processing latest input file: {latest_file.name}")
        
        return jsonify({
            'success': True,
            'upload_id': upload_id,
            'filepath': str(latest_file),
            'filename': latest_file.name,
            'message': f'Found file: {latest_file.name}'
        })
        
    except Exception as e:
        logger.error(f"Process latest input error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/admin/fetch_from_email', methods=['POST'])
@login_required
def fetch_from_email():
    """Fetch SR data from Outlook email using Microsoft Graph API (cross-platform)"""
    import traceback
    try:
        data = request.json
        days_back = data.get('days_back', 3)
        
        # Use Graph API email fetcher (cross-platform)
        from admin.email.email_fetcher_graph import GraphEmailFetcher, O365_AVAILABLE
        
        if not O365_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'O365 library not installed. Run: pip install O365'
            }), 500
        
        fetcher = GraphEmailFetcher()
        
        # Try to connect (uses saved token or prompts for auth)
        if not fetcher.connect():
            return jsonify({
                'success': False,
                'error': 'Failed to connect to Microsoft Graph API. Check config/email_config.json credentials or run: python -m admin.email.email_fetcher_graph --list'
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
        if 'authentication' in error_msg.lower() or 'token' in error_msg.lower():
            error_msg = 'Authentication failed. Run: python -m admin.email.email_fetcher_graph --list to authenticate.'
        elif 'credentials' in error_msg.lower() or 'client_id' in error_msg.lower():
            error_msg = 'Missing credentials. Check config/email_config.json'
        
        return jsonify({'success': False, 'error': error_msg}), 500


