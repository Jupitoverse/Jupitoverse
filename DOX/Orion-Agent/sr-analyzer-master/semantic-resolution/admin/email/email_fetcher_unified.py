#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Email Fetcher - Automatically picks the right implementation

Platform Selection (Graph API is now default):
- All platforms: Uses Microsoft Graph API (O365) - cross-platform
- Fallback on Windows: pywin32 (COM) if Graph API not available

Usage:
    from admin.email.email_fetcher_unified import get_email_fetcher, fetch_daily_report
    
    # Get the appropriate fetcher for this platform
    fetcher = get_email_fetcher()
    file_path = fetcher.fetch_today_report()
    
    # Or use the convenience function
    file_path = fetch_daily_report()
"""

import platform
import sys
from typing import Optional, Tuple
from datetime import datetime


def get_email_fetcher(force_graph_api: bool = True):
    """
    Get the appropriate email fetcher for the current platform
    
    Selection priority (when force_graph_api=True, default):
    1. O365 available: Use GraphEmailFetcher (Graph API) - cross-platform
    2. Windows + pywin32: Fall back to OutlookEmailFetcher (COM)
    3. Neither: Return None
    
    Args:
        force_graph_api: If True (default), always prefer Graph API over pywin32
    
    Returns:
        Email fetcher instance, or None if no fetcher available
    """
    system = platform.system()
    
    # Try Graph API first (cross-platform, preferred)
    try:
        from .email_fetcher_graph import GraphEmailFetcher, O365_AVAILABLE
        if O365_AVAILABLE:
            print(f"[INFO] Platform: {system} - Using Microsoft Graph API")
            print("[INFO] (Cross-platform, token-based authentication)")
            return GraphEmailFetcher()
        else:
            print("[WARN] O365 library not installed")
    except ImportError as e:
        print(f"[WARN] Graph API fetcher not available: {e}")
    
    # Fall back to pywin32 on Windows only if Graph API not available
    if system == "Windows" and not force_graph_api:
        try:
            from .email_fetcher import OutlookEmailFetcher, OUTLOOK_COM_AVAILABLE
            if OUTLOOK_COM_AVAILABLE:
                print("[INFO] Platform: Windows - Using Outlook COM interface (fallback)")
                print("[INFO] (No authentication needed - uses your logged-in Outlook)")
                return OutlookEmailFetcher()
        except ImportError as e:
            print(f"[WARN] Windows COM not available: {e}")
    
    # No fetcher available
    print("[ERROR] No email fetcher available!")
    print("")
    print("To enable email fetching, install:")
    print("")
    print("  pip install O365")
    print("  (Requires Azure AD app registration - see config/email_config.json)")
    print("")
    
    return None


def fetch_daily_report(days_back: int = 2) -> Optional[str]:
    """
    Fetch daily report using the best available method
    
    Args:
        days_back: How many days back to search
        
    Returns:
        Path to downloaded file, or None if failed
    """
    fetcher = get_email_fetcher()
    if fetcher:
        return fetcher.fetch_today_report()
    return None


def fetch_report_with_date(days_back: int = 2) -> Optional[Tuple[str, datetime]]:
    """
    Fetch daily report and return both path and email date
    
    Args:
        days_back: How many days back to search
        
    Returns:
        Tuple of (file_path, email_date), or None if failed
    """
    fetcher = get_email_fetcher()
    if fetcher:
        return fetcher.fetch_latest_report(days_back=days_back)
    return None


def list_recent_emails(days_back: int = 3, limit: int = 20):
    """
    List recent emails for debugging
    
    Args:
        days_back: How many days back to search
        limit: Maximum emails to list
    """
    fetcher = get_email_fetcher()
    if fetcher:
        fetcher.list_recent_emails(days_back=days_back, limit=limit)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Unified Email Fetcher - Auto-selects best method"
    )
    parser.add_argument(
        "--days-back", type=int, default=2,
        help="How many days back to search (default: 2)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List recent emails (debug mode)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("UNIFIED EMAIL FETCHER")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS: {platform.system()} {platform.release()}")
    print()
    
    if args.list:
        list_recent_emails(days_back=args.days_back)
    else:
        result = fetch_report_with_date(days_back=args.days_back)
        
        if result:
            file_path, email_date = result
            print("\n" + "=" * 70)
            print("SUCCESS!")
            print("=" * 70)
            print(f"File: {file_path}")
            print(f"Email Date: {email_date}")
        else:
            print("\n" + "=" * 70)
            print("FAILED TO FETCH REPORT")
            print("=" * 70)
            print("\nTry: python -m admin.email.email_fetcher_unified --list")
