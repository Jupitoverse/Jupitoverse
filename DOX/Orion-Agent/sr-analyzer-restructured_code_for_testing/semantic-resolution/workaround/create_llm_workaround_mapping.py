import pandas as pd
import os
from pathlib import Path
from collections import defaultdict
import re

def read_past_data_files():
    """Read all Excel files from past_data folder"""
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
    
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal rows from past data: {len(combined_df)}")
    
    return combined_df

def read_category_mappings():
    """Read category mapping files"""
    print("\nReading category mappings...")
    
    # Read midmarket amdocs issue mapping
    amdocs_df = pd.read_csv("category mapping/midmarket_amdocs_issue(Sheet1).csv")
    print(f"✓ Read Amdocs Issue Mapping: {len(amdocs_df)} rows")
    
    # Read incident resolution SLA category mapping (customer issues)
    customer_df = pd.read_csv("category mapping/incident_resolution_sla_category_and_status(Sheet1).csv")
    print(f"✓ Read Customer Issue Mapping: {len(customer_df)} rows")
    
    return amdocs_df, customer_df

def extract_workaround_examples(past_df):
    """Extract actual workaround examples from past data"""
    print("\nExtracting workaround examples from past data...")
    
    # Group by tier categories and collect workaround examples
    workaround_examples = defaultdict(list)
    
    # Filter rows with non-empty workarounds
    past_df_with_wa = past_df[past_df['Workaround'].notna() & (past_df['Workaround'].str.strip() != '')]
    
    print(f"Found {len(past_df_with_wa)} records with workarounds")
    
    for _, row in past_df_with_wa.iterrows():
        tier1 = str(row['SLA Resolution Categorization T1']).strip() if pd.notna(row['SLA Resolution Categorization T1']) else ""
        tier2 = str(row['SLA Resolution Category']).strip() if pd.notna(row['SLA Resolution Category']) else ""
        tier3 = str(row['Resolution Categorization(Resolution Category Tier 3)']).strip() if pd.notna(row['Resolution Categorization(Resolution Category Tier 3)']) else ""
        workaround = str(row['Workaround']).strip() if pd.notna(row['Workaround']) else ""
        
        if tier1 and tier2 and tier3 and workaround:
            key = f"{tier1}|{tier2}|{tier3}"
            # Clean workaround text
            workaround_clean = re.sub(r'\s+', ' ', workaround).strip()
            if len(workaround_clean) > 10:  # Only meaningful workarounds
                workaround_examples[key].append(workaround_clean)
    
    print(f"Created workaround examples for {len(workaround_examples)} unique tier combinations")
    
    return workaround_examples

def create_comprehensive_mapping(amdocs_df, customer_df, workaround_examples):
    """Create comprehensive mapping with examples"""
    print("\nCreating comprehensive mapping...")
    
    mapping_data = []
    
    # Process Amdocs Issue mappings
    print("Processing Amdocs Issue mappings...")
    for _, row in amdocs_df.iterrows():
        tier1 = str(row['Tier1']).strip()
        tier2 = str(row['Tier2']).strip()
        tier3 = str(row['Tier3']).strip()
        workaround_guideline = str(row['Workaround comment']).strip() if pd.notna(row['Workaround comment']) else ""
        status = str(row['Status']).strip() if pd.notna(row['Status']) else ""
        pmr_masking = str(row['PMR Masking']).strip() if pd.notna(row['PMR Masking']) else ""
        
        key = f"{tier1}|{tier2}|{tier3}"
        
        # Get actual examples from past data
        examples = workaround_examples.get(key, [])
        example_count = len(examples)
        
        # Get top 3 unique examples
        unique_examples = list(set(examples))[:3]
        example_1 = unique_examples[0] if len(unique_examples) > 0 else ""
        example_2 = unique_examples[1] if len(unique_examples) > 1 else ""
        example_3 = unique_examples[2] if len(unique_examples) > 2 else ""
        
        mapping_data.append({
            'Issue Type': 'Amdocs Internal Issue',
            'Tier 1 (SLA Resolution Categorization T1)': tier1,
            'Tier 2 (SLA Resolution Category)': tier2,
            'Tier 3 (Resolution Category Tier 3)': tier3,
            'Workaround Guideline': workaround_guideline,
            'Status': status,
            'PMR Masking': pmr_masking,
            'Number of Past Examples': example_count,
            'Example Workaround 1': example_1,
            'Example Workaround 2': example_2,
            'Example Workaround 3': example_3,
            'Description': 'Issues within Amdocs platform/code'
        })
    
    # Process Customer Issue mappings
    print("Processing Customer Issue mappings...")
    for _, row in customer_df.iterrows():
        tier1 = str(row['Tier1']).strip()
        tier2 = str(row['Tier2']).strip()
        tier3 = str(row['Tier3']).strip()
        workaround_guideline = str(row['Workaround comment']).strip() if pd.notna(row['Workaround comment']) else ""
        status = str(row['Status']).strip() if pd.notna(row['Status']) else ""
        pmr_masking = str(row['PMR Masking']).strip() if pd.notna(row['PMR Masking']) else ""
        
        key = f"{tier1}|{tier2}|{tier3}"
        
        # Get actual examples from past data
        examples = workaround_examples.get(key, [])
        example_count = len(examples)
        
        # Get top 3 unique examples
        unique_examples = list(set(examples))[:3]
        example_1 = unique_examples[0] if len(unique_examples) > 0 else ""
        example_2 = unique_examples[1] if len(unique_examples) > 1 else ""
        example_3 = unique_examples[2] if len(unique_examples) > 2 else ""
        
        mapping_data.append({
            'Issue Type': 'Customer/Third-Party Issue',
            'Tier 1 (SLA Resolution Categorization T1)': tier1,
            'Tier 2 (SLA Resolution Category)': tier2,
            'Tier 3 (Resolution Category Tier 3)': tier3,
            'Workaround Guideline': workaround_guideline,
            'Status': status,
            'PMR Masking': pmr_masking,
            'Number of Past Examples': example_count,
            'Example Workaround 1': example_1,
            'Example Workaround 2': example_2,
            'Example Workaround 3': example_3,
            'Description': 'Issues related to customer or third-party systems'
        })
    
    df = pd.DataFrame(mapping_data)
    print(f"Created {len(df)} mapping entries")
    
    return df

def create_statistics_sheet(past_df):
    """Create statistics about the data"""
    print("\nCreating statistics...")
    
    stats_data = []
    
    # Tier 1 distribution
    tier1_counts = past_df['SLA Resolution Categorization T1'].value_counts()
    for idx, (tier1, count) in enumerate(tier1_counts.items()):
        stats_data.append({
            'Category': 'Tier 1 Distribution',
            'Value': tier1,
            'Count': count,
            'Percentage': f"{(count/len(past_df)*100):.2f}%"
        })
    
    # Tier 2 distribution (top 20)
    tier2_counts = past_df['SLA Resolution Category'].value_counts().head(20)
    for tier2, count in tier2_counts.items():
        stats_data.append({
            'Category': 'Tier 2 Distribution (Top 20)',
            'Value': tier2,
            'Count': count,
            'Percentage': f"{(count/len(past_df)*100):.2f}%"
        })
    
    # Tier 3 distribution (top 20)
    tier3_counts = past_df['Resolution Categorization(Resolution Category Tier 3)'].value_counts().head(20)
    for tier3, count in tier3_counts.items():
        stats_data.append({
            'Category': 'Tier 3 Distribution (Top 20)',
            'Value': tier3,
            'Count': count,
            'Percentage': f"{(count/len(past_df)*100):.2f}%"
        })
    
    df = pd.DataFrame(stats_data)
    return df

def create_instructions_sheet():
    """Create instructions for LLM"""
    instructions = [
        {
            'Section': 'PURPOSE',
            'Content': 'This mapping file helps generate appropriate workaround comments based on SR categorization'
        },
        {
            'Section': 'HOW TO USE',
            'Content': '1. Identify the Tier 1 (Issue Type) - Is it Amdocs Internal or Customer/Third-Party?'
        },
        {
            'Section': 'HOW TO USE',
            'Content': '2. Match Tier 2 (SLA Resolution Category) - What category does the issue fall into?'
        },
        {
            'Section': 'HOW TO USE',
            'Content': '3. Match Tier 3 (Resolution Category Tier 3) - What specific resolution type?'
        },
        {
            'Section': 'HOW TO USE',
            'Content': '4. Use Workaround Guideline + Example Workarounds to generate appropriate comment'
        },
        {
            'Section': 'ISSUE TYPES',
            'Content': 'Amdocs Internal Issue - Problems within Amdocs platform, code, or systems'
        },
        {
            'Section': 'ISSUE TYPES',
            'Content': 'Customer/Third-Party Issue - Problems related to customer data, external systems, or third-party integrations'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Tier 1 - Primary categorization of issue source (Amdocs vs Customer)'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Tier 2 - Secondary categorization by problem area (Code Quality, Data, Environment, etc.)'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Tier 3 - Specific resolution type (Code Fix, Manual Intervention, User Error, etc.)'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Workaround Guideline - General guidance on what workaround to apply'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Example Workarounds 1-3 - Real workarounds from past SRs for this category'
        },
        {
            'Section': 'KEY FIELDS',
            'Content': 'Number of Past Examples - How many times this category has occurred in historical data'
        },
        {
            'Section': 'BEST PRACTICES',
            'Content': 'Use the Workaround Guideline as the base template'
        },
        {
            'Section': 'BEST PRACTICES',
            'Content': 'Reference Example Workarounds to understand common patterns and language'
        },
        {
            'Section': 'BEST PRACTICES',
            'Content': 'Adapt the workaround to the specific SR context and details'
        },
        {
            'Section': 'BEST PRACTICES',
            'Content': 'Categories with more past examples are more reliable patterns'
        },
    ]
    
    df = pd.DataFrame(instructions)
    return df

def save_to_excel(mapping_df, stats_df, instructions_df):
    """Save all data to Excel file"""
    output_file = "LLM_Workaround_Mapping.xlsx"
    
    print(f"\nSaving to {output_file}...")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Instructions sheet
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Main mapping sheet
        mapping_df.to_excel(writer, sheet_name='Workaround Mapping', index=False)
        
        # Statistics sheet
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        # Separate sheets for Amdocs and Customer issues
        amdocs_df = mapping_df[mapping_df['Issue Type'] == 'Amdocs Internal Issue']
        customer_df = mapping_df[mapping_df['Issue Type'] == 'Customer/Third-Party Issue']
        
        amdocs_df.to_excel(writer, sheet_name='Amdocs Issues', index=False)
        customer_df.to_excel(writer, sheet_name='Customer Issues', index=False)
    
    print(f"✓ Successfully created {output_file}")
    print(f"\nSheets created:")
    print(f"  1. Instructions - How to use this mapping")
    print(f"  2. Workaround Mapping - Complete mapping with examples")
    print(f"  3. Amdocs Issues - Filtered view of Amdocs-specific issues")
    print(f"  4. Customer Issues - Filtered view of Customer/Third-party issues")
    print(f"  5. Statistics - Data distribution statistics")

def main():
    print("="*80)
    print("LLM WORKAROUND MAPPING GENERATOR")
    print("="*80)
    
    # Step 1: Read past data
    past_df = read_past_data_files()
    
    # Step 2: Read category mappings
    amdocs_df, customer_df = read_category_mappings()
    
    # Step 3: Extract workaround examples from past data
    workaround_examples = extract_workaround_examples(past_df)
    
    # Step 4: Create comprehensive mapping
    mapping_df = create_comprehensive_mapping(amdocs_df, customer_df, workaround_examples)
    
    # Step 5: Create statistics
    stats_df = create_statistics_sheet(past_df)
    
    # Step 6: Create instructions
    instructions_df = create_instructions_sheet()
    
    # Step 7: Save to Excel
    save_to_excel(mapping_df, stats_df, instructions_df)
    
    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)
    print("\nYou can now use 'LLM_Workaround_Mapping.xlsx' to provide context to LLM")
    print("for generating appropriate workaround comments.")

if __name__ == "__main__":
    main()




