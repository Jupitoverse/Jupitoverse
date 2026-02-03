#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Admin Upload & Merge with RAG Integration
Complete flow: Upload → Semantic Analysis → RAG Analysis → Merge to Historical DB
"""

import sys
import os
import pickle
import shutil
import pandas as pd
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from comprehensive_sr_analyzer import ComprehensiveSRAnalyzer


def upload_and_merge_with_rag(excel_path, progress_callback=None):
    """
    Complete admin flow with RAG integration:
    1. Admin uploads Excel file
    2. Run semantic search (existing ComprehensiveSRAnalyzer)
    3. Save to output/reports/Admin_Upload_TIMESTAMP.xlsx
    4. Extract semantic workarounds and save to RAG input folder
    5. Run RAG pipeline on the extracted file
    6. Save RAG output to llm output folder
    7. Merge new SRs to historical database (history_data.db):
       - All data from Admin_Upload_TIMESTAMP.xlsx EXCEPT AI Workaround
       - AI Workaround taken from RAG-generated Excel (match SR ID)
    8. Rebuild index for future searches
    """
    
    def log(message, percent=None):
        """Helper to both print and call progress_callback"""
        print(message)
        if progress_callback and percent is not None:
            progress_callback(percent, message)
    
    log("=" * 80, 5)
    log("ADMIN: UPLOAD & MERGE WITH RAG PIPELINE")
    log("=" * 80)
    log(f"File: {excel_path}")
    log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    
    if not os.path.exists(excel_path):
        log(f"[ERROR] File not found: {excel_path}", 0)
        return False
    
    try:
        # ==================================================
        # STEP 1: Analyze SRs with Semantic Search
        # ==================================================
        log("Step 1: Analyzing SRs with Semantic Search...", 10)
        log("-" * 80)
        
        df = pd.read_excel(excel_path)
        
        # Standardize column names
        column_mapping = {
            'Call ID': ['SR ID', 'call id', 'sr id', 'Inc Call ID'],
            'Description': ['description', 'Issue Description', 'Inc Description'],
            'Notes': ['notes', 'Additional Notes', 'Resolution', 'Inc Resolution'],
            'Customer Priority': ['Priority', 'priority', 'UTS Priority'],
            'STATUS': ['Status', 'status', 'Inc Current EIR - Status'],
            'Assigned Group': ['Application', 'assigned group', 'Assignee Support Group'],
            'Submit Date': ['Created Date', 'submit date', 'Inc Created Date'],
            # 🆕 ADD SLA RESOLUTION FIELDS
            'SLA Resolution Categorization T1': ['sla_resolution_categorization_t1', 'SLA Resolution Categorization T1'],
            'SLA Resolution Category': ['sla_resolution_category', 'SLA Resolution Category'],
            'Resolution Categorization': ['resolution_categorization', 'Resolution Categorization', 'Resolution Category']
        }
        
        for standard_col, alternatives in column_mapping.items():
            if standard_col not in df.columns:
                for alt_col in alternatives:
                    if alt_col in df.columns:
                        df.rename(columns={alt_col: standard_col}, inplace=True)
                        break
        
        log(f"   Found {len(df)} SRs in Excel", 15)
        
        # Analyze with semantic search
        log("   Running semantic analysis...", 20)
        analyzer = ComprehensiveSRAnalyzer()
        sr_data_list = df.to_dict('records')
        
        results = []
        total_srs = len(sr_data_list)
        for idx, sr_data in enumerate(sr_data_list, 1):
            sr_id = sr_data.get('Call ID', sr_data.get('SR ID', f'SR{idx}'))
            log(f"   Analyzing SR {idx}/{total_srs}: {sr_id}", 20 + int((idx/total_srs)*15))
            sr_result = analyzer.analyze_sr_batch([sr_data])
            if sr_result:
                results.extend(sr_result)
        
        log(f"   [OK] Analyzed {len(results)} SRs successfully", 35)
        log("")
        
        # ==================================================
        # STEP 2: Save Admin_Upload_TIMESTAMP.xlsx
        # ==================================================
        log("Step 2: Saving semantic analysis results...", 40)
        log("-" * 80)
        
        output_dir = 'output/reports'
        os.makedirs(output_dir, exist_ok=True)
        
        results_df = pd.DataFrame(results)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        admin_upload_path = os.path.join(output_dir, f"Admin_Upload_{timestamp}.xlsx")
        
        results_df.to_excel(admin_upload_path, index=False)
        log(f"   [OK] Saved: {admin_upload_path}", 45)
        log("")
        
        # ==================================================
        # STEP 3: Extract Semantic Workarounds (merge with original)
        # ==================================================
        log("Step 3: Preparing file for RAG pipeline...", 50)
        log("-" * 80)
        
        # Import the extraction function
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG'))
        from extract_semantic_workarounds import merge_with_original
        
        # Prepare directories
        rag_input_dir = 'RAG/input'
        os.makedirs(rag_input_dir, exist_ok=True)
        
        # Merge semantic workarounds (+ Resolution Category + Status Reason) with original file
        rag_input_filename = None  # Initialize variable
        try:
            log("   Merging semantic workarounds with original input file...", 52)
            rag_input_path = merge_with_original(
                analysis_excel=admin_upload_path,
                original_excel=excel_path,
                output_dir=rag_input_dir
            )
            # Extract filename from the returned path
            rag_input_filename = os.path.basename(rag_input_path)
            log(f"   [OK] RAG input file created: {rag_input_path}", 55)
        except Exception as merge_error:
            # Fallback: if merge fails, use the analyzed results directly
            log(f"   [WARNING] Merge failed: {str(merge_error)}", 52)
            log("   Falling back to direct copy...", 53)
            base_name = os.path.splitext(os.path.basename(excel_path))[0]
            rag_input_filename = f"{timestamp}_{base_name}_with_Semantic_Workarounds_{timestamp}.xlsx"
            rag_input_path = os.path.join(rag_input_dir, rag_input_filename)
            results_df.to_excel(rag_input_path, index=False)
            log(f"   [OK] Fallback RAG input created: {rag_input_path}", 55)
        
        log("")
        
        # ==================================================
        # STEP 4: Run RAG Pipeline on extracted file
        # ==================================================
        log("Step 4: Running RAG pipeline for AI-generated workarounds...", 60)
        log("-" * 80)
        
        rag_output_path = None
        try:
            # Import RAG pipeline
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG', 'rag'))
            
            # Try Ollama pipeline first
            try:
                from rag_pipeline_ollama import SRAnalysisPipeline
                log("   Initializing Ollama RAG pipeline...", 62)
                use_ollama = True
            except ImportError:
                from rag_pipeline import SRAnalysisPipeline
                log("   Initializing DeepSeek RAG pipeline...", 62)
                use_ollama = False
            
            # Initialize RAG pipeline (automatically loads components in __init__)
            rag_pipeline = SRAnalysisPipeline()
            
            log("   Processing SRs through RAG...", 65)
            
            # Read the Excel file for RAG processing
            rag_input_df = pd.read_excel(rag_input_path)
            
            # Run RAG analysis using process_all_srs method
            # This populates rag_pipeline.results internally
            rag_pipeline.process_all_srs(rag_input_df)
            
            # Get results from the pipeline
            rag_results = rag_pipeline.results
            
            if rag_results and len(rag_results) > 0:
                # Save RAG output to llm output folder
                llm_output_dir = 'RAG/llm output'
                os.makedirs(llm_output_dir, exist_ok=True)
                
                rag_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                rag_output_filename = f"{rag_input_filename.replace('.xlsx', '')}_analysis_{rag_timestamp}.xlsx"
                rag_output_path = os.path.join(llm_output_dir, rag_output_filename)
                
                # Save to Excel
                rag_df = pd.DataFrame(rag_results)
                rag_df.to_excel(rag_output_path, index=False)
                
                log(f"   [OK] RAG analysis saved: {rag_output_path}", 75)
            else:
                log("[WARNING] No RAG results generated", 75)
        except Exception as rag_error:
            log(f"[WARNING] RAG pipeline error: {str(rag_error)}", 75)
            log("   Continuing without AI workarounds...", 75)
        
        log("")
        
        # ==================================================
        # STEP 5: Merge to Historical Database (history_data.db)
        # ==================================================
        log("Step 5: Merging to historical database (history_data.db)...", 80)
        log("-" * 80)
        
        # Import history database manager
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from history_db_manager import HistoryDatabaseManager
        
        # Initialize history database
        hist_db_path = 'vector store/clean_history_data.db'
        hist_manager = HistoryDatabaseManager(hist_db_path)
        
        if not hist_manager.db_data:
            log("[WARNING] History database not loaded. Data will not be merged.", 82)
        else:
            # Get existing SR IDs
            existing_sr_ids = set()
            for metadata in hist_manager.db_data.get('metadata', []):
                sr_id = metadata.get('call_id')
                if sr_id:
                    existing_sr_ids.add(str(sr_id))
            
            log(f"   Current historical records: {len(existing_sr_ids)}", 82)
            
            # Load RAG results if available (for AI Workaround AND Assigned To)
            rag_workarounds = {}
            rag_assignments = {}
            if rag_output_path and os.path.exists(rag_output_path):
                try:
                    rag_df = pd.read_excel(rag_output_path)
                    # Create mappings: SR ID -> AI Workaround AND Assigned To
                    for _, row in rag_df.iterrows():
                        sr_id = row.get('SR ID', row.get('Call ID'))
                        ai_workaround = row.get('AI Workaround', row.get('AI Generated Workaround'))
                        assigned_to = row.get('Assigned To')
                        
                        if pd.notna(sr_id) and pd.notna(ai_workaround):
                            rag_workarounds[str(sr_id)] = str(ai_workaround)
                        
                        if pd.notna(sr_id) and pd.notna(assigned_to):
                            rag_assignments[str(sr_id)] = str(assigned_to)
                    
                    log(f"   Loaded {len(rag_workarounds)} AI workarounds from RAG output", 84)
                    log(f"   Loaded {len(rag_assignments)} assignments from RAG output", 84)
                except Exception as e:
                    log(f"   [WARNING] Could not load RAG results: {e}", 84)
            else:
                log("   No RAG results available (using semantic only)", 84)
            
            # Add new SRs or update existing ones in historical database
            new_records = 0
            updated_records = 0
            
            for idx, result in enumerate(results, 1):
                sr_id = str(result.get('SR ID', result.get('Call ID', 'Unknown')))
                
                # Get AI workaround from RAG output, if available
                ai_workaround = rag_workarounds.get(sr_id, "NA")
                
                # Get assigned_to from RAG output
                assigned_to = rag_assignments.get(sr_id, 'Not Assigned')
                
                # Get semantic workaround as fallback
                semantic_workaround = result.get('Suggested Workaround', 'NA')
                
                # Check if already exists
                if sr_id in existing_sr_ids:
                    # 🆕 UPDATE existing SR with NEW admin data (especially AI workaround)
                    log(f"   Updating existing SR {idx}/{len(results)}: {sr_id}", 
                        84 + int((idx/len(results))*10))
                    
                    # Update with new AI workaround from RAG
                    # IMPORTANT: Preserve user_corrected_workaround (don't overwrite!)
                    success = hist_manager.update_sr_from_admin(
                        sr_id=sr_id,
                        description=result.get('Original Description', ''),
                        notes=result.get('Original Notes/Summary', ''),
                        ai_generated_workaround=ai_workaround if ai_workaround != "NA" else semantic_workaround,
                        priority=result.get('Priority', result.get('Customer Priority', 'P3')),
                        function_category=result.get('Interface', 'Unknown'),
                        resolution_categorization=result.get('Resolution Categorization', 'Unknown'),
                        sla_resolution_categorization_t1=result.get('SLA Resolution', 'Unknown'),
                        sla_resolution_category=result.get('SLA Resolution Category', ''),
                        resolution=semantic_workaround,
                        workaround=semantic_workaround,
                        status=result.get('Status', 'Resolved'),
                        application=result.get('Application', 'Unknown'),
                        assigned_to=assigned_to,
                        preserve_user_feedback=True  # 🔒 DON'T overwrite user corrections
                    )
                    
                    if success:
                        updated_records += 1
                else:
                    # Add new SR (existing logic)
                    log(f"   Adding new SR {idx}/{len(results)}: {sr_id}", 
                        84 + int((idx/len(results))*10))
                    
                    success = hist_manager.add_user_feedback_entry(
                        sr_id=sr_id,
                        description=result.get('Original Description', ''),
                        notes=result.get('Original Notes/Summary', ''),
                        user_corrected_workaround='',  # Empty initially
                        ai_generated_workaround=ai_workaround if ai_workaround != "NA" else semantic_workaround,
                        priority=result.get('Priority', result.get('Customer Priority', 'P3')),
                        function_category=result.get('Interface', 'Unknown'),
                        resolution_categorization=result.get('Resolution Categorization', 'Unknown'),
                        sla_resolution_categorization_t1=result.get('SLA Resolution', 'Unknown'),
                        sla_resolution_category=result.get('SLA Resolution Category', ''),
                        resolution=semantic_workaround,
                        workaround=semantic_workaround,
                        status=result.get('Status', 'Resolved'),
                        application=result.get('Application', 'Unknown'),
                        assigned_to=assigned_to
                    )
                    
                    if success:
                        new_records += 1
            
            # Log results
            if updated_records > 0:
                log(f"   [UPDATE] Updated {updated_records} existing SRs with new AI workarounds", 94)
            
            if new_records > 0:
                log(f"   [NEW] Added {new_records} new SRs to history database", 94)
            
            if new_records == 0 and updated_records == 0:
                log("[WARNING] No records added or updated", 95)
            else:
                log(f"   [OK] Total: {new_records} new + {updated_records} updated = {new_records + updated_records} SRs processed", 95)
        
        log("")
        
        # ==================================================
        # STEP 5.5: Inject to Vector Store (New SRs become searchable)
        # ==================================================
        log("Step 5.5: Injecting new SRs to vector store...", 96)
        log("-" * 80)
        
        try:
            # Import the injection function
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from sr_feedback_app import inject_to_vectorstore
            
            # Prepare RAG results for injection - ONLY NEW SRs!
            # (Existing SRs were already updated in Step 5 with user feedback preserved)
            rag_results_list = None
            new_srs_df = None
            
            if rag_output_path and os.path.exists(rag_output_path):
                rag_results_list = rag_results if rag_results else []
                
                # Filter to only NEW SRs (not in existing_sr_ids)
                if new_records > 0:
                    # Get list of new SR IDs from results
                    new_sr_ids = [
                        str(result.get('SR ID', result.get('Call ID')))
                        for result in results
                        if str(result.get('SR ID', result.get('Call ID'))) not in existing_sr_ids
                    ]
                    
                    # Create DataFrame with only new SRs
                    sr_id_column = 'SR ID' if 'SR ID' in df.columns else 'Call ID'
                    new_srs_df = df[df[sr_id_column].astype(str).isin(new_sr_ids)].copy()
                    
                    # Filter RAG results to only new SRs
                    rag_results_list = [
                        r for r in rag_results_list
                        if str(r.get('SR ID', r.get('Call ID'))) not in existing_sr_ids
                    ]
                    
                    log(f"   Filtered to {len(new_srs_df)} new SRs for injection", 96)
                else:
                    # No new SRs to inject
                    new_srs_df = pd.DataFrame()
                    rag_results_list = []
                    log("   No new SRs to inject (all SRs already exist in vectorstore)", 96)
            else:
                # No RAG results, inject all from df (backward compatibility)
                new_srs_df = df.copy()
            
            # Inject ONLY NEW SRs to vector store
            if new_srs_df is not None and not new_srs_df.empty:
                injected_count = inject_to_vectorstore(new_srs_df, rag_results_list)
                
                if injected_count > 0:
                    log(f"✅ Injected {injected_count} NEW SRs to vector store", 98)
                else:
                    log("[WARNING] No SRs injected to vector store", 98)
            else:
                injected_count = 0
                log("   ⏭️  Skipped injection - existing SRs already updated in Step 5 (user feedback preserved)", 98)
                
        except Exception as inject_error:
            log(f"[WARNING] Vector store injection failed: {str(inject_error)}", 98)
            log("   Continuing without vector store update...", 98)
        
        log("")
        
        # ==================================================
        # STEP 5.6: Cleanup Old Excel Files (Keep only latest)
        # ==================================================
        log("Step 5.6: Cleaning up old Excel files...", 99)
        log("-" * 80)
        
        try:
            # Import the cleanup function
            from sr_feedback_app import cleanup_old_excel_files
            
            # Keep only the latest file (current one)
            deleted_count = cleanup_old_excel_files(keep_latest=1)
            
            if deleted_count > 0:
                log(f"✅ Cleaned up {deleted_count} old Excel files", 99)
            else:
                log("   No old files to cleanup", 99)
                
        except Exception as cleanup_error:
            log(f"[WARNING] Cleanup failed: {str(cleanup_error)}", 99)
            log("   Old files may remain in directories", 99)
        
        log("")
        
        # ==================================================
        # STEP 6: Summary
        # ==================================================
        log("=" * 80, 100)
        log("[SUCCESS] COMPLETE PIPELINE EXECUTED", 100)
        log("=" * 80)
        log("")
        log(f"Summary:")
        log(f"   - SRs analyzed: {len(results)}")
        log(f"   - New SRs added to database: {new_records if 'new_records' in locals() else 0}")
        log(f"   - Existing SRs updated: {updated_records if 'updated_records' in locals() else 0}")
        log(f"   - Semantic analysis: {admin_upload_path}")
        log(f"   - RAG input: {rag_input_path}")
        log(f"   - RAG output: {rag_output_path if rag_output_path else 'N/A (AI workarounds not generated)'}")
        log(f"   - Historical database: {hist_db_path}")
        log("")
        log("Next Steps:")
        log("   1. Users can now search SRs via web interface")
        log("   2. Semantic workarounds are available for all SRs")
        if rag_output_path:
            log("   3. AI-generated workarounds are available from RAG pipeline")
        else:
            log("   3. AI workarounds not available - users can generate on-demand")
        log("   4. Users can provide feedback to improve the system")
        log("")
        
        return True
        
    except Exception as e:
        log("", 0)
        log("=" * 80, 0)
        log("[ERROR] Processing failed", 0)
        log("=" * 80, 0)
        log(f"Error: {e}", 0)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print()
        print("Usage: python admin_upload_and_merge_with_rag.py <excel_file>")
        print()
        print("Example:")
        print("  python admin_upload_and_merge_with_rag.py uploads/today_srs.xls")
        print()
        sys.exit(1)
    
    excel_path = sys.argv[1]
    success = upload_and_merge_with_rag(excel_path)
    
    if not success:
        sys.exit(1)

