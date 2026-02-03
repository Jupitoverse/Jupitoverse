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

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Fix SQLite version for ChromaDB on older Linux systems
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from analyzers.comprehensive_sr_analyzer import ComprehensiveSRAnalyzer


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
        return False, None, []
    
    try:
        # ==================================================
        # STEP 1: Analyze SRs with Semantic Search
        # ==================================================
        log("Step 1: Analyzing SRs with Semantic Search...", 10)
        log("-" * 80)
        
        df = pd.read_excel(excel_path)
        
        # Clean Excel data - remove blank rows and date footer
        def clean_excel_data(df_input):
            """Remove blank rows and date footer from Excel data"""
            df_clean = df_input.copy()
            
            # Get the SR ID column
            sr_col = None
            for col in ['Call ID', 'SR ID', 'call id', 'sr id']:
                if col in df_clean.columns:
                    sr_col = col
                    break
            
            if sr_col:
                # Remove rows where SR ID is blank/NaN
                df_clean = df_clean.dropna(subset=[sr_col])
                df_clean = df_clean[df_clean[sr_col].astype(str).str.strip() != '']
                
                # Remove rows that look like dates (contain month names or date patterns)
                # These are footer rows like "Dec 23, 2025 9:30 PM"
                date_patterns = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 
                                'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ',
                                ' AM', ' PM', '/202', '-202']
                mask = ~df_clean[sr_col].astype(str).str.contains('|'.join(date_patterns), case=False, na=False)
                df_clean = df_clean[mask]
            
            # Drop any completely blank rows
            df_clean = df_clean.dropna(how='all')
            
            return df_clean.reset_index(drop=True)
        
        original_count = len(df)
        df = clean_excel_data(df)
        cleaned_count = original_count - len(df)
        if cleaned_count > 0:
            log(f"   🧹 Cleaned {cleaned_count} invalid/blank/date rows from Excel", 12)
        
        # Standardize column names
        column_mapping = {
            'Call ID': ['SR ID', 'call id', 'sr id', 'Inc Call ID'],
            'Description': ['description', 'Issue Description', 'Inc Description'],
            'Notes': ['notes', 'Additional Notes', 'Resolution', 'Inc Resolution'],
            'Customer Priority': ['Priority', 'priority', 'UTS Priority'],
            'STATUS': ['Status', 'status', 'Inc Current EIR - Status'],
            'Assigned Group': ['Application', 'assigned group', 'Assignee Support Group'],
            'Submit Date': ['Created Date', 'submit date', 'Inc Created Date'],
            # SLA resolution categorization fields
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
                # Preserve Reported Date for business day age calculation
                for r in sr_result:
                    if 'Reported Date' not in r and 'Reported Date' in sr_data:
                        r['Reported Date'] = sr_data.get('Reported Date')
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
        
        # Import the extraction function (RAG folder is in parent's parent directory)
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'RAG'))
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
            # Import RAG pipeline (RAG folder is in parent's parent directory)
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'RAG', 'pipeline'))
            
            # Use Multi-Model RAG pipeline (4 LLM calls for better accuracy)
            from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline as SRAnalysisPipeline
            log("   Initializing Multi-Model RAG pipeline (5 LLM calls)...", 62)
            use_chatgpt = True
            
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
                
                # Log LLM usage statistics and save for admin dashboard
                try:
                    usage = rag_pipeline.llm.get_usage_summary()
                    log("")
                    log("💰 LLM USAGE SUMMARY:", 76)
                    log(f"   📊 Total API Calls: {usage.get('total_requests', usage.get('total_calls', 0))}", 76)
                    log(f"   📥 Input Tokens: {usage.get('total_input_tokens', 0):,}", 76)
                    log(f"   📤 Output Tokens: {usage.get('total_output_tokens', 0):,}", 76)
                    log(f"   💵 Total Cost: ${usage.get('total_cost', 0):.4f}", 76)
                    log("")
                    
                    # Save usage to JSON file for admin dashboard
                    import json
                    usage_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'database', 'llm_usage_stats.json')
                    usage_data = {
                        'last_updated': datetime.now().isoformat(),
                        'last_run': {
                            'total_calls': usage.get('total_requests', usage.get('total_calls', 0)),
                            'input_tokens': usage.get('total_input_tokens', 0),
                            'output_tokens': usage.get('total_output_tokens', 0),
                            'cost': usage.get('total_cost', 0),
                            'srs_processed': len(rag_results)
                        }
                    }
                    
                    # Load existing cumulative data if exists
                    cumulative = {'total_cost': 0, 'total_tokens': 0, 'total_calls': 0}
                    if os.path.exists(usage_file):
                        try:
                            with open(usage_file, 'r') as f:
                                existing = json.load(f)
                                cumulative = existing.get('cumulative', cumulative)
                        except:
                            pass
                    
                    # Update cumulative
                    cumulative['total_cost'] += usage.get('total_cost', 0)
                    cumulative['total_tokens'] += usage.get('total_input_tokens', 0) + usage.get('total_output_tokens', 0)
                    cumulative['total_calls'] += usage.get('total_requests', usage.get('total_calls', 0))
                    usage_data['cumulative'] = cumulative
                    
                    with open(usage_file, 'w') as f:
                        json.dump(usage_data, f, indent=2)
                        
                except Exception as usage_error:
                    log(f"   [NOTE] Could not retrieve usage stats: {usage_error}", 76)
            else:
                log("[WARNING] No RAG results generated", 75)
        except Exception as rag_error:
            log(f"[WARNING] RAG pipeline error: {str(rag_error)}", 75)
            log("   Continuing without AI workarounds...", 75)
        
        log("")
        
        # ==================================================
        # STEP 5: Merge to Historical Database (history_data.db)
        # ==================================================
        log("Step 5: Merging to ChromaDB vectorstore...", 80)
        log("-" * 80)
        
        # Import history database manager
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'RAG', 'utils'))
        from history_db_manager import HistoryDatabaseManager
        
        # Initialize ChromaDB - vectorstore is in data/vectorstore/chromadb_store
        chromadb_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'vectorstore', 'chromadb_store')
        hist_manager = HistoryDatabaseManager(chromadb_path=chromadb_path)
        
        if not hist_manager.use_chromadb:
            log("[WARNING] History database not loaded. Data will not be merged.", 82)
        else:
            # Get existing SR IDs from ChromaDB
            existing_sr_ids = set()
            try:
                # Get all records from ChromaDB to check existing SR IDs
                all_records = hist_manager.chromadb_collection.get(include=['metadatas'])
                for metadata in all_records.get('metadatas', []):
                    sr_id = metadata.get('call_id')
                    if sr_id:
                        existing_sr_ids.add(str(sr_id).upper())
                log(f"   Current ChromaDB records: {len(existing_sr_ids)}", 82)
            except Exception as e:
                log(f"   [WARN] Could not get existing records: {e}", 82)
            
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
                
                # 🔧 FIX: Get assigned_to - prefer RAG output, fallback to semantic analyzer result
                # This ensures every SR gets an assignment from the intelligent_team_assignment function
                assigned_to = rag_assignments.get(sr_id)
                if not assigned_to or assigned_to in ['Not Assigned', 'NA', '', 'None']:
                    # Use assignment from semantic analyzer results
                    assigned_to = result.get('Assigned To', 'Not Assigned')
                
                # Final fallback - should not happen with the new guaranteed assignment
                if not assigned_to or assigned_to in ['NA', '', 'None']:
                    assigned_to = 'Not Assigned'
                
                # Get semantic workaround (from semantic search - AI suggestion)
                semantic_workaround = result.get('Suggested Workaround', 'NA')
                
                # 🔧 FIX: Get ORIGINAL workaround from input data (if exists)
                # Look for actual workaround/resolution columns from the original input file
                original_workaround = result.get('Workaround', 
                                      result.get('Resolution', 
                                      result.get('Original Workaround', '')))
                # Clean up - don't use semantic_workaround as original workaround
                if not original_workaround or str(original_workaround).strip() in ['', 'NA', 'N/A', 'nan', 'None']:
                    original_workaround = ''  # Leave empty if no real original workaround
                
                # Check if already exists
                if sr_id in existing_sr_ids:
                    # Update existing SR with new admin data (preserves user corrections)
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
                        resolution=original_workaround if original_workaround else '',  # 🔧 FIX: Use original, not semantic
                        workaround=original_workaround if original_workaround else '',  # 🔧 FIX: Use original, not semantic
                        status=result.get('Status', 'Resolved'),
                        application=result.get('Application', 'Unknown'),
                        assigned_to=assigned_to,
                        preserve_user_feedback=True,  # 🔒 DON'T overwrite user corrections
                        reported_date=result.get('Reported Date')  # For business day age calculation
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
                        resolution=original_workaround if original_workaround else '',  # 🔧 FIX: Use original, not semantic
                        workaround=original_workaround if original_workaround else '',  # 🔧 FIX: Use original, not semantic
                        status=result.get('Status', 'Resolved'),
                        application=result.get('Application', 'Unknown'),
                        assigned_to=assigned_to,
                        reported_date=result.get('Reported Date')  # For business day age calculation
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
        
        # NOTE: Step 5.5 (Vector Store Injection) removed - data is already saved to ChromaDB
        # in Step 5 via HistoryDatabaseManager.add_user_feedback_entry() and update_sr_from_admin()
        
        # ==================================================
        # STEP 5.5: Final Cleanup (Input, Output, Email files)
        # ==================================================
        log("Step 5.6: Final cleanup of temporary files...", 99)
        log("-" * 80)
        
        from pathlib import Path
        total_deleted = 0
        
        # Directories to clean up
        cleanup_dirs = [
            ('RAG input', Path(__file__).parent.parent.parent / 'RAG' / 'input'),
            ('RAG output', Path(__file__).parent.parent.parent / 'RAG' / 'output'),
            ('Email reports', Path(__file__).parent.parent.parent / 'downloads' / 'email_reports'),
            ('LLM output', Path(__file__).parent.parent.parent / 'RAG' / 'llm output'),
        ]
        
        for dir_name, dir_path in cleanup_dirs:
            try:
                if dir_path.exists():
                    excel_files = list(dir_path.glob("*.xlsx")) + list(dir_path.glob("*.xls"))
                    deleted_count = 0
                    
                    for excel_file in excel_files:
                        try:
                            excel_file.unlink()
                            deleted_count += 1
                        except Exception:
                            pass
                    
                    if deleted_count > 0:
                        log(f"   ✅ {dir_name}: Cleaned {deleted_count} file(s)", 99)
                        total_deleted += deleted_count
            except Exception as e:
                log(f"   [WARN] {dir_name} cleanup error: {e}", 99)
        
        if total_deleted > 0:
            log(f"✅ Total files cleaned up: {total_deleted}", 99)
        else:
            log("   No temporary files to cleanup", 99)
        
        log("")
        
        # ==================================================
        # STEP 6: Summary (with Assignment Distribution)
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
        log(f"   - Historical database: ChromaDB (data/vectorstore/chromadb_store)")
        log("")
        
        # Show assignment distribution summary
        log("Assignment Distribution:")
        try:
            from collections import Counter
            # Collect all assignments from results
            assignments = [r.get('Assigned To', 'Not Assigned') for r in results]
            assignment_counts = Counter(assignments)
            
            unassigned = assignment_counts.pop('Not Assigned', 0) + assignment_counts.pop('NA', 0) + assignment_counts.pop('', 0)
            
            if assignment_counts:
                for assignee, count in sorted(assignment_counts.items(), key=lambda x: -x[1]):
                    log(f"   - {assignee}: {count} SR(s)")
            
            if unassigned > 0:
                log(f"   - Not Assigned: {unassigned} SR(s) [WARNING]")
            else:
                log("   ✅ All SRs have been assigned!")
        except Exception as e:
            log(f"   [Could not calculate assignment distribution: {e}]")
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
        
        return True, admin_upload_path, []
        
    except Exception as e:
        log("", 0)
        log("=" * 80, 0)
        log("[ERROR] Processing failed", 0)
        log("=" * 80, 0)
        log(f"Error: {e}", 0)
        import traceback
        traceback.print_exc()
        return False, None, []


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

