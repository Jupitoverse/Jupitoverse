#!/usr/bin/env python3
"""
Convert OSO Activity Data Excel file to JSON for faster loading
Run this script once to convert the Excel file to JSON format
"""

import pandas as pd
import json
import os
from pathlib import Path

def convert_excel_to_json():
    """Convert Excel file to JSON format"""
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    excel_path = project_root / 'OSO_activity_data (1).xlsx'
    json_path = project_root / 'backend' / 'data' / 'oso_activity_data.json'
    
    # Create data directory if it doesn't exist
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not excel_path.exists():
        print(f"[ERROR] Excel file not found: {excel_path}")
        return False
    
    try:
        print(f"[INFO] Reading Excel file: {excel_path}")
        df = pd.read_excel(excel_path, engine='openpyxl')
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Fill NaN values with empty strings
        df = df.fillna('')
        
        # Convert to list of dictionaries
        print(f"[INFO] Converting {len(df)} records to JSON format...")
        data = {
            'columns': list(df.columns),
            'data': df.to_dict('records'),
            'total_rows': len(df),
            'metadata': {
                'source_file': str(excel_path),
                'converted_at': pd.Timestamp.now().isoformat(),
                'columns_count': len(df.columns)
            }
        }
        
        # Save to JSON file
        print(f"[INFO] Saving to JSON file: {json_path}")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        file_size = json_path.stat().st_size / (1024 * 1024)  # Size in MB
        print(f"[SUCCESS] Converted {len(df)} records to JSON")
        print(f"[INFO] JSON file size: {file_size:.2f} MB")
        print(f"[INFO] JSON file saved at: {json_path}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to convert Excel to JSON: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("OSO Activity Data - Excel to JSON Converter")
    print("=" * 60)
    success = convert_excel_to_json()
    if success:
        print("\n[SUCCESS] Conversion completed! You can now use the JSON file.")
    else:
        print("\n[ERROR] Conversion failed. Please check the error messages above.")
    print("=" * 60)
