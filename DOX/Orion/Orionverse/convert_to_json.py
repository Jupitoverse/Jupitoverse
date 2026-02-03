#!/usr/bin/env python
# convert_to_json.py - Convert Excel files to JSON
import pandas as pd
import json
import os

def convert_excel_to_json(file_path, output_path):
    """Convert Excel file to JSON with proper date handling"""
    print(f"Converting {file_path}...")
    df = pd.read_excel(file_path)
    
    # Convert all datetime columns to strings
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].astype(str)
    
    # Replace NaN with None
    df = df.where(pd.notnull(df), None)
    
    # Convert to dict
    data = df.to_dict(orient='records')
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(data)} records to {output_path}")
    return len(data)

def convert_multi_sheet_excel_to_json(file_path, output_path):
    """Convert multi-sheet Excel file to JSON"""
    print(f"Converting {file_path}...")
    xls = pd.ExcelFile(file_path)
    
    sheets_data = {}
    for sheet_name in xls.sheet_names:
        print(f"  Processing sheet: {sheet_name}")
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Convert all datetime columns to strings
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].astype(str)
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        sheets_data[sheet_name] = df.to_dict(orient='records')
        print(f"    ✅ {len(sheets_data[sheet_name])} records")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sheets_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(sheets_data)} sheets to {output_path}")
    return len(sheets_data)

if __name__ == "__main__":
    # Convert Ultron.xls
    try:
        count = convert_excel_to_json(
            'Ultron (16).xls',
            'backend/data/ultron_data.json'
        )
        print(f"✅ Ultron: {count} records")
    except Exception as e:
        print(f"❌ Error converting Ultron: {e}")
    
    # Convert Orion Outage Report
    try:
        count = convert_multi_sheet_excel_to_json(
            'Orion Outage Report for 20251120Abhi.xlsx',
            'backend/data/outage_report_data.json'
        )
        print(f"✅ Outage Report: {count} sheets")
    except Exception as e:
        print(f"❌ Error converting Outage Report: {e}")
    
    print("\n🎉 All conversions complete!")



