import pandas as pd
import os
from pathlib import Path
import json

def read_past_data_files():
    """Read all Excel files from past_data folder and analyze resolution columns"""
    past_data_dir = Path("past_data")
    all_data = []
    
    print("Reading past data files...")
    for file in past_data_dir.glob("*.xls"):
        try:
            df = pd.read_excel(file)
            all_data.append(df)
            print(f"✓ Read {file.name}: {len(df)} rows")
        except Exception as e:
            print(f"✗ Error reading {file.name}: {e}")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal rows from past data: {len(combined_df)}")
    print(f"Columns: {list(combined_df.columns)}")
    
    return combined_df

def analyze_resolution_categories(df):
    """Analyze resolution and SLA category columns"""
    print("\n" + "="*80)
    print("ANALYZING RESOLUTION CATEGORIES")
    print("="*80)
    
    # Find columns related to resolution
    resolution_cols = [col for col in df.columns if 'resolution' in col.lower()]
    sla_cols = [col for col in df.columns if 'sla' in col.lower() or 'category' in col.lower()]
    
    print(f"\nResolution columns found: {resolution_cols}")
    print(f"SLA/Category columns found: {sla_cols}")
    
    # Analyze resolution tier 3
    if resolution_cols:
        for col in resolution_cols:
            print(f"\n--- {col} ---")
            print(f"Unique values: {df[col].nunique()}")
            print(f"Value counts:")
            print(df[col].value_counts().head(20))
    
    # Analyze SLA categories
    if sla_cols:
        for col in sla_cols:
            print(f"\n--- {col} ---")
            print(f"Unique values: {df[col].nunique()}")
            print(f"Value counts:")
            print(df[col].value_counts().head(20))
    
    return resolution_cols, sla_cols

def read_category_mappings():
    """Read category mapping files"""
    print("\n" + "="*80)
    print("READING CATEGORY MAPPINGS")
    print("="*80)
    
    # Read midmarket amdocs issue mapping
    amdocs_df = pd.read_csv("category mapping/midmarket_amdocs_issue(Sheet1).csv")
    print(f"\n✓ Read Amdocs Issue Mapping: {len(amdocs_df)} rows")
    print(f"Columns: {list(amdocs_df.columns)}")
    print("\nSample data:")
    print(amdocs_df.head(10))
    
    # Read incident resolution SLA category mapping
    sla_df = pd.read_csv("category mapping/incident_resolution_sla_category_and_status(Sheet1).csv")
    print(f"\n✓ Read SLA Category Mapping: {len(sla_df)} rows")
    print(f"Columns: {list(sla_df.columns)}")
    print("\nSample data:")
    print(sla_df.head(10))
    
    return amdocs_df, sla_df

def create_workaround_mapping(past_df, amdocs_df, sla_df):
    """Create a comprehensive workaround mapping"""
    print("\n" + "="*80)
    print("CREATING WORKAROUND MAPPING")
    print("="*80)
    
    # Create mapping dictionaries
    
    # 1. Amdocs Issue Mapping (Tier1 -> Tier2 -> Tier3 -> Workaround)
    amdocs_mapping = {}
    for _, row in amdocs_df.iterrows():
        tier1 = str(row['Tier1']).strip()
        tier2 = str(row['Tier2']).strip()
        tier3 = str(row['Tier3']).strip()
        workaround = str(row['Workaround comment']).strip() if pd.notna(row['Workaround comment']) else ""
        status = str(row['Status']).strip() if pd.notna(row['Status']) else ""
        pmr = str(row['PMR Masking']).strip() if pd.notna(row['PMR Masking']) else ""
        
        key = f"{tier1}|{tier2}|{tier3}"
        amdocs_mapping[key] = {
            'tier1': tier1,
            'tier2': tier2,
            'tier3': tier3,
            'workaround': workaround,
            'status': status,
            'pmr_masking': pmr,
            'issue_type': 'amdocs_internal'
        }
    
    # 2. Customer Issue Mapping (Tier1 -> Tier2 -> Tier3 -> Workaround)
    customer_mapping = {}
    for _, row in sla_df.iterrows():
        tier1 = str(row['Tier1']).strip()
        tier2 = str(row['Tier2']).strip()
        tier3 = str(row['Tier3']).strip()
        workaround = str(row['Workaround comment']).strip() if pd.notna(row['Workaround comment']) else ""
        status = str(row['Status']).strip() if pd.notna(row['Status']) else ""
        pmr = str(row['PMR Masking']).strip() if pd.notna(row['PMR Masking']) else ""
        
        key = f"{tier1}|{tier2}|{tier3}"
        customer_mapping[key] = {
            'tier1': tier1,
            'tier2': tier2,
            'tier3': tier3,
            'workaround': workaround,
            'status': status,
            'pmr_masking': pmr,
            'issue_type': 'customer_third_party'
        }
    
    # Combine both mappings
    combined_mapping = {**amdocs_mapping, **customer_mapping}
    
    print(f"\nTotal Amdocs Issue mappings: {len(amdocs_mapping)}")
    print(f"Total Customer Issue mappings: {len(customer_mapping)}")
    print(f"Total combined mappings: {len(combined_mapping)}")
    
    return combined_mapping

def save_mapping_to_file(mapping):
    """Save the mapping to a JSON file for easy use"""
    output_file = "workaround_mapping.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved mapping to {output_file}")
    
    # Also save as a readable text file
    output_txt = "workaround_mapping.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("WORKAROUND MAPPING REFERENCE\n")
        f.write("="*80 + "\n\n")
        
        # Group by issue type
        amdocs_items = [v for v in mapping.values() if v['issue_type'] == 'amdocs_internal']
        customer_items = [v for v in mapping.values() if v['issue_type'] == 'customer_third_party']
        
        f.write("AMDOCS INTERNAL ISSUES\n")
        f.write("-"*80 + "\n")
        for item in amdocs_items:
            f.write(f"\nTier1: {item['tier1']}\n")
            f.write(f"Tier2: {item['tier2']}\n")
            f.write(f"Tier3: {item['tier3']}\n")
            f.write(f"Workaround: {item['workaround']}\n")
            f.write(f"Status: {item['status']}\n")
            f.write(f"PMR Masking: {item['pmr_masking']}\n")
            f.write("-"*40 + "\n")
        
        f.write("\n\nCUSTOMER/THIRD-PARTY ISSUES\n")
        f.write("-"*80 + "\n")
        for item in customer_items:
            f.write(f"\nTier1: {item['tier1']}\n")
            f.write(f"Tier2: {item['tier2']}\n")
            f.write(f"Tier3: {item['tier3']}\n")
            f.write(f"Workaround: {item['workaround']}\n")
            f.write(f"Status: {item['status']}\n")
            f.write(f"PMR Masking: {item['pmr_masking']}\n")
            f.write("-"*40 + "\n")
    
    print(f"✓ Saved readable format to {output_txt}")

def analyze_past_data_matches(past_df, mapping):
    """Analyze how many past data entries match the mapping"""
    print("\n" + "="*80)
    print("ANALYZING PAST DATA MATCHES")
    print("="*80)
    
    # Try to find resolution columns
    resolution_cols = [col for col in past_df.columns if 'resolution' in col.lower() or 'tier' in col.lower()]
    
    print(f"\nAvailable columns in past data:")
    for i, col in enumerate(past_df.columns, 1):
        print(f"{i}. {col}")
    
    print(f"\nColumns that might contain tier information: {resolution_cols}")

def main():
    print("="*80)
    print("WORKAROUND MAPPING ANALYSIS")
    print("="*80)
    
    # Step 1: Read past data
    past_df = read_past_data_files()
    
    # Step 2: Analyze resolution categories
    resolution_cols, sla_cols = analyze_resolution_categories(past_df)
    
    # Step 3: Read category mappings
    amdocs_df, sla_df = read_category_mappings()
    
    # Step 4: Create comprehensive mapping
    mapping = create_workaround_mapping(past_df, amdocs_df, sla_df)
    
    # Step 5: Save mapping
    save_mapping_to_file(mapping)
    
    # Step 6: Analyze matches
    analyze_past_data_matches(past_df, mapping)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("1. workaround_mapping.json - JSON format for programmatic use")
    print("2. workaround_mapping.txt - Human-readable format")

if __name__ == "__main__":
    main()




