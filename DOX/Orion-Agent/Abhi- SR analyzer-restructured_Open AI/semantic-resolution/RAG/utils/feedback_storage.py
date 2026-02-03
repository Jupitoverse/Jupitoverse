"""
Workaround Feedback Storage System
Stores and retrieves upvote/downvote feedback for workarounds using SQLite
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class WorkaroundFeedbackStorage:
    """Store and retrieve upvote/downvote feedback for workarounds"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default path: data/database/workaround_feedback.db
            base_dir = Path(__file__).parent.parent.parent  # semantic-resolution folder
            db_path = base_dir / "data" / "database" / "workaround_feedback.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Create feedback table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main feedback table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workaround_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sr_id TEXT NOT NULL,
            workaround_type TEXT NOT NULL,
            workaround_text TEXT NOT NULL,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0,
            score INTEGER GENERATED ALWAYS AS (upvotes - downvotes) STORED,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(sr_id, workaround_type)
        )
        """)
        
        # Create indices for fast lookups
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sr_workaround 
        ON workaround_feedback(sr_id, workaround_type)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_vote_score 
        ON workaround_feedback(score DESC, upvotes DESC)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sr_id 
        ON workaround_feedback(sr_id)
        """)
        
        # Vote history table (optional - for tracking individual votes over time)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vote_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sr_id TEXT NOT NULL,
            workaround_type TEXT NOT NULL,
            vote_type TEXT NOT NULL,
            user_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sr_id, workaround_type) 
                REFERENCES workaround_feedback(sr_id, workaround_type)
        )
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_vote_history_sr 
        ON vote_history(sr_id, workaround_type)
        """)
        
        conn.commit()
        conn.close()
        
        print(f"[OK] Feedback database initialized: {self.db_path}")
    
    def upvote(self, sr_id: str, workaround_type: str, workaround_text: str = "", user_id: str = None):
        """
        Add an upvote to a workaround
        
        Args:
            sr_id: Service request ID
            workaround_type: Type of workaround ('original', 'ai', 'user_corrected')
            workaround_text: Text of the workaround (first 500 chars stored for reference)
            user_id: Optional user identifier for tracking
        """
        # Normalize SR ID to uppercase for consistent storage
        sr_id = sr_id.upper().strip()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Upsert (insert or update)
            cursor.execute("""
            INSERT INTO workaround_feedback (sr_id, workaround_type, workaround_text, upvotes)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(sr_id, workaround_type) 
            DO UPDATE SET 
                upvotes = upvotes + 1,
                last_updated = CURRENT_TIMESTAMP
            """, (sr_id, workaround_type, workaround_text[:500]))
            
            # Log to vote history
            cursor.execute("""
            INSERT INTO vote_history (sr_id, workaround_type, vote_type, user_id)
            VALUES (?, ?, 'upvote', ?)
            """, (sr_id, workaround_type, user_id))
            
            conn.commit()
            print(f"[FEEDBACK] Upvote recorded: SR={sr_id}, Type={workaround_type}")
            
        except Exception as e:
            print(f"[ERROR] Failed to record upvote: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def downvote(self, sr_id: str, workaround_type: str, workaround_text: str = "", user_id: str = None):
        """
        Add a downvote to a workaround
        
        Args:
            sr_id: Service request ID
            workaround_type: Type of workaround ('original', 'ai', 'user_corrected')
            workaround_text: Text of the workaround (first 500 chars stored for reference)
            user_id: Optional user identifier for tracking
        """
        # Normalize SR ID to uppercase for consistent storage
        sr_id = sr_id.upper().strip()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO workaround_feedback (sr_id, workaround_type, workaround_text, downvotes)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(sr_id, workaround_type) 
            DO UPDATE SET 
                downvotes = downvotes + 1,
                last_updated = CURRENT_TIMESTAMP
            """, (sr_id, workaround_type, workaround_text[:500]))
            
            # Log to vote history
            cursor.execute("""
            INSERT INTO vote_history (sr_id, workaround_type, vote_type, user_id)
            VALUES (?, ?, 'downvote', ?)
            """, (sr_id, workaround_type, user_id))
            
            conn.commit()
            print(f"[FEEDBACK] Downvote recorded: SR={sr_id}, Type={workaround_type}")
            
        except Exception as e:
            print(f"[ERROR] Failed to record downvote: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_votes(self, sr_id: str, workaround_type: str) -> Dict[str, int]:
        """
        Get vote counts for a specific workaround
        
        Returns:
            Dictionary with 'upvotes', 'downvotes', and 'score' (upvotes - downvotes)
        """
        # Normalize SR ID to uppercase for consistent lookup
        sr_id = sr_id.upper().strip()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT upvotes, downvotes, score FROM workaround_feedback
        WHERE sr_id = ? AND workaround_type = ?
        """, (sr_id, workaround_type))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'upvotes': row[0],
                'downvotes': row[1],
                'score': row[2]
            }
        return {'upvotes': 0, 'downvotes': 0, 'score': 0}
    
    def get_all_votes_for_sr(self, sr_id: str) -> Dict[str, Dict[str, int]]:
        """
        Get votes for all workaround types of a specific SR
        
        Returns:
            Dictionary mapping workaround_type to vote counts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT workaround_type, upvotes, downvotes, score 
        FROM workaround_feedback
        WHERE LOWER(sr_id) = LOWER(?)
        """, (sr_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        result = {}
        for row in rows:
            result[row[0]] = {
                'upvotes': row[1],
                'downvotes': row[2],
                'score': row[3]
            }
        
        return result
    
    def get_vote_score(self, sr_id: str, workaround_type: str) -> int:
        """
        Calculate priority score (upvotes - downvotes)
        
        Returns:
            Integer score (can be negative)
        """
        votes = self.get_votes(sr_id, workaround_type)
        return votes['score']
    
    def get_top_workarounds(self, limit: int = 10, min_votes: int = 1) -> List[Dict]:
        """
        Get highest-voted workarounds across all SRs
        
        Args:
            limit: Maximum number of results
            min_votes: Minimum number of upvotes to include
        
        Returns:
            List of workaround dictionaries sorted by score
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT sr_id, workaround_type, workaround_text, upvotes, downvotes, score
        FROM workaround_feedback
        WHERE upvotes >= ?
        ORDER BY score DESC, upvotes DESC, last_updated DESC
        LIMIT ?
        """, (min_votes, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'sr_id': row[0],
                'workaround_type': row[1],
                'workaround_text': row[2],
                'upvotes': row[3],
                'downvotes': row[4],
                'score': row[5]
            }
            for row in rows
        ]
    
    def get_bottom_workarounds(self, limit: int = 10) -> List[Dict]:
        """
        Get lowest-voted workarounds (for identifying problems)
        
        Returns:
            List of workaround dictionaries sorted by score (ascending)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT sr_id, workaround_type, workaround_text, upvotes, downvotes, score
        FROM workaround_feedback
        WHERE downvotes > 0
        ORDER BY score ASC, downvotes DESC, last_updated DESC
        LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'sr_id': row[0],
                'workaround_type': row[1],
                'workaround_text': row[2],
                'upvotes': row[3],
                'downvotes': row[4],
                'score': row[5]
            }
            for row in rows
        ]
    
    def get_statistics(self) -> Dict:
        """
        Get overall statistics about feedback
        
        Returns:
            Dictionary with various statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total workarounds with feedback
        cursor.execute("SELECT COUNT(*) FROM workaround_feedback WHERE upvotes > 0 OR downvotes > 0")
        total_with_feedback = cursor.fetchone()[0]
        
        # Total votes
        cursor.execute("SELECT SUM(upvotes), SUM(downvotes) FROM workaround_feedback")
        total_votes = cursor.fetchone()
        
        # Average score
        cursor.execute("SELECT AVG(score) FROM workaround_feedback WHERE upvotes > 0 OR downvotes > 0")
        avg_score = cursor.fetchone()[0] or 0
        
        # Best workaround
        cursor.execute("""
        SELECT sr_id, workaround_type, score 
        FROM workaround_feedback 
        ORDER BY score DESC, upvotes DESC 
        LIMIT 1
        """)
        best = cursor.fetchone()
        
        # Worst workaround
        cursor.execute("""
        SELECT sr_id, workaround_type, score 
        FROM workaround_feedback 
        ORDER BY score ASC, downvotes DESC 
        LIMIT 1
        """)
        worst = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_workarounds_with_feedback': total_with_feedback,
            'total_upvotes': total_votes[0] or 0,
            'total_downvotes': total_votes[1] or 0,
            'average_score': round(avg_score, 2),
            'best_workaround': {
                'sr_id': best[0] if best else None,
                'type': best[1] if best else None,
                'score': best[2] if best else None
            },
            'worst_workaround': {
                'sr_id': worst[0] if worst else None,
                'type': worst[1] if worst else None,
                'score': worst[2] if worst else None
            }
        }
    
    def export_to_csv(self, output_path: str):
        """Export all feedback data to CSV"""
        import pandas as pd
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("""
        SELECT sr_id, workaround_type, upvotes, downvotes, score, 
               created_at, last_updated
        FROM workaround_feedback
        ORDER BY score DESC
        """, conn)
        conn.close()
        
        df.to_csv(output_path, index=False)
        print(f"[OK] Feedback data exported to: {output_path}")


# Utility functions for easy access
def record_upvote(sr_id: str, workaround_type: str, workaround_text: str = ""):
    """Quick utility to record an upvote"""
    storage = WorkaroundFeedbackStorage()
    storage.upvote(sr_id, workaround_type, workaround_text)


def record_downvote(sr_id: str, workaround_type: str, workaround_text: str = ""):
    """Quick utility to record a downvote"""
    storage = WorkaroundFeedbackStorage()
    storage.downvote(sr_id, workaround_type, workaround_text)


def get_feedback(sr_id: str, workaround_type: str) -> Dict[str, int]:
    """Quick utility to get feedback for a workaround"""
    storage = WorkaroundFeedbackStorage()
    return storage.get_votes(sr_id, workaround_type)


if __name__ == "__main__":
    # Test the feedback storage
    print("Testing Feedback Storage System...")
    
    storage = WorkaroundFeedbackStorage()
    
    # Test upvote
    storage.upvote("SR-001", "ai", "Check PS config and update ipAddressRange")
    storage.upvote("SR-001", "ai", "Check PS config and update ipAddressRange")
    storage.upvote("SR-001", "original", "Manual fix required")
    
    # Test downvote
    storage.downvote("SR-001", "original", "Manual fix required")
    storage.downvote("SR-001", "original", "Manual fix required")
    
    # Get votes
    ai_votes = storage.get_votes("SR-001", "ai")
    print(f"\nAI Workaround votes: {ai_votes}")
    
    original_votes = storage.get_votes("SR-001", "original")
    print(f"Original Workaround votes: {original_votes}")
    
    # Get all votes for SR
    all_votes = storage.get_all_votes_for_sr("SR-001")
    print(f"\nAll votes for SR-001: {all_votes}")
    
    # Get statistics
    stats = storage.get_statistics()
    print(f"\nStatistics: {stats}")
    
    print("\n[OK] Test complete!")

