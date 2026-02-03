#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email to RAG Processor
Fetches daily report from Outlook and processes through RAG pipeline

Usage:
    python email_to_rag_processor.py                   # Full pipeline: Fetch + RAG
    python email_to_rag_processor.py --fetch-only      # Only fetch, don't run RAG
    python email_to_rag_processor.py --days-back 3     # Search last 3 days
    python email_to_rag_processor.py -i                # Interactive menu
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))  # semantic-resolution folder

from email_processing.email_fetcher import OutlookEmailFetcher
from admin.admin_upload_and_merge_with_rag import upload_and_merge_with_rag


class EmailToRAGProcessor:
    """Complete pipeline: Email -> Download -> RAG Analysis"""
    
    def __init__(self):
        """Initialize the processor"""
        self.fetcher = OutlookEmailFetcher()
        self.last_fetched_file = None
        self.last_fetch_time = None
        
    def fetch_from_email(self, days_back: int = 2) -> bool:
        """
        Step 1: Fetch the Excel from email
        
        Args:
            days_back: How many days back to search
            
        Returns:
            True if file fetched successfully
        """
        print("\n" + "=" * 70)
        print("STEP 1: FETCHING REPORT FROM OUTLOOK")
        print("=" * 70)
        
        result = self.fetcher.fetch_latest_report(days_back=days_back)
        
        if result:
            self.last_fetched_file, self.last_fetch_time = result
            return True
        return False
    
    def run_rag_analysis(self, progress_callback=None) -> bool:
        """
        Step 2: Run RAG analysis on fetched file
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if analysis completed successfully
        """
        if not self.last_fetched_file:
            print("[ERROR] No file fetched. Run fetch_from_email() first.")
            return False
        
        print("\n" + "=" * 70)
        print("STEP 2: RUNNING RAG ANALYSIS")
        print("=" * 70)
        print(f"File: {self.last_fetched_file}")
        
        return upload_and_merge_with_rag(
            self.last_fetched_file,
            progress_callback=progress_callback
        )
    
    def process_complete(self, days_back: int = 2, progress_callback=None) -> dict:
        """
        Complete pipeline: Fetch + Analyze
        
        Args:
            days_back: How many days back to search for email
            progress_callback: Optional callback for progress updates
            
        Returns:
            dict with status and details
        """
        result = {
            "success": False,
            "file_path": None,
            "email_date": None,
            "rag_completed": False,
            "error": None
        }
        
        try:
            # Step 1: Fetch from email
            if not self.fetch_from_email(days_back):
                result["error"] = "Failed to fetch report from email"
                return result
            
            result["file_path"] = self.last_fetched_file
            result["email_date"] = str(self.last_fetch_time)
            
            # Step 2: Run RAG analysis
            if self.run_rag_analysis(progress_callback):
                result["rag_completed"] = True
                result["success"] = True
            else:
                result["error"] = "RAG analysis failed"
                
        except Exception as e:
            result["error"] = str(e)
            import traceback
            traceback.print_exc()
        
        return result


# ============================================================
# Functions for Admin Portal Integration
# ============================================================

def get_fetched_file_for_user(days_back: int = 2) -> str:
    """
    For admin portal: Fetch file from email and return path
    User can then decide to run RAG on it
    
    Args:
        days_back: How many days back to search
        
    Returns:
        Path to downloaded file, or None if failed
    """
    processor = EmailToRAGProcessor()
    
    if processor.fetch_from_email(days_back):
        return processor.last_fetched_file
    return None


def run_rag_on_fetched_file(file_path: str, progress_callback=None) -> bool:
    """
    For admin portal: Run RAG analysis on a fetched file
    
    Args:
        file_path: Path to the Excel file to process
        progress_callback: Optional callback for progress updates
        
    Returns:
        True if successful
    """
    return upload_and_merge_with_rag(file_path, progress_callback)


def fetch_and_process_complete(days_back: int = 2, progress_callback=None) -> dict:
    """
    For admin portal: Complete pipeline in one call
    
    Args:
        days_back: How many days back to search
        progress_callback: Optional callback for progress updates
        
    Returns:
        dict with status and details
    """
    processor = EmailToRAGProcessor()
    return processor.process_complete(days_back, progress_callback)


# ============================================================
# Interactive Menu
# ============================================================

def interactive_menu():
    """Interactive menu for user to choose what to do"""
    print("\n" + "=" * 70)
    print("EMAIL TO RAG PROCESSOR - INTERACTIVE MODE")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Outlook Desktop App")
    print()
    
    while True:
        print("\nOptions:")
        print("  1. Fetch latest report from Outlook")
        print("  2. Fetch and run RAG analysis (full pipeline)")
        print("  3. List recent emails (debug)")
        print("  4. Exit")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            days = input("How many days back to search? [2]: ").strip()
            days = int(days) if days else 2
            
            processor = EmailToRAGProcessor()
            if processor.fetch_from_email(days):
                print(f"\n[SUCCESS] File ready: {processor.last_fetched_file}")
                
                run_rag = input("\nRun RAG analysis now? (y/n) [n]: ").strip().lower()
                if run_rag == 'y':
                    processor.run_rag_analysis()
            else:
                print("\n[FAILED] Could not fetch report")
                
        elif choice == "2":
            days = input("How many days back to search? [2]: ").strip()
            days = int(days) if days else 2
            
            processor = EmailToRAGProcessor()
            result = processor.process_complete(days)
            
            if result["success"]:
                print("\n" + "=" * 70)
                print("COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
                print("=" * 70)
                print(f"File: {result['file_path']}")
                print(f"Email Date: {result['email_date']}")
            else:
                print(f"\n[FAILED] {result['error']}")
                
        elif choice == "3":
            days = input("How many days back to search? [3]: ").strip()
            days = int(days) if days else 3
            
            fetcher = OutlookEmailFetcher()
            fetcher.list_recent_emails(days_back=days)
            
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1-4.")


# ============================================================
# CLI Interface
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Email to RAG Processor")
    parser.add_argument("--fetch-only", action="store_true", 
                        help="Only fetch the file, don't run RAG")
    parser.add_argument("--days-back", type=int, default=2,
                        help="How many days back to search for email (default: 2)")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Run in interactive menu mode")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_menu()
        sys.exit(0)
    
    print("=" * 70)
    print("EMAIL TO RAG PROCESSOR")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Fetch Only' if args.fetch_only else 'Full Pipeline (Fetch + RAG)'}")
    print(f"Days Back: {args.days_back}")
    print()
    
    processor = EmailToRAGProcessor()
    
    if args.fetch_only:
        # Just fetch the file
        if processor.fetch_from_email(args.days_back):
            print("\n" + "=" * 70)
            print("FETCH COMPLETE!")
            print("=" * 70)
            print(f"File: {processor.last_fetched_file}")
            print("\nTo run RAG analysis:")
            print(f"  python email_to_rag_processor.py")
        else:
            print("\n[FAILED] Failed to fetch report")
            sys.exit(1)
    else:
        # Full pipeline
        result = processor.process_complete(args.days_back)
        
        if result["success"]:
            print("\n" + "=" * 70)
            print("COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
            print("=" * 70)
            print(f"File: {result['file_path']}")
            print(f"Email Date: {result['email_date']}")
        else:
            print("\n" + "=" * 70)
            print("PIPELINE FAILED")
            print("=" * 70)
            print(f"Error: {result['error']}")
            sys.exit(1)
