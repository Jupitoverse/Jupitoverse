"""
Compatibility wrapper that exposes the legacy ComprehensiveSRAnalyzer interface
while delegating to the modern AIEnhancedServiceRequestAnalyzer implementation.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List, Dict, Any

from batch_sr_analyser import AIEnhancedServiceRequestAnalyzer  # noqa: F401

logger = logging.getLogger(__name__)


class ComprehensiveSRAnalyzer:
    """
    Thin wrapper around AIEnhancedServiceRequestAnalyzer preserving the historic
    API expected by tooling such as sr_batch_processor.py.
    """

    def __init__(self, vector_store_path: str = "vector store") -> None:
        self.vector_store_path = Path(vector_store_path)
        self.engine = AIEnhancedServiceRequestAnalyzer()
        self._repoint_model_paths()

    def _repoint_model_paths(self) -> None:
        """
        Ensure the wrapped analyzer looks inside the provided vector store path
        for its SQLite databases and indices.
        """
        java_db = self.vector_store_path / "javaMapping.db"
        sr_db = self.vector_store_path / "sr_tracking.db"
        skills_db = self.vector_store_path / "people_skills.db"
        historical_index = self.vector_store_path / "historical_sr_index.pkl"
        java_classes = self.vector_store_path / "comcast_java_classes.pkl"

        if java_db.exists():
            self.engine.java_db_path = java_db
        if sr_db.exists():
            self.engine.sr_db_path = sr_db
        if skills_db.exists():
            self.engine.skills_db_path = skills_db

        # Try to load Phase 1 NLP-enhanced version first, then fallback to Phase 1, then original
        phase1_nlp_index = Path(self.vector_store_path) / "historical_sr_index_phase1_enhanced.pkl"
        phase1_index = Path(self.vector_store_path) / "historical_sr_index_phase1.pkl"
        
        if phase1_nlp_index.exists():
            self.engine.historical_index_path = phase1_nlp_index
            if self.engine.historical_indexer:
                try:
                    self.engine.historical_indexer.load_index(str(phase1_nlp_index))
                    self.engine.index_loaded = True
                    self.engine.phase1_enhanced = True
                    logger.info(f"Loaded Phase 1 NLP-enhanced index from {phase1_nlp_index}")
                except Exception as exc:
                    logger.warning("Failed to reload Phase 1 NLP-enhanced index: %s", exc)
        elif phase1_index.exists():
            self.engine.historical_index_path = phase1_index
            if self.engine.historical_indexer:
                try:
                    self.engine.historical_indexer.load_index(str(phase1_index))
                    self.engine.index_loaded = True
                    self.engine.phase1_enhanced = True
                    logger.info(f"Loaded Phase 1 index from {phase1_index}")
                except Exception as exc:
                    logger.warning("Failed to reload Phase 1 index: %s", exc)
        elif historical_index.exists():
            self.engine.historical_index_path = historical_index
            if self.engine.historical_indexer:
                try:
                    self.engine.historical_indexer.load_index(str(historical_index))
                    self.engine.index_loaded = True
                    logger.info(f"Loaded original historical index from {historical_index}")
                except Exception as exc:
                    logger.warning("Failed to reload historical index: %s", exc)
        
        # Load Java classes if available
        if java_classes.exists():
            self.engine.java_classes_path = java_classes
            try:
                import pickle
                with open(java_classes, 'rb') as f:
                    self.engine.java_classes_data = pickle.load(f)
                self.engine.java_class_index = self.engine.java_classes_data.get('class_index', {})
                self.engine.java_project_index = self.engine.java_classes_data.get('project_index', {})
                logger.info(f"Loaded {self.engine.java_classes_data.get('total_classes', 0)} Java classes")
            except Exception as exc:
                logger.warning("Failed to load Java classes: %s", exc)
        
        # Reload user feedback if available
        if self.engine.user_feedback_manager:
            try:
                self.engine.user_feedback_manager.load_feedback()
                if self.engine.user_feedback_manager.total_feedback_count > 0:
                    self.engine.user_feedback_loaded = True
                    logger.info(f"Reloaded {self.engine.user_feedback_manager.total_feedback_count} user feedback records")
            except Exception as exc:
                logger.warning("Failed to reload user feedback: %s", exc)

    def analyze_sr_batch(self, sr_records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze a collection of SR dictionaries and return the structured results.
        """
        results: List[Dict[str, Any]] = []

        for idx, record in enumerate(sr_records, start=1):
            try:
                analysis = self.engine.analyze_single_sr(record)
                results.append(analysis)
            except Exception as exc:
                logger.error("Failed to analyze record #%s (SR ID: %s): %s",
                             idx, record.get('Call ID') or record.get('SR ID'), exc)

        return results

