#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Platform Email Fetcher using Microsoft Graph API
Works on Windows, Linux, and Mac

Uses O365 library to connect to Microsoft 365/Outlook via Graph API.
Authentication token is saved locally and automatically refreshed.

Usage:
    python email_fetcher_graph.py                  # Fetch latest report
    python email_fetcher_graph.py --days-back 2    # Search last 2 days
    python email_fetcher_graph.py --list           # List recent emails
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, List, Dict

try:
    from O365 import Account, FileSystemTokenBackend
    O365_AVAILABLE = True
except ImportError:
    O365_AVAILABLE = False
    Account = None
    FileSystemTokenBackend = None


class GraphEmailFetcher:
    """
    Fetch emails from Outlook using Microsoft Graph API (cross-platform)
    
    This class uses the O365 library to connect to Microsoft 365 mailboxes.
    It works on any operating system (Windows, Linux, Mac).
    
    Authentication:
    - First run requires browser authentication (OAuth2)
    - Token is saved to o365_token.txt and automatically refreshed
    - Subsequent runs don't require authentication
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize with config file or environment variables
        
        Args:
            config_path: Path to email_config.json (optional)
        """
        self.config = self._load_config(config_path)
        self.account = None
        self.connected = False
        
        # Email filter settings from config
        self.sender_filter = self.config.get("sender_filter", "")
        self.subject_pattern = self.config.get("subject_pattern", "")
        self.attachment_pattern = self.config.get("attachment_pattern", "")
        
        # Download folder - same location as Windows version
        self.download_folder = Path(__file__).parent / "downloads" / "email_reports"
        self.download_folder.mkdir(parents=True, exist_ok=True)
        
        # Token storage folder
        self.token_folder = Path(__file__).parent / "downloads"
        self.token_folder.mkdir(parents=True, exist_ok=True)
        
    def _load_config(self, config_path: str = None) -> dict:
        """
        Load configuration from file or environment variables
        
        Priority:
        1. Provided config_path
        2. Default config file location
        3. Environment variables
        """
        # Try config file first
        if config_path is None:
            # Look in config folder
            config_path = Path(__file__).parent.parent.parent / "config" / "email_config.json"
        
        config_path = Path(config_path)
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    print(f"[INFO] Loaded config from: {config_path}")
                    return config
            except Exception as e:
                print(f"[WARN] Failed to load config file: {e}")
        
        # Fall back to environment variables
        print("[INFO] Using environment variables for configuration")
        return {
            "client_id": os.environ.get("O365_CLIENT_ID"),
            "client_secret": os.environ.get("O365_CLIENT_SECRET"),
            "tenant_id": os.environ.get("O365_TENANT_ID"),
            "sender_filter": os.environ.get("EMAIL_SENDER_FILTER", "GSSUTSMail@amdocs.com"),
            "subject_pattern": os.environ.get("EMAIL_SUBJECT_PATTERN", "Scheduled Report"),
            "attachment_pattern": os.environ.get("EMAIL_ATTACHMENT_PATTERN", "")
        }
    
    def connect(self) -> bool:
        """
        Authenticate with Microsoft Graph API
        
        First time: Opens browser for OAuth2 authentication
        Subsequent: Uses saved token (auto-refreshed)
        
        Returns:
            True if connected successfully, False otherwise
        """
        if not O365_AVAILABLE:
            print("[ERROR] O365 library not installed!")
            print("        Install with: pip install O365")
            return False
        
        client_id = self.config.get("client_id")
        client_secret = self.config.get("client_secret")
        tenant_id = self.config.get("tenant_id")
        
        if not client_id or not client_secret:
            print("[ERROR] Missing Azure AD credentials!")
            print("        Create config/email_config.json with:")
            print('        {"client_id": "...", "client_secret": "...", "tenant_id": "..."}')
            return False
        
        try:
            print("[INFO] Connecting to Microsoft Graph API...")
            
            credentials = (client_id, client_secret)
            
            # Token storage for persistence (saves to o365_token.txt)
            token_backend = FileSystemTokenBackend(
                token_path=str(self.token_folder),
                token_filename='o365_token.txt'
            )
            
            self.account = Account(
                credentials=credentials,
                tenant_id=tenant_id,
                token_backend=token_backend
            )
            
            # Check if already authenticated
            if self.account.is_authenticated:
                print("[INFO] Using saved authentication token")
                self.connected = True
                return True
            
            # Need to authenticate (first time only)
            print("\n" + "=" * 60)
            print("FIRST-TIME AUTHENTICATION REQUIRED")
            print("=" * 60)
            print("A browser window will open for Microsoft login.")
            print("After login, copy the URL you're redirected to and paste it here.")
            print("=" * 60 + "\n")
            
            # Request delegated permissions
            result = self.account.authenticate(scopes=['basic', 'message_all'])
            
            if result:
                self.connected = True
                print("\n[SUCCESS] Authentication successful!")
                print("[INFO] Token saved - no need to authenticate again")
                return True
            else:
                print("[ERROR] Authentication failed")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def fetch_latest_report(self, days_back: int = 2) -> Optional[Tuple[str, datetime]]:
        """
        Fetch the latest daily report from email
        
        Args:
            days_back: How many days back to search (default: 2)
            
        Returns:
            Tuple of (file_path, email_date) if found, None otherwise
        """
        if not self.connected:
            if not self.connect():
                return None
        
        print(f"\n[INFO] Searching for report...")
        if self.sender_filter:
            print(f"[INFO] From: {self.sender_filter}")
        if self.subject_pattern:
            print(f"[INFO] Subject contains: '{self.subject_pattern}'")
        print(f"[INFO] Looking back {days_back} day(s)...")
        
        try:
            mailbox = self.account.mailbox()
            inbox = mailbox.inbox_folder()
            
            # Calculate date filter
            since_date = datetime.now() - timedelta(days=days_back)
            
            # Build query - search for matching emails
            query = inbox.new_query()
            
            # Add sender filter if specified
            if self.sender_filter:
                query = query.on_attribute('from').contains(self.sender_filter)
            
            # Add subject filter if specified
            if self.subject_pattern:
                if self.sender_filter:
                    query = query.chain('and').on_attribute('subject').contains(self.subject_pattern)
                else:
                    query = query.on_attribute('subject').contains(self.subject_pattern)
            
            # Get messages (sorted by received date, newest first)
            messages = inbox.get_messages(query=query, limit=30)
            
            found_count = 0
            for message in messages:
                found_count += 1
                
                # Get received time
                try:
                    received = message.received
                    if received:
                        email_date = received.replace(tzinfo=None)
                    else:
                        email_date = datetime.now()
                except:
                    email_date = datetime.now()
                
                # Check if within date range
                if email_date < since_date:
                    continue
                
                print(f"\n[INFO] Found matching email:")
                print(f"       Subject: {message.subject}")
                print(f"       From: {message.sender}")
                print(f"       Date: {email_date}")
                
                # Check for attachments
                if message.has_attachments:
                    # Download attachments to memory
                    message.attachments.download_attachments()
                    
                    for attachment in message.attachments:
                        att_name = attachment.name or ""
                        print(f"       Attachment: {att_name}")
                        
                        # Check if it matches our target (Excel file with pattern)
                        is_excel = att_name.lower().endswith(('.xls', '.xlsx'))
                        matches_pattern = (
                            not self.attachment_pattern or 
                            self.attachment_pattern.lower() in att_name.lower()
                        )
                        
                        if is_excel and matches_pattern:
                            # Save attachment
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            original_ext = Path(att_name).suffix
                            save_name = f"Incident_{timestamp}{original_ext}"
                            save_path = self.download_folder / save_name
                            
                            # Save the attachment
                            attachment.save(location=str(self.download_folder), custom_name=save_name)
                            
                            print(f"\n[SUCCESS] Downloaded: {save_path}")
                            return str(save_path), email_date
            
            print(f"\n[WARN] No matching report found ({found_count} emails checked)")
            print(f"       Searched {days_back} day(s) back")
            if self.sender_filter:
                print(f"       Sender filter: {self.sender_filter}")
            if self.subject_pattern:
                print(f"       Subject pattern: {self.subject_pattern}")
            return None
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch emails: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def fetch_today_report(self) -> Optional[str]:
        """
        Convenience method to fetch today's/latest report
        
        Returns:
            Path to downloaded file, or None if not found
        """
        result = self.fetch_latest_report(days_back=2)
        if result:
            return result[0]  # Return just the file path
        return None
    
    def list_recent_emails(self, days_back: int = 3, limit: int = 20) -> List[Dict]:
        """
        Debug method: List recent emails to see what's available
        
        Args:
            days_back: How many days back to search
            limit: Maximum number of emails to list
            
        Returns:
            List of email dictionaries
        """
        if not self.connected:
            if not self.connect():
                return []
        
        print(f"\n[DEBUG] Listing last {limit} emails from past {days_back} days:")
        print("-" * 80)
        
        emails = []
        
        try:
            mailbox = self.account.mailbox()
            inbox = mailbox.inbox_folder()
            
            messages = inbox.get_messages(limit=limit)
            
            for i, message in enumerate(messages, 1):
                try:
                    subject = message.subject or "(No subject)"
                    sender = str(message.sender) if message.sender else "Unknown"
                    received = message.received
                    has_attachments = message.has_attachments
                    
                    email_info = {
                        "index": i,
                        "subject": subject,
                        "sender": sender,
                        "received": received,
                        "has_attachments": has_attachments
                    }
                    emails.append(email_info)
                    
                    print(f"\n{i}. {subject}")
                    print(f"   From: {sender}")
                    print(f"   Date: {received}")
                    if has_attachments:
                        print(f"   Has Attachments: Yes")
                        
                except Exception as e:
                    print(f"\n{i}. [Error reading email: {e}]")
                    continue
            
            return emails
                    
        except Exception as e:
            print(f"[ERROR] Failed to list emails: {e}")
            return []


def fetch_daily_report(days_back: int = 2) -> Optional[str]:
    """
    Main function to fetch the daily report using Graph API
    
    Args:
        days_back: How many days back to search
        
    Returns:
        Path to downloaded file, or None if failed
    """
    fetcher = GraphEmailFetcher()
    return fetcher.fetch_today_report()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Graph API Email Fetcher - Cross-Platform Outlook Access"
    )
    parser.add_argument(
        "--days-back", type=int, default=2,
        help="How many days back to search (default: 2)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List recent emails (debug mode)"
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="Path to config file (default: config/email_config.json)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("GRAPH API EMAIL FETCHER - Cross-Platform")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Microsoft Graph API")
    print()
    
    fetcher = GraphEmailFetcher(config_path=args.config)
    
    if args.list:
        # Debug: list recent emails
        fetcher.list_recent_emails(days_back=args.days_back)
    else:
        # Fetch the report
        result = fetcher.fetch_latest_report(days_back=args.days_back)
        
        if result:
            file_path, email_date = result
            print("\n" + "=" * 70)
            print("SUCCESS!")
            print("=" * 70)
            print(f"File: {file_path}")
            print(f"Email Date: {email_date}")
            print("\nYou can now run RAG analysis on this file.")
        else:
            print("\n" + "=" * 70)
            print("FAILED TO FETCH REPORT")
            print("=" * 70)
            print("\nTry the following:")
            print("  1. Check config/email_config.json credentials")
            print("  2. List emails: python email_fetcher_graph.py --list")
            print("  3. Search more days: python email_fetcher_graph.py --days-back 5")
