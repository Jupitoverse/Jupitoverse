#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Upload & Merge - Upload Excel and immediately add to historical data
"""

# Fix Windows console encoding issues - MUST BE FIRST
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import pickle
import shutil
from datetime import datetime
from pathlib import Path
from comprehensive_sr_analyzer import ComprehensiveSRAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

def upload_and_merge(excel_path, progress_callback=None):
    """
    Upload Excel, analyze SRs, and immediately add to historical data
    Args:
        excel_path: Path to Excel file
        progress_callback: Optional callback function(percent, message) for progress updates
    """
    def log(message, percent=None):
        """Helper to both print and call progress_callback"""
        print(message)
        if progress_callback and percent is not None:
            progress_callback(percent, message)
    
    log("=" * 80, 5)
    log("ADMIN: UPLOAD & MERGE TO HISTORICAL DATA")
    log("=" * 80)
    log("")
    log(f"File: {excel_path}")
    log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    
    if not os.path.exists(excel_path):
        log(f"[ERROR] File not found: {excel_path}", 0)
        return False
    
    try:
        # Step 1: Analyze SRs
        log("Step 1: Analyzing SRs...", 10)
        log("-" * 80)
        
        import pandas as pd
        df = pd.read_excel(excel_path)
        
        # Standardize column names
        column_mapping = {
            'Call ID': ['SR ID', 'call id', 'sr id'],
            'Description': ['description', 'Issue Description'],
            'Notes': ['notes', 'Additional Notes', 'Resolution'],
            'Customer Priority': ['Priority', 'priority'],
            'STATUS': ['Status', 'status'],
            'Assigned Group': ['Application', 'assigned group'],
            'Submit Date': ['Created Date', 'submit date']
        }
        
        for standard_col, alternatives in column_mapping.items():
            if standard_col not in df.columns:
                for alt_col in alternatives:
                    if alt_col in df.columns:
                        df.rename(columns={alt_col: standard_col}, inplace=True)
                        break
        
        log(f"   Found {len(df)} SRs in Excel", 15)
        
        # Analyze
        log("", 15)
        log("Step 1.1: Analyzing SRs with AI...", 20)
        log("-" * 80, 20)
        analyzer = ComprehensiveSRAnalyzer()
        sr_data_list = df.to_dict('records')
        
        # Analyze each SR individually to show progress
        results = []
        total_srs = len(sr_data_list)
        for idx, sr_data in enumerate(sr_data_list, 1):
            sr_id = sr_data.get('SR ID', f'SR{idx}')
            log(f"   Analyzing SR {idx}/{total_srs}: {sr_id}", 20 + int((idx/total_srs)*15))
            
            # Analyze single SR
            sr_result = analyzer.analyze_sr_batch([sr_data])
            if sr_result:
                results.extend(sr_result)
        
        log(f"", 35)
        log(f"   [OK] Analyzed {len(results)} SRs successfully", 35)
        log("")
        
        # Step 2: Load historical index
        log("Step 2: Loading historical data...", 40)
        log("-" * 80)
        
        hist_path = 'vector store/historical_sr_index.pkl'
        with open(hist_path, 'rb') as f:
            hist_index = pickle.load(f)
        
        historical_data = hist_index.get('historical_data', [])
        existing_sr_ids = {sr.get('sr_id') for sr in historical_data}
        
        log(f"   Current historical records: {len(historical_data):,}", 45)
        log("")
        
        # Step 3: Convert analyzed SRs to historical format
        log("Step 3: Adding new SRs to historical data...", 50)
        log("-" * 80, 50)
        
        new_records = []
        skipped = 0
        
        for idx, result in enumerate(results, 1):
            sr_id = result.get('SR ID', 'Unknown')
            
            # Skip if already exists
            if sr_id in existing_sr_ids:
                log(f"   Skipping existing SR {idx}/{len(results)}: {sr_id}", 50 + int((idx/len(results))*10))
                skipped += 1
                continue
            
            # Get workaround from analysis
            workaround = result.get('Suggested Workaround', 'NA')
            
            # Create historical record
            historical_record = {
                'sr_id': sr_id,
                'description': result.get('Original Description', ''),
                'searchable_text': f"{result.get('Original Description', '')} {result.get('Original Notes/Summary', '')}",
                'priority': result.get('Priority', 'P3'),
                'assigned_group': result.get('Application', 'Unknown'),
                'status': result.get('Status', 'Resolved'),
                'outcome': {
                    'has_workaround': workaround != 'NA',
                    'workaround_text': workaround,
                    'resolution_type': 'Admin Upload'
                },
                'resolution': workaround,  # This is what semantic search uses
                'created_date': result.get('Created Date', datetime.now().isoformat()),
                'success_flag': True,
                'application': result.get('Application', 'Unknown'),
                'functional_area': result.get('Interface', 'Unknown'),
                'keywords': [],
                'phase1_workaround': {}  # Can be enhanced later
            }
            
            new_records.append(historical_record)
            log(f"   Adding SR {idx}/{len(results)}: {sr_id}", 50 + int((idx/len(results))*10))
        
        if skipped > 0:
            log(f"   [SKIP] Skipped {skipped} existing SRs")
        
        if not new_records:
            log("")
            log("[WARNING] No new records to add (all SRs already exist)", 60)
            log("")
            # Still save the Excel for user review
            log("Step 4: Saving analyzed Excel for user review...", 80)
            log("-" * 80)
            
            output_dir = 'output/reports'
            os.makedirs(output_dir, exist_ok=True)
            
            results_df = pd.DataFrame(results)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f"Admin_Upload_{timestamp}.xlsx")
            
            results_df.to_excel(output_path, index=False)
            log(f"   [OK] Saved: {output_path}", 95)
            log("")
            log("=" * 80)
            log("[SUCCESS] ANALYSIS COMPLETE (No new records added)", 100)
            log("=" * 80)
            log("")
            log(f"Summary:")
            log(f"   - Analyzed SRs: {len(results)}")
            log(f"   - Already in system: {skipped}")
            log(f"   - Total historical: {len(historical_data):,}")
            log(f"   - Excel for review: {output_path}")
            log("")
            return True
        
        log("")
        log(f"   Total new records: {len(new_records)}", 60)
        log("")
        
        # Step 4: Backup and save
        log("Step 4: Saving updated historical data...", 65)
        log("-" * 80)
        
        # Backup
        backup_path = f"{hist_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(hist_path, backup_path)
        log(f"   [BACKUP] Backup created", 68)
        
        # Add new records
        historical_data.extend(new_records)
        hist_index['historical_data'] = historical_data
        hist_index['indexed_at'] = datetime.now().isoformat()
        
        # Save
        with open(hist_path, 'wb') as f:
            pickle.dump(hist_index, f)
        
        log(f"   [OK] Saved {len(historical_data):,} total records", 72)
        log("")
        
        # Step 5: Rebuild vectors
        log("Step 5: Rebuilding TF-IDF vectors...", 75)
        log("-" * 80)
        
        log(f"   Preparing {len(historical_data):,} documents...", 76)
        searchable_texts = [sr.get('searchable_text', '') for sr in historical_data]
        
        log("   Initializing TF-IDF vectorizer...", 78)
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8,
            stop_words='english'
        )
        
        log("   Computing TF-IDF matrix (this may take 10-30 seconds)...", 80)
        # Note: This is a long-running operation with no intermediate progress
        tfidf_matrix = vectorizer.fit_transform(searchable_texts)
        log("   [OK] TF-IDF computation complete!", 85)
        
        hist_index['vectorizer'] = vectorizer
        hist_index['tfidf_matrix'] = tfidf_matrix
        
        log("   Saving vectors to database...", 86)
        # Save again with vectors
        with open(hist_path, 'wb') as f:
            pickle.dump(hist_index, f)
        
        log(f"   [OK] TF-IDF matrix: {tfidf_matrix.shape}", 88)
        log(f"   [OK] Features: {tfidf_matrix.shape[1]:,}")
        log(f"   [OK] Documents: {tfidf_matrix.shape[0]:,}")
        log("")
        
        # Step 6: Save analyzed Excel for user review
        log("Step 6: Saving analyzed Excel for user review...", 92)
        log("-" * 80)
        
        output_dir = 'output/reports'
        os.makedirs(output_dir, exist_ok=True)
        
        results_df = pd.DataFrame(results)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(output_dir, f"Admin_Upload_{timestamp}.xlsx")
        
        results_df.to_excel(output_path, index=False)
        log(f"   [OK] Saved: {output_path}", 97)
        log("")
        
        # Summary
        log("=" * 80)
        log("[SUCCESS] UPLOAD & MERGE COMPLETE", 100)
        log("=" * 80)
        log("")
        log(f"Summary:")
        log(f"   - New SRs added: {len(new_records)}")
        log(f"   - Total historical: {len(historical_data):,}")
        log(f"   - Vectors rebuilt: YES")
        log(f"   - Excel for review: {output_path}")
        log("")
        log("Next Steps:")
        log("   1. Users can now access web interface")
        log("   2. Review AI workarounds")
        log("   3. Provide feedback on incorrect ones")
        log("   4. System learns from feedback")
        log("")
        log("   Run: START_FEEDBACK_SYSTEM.bat")
        log("")
        
        return True
        
    except Exception as e:
        log("", 0)
        log("=" * 80, 0)
        log("[ERROR] Processing failed", 0)
        log("=" * 80, 0)
        log("", 0)
        log(f"Error: {e}", 0)
        log("", 0)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print()
        print("Usage: python admin_upload_and_merge.py <excel_file>")
        print()
        print("Example:")
        print("  python admin_upload_and_merge.py uploads/today_srs.xls")
        print()
        sys.exit(1)
    
    excel_path = sys.argv[1]
    success = upload_and_merge(excel_path)
    
    if not success:
        sys.exit(1)

