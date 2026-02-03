#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outlook Email Fetcher for Daily SR Report
Fetches the daily Incident report from corporate Outlook (Amdocs)

Uses Windows Outlook COM interface - no authentication needed!
(Uses your already logged-in Outlook desktop app)

Usage:
    python email_fetcher.py                  # Fetch latest report
    python email_fetcher.py --days-back 2    # Search last 2 days
    python email_fetcher.py --list           # List recent emails
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# For Windows Outlook COM interface
try:
    import win32com.client
    import pythoncom
    OUTLOOK_COM_AVAILABLE = True
except ImportError:
    OUTLOOK_COM_AVAILABLE = False
    pythoncom = None
    print("[WARN] pywin32 not available. Install with: pip install pywin32")


def _init_com():
    """Initialize COM library for the current thread (safe to call multiple times)"""
    if pythoncom is not None:
        try:
            pythoncom.CoInitialize()
        except Exception:
            pass  # Already initialized or not needed


# ============================================================
# CONFIGURATION - AUTO-DETECT USER EMAIL
# ============================================================

# Email filter settings - CHANGE THESE if looking for different report
SENDER_EMAIL = "GSSUTSMail@amdocs.com"        # Who sends the email?
SUBJECT_PATTERN = "Scheduled Report - Mukul"  # What's in the subject line?
ATTACHMENT_PATTERN = "mukul"                  # What's the attachment name contain?


def get_current_outlook_email():
    """Auto-detect the logged-in Outlook user's email address"""
    try:
        if not OUTLOOK_COM_AVAILABLE:
            return "Unknown (Outlook not available)"
        
        # Initialize COM for this thread
        _init_com()
        
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        
        # Method 1: Get from default account (most reliable)
        try:
            accounts = namespace.Accounts
            if accounts.Count > 0:
                return accounts.Item(1).SmtpAddress
        except:
            pass
        
        # Method 2: Get from CurrentUser
        try:
            current_user = namespace.CurrentUser
            if current_user:
                # Try to get email address
                address = current_user.Address
                if address and '@' in address:
                    return address
                # Try AddressEntry
                addr_entry = current_user.AddressEntry
                if addr_entry:
                    return addr_entry.GetExchangeUser().PrimarySmtpAddress
        except:
            pass
        
        # Method 3: Get from default folder's store
        try:
            inbox = namespace.GetDefaultFolder(6)  # 6 = Inbox
            store = inbox.Store
            if store:
                return store.DisplayName
        except:
            pass
        
        return "Unknown"
    except Exception as e:
        return f"Unknown ({str(e)[:30]})"


# Auto-detect email on module load
EMAIL_CONFIG = {
    "email": get_current_outlook_email()
}


class OutlookEmailFetcher:
    """Fetches daily SR report from Outlook desktop app (Windows COM)"""
    
    def __init__(self, email: str = None):
        """
        Initialize the fetcher
        
        Args:
            email: Your Outlook email (for display purposes)
        """
        self.email = email or EMAIL_CONFIG.get("email")
        self.outlook = None
        self.namespace = None
        self.inbox = None
        self.connected = False
        
        # Email filter settings
        self.sender_email = SENDER_EMAIL
        self.subject_pattern = SUBJECT_PATTERN
        self.attachment_pattern = ATTACHMENT_PATTERN
        
        # Save location - downloads folder in semantic-resolution
        self.download_folder = Path(__file__).parent / "downloads" / "email_reports"
        self.download_folder.mkdir(parents=True, exist_ok=True)
        
    def connect(self) -> bool:
        """Connect to Outlook desktop application"""
        if not OUTLOOK_COM_AVAILABLE:
            print("[ERROR] pywin32 not installed. Run: pip install pywin32")
            return False
        
        try:
            print("[INFO] Connecting to Outlook desktop app...")
            
            # Initialize COM for this thread (required for Flask/background contexts)
            _init_com()
            
            # Connect to Outlook via COM
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = self.outlook.GetNamespace("MAPI")
            
            # Get inbox (folder index 6 = Inbox)
            self.inbox = self.namespace.GetDefaultFolder(6)
            
            print(f"[SUCCESS] Connected to Outlook: {self.inbox.Name}")
            print(f"[INFO] Mailbox: {self.namespace.CurrentUser.Name}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to connect to Outlook: {str(e)}")
            print("[HINT] Make sure Outlook desktop app is running and you're logged in")
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
        
        print(f"\n[INFO] Searching for report from {self.sender_email}...")
        print(f"[INFO] Subject contains: '{self.subject_pattern}'")
        print(f"[INFO] Looking back {days_back} day(s)...")
        
        try:
            # Calculate date filter
            since_date = datetime.now() - timedelta(days=days_back)
            since_date_str = since_date.strftime("%m/%d/%Y")
            
            # Get all items from inbox
            messages = self.inbox.Items
            messages.Sort("[ReceivedTime]", True)  # Sort by date descending
            
            # Filter by date
            filter_str = f"[ReceivedTime] >= '{since_date_str}'"
            filtered_messages = messages.Restrict(filter_str)
            
            count = filtered_messages.Count
            print(f"[INFO] Found {count} emails in the last {days_back} days")
            
            for i in range(1, count + 1):
                try:
                    msg = filtered_messages.Item(i)
                    
                    # Get sender email
                    try:
                        sender = msg.SenderEmailAddress or ""
                    except:
                        sender = ""
                    
                    # Check sender
                    if self.sender_email.lower() not in sender.lower() and "gssuts" not in sender.lower():
                        continue
                    
                    # Get subject
                    subject = msg.Subject or ""
                    
                    # Check subject
                    if "mukul" not in subject.lower() and "scheduled report" not in subject.lower():
                        continue
                    
                    # Get received time
                    try:
                        received_time = msg.ReceivedTime
                        # Convert to Python datetime
                        email_date = datetime(
                            received_time.year, received_time.month, received_time.day,
                            received_time.hour, received_time.minute, received_time.second
                        )
                    except:
                        email_date = datetime.now()
                    
                    print(f"\n[INFO] Found matching email:")
                    print(f"       Subject: {subject}")
                    print(f"       From: {sender}")
                    print(f"       Date: {email_date}")
                    
                    # Check attachments
                    attachments = msg.Attachments
                    if attachments.Count > 0:
                        for j in range(1, attachments.Count + 1):
                            att = attachments.Item(j)
                            att_name = att.FileName or ""
                            print(f"       Attachment: {att_name}")
                            
                            # Check if it matches our target
                            if self.attachment_pattern in att_name.lower() and att_name.lower().endswith(('.xls', '.xlsx')):
                                # Save the attachment
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                original_ext = Path(att_name).suffix
                                save_name = f"Incident_{timestamp}{original_ext}"
                                save_path = self.download_folder / save_name
                                
                                att.SaveAsFile(str(save_path))
                                
                                print(f"\n[SUCCESS] Downloaded: {save_path}")
                                return str(save_path), email_date
                    
                except Exception as e:
                    # Skip problematic emails
                    continue
            
            print("\n[WARN] No matching report found in recent emails.")
            print(f"       Searched {days_back} day(s) back for emails from {self.sender_email}")
            return None
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch emails: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def fetch_today_report(self) -> Optional[str]:
        """Convenience method to fetch today's/latest report"""
        result = self.fetch_latest_report(days_back=2)
        if result:
            return result[0]  # Return just the file path
        return None
    
    def list_recent_emails(self, days_back: int = 3, limit: int = 50):
        """Debug method: List recent emails to see what's available"""
        if not self.connected:
            if not self.connect():
                return
        
        print(f"\n[DEBUG] Listing last {limit} emails from past {days_back} days:")
        print("-" * 80)
        
        try:
            since_date = datetime.now() - timedelta(days=days_back)
            since_date_str = since_date.strftime("%m/%d/%Y")
            
            messages = self.inbox.Items
            messages.Sort("[ReceivedTime]", True)
            
            filter_str = f"[ReceivedTime] >= '{since_date_str}'"
            filtered_messages = messages.Restrict(filter_str)
            
            count = min(filtered_messages.Count, limit)
            
            for i in range(1, count + 1):
                try:
                    msg = filtered_messages.Item(i)
                    
                    subject = msg.Subject or "(No subject)"
                    sender = msg.SenderEmailAddress or "Unknown"
                    
                    try:
                        received = msg.ReceivedTime
                        date_str = f"{received.year}-{received.month:02d}-{received.day:02d} {received.hour:02d}:{received.minute:02d}"
                    except:
                        date_str = "Unknown"
                    
                    # Get attachments
                    attachments = []
                    try:
                        for j in range(1, msg.Attachments.Count + 1):
                            attachments.append(msg.Attachments.Item(j).FileName)
                    except:
                        pass
                    
                    print(f"\n{i}. {subject}")
                    print(f"   From: {sender}")
                    print(f"   Date: {date_str}")
                    if attachments:
                        print(f"   Attachments: {', '.join(attachments)}")
                        
                except Exception as e:
                    print(f"\n{i}. [Error reading email: {str(e)}]")
                    continue
                    
        except Exception as e:
            print(f"[ERROR] Failed to list emails: {str(e)}")


def fetch_daily_report(days_back: int = 2) -> Optional[str]:
    """
    Main function to fetch the daily report
    
    Args:
        days_back: How many days back to search
        
    Returns:
        Path to downloaded file, or None if failed
    """
    fetcher = OutlookEmailFetcher()
    return fetcher.fetch_today_report()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Outlook Email Fetcher - Daily SR Report")
    parser.add_argument("--days-back", type=int, default=2,
                        help="How many days back to search (default: 2)")
    parser.add_argument("--list", action="store_true",
                        help="List recent emails (debug mode)")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("OUTLOOK EMAIL FETCHER - Daily SR Report")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Outlook Desktop App (Windows COM)")
    print()
    
    fetcher = OutlookEmailFetcher()
    
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
            print("  1. Make sure Outlook desktop app is running")
            print("  2. List emails: python email_fetcher.py --list")
            print("  3. Search more days: python email_fetcher.py --days-back 5")
