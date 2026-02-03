#!/usr/bin/env python3
"""
Script to add "Suggested Workaround" column to Category Summary sheet
Analyzes all workarounds in each category and creates an AI-generated summary
"""
import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_excel_data(file_path='category mapping/Workaround_Comments_Final.xlsx'):
    """Load both sheets from the Excel file"""
    print(f"\n{'='*80}")
    print(f"LOADING DATA FROM {file_path}")
    print(f"{'='*80}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return None, None
    
    try:
        # Load both sheets
        all_workarounds_df = pd.read_excel(file_path, sheet_name='All Workarounds')
        category_summary_df = pd.read_excel(file_path, sheet_name='Category Summary')
        
        print(f"✓ All Workarounds sheet: {len(all_workarounds_df)} rows")
        print(f"✓ Category Summary sheet: {len(category_summary_df)} rows")
        
        print(f"\nColumns in All Workarounds:")
        for col in all_workarounds_df.columns:
            print(f"  - {col}")
        
        print(f"\nColumns in Category Summary:")
        for col in category_summary_df.columns:
            print(f"  - {col}")
        
        return all_workarounds_df, category_summary_df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def summarize_workarounds_for_category(workarounds_list):
    """
    Create a summarized workaround from a list of individual workarounds
    
    This uses a simple rule-based approach to consolidate workarounds:
    1. If there's one dominant workaround (>50% of occurrences), use it
    2. Otherwise, create a consolidated summary of the most common approaches
    """
    if not workarounds_list:
        return "No specific workaround available"
    
    # Filter out empty/invalid workarounds
    valid_workarounds = []
    for w in workarounds_list:
        if w and str(w).strip() and str(w).lower() not in ['nan', 'none', '', 'na']:
            valid_workarounds.append(str(w).strip())
    
    if not valid_workarounds:
        return "No specific workaround available"
    
    # Count occurrences
    from collections import Counter
    workaround_counts = Counter(valid_workarounds)
    
    # Get total count
    total = sum(workaround_counts.values())
    
    # Get most common
    most_common = workaround_counts.most_common(3)
    
    # If one workaround is dominant (>50%), use it
    if most_common[0][1] / total > 0.5:
        return most_common[0][0]
    
    # Otherwise, create a summary combining top approaches
    if len(most_common) == 1:
        return most_common[0][0]
    elif len(most_common) == 2:
        # Check if they're very similar (avoid redundancy)
        wa1 = most_common[0][0].lower()
        wa2 = most_common[1][0].lower()
        if wa1 in wa2 or wa2 in wa1:
            return most_common[0][0]
        return f"{most_common[0][0]}; alternatively: {most_common[1][0]}"
    else:
        # Combine top 3
        suggestions = [w[0] for w in most_common]
        
        # Remove very similar ones
        unique_suggestions = [suggestions[0]]
        for s in suggestions[1:]:
            is_similar = False
            for existing in unique_suggestions:
                if s.lower() in existing.lower() or existing.lower() in s.lower():
                    is_similar = True
                    break
            if not is_similar:
                unique_suggestions.append(s)
        
        if len(unique_suggestions) == 1:
            return unique_suggestions[0]
        elif len(unique_suggestions) == 2:
            return f"{unique_suggestions[0]}; alternatively: {unique_suggestions[1]}"
        else:
            return f"{unique_suggestions[0]}; alternatives: {unique_suggestions[1]} or {unique_suggestions[2]}"


def generate_suggested_workarounds(all_workarounds_df, category_summary_df):
    """
    For each row in category_summary, analyze all workarounds from that category
    and create a suggested workaround
    """
    print(f"\n{'='*80}")
    print(f"GENERATING SUGGESTED WORKAROUNDS")
    print(f"{'='*80}")
    
    suggested_workarounds = []
    
    for idx, summary_row in category_summary_df.iterrows():
        # Get category keys
        t2 = summary_row['Resolution Categorization T2']
        t3 = summary_row['Resolution Category Tier 3']
        sla_t1 = summary_row['SLA Resolution Categorization T1']
        sla_cat = summary_row['SLA Resolution Category']
        
        # Find all workarounds for this category in the All Workarounds sheet
        mask = (
            (all_workarounds_df['Resolution Categorization T2'] == t2) &
            (all_workarounds_df['Resolution Category Tier 3'] == t3) &
            (all_workarounds_df['SLA Resolution Categorization T1'] == sla_t1) &
            (all_workarounds_df['SLA Resolution Category'] == sla_cat)
        )
        
        category_workarounds = all_workarounds_df[mask]
        
        # Get list of actual workarounds (with their occurrence counts)
        workarounds_list = []
        for _, row in category_workarounds.iterrows():
            workaround = row['Actual Workaround Comment']
            occurrences = row.get('Occurrences', 1)
            # Add the workaround multiple times based on occurrences
            workarounds_list.extend([workaround] * int(occurrences))
        
        # Generate suggested workaround
        suggested = summarize_workarounds_for_category(workarounds_list)
        suggested_workarounds.append(suggested)
        
        if (idx + 1) % 20 == 0:
            print(f"  Processed {idx + 1}/{len(category_summary_df)} categories...")
    
    print(f"✓ Generated suggested workarounds for {len(suggested_workarounds)} categories")
    
    # Add the new column
    category_summary_df['Suggested Workaround'] = suggested_workarounds
    
    return category_summary_df


def save_updated_excel(all_workarounds_df, updated_summary_df, output_path='category mapping/Workaround_Comments_Final.xlsx'):
    """Save the updated Excel file with the new column"""
    print(f"\n{'='*80}")
    print(f"SAVING UPDATED EXCEL")
    print(f"{'='*80}")
    
    # Try to save to original location
    try:
        # Create backup of original
        backup_path = output_path.replace('.xlsx', '_backup.xlsx')
        if os.path.exists(output_path):
            import shutil
            shutil.copy2(output_path, backup_path)
            print(f"✓ Backup created: {backup_path}")
        
        # Save updated file
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            all_workarounds_df.to_excel(writer, sheet_name='All Workarounds', index=False)
            updated_summary_df.to_excel(writer, sheet_name='Category Summary', index=False)
        
        print(f"✓ Saved updated file: {output_path}")
        print(f"\nNew column 'Suggested Workaround' added to 'Category Summary' sheet")
        return output_path
    except PermissionError:
        # File is open - save to a new file
        new_output_path = output_path.replace('.xlsx', '_with_suggestions.xlsx')
        print(f"\n⚠️  Original file is open in Excel!")
        print(f"   Saving to new file: {new_output_path}")
        
        with pd.ExcelWriter(new_output_path, engine='openpyxl') as writer:
            all_workarounds_df.to_excel(writer, sheet_name='All Workarounds', index=False)
            updated_summary_df.to_excel(writer, sheet_name='Category Summary', index=False)
        
        print(f"✓ Saved to new file: {new_output_path}")
        print(f"\nNew column 'Suggested Workaround' added to 'Category Summary' sheet")
        print(f"\n📝 To use this file:")
        print(f"   1. Close the original Excel file")
        print(f"   2. Rename or delete the original")
        print(f"   3. Rename this file to remove '_with_suggestions'")
        return new_output_path


def main():
    """Main function"""
    print("\n" + "="*80)
    print(" ADD SUGGESTED WORKAROUND COLUMN TO CATEGORY SUMMARY")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Step 1: Load data
    all_workarounds_df, category_summary_df = load_excel_data('category mapping/Workaround_Comments_Final.xlsx')
    
    if all_workarounds_df is None or category_summary_df is None:
        print("\n✗ Failed to load data. Exiting.")
        return False
    
    # Step 2: Generate suggested workarounds
    updated_summary_df = generate_suggested_workarounds(all_workarounds_df, category_summary_df)
    
    # Step 3: Save updated Excel
    output_file = save_updated_excel(all_workarounds_df, updated_summary_df)
    
    # Show sample results
    print(f"\n{'='*80}")
    print("SAMPLE RESULTS (First 5 categories)")
    print(f"{'='*80}")
    
    for idx, row in updated_summary_df.head(5).iterrows():
        print(f"\n[{idx+1}]")
        print(f"  Category: {row['Resolution Categorization T2']} / {row['Resolution Category Tier 3']}")
        print(f"  Total Workarounds: {row['Total Actual Workarounds']}")
        print(f"  Most Common: {str(row['Most Common Workaround'])[:80]}...")
        print(f"  Suggested: {str(row['Suggested Workaround'])[:80]}...")
    
    print(f"\n{'='*80}")
    print("✅ SUCCESS!")
    print(f"{'='*80}")
    print(f"\nFile updated: {output_file}")
    print(f"New column added: 'Suggested Workaround' in 'Category Summary' sheet")
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

