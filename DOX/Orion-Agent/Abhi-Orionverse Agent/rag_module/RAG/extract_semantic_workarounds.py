#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract Semantic Workarounds - Trim latest Excel to SR ID and Suggested Workaround only
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import glob

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def find_latest_excel(reports_dir: str = "../output/reports") -> str:
    """
    Find the latest Admin_Upload Excel file in the reports directory
    
    Args:
        reports_dir: Path to reports directory
        
    Returns:
        Path to the latest Excel file
    """
    # Convert to absolute path
    script_dir = Path(__file__).parent
    reports_path = (script_dir / reports_dir).resolve()
    
    # Find all Admin_Upload Excel files
    pattern = str(reports_path / "Admin_Upload_*.xlsx")
    excel_files = glob.glob(pattern)
    
    if not excel_files:
        raise FileNotFoundError(f"No Admin_Upload Excel files found in {reports_path}")
    
    # Get the latest file by modification time
    latest_file = max(excel_files, key=os.path.getmtime)
    
    return latest_file


def find_original_input_file(uploads_dir: str = "../uploads") -> str:
    """
    Find the latest input Excel file in the uploads directory
    
    Args:
        uploads_dir: Path to uploads directory
        
    Returns:
        Path to the latest Excel file
    """
    # Convert to absolute path
    script_dir = Path(__file__).parent
    uploads_path = (script_dir / uploads_dir).resolve()
    
    # Find all Excel files (both .xlsx and .xls)
    patterns = [
        str(uploads_path / "*.xlsx"),
        str(uploads_path / "*.xls")
    ]
    
    excel_files = []
    for pattern in patterns:
        excel_files.extend(glob.glob(pattern))
    
    if not excel_files:
        raise FileNotFoundError(f"No Excel files found in {uploads_path}")
    
    # Get the latest file by modification time
    latest_file = max(excel_files, key=os.path.getmtime)
    
    return latest_file


def merge_with_original(analysis_excel: str, original_excel: str, output_dir: str) -> str:
    """
    Merge original input file with semantic workarounds from analysis
    
    Args:
        analysis_excel: Path to Admin_Upload analysis Excel file
        original_excel: Path to original input Excel file
        output_dir: Path to output directory
        
    Returns:
        Path to the saved merged Excel file
    """
    print("=" * 80)
    print("ADD SEMANTIC WORKAROUNDS TO ORIGINAL FILE")
    print("=" * 80)
    print()
    
    # Read the analysis file (contains AI-generated workarounds)
    print(f"[FILE] Reading analysis file: {os.path.basename(analysis_excel)}")
    try:
        analysis_df = pd.read_excel(analysis_excel)
        print(f"   [OK] Loaded {len(analysis_df)} analyzed records")
    except Exception as e:
        raise Exception(f"Error reading analysis file: {str(e)}")
    
    # Check if required columns exist in analysis
    if 'SR ID' not in analysis_df.columns or 'Suggested Workaround' not in analysis_df.columns:
        print(f"\n[WARN] Available columns: {list(analysis_df.columns)}")
        raise ValueError(f"Missing required columns in analysis file")
    
    # Extract SR ID, Suggested Workaround, Resolution Category, and Status Reason for merging
    columns_to_extract = ['SR ID', 'Suggested Workaround']
    
    # Add Resolution Categories (Similar SRs) if available
    if 'Resolution Categories (Similar SRs)' in analysis_df.columns:
        columns_to_extract.append('Resolution Categories (Similar SRs)')
        print(f"   [+] Including 'Resolution Categories (Similar SRs)' column")
    elif 'Resolution Categorization' in analysis_df.columns:
        columns_to_extract.append('Resolution Categorization')
        print(f"   [+] Including 'Resolution Categorization' column")
    
    # Add Status Reasons (Similar SRs) if available
    if 'Status Reasons (Similar SRs)' in analysis_df.columns:
        columns_to_extract.append('Status Reasons (Similar SRs)')
        print(f"   [+] Including 'Status Reasons (Similar SRs)' column")
    elif 'Status Reason' in analysis_df.columns:
        columns_to_extract.append('Status Reason')
        print(f"   [+] Including 'Status Reason' column")
    
    workarounds_df = analysis_df[columns_to_extract].copy()
    print()
    
    # Read the original input file
    print(f"[FILE] Reading original file: {os.path.basename(original_excel)}")
    try:
        # Handle both .xls and .xlsx files
        if original_excel.endswith('.xls'):
            original_df = pd.read_excel(original_excel, engine='xlrd')
        else:
            original_df = pd.read_excel(original_excel, engine='openpyxl')
        print(f"   [OK] Loaded {len(original_df)} original records")
    except Exception as e:
        raise Exception(f"Error reading original file: {str(e)}")
    
    # Identify SR ID column in original file (could be 'Call ID', 'SR ID', etc.)
    sr_id_column = None
    possible_sr_columns = ['Call ID', 'SR ID', 'call id', 'sr id', 'Inc Call ID']
    for col in possible_sr_columns:
        if col in original_df.columns:
            sr_id_column = col
            break
    
    if sr_id_column is None:
        print(f"\n[WARN] Available columns: {list(original_df.columns)}")
        raise ValueError(f"Could not find SR ID column in original file")
    
    print(f"   [OK] SR ID column identified: '{sr_id_column}'")
    print()
    
    # Rename for consistent merging
    if sr_id_column != 'SR ID':
        workarounds_df = workarounds_df.rename(columns={'SR ID': sr_id_column})
    
    # Merge the workarounds into the original file
    print(f"[MERGE] Merging semantic workarounds...")
    merged_df = original_df.merge(
        workarounds_df, 
        on=sr_id_column, 
        how='left'
    )
    
    # Rename the column to "Semantic Workaround"
    merged_df = merged_df.rename(columns={'Suggested Workaround': 'Semantic Workaround'})
    
    matched_count = merged_df['Semantic Workaround'].notna().sum()
    print(f"   [OK] Merged {matched_count}/{len(merged_df)} records with workarounds")
    
    # Report on additional columns
    if 'Resolution Categories (Similar SRs)' in merged_df.columns:
        res_cat_count = merged_df['Resolution Categories (Similar SRs)'].notna().sum()
        print(f"   [OK] Added 'Resolution Categories (Similar SRs)' for {res_cat_count} records")
    elif 'Resolution Categorization' in merged_df.columns:
        res_cat_count = merged_df['Resolution Categorization'].notna().sum()
        print(f"   [OK] Added 'Resolution Categorization' for {res_cat_count} records")
    
    if 'Status Reasons (Similar SRs)' in merged_df.columns:
        status_count = merged_df['Status Reasons (Similar SRs)'].notna().sum()
        print(f"   [OK] Added 'Status Reasons (Similar SRs)' for {status_count} records")
    elif 'Status Reason' in merged_df.columns:
        status_count = merged_df['Status Reason'].notna().sum()
        print(f"   [OK] Added 'Status Reason' for {status_count} records")
    
    print()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(original_excel))[0]
    output_filename = f"{base_name}_with_Semantic_Workarounds_{timestamp}.xlsx"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the merged Excel to primary location
    print(f"[SAVE] Saving merged file...")
    merged_df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"   [OK] Saved to: {output_path}")
    
    # Also save to RAG/input directory
    script_dir = Path(__file__).parent
    input_dir = script_dir / "input"
    os.makedirs(input_dir, exist_ok=True)
    
    input_output_path = os.path.join(input_dir, output_filename)
    merged_df.to_excel(input_output_path, index=False, engine='openpyxl')
    
    print(f"   [OK] Also saved to: {input_output_path}")
    print()
    
    # Display summary
    print("=" * 80)
    print("[SUCCESS] MERGE COMPLETE")
    print("=" * 80)
    print()
    print(f"[SUMMARY]")
    print(f"   - Original file: {os.path.basename(original_excel)}")
    print(f"   - Original columns: {len(original_df.columns)}")
    print(f"   - Records: {len(merged_df)}")
    print(f"   - Workarounds added: {matched_count}")
    print(f"   - New column: 'Semantic Workaround'")
    print(f"   - Total columns: {len(merged_df.columns)}")
    print(f"   - Output file: {output_filename}")
    print()
    print(f"[SAVED TO] 2 locations:")
    print(f"   1. {output_dir}")
    print(f"   2. {input_dir}")
    print()
    
    # Show column names
    print("[COLUMNS] Output Columns:")
    print("-" * 80)
    for idx, col in enumerate(merged_df.columns, 1):
        marker = "[NEW]" if col == "Semantic Workaround" else "     "
        print(f"   {marker} {idx}. {col}")
    print("-" * 80)
    print()
    
    # Show sample data (first 3 rows with workarounds)
    sample_df = merged_df[merged_df['Semantic Workaround'].notna()].head(3)
    if len(sample_df) > 0:
        print("[SAMPLE] Sample Data (first 3 records with workarounds):")
        print("-" * 80)
        for idx, row in sample_df.iterrows():
            sr_id = row[sr_id_column]
            workaround = str(row['Semantic Workaround'])
            # Truncate workaround for display
            workaround_preview = workaround[:80] + "..." if len(workaround) > 80 else workaround
            print(f"   {sr_id}: {workaround_preview}")
        print("-" * 80)
        print()
    
    return output_path


def main():
    """Main execution function"""
    try:
        # Set up paths
        script_dir = Path(__file__).parent
        reports_dir = "../output/reports"
        uploads_dir = "../uploads"
        output_dir = str(script_dir / "Semantic workarounds")
        
        print()
        print("[SEARCH] Finding latest Admin_Upload Excel file (with AI analysis)...")
        
        # Find the latest analysis Excel file
        analysis_excel = find_latest_excel(reports_dir)
        print(f"   [OK] Found: {os.path.basename(analysis_excel)}")
        print()
        
        print("[SEARCH] Finding latest original input Excel file...")
        
        # Find the latest original input file
        original_excel = find_original_input_file(uploads_dir)
        print(f"   [OK] Found: {os.path.basename(original_excel)}")
        print()
        
        # Merge original file with semantic workarounds
        output_file = merge_with_original(analysis_excel, original_excel, output_dir)
        
        print("[SUCCESS] Original file enhanced with semantic workarounds.")
        print()
        
        return 0
        
    except FileNotFoundError as e:
        print()
        print("=" * 80)
        print("[ERROR] FILE NOT FOUND")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        print("[TIP] Possible solutions:")
        print("   1. Run admin_upload_and_merge.py first to generate an Excel file")
        print("   2. Check that output/reports/ directory exists")
        print("   3. Verify Excel files are in output/reports/ folder")
        print()
        return 1
        
    except ValueError as e:
        print()
        print("=" * 80)
        print("[ERROR] INVALID DATA")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        return 1
        
    except Exception as e:
        print()
        print("=" * 80)
        print("[ERROR] EXCEPTION OCCURRED")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())

