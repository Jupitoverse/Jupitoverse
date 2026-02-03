"""
Automated Index Scheduler for Continuous Learning
Rebuilds historical SR index daily/weekly to include new Mukul uploads
Runs as background service to enable continuous system learning
"""

import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SCHEDULER] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/index_scheduler.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path('logs').mkdir(exist_ok=True)


class IndexScheduler:
    """Automated scheduler for index rebuilding"""
    
    def __init__(self, rebuild_frequency='daily', rebuild_time='23:00'):
        """
        Initialize scheduler
        
        Args:
            rebuild_frequency: 'daily' or 'weekly' (default: 'daily')
            rebuild_time: Time in HH:MM format (default: '23:00' = 11 PM)
        """
        self.rebuild_frequency = rebuild_frequency.lower()
        self.rebuild_time = rebuild_time
        self.last_rebuild = None
        self.rebuild_count = 0
        self.errors = 0
        
        # Validate frequency
        if self.rebuild_frequency not in ['daily', 'weekly']:
            logger.warning(f"Invalid frequency '{rebuild_frequency}', using 'daily'")
            self.rebuild_frequency = 'daily'
        
        logger.info(f"[OK] Scheduler initialized - Mode: {self.rebuild_frequency.upper()} at {self.rebuild_time}")
    
    def rebuild_index(self):
        """Rebuild the historical SR index with new data"""
        try:
            logger.info("=" * 80)
            logger.info("[REBUILD] STARTING INDEX REBUILD")
            logger.info("=" * 80)
            
            start_time = datetime.now()
            logger.info(f"Start time: {start_time}")
            
            # Import here to avoid circular imports
            from historical_data_indexer import HistoricalDataIndexer
            
            # Initialize indexer
            logger.info("[1/4] Initializing indexer...")
            indexer = HistoricalDataIndexer()
            
            # Load historical data (includes past_data/*.xls + sr_tracking.db)
            logger.info("[2/4] Loading historical data from past_data/ and sr_tracking.db...")
            records_loaded = indexer.load_historical_data()
            logger.info(f"   [OK] Loaded {records_loaded:,} records")
            
            # Build TF-IDF index
            logger.info("[3/4] Building TF-IDF semantic search index...")
            indexer.build_index()
            logger.info(f"   [OK] Index built: {indexer.tfidf_matrix.shape[0]:,} documents × {indexer.tfidf_matrix.shape[1]:,} features")
            
            # Save index
            logger.info("[4/4] Saving index to disk...")
            indexer.save_index("historical_sr_index.pkl")
            logger.info("   [OK] Index saved")
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"[OK] INDEX REBUILD SUCCESSFUL")
            logger.info(f"   Duration: {duration:.1f} seconds")
            logger.info(f"   Total records: {records_loaded:,}")
            logger.info(f"   Timestamp: {end_time}")
            logger.info("=" * 80)
            
            self.last_rebuild = end_time
            self.rebuild_count += 1
            
            return True
            
        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"❌ INDEX REBUILD FAILED: {str(e)}")
            logger.error("=" * 80)
            self.errors += 1
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def schedule_daily(self):
        """Schedule rebuild every day at specified time"""
        schedule.every().day.at(self.rebuild_time).do(self.rebuild_index)
        logger.info(f"[SCHEDULE] Daily rebuild at {self.rebuild_time}")
    
    def schedule_weekly(self):
        """Schedule rebuild every Friday at specified time"""
        schedule.every().friday.at(self.rebuild_time).do(self.rebuild_index)
        logger.info(f"[SCHEDULE] Weekly rebuild every Friday at {self.rebuild_time}")
    
    def start(self):
        """Start the scheduler (blocking)"""
        logger.info("\n" + "=" * 80)
        logger.info("[START] STARTING AUTOMATED INDEX SCHEDULER")
        logger.info("=" * 80)
        logger.info(f"Frequency: {self.rebuild_frequency.upper()}")
        logger.info(f"Rebuild time: {self.rebuild_time}")
        logger.info(f"Press Ctrl+C to stop")
        logger.info("=" * 80 + "\n")
        
        # Schedule based on frequency
        if self.rebuild_frequency == 'daily':
            self.schedule_daily()
        else:
            self.schedule_weekly()
        
        # First rebuild on startup (optional - comment out if not wanted)
        logger.info("💡 Tip: First rebuild runs immediately on startup")
        logger.info("   (Comment out the next line if you want to wait until scheduled time)\n")
        self.rebuild_index()
        
        # Main loop - keeps scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute if a job needs to run
        except KeyboardInterrupt:
            logger.info("\n⏹️  Scheduler stopped by user")
            self._print_summary()
    
    def start_background(self):
        """Start scheduler in background thread (non-blocking)"""
        import threading
        
        logger.info("\n" + "=" * 80)
        logger.info("[START] STARTING BACKGROUND INDEX SCHEDULER")
        logger.info("=" * 80)
        logger.info(f"Frequency: {self.rebuild_frequency.upper()}")
        logger.info(f"Rebuild time: {self.rebuild_time}")
        logger.info("=" * 80 + "\n")
        
        # Schedule based on frequency
        if self.rebuild_frequency == 'daily':
            self.schedule_daily()
        else:
            self.schedule_weekly()
        
        # First rebuild on startup
        self.rebuild_index()
        
        # Start background thread
        def scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        thread = threading.Thread(target=scheduler_loop, daemon=True)
        thread.start()
        logger.info("[OK] Scheduler running in background")
        return thread
    
    def _print_summary(self):
        """Print scheduler summary"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 SCHEDULER SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total rebuilds: {self.rebuild_count}")
        logger.info(f"Last rebuild: {self.last_rebuild}")
        logger.info(f"Errors: {self.errors}")
        logger.info("=" * 80)


def main():
    """Main entry point for running scheduler from command line"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Index Scheduler for SR System')
    parser.add_argument(
        '--frequency',
        choices=['daily', 'weekly'],
        default='daily',
        help='Rebuild frequency (default: daily)'
    )
    parser.add_argument(
        '--time',
        default='23:00',
        help='Rebuild time in HH:MM format (default: 23:00)'
    )
    parser.add_argument(
        '--background',
        action='store_true',
        help='Run in background (non-blocking)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test rebuild once and exit'
    )
    
    args = parser.parse_args()
    
    # Create scheduler
    scheduler = IndexScheduler(
        rebuild_frequency=args.frequency,
        rebuild_time=args.time
    )
    
    # Test mode - single rebuild
    if args.test:
        logger.info("🧪 TEST MODE: Running single rebuild")
        scheduler.rebuild_index()
        return
    
    # Background mode
    if args.background:
        scheduler.start_background()
        logger.info("Scheduler running in background. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n⏹️  Scheduler stopped")
        return
    
    # Foreground mode (blocking)
    scheduler.start()


if __name__ == '__main__':
    main()
