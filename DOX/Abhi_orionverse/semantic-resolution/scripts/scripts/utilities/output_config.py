"""
Output Configuration for SR Analyzer System
Centralizes all output paths for generated files
"""
import os
from datetime import datetime
from pathlib import Path

# Base directories - use project root instead of script directory
BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
OUTPUT_DIR = BASE_DIR / "output"
ARCHIVE_DIR = BASE_DIR / "archive"
UPLOADS_DIR = BASE_DIR / "uploads"

# Output subdirectories
DAILY_ASSIGNMENTS_DIR = OUTPUT_DIR / "daily_assignments"
REPORTS_DIR = OUTPUT_DIR / "reports"
EXPORTS_DIR = OUTPUT_DIR / "exports"
OLD_UPLOADS_DIR = ARCHIVE_DIR / "old_uploads"

# Ensure directories exist
def ensure_directories():
    """Create all output directories if they don't exist"""
    directories = [
        OUTPUT_DIR,
        DAILY_ASSIGNMENTS_DIR,
        REPORTS_DIR,
        EXPORTS_DIR,
        ARCHIVE_DIR,
        OLD_UPLOADS_DIR,
        UPLOADS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Output directories initialized")


def get_daily_assignment_path(timestamp: str = None) -> str:
    """
    Get path for daily assignment file
    
    Args:
        timestamp: Optional timestamp string (YYYYMMDD_HHMM). If None, uses current time.
    
    Returns:
        Full path to daily assignment file
    """
    ensure_directories()
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    filename = f"daily_sr_assignments_{timestamp}.xlsx"
    return str(DAILY_ASSIGNMENTS_DIR / filename)


def get_report_path(report_name: str, extension: str = "html") -> str:
    """
    Get path for report file
    
    Args:
        report_name: Name of the report
        extension: File extension (html, json, etc.)
    
    Returns:
        Full path to report file
    """
    ensure_directories()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_name}_{timestamp}.{extension}"
    return str(REPORTS_DIR / filename)


def get_export_path(export_name: str, extension: str = "xlsx") -> str:
    """
    Get path for export file
    
    Args:
        export_name: Name of the export
        extension: File extension (xlsx, json, csv, etc.)
    
    Returns:
        Full path to export file
    """
    ensure_directories()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_name}_{timestamp}.{extension}"
    return str(EXPORTS_DIR / filename)


def get_upload_path(original_filename: str) -> str:
    """
    Get path for uploaded file with timestamp
    
    Args:
        original_filename: Original name of uploaded file
    
    Returns:
        Full path for storing uploaded file
    """
    ensure_directories()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{original_filename}"
    return str(UPLOADS_DIR / filename)


def archive_old_files(days_old: int = 7):
    """
    Archive files older than specified days
    
    Args:
        days_old: Number of days to keep files before archiving
    """
    from datetime import timedelta
    import shutil
    
    ensure_directories()
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    archived_count = 0
    
    # Archive old uploads
    if UPLOADS_DIR.exists():
        for file in UPLOADS_DIR.glob("*"):
            if file.is_file() and file.name != ".gitkeep":
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                if file_time < cutoff_date:
                    dest = OLD_UPLOADS_DIR / file.name
                    shutil.move(str(file), str(dest))
                    archived_count += 1
    
    if archived_count > 0:
        print(f"✓ Archived {archived_count} old files")
    
    return archived_count


def cleanup_root_outputs():
    """
    Move any output files from root directory to proper output folders
    """
    moved_count = 0
    
    # Move daily assignments from root
    for file in BASE_DIR.glob("daily_sr_assignments_*.xlsx"):
        dest = DAILY_ASSIGNMENTS_DIR / file.name
        file.rename(dest)
        moved_count += 1
        print(f"  Moved: {file.name} → output/daily_assignments/")
    
    # Move SR assignment reports
    for file in BASE_DIR.glob("sr_assignment_report_*.xlsx"):
        dest = EXPORTS_DIR / file.name
        file.rename(dest)
        moved_count += 1
        print(f"  Moved: {file.name} → output/exports/")
    
    # Move JSON reports
    for file in BASE_DIR.glob("sr_intelligent_assignments_*.json"):
        dest = EXPORTS_DIR / file.name
        file.rename(dest)
        moved_count += 1
        print(f"  Moved: {file.name} → output/exports/")
    
    if moved_count > 0:
        print(f"✓ Moved {moved_count} files from root to output directories")
    
    return moved_count


# Initialize on import
if __name__ != "__main__":
    ensure_directories()


if __name__ == "__main__":
    # Test and cleanup when run directly
    print("SR Analyzer Output Configuration")
    print("=" * 50)
    
    ensure_directories()
    print("\nDirectory Structure:")
    print(f"  Output:     {OUTPUT_DIR}")
    print(f"  Uploads:    {UPLOADS_DIR}")
    print(f"  Archive:    {ARCHIVE_DIR}")
    
    print("\nCleaning up root directory...")
    cleanup_root_outputs()
    
    print("\nArchiving old files...")
    archive_old_files(days_old=7)
    
    print("\n✓ Cleanup complete!")

