"""
Process User File with Historical Predictions
Usage: python process_user_file.py [filename]

This script processes user input files (like Mukul.xlsx) and predicts:
- Where tickets will end up (interface issue, Amdocs WA, etc.)
- Classification (Easy Win, Moderate, Tough)
- Expected resolution path and time
- Similar historical cases
"""

import sys
import os
from scripts.ml_models.enhanced_historical_predictor import EnhancedHistoricalPredictor
import pandas as pd


def main():
    # Get filename from command line or use default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Look for Mukul.xlsx or any Excel file
        excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls')) and 'mukul' in f.lower()]
        if not excel_files:
            excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            print("Error: No Excel files found in current directory")
            print("Usage: python process_user_file.py <filename>")
            return
        
        input_file = excel_files[0]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        return
    
    print("=" * 80)
    print("HISTORICAL SR PREDICTION SYSTEM")
    print("=" * 80)
    print(f"Input file: {input_file}")
    print("Using: 15,311 historical SRs for semantic search")
    print("=" * 80)
    
    # Initialize predictor
    predictor = EnhancedHistoricalPredictor()
    
    # Process the file
    result = predictor.process_user_file(input_file)
    
    if result['success']:
        print("\n" + "=" * 80)
        print("PROCESSING COMPLETE")
        print("=" * 80)
        print(f"Total SRs analyzed: {result['total_processed']}")
        print(f"Output file: {result['output_file']}")
        
        # Show summary
        summary = result['summary']
        print("\nSUMMARY:")
        print("-" * 40)
        
        if 'classifications' in summary:
            print("\nClassifications:")
            for clf, count in summary['classifications'].items():
                print(f"  - {clf}: {count} SRs")
        
        print(f"\nInterface Issues: {summary.get('interface_issues', 0)} SRs")
        print(f"Workarounds Likely: {summary.get('workarounds_likely', 0)} SRs")
        print(f"Average Confidence: {summary.get('average_confidence', 0):.0%}")
        
        # Show sample predictions
        if result['predictions']:
            print("\n" + "=" * 80)
            print("SAMPLE PREDICTIONS (First 3)")
            print("=" * 80)
            
            for i, pred in enumerate(result['predictions'][:3], 1):
                print(f"\n{i}. SR ID: {pred['sr_id']}")
                print(f"   Description: {pred['description']}")
                print(f"   Priority: {pred['priority']}")
                
                p = pred['prediction']
                print(f"\n   PREDICTION:")
                print(f"   - Classification: {p['classification']} (Confidence: {p['confidence']:.0%})")
                print(f"   - Complexity: {p['complexity']}")
                print(f"   - Resolution Type: {p['resolution_type']}")
                print(f"   - Interface Issue: {'Yes' if p['interface_likelihood'] > 0.5 else 'No'}")
                print(f"   - Workaround Available: {'Likely' if p['workaround_likelihood'] > 0.5 else 'Unlikely'}")
                print(f"   - Expected Path: {p['expected_path']}")
                print(f"   - Estimated Hours: {p['estimated_hours']}")
                
                if p['recommendations']:
                    print(f"\n   RECOMMENDATIONS:")
                    for rec in p['recommendations']:
                        print(f"   • {rec}")
                
                if p['similar_cases']:
                    print(f"\n   SIMILAR HISTORICAL CASES:")
                    for case in p['similar_cases'][:2]:
                        print(f"   • {case['sr_id']} - {case['description'][:60]}...")
                        print(f"     Similarity: {case['similarity']:.0%}, Outcome: {case['outcome']['classification']}")
        
        print("\n" + "=" * 80)
        print(f"Full report saved to: {result['output_file']}")
        print("Open the Excel file for detailed predictions and similar cases")
        print("=" * 80)
        
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
