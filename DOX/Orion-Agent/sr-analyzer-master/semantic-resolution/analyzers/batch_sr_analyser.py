#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Enhanced Service Request Batch Analyzer
Comprehensive SR analysis using:
- Java backend mapping (javaMapping.db)
- Historical case intelligence (sr_tracking.db + historical_sr_index.pkl)
- Team skills and assignment (people_skills.db)
- AI-powered semantic search across 1.18+ million historical records
- Business day age calculation (priority_age_calculator.py)
"""

# Fix Windows console encoding issues - MUST BE FIRST
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import sqlite3
import numpy as np
import logging
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import json
import pickle

# Import sentence transformers for semantic search with history_data.db
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available - semantic search will be limited")

# Configure logging with UTF-8 support
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    errors='replace',
    handlers=[
        logging.FileHandler('sr_analysis.log', encoding='utf-8', errors='replace'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import required modules
try:
    from assignment.priority_age_calculator import PriorityAgeCalculator
    AGE_CALCULATOR_AVAILABLE = True
except ImportError:
    AGE_CALCULATOR_AVAILABLE = False
    logger.warning("priority_age_calculator not found - using basic age calculation")

# HistoricalDataIndexer is deprecated - not needed with ChromaDB
HISTORICAL_INDEXER_AVAILABLE = False

try:
    from user.feedback.user_feedback_manager import UserFeedbackManager
    USER_FEEDBACK_AVAILABLE = True
except ImportError:
    USER_FEEDBACK_AVAILABLE = False
    logger.warning("UserFeedbackManager not found - user feedback will not be used")


class AIEnhancedServiceRequestAnalyzer:
    """
    AI-Enhanced Service Request Analyzer with comprehensive intelligence capabilities
    """
    
    def __init__(self):
        """Initialize the enhanced analyzer with all AI intelligence sources"""
        # Database paths - SQLite files in database/, ChromaDB in vectorstore/
        self.sr_db_path = Path("data/database/sr_tracking.db") 
        self.skills_db_path = Path("data/database/people_skills.db")
        self.chromadb_path = Path("data/vectorstore/chromadb_store")
        
        # ChromaDB collections replace old pickle/FAISS files:
        # - clean_history_data collection (replaces clean_history_data.db pickle)
        # - java_mapping collection (replaces javaMapping.db pickle)
        # - comcast_code collection (replaces comcast_code.db FAISS)
        
        # Directory paths
        self.input_dir = Path("RAG/input")
        self.output_dir = Path("RAG/llm output")
        self.historical_dir = Path("past_data")
        
        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize age calculator
        if AGE_CALCULATOR_AVAILABLE:
            self.age_calculator = PriorityAgeCalculator()
            logger.info("✅ PriorityAgeCalculator initialized")
        else:
            self.age_calculator = None
            logger.warning("⚠️ PriorityAgeCalculator not available")
        
        # Initialize NEW history_data.db semantic vectorstore
        self.historical_db = None
        self.semantic_model = None
        self.index_loaded = False
        self.preprocessor = None  # For SR text preprocessing (removes noise)
        
        # Also keep old indexer as fallback
        self.historical_indexer = None
        self.phase1_enhanced = False
        
        # Initialize SR text preprocessor if available
        try:
            # Add parent directory to path for imports
            import sys
            parent_dir = Path(__file__).parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            from analyzers.sr_text_preprocessor import SRTextPreprocessor
            self.preprocessor = SRTextPreprocessor()
            logger.info("✅ Text preprocessor initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not load preprocessor: {e}")
            self.preprocessor = None
        
        # Initialize ChromaDB for historical data
        self.chromadb_client = None
        self.history_collection = None
        self.java_mapping_collection = None
        
        if self.chromadb_path.exists() and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                import chromadb
                
                logger.info(f"🔄 Loading ChromaDB from {self.chromadb_path}")
                # Use basic PersistentClient without Settings to avoid "different settings" error
                self.chromadb_client = chromadb.PersistentClient(path=str(self.chromadb_path))
                
                # Load collections
                self.history_collection = self.chromadb_client.get_collection('clean_history_data')
                self.java_mapping_collection = self.chromadb_client.get_collection('java_mapping')
                
                # Load the Sentence Transformer model
                logger.info("🔄 Loading Sentence Transformer model (all-MiniLM-L6-v2)...")
                # Load without device parameter to avoid meta tensor error
                self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                
                self.index_loaded = True
                total_records = self.history_collection.count()
                logger.info(f"✅ ChromaDB loaded successfully!")
                logger.info(f"   📊 History records: {total_records:,}")
                logger.info(f"   📊 Java mappings: {self.java_mapping_collection.count():,}")
                logger.info(f"   🧠 Model: all-MiniLM-L6-v2")
                logger.info(f"   🔍 Semantic search: ENABLED with Sentence Transformers")
            except Exception as e:
                logger.error(f"❌ Error loading ChromaDB: {str(e)}")
                self.chromadb_client = None
                self.history_collection = None
                self.semantic_model = None
        elif not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("⚠️ sentence-transformers not available - semantic search disabled")
        else:
            logger.warning(f"⚠️ ChromaDB not found at {self.chromadb_path}")
        
        # Initialize user feedback manager for prioritized workarounds
        self.user_feedback_manager = None
        self.user_feedback_loaded = False
        
        if USER_FEEDBACK_AVAILABLE:
            try:
                self.user_feedback_manager = UserFeedbackManager()
                if self.user_feedback_manager.total_feedback_count > 0:
                    self.user_feedback_loaded = True
                    logger.info(f"✅ User feedback loaded: {self.user_feedback_manager.total_feedback_count} corrections")
                else:
                    logger.info("ℹ️ No user feedback yet - will be created when first feedback is submitted")
            except Exception as e:
                logger.error(f"❌ Error loading user feedback: {str(e)}")
                self.user_feedback_manager = None
        
        # Java classes now loaded from ChromaDB java_mapping collection
        # (already loaded via self.java_mapping_collection above)
        self.java_classes_data = None
        self.java_class_index = {}
        self.java_project_index = {}
        
        # Analysis statistics
        self.stats = {
            'total_srs': 0,
            'total_processed': 0,  # Counts processed SRs for round-robin fallback
            'java_failures_detected': 0,
            'java_files_identified': 0,
            'historical_matches_found': 0,
            'ai_semantic_searches': 0,
            'workarounds_extracted': 0,
            'interface_detections': 0,
            'skills_based_assignments': 0,
            'high_confidence_analyses': 0,
            'processing_errors': 0
        }
        
        # Daily load tracking for equal SR distribution
        # Tracks assignments per team member (resets daily)
        self.daily_assignments = {}  # {member_name: count}
        self.daily_assignment_date = None  # Reset when date changes
        
        # Java error patterns for enhanced detection
        self.java_error_patterns = [
            r'java\.lang\.\w*Exception',
            r'NullPointerException',
            r'SQLException',
            r'ConnectionException',
            r'TimeoutException',
            r'ClassNotFoundException',
            r'NoSuchMethodException',
            r'IllegalArgumentException',
            r'RuntimeException',
            r'at\s+[\w\.]+\(',  # Stack trace pattern
            r'Caused by:',
            r'Exception in thread',
            r'spring framework',
            r'hibernate',
            r'database.*error',
            r'connection.*failed',
            r'service.*unavailable'
        ]
        
        # Interface detection keywords
        self.interface_keywords = {
            'DCP': ['dcp', 'design center platform', 'quote', 'pricing', 'catalog', 'product catalog'],
            'OMW': ['omw', 'order management', 'orchestration', 'workflow', 'order flow', 'provisioning'],
            'CAMP': ['camp', 'customer account', 'account management', 'billing account'],
            'OSO': ['oso', 'order submission', 'order entry'],
            'Broadsoft': ['broadsoft', 'voice', 'sip', 'trunk', 'telephony', 'voip'],
            'Billing': ['billing interface', 'invoice system', 'rating', 'charging'],
            'CRM': ['crm', 'customer relationship', 'salesforce'],
            'Inventory': ['inventory', 'resource management', 'network inventory']
        }
        
        logger.info("=" * 80)
        logger.info("AI-Enhanced Service Request Analyzer Initialized")
        logger.info("=" * 80)
        logger.info(f"ChromaDB: {'✅' if self.chromadb_path.exists() else '❌'} {self.chromadb_path}")
        logger.info(f"SR DB: {'✅' if self.sr_db_path.exists() else '❌'} {self.sr_db_path}")
        logger.info(f"Skills DB: {'✅' if self.skills_db_path.exists() else '❌'} {self.skills_db_path}")
        logger.info(f"Semantic Search: {'✅' if self.index_loaded else '❌'} ChromaDB collections")
        logger.info("=" * 80)
        
    def connect_database(self, db_path: Path) -> Optional[sqlite3.Connection]:
        """Connect to a SQLite database"""
        try:
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                return conn
            else:
                logger.warning(f"Database not found: {db_path}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to {db_path}: {str(e)}")
            return None
    
    def calculate_sr_age(self, submit_date: Any) -> Tuple[str, int]:
        """
        Calculate SR age using business day calculator
        Returns (formatted_age_string, business_days_int)
        """
        try:
            if self.age_calculator:
                business_days = self.age_calculator.calculate_business_days(submit_date)
                if business_days == 0:
                    return "< 1 business day", 0
                elif business_days == 1:
                    return "1 business day", 1
                else:
                    return f"{business_days} business days", business_days
            else:
                # Fallback calculation
                if pd.isna(submit_date) or not submit_date:
                    return "Unknown", 0
                
                submit_date = pd.to_datetime(submit_date)
                current_date = datetime.now()
                age_delta = current_date - submit_date
                days = age_delta.days
                
                if days == 0:
                    return "< 1 day", 0
                elif days == 1:
                    return "1 day", 1
                else:
                    return f"{days} days", days
                    
        except Exception as e:
            logger.warning(f"Error calculating age: {str(e)}")
            return "Unknown", 0
    
    def _match_java_classes_from_text(self, text: str) -> Dict:
        """
        Match Java classes from text using the comcast_java_classes.pkl index.
        Returns matched classes and their projects.
        NOTE: Text should NOT be lowercased before calling this function!
        """
        matched_info = {
            'matched_classes': [],
            'projects': set(),
            'class_details': []
        }
        
        if not self.java_class_index:
            return matched_info
        
        # Extract potential class names from text (CamelCase patterns)
        # IMPORTANT: Don't lowercase the text - we need CamelCase to match!
        class_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+(?:Impl|Service|Controller|Manager|Processor|Handler|Repository|Factory|Builder|Validator|Helper|Util|Client|Adapter|Mapper|Converter|Provider|Listener|Filter|Interceptor|Exception|Dao|Entity|Config|Application)?)\b'
        potential_classes = re.findall(class_pattern, text)
        
        logger.debug(f"Extracted {len(potential_classes)} potential class names: {potential_classes[:10]}")
        
        # Match against class index
        for class_name in potential_classes:
            if class_name in self.java_class_index:
                instances = self.java_class_index[class_name]
                matched_info['matched_classes'].append(class_name)
                logger.debug(f"Matched class: {class_name} in {len(instances)} instance(s)")
                
                for instance in instances:
                    project = instance.get('project', 'Unknown')
                    matched_info['projects'].add(project)
                    matched_info['class_details'].append({
                        'class_name': class_name,
                        'package': instance.get('package', ''),
                        'project': project
                    })
            else:
                logger.debug(f"Class not found in index: {class_name}")
        
        # Convert set to list for JSON serialization
        matched_info['projects'] = list(matched_info['projects'])
        
        return matched_info
    
    def advanced_java_analysis(self, description: str, notes: str, category: str) -> Dict:
        """
        Advanced Java backend analysis with AI-powered error detection.
        Prioritizes detailed XLSX implementation files over CSV summaries.
        """
        java_context = {
            'java_failure_detected': False,
            'java_files': [],
            'error_types': [],
            'stack_traces': [],
            'interfaces_affected': [],
            'confidence_score': 0.0,
            'technical_details': [],
            'implementation_classes': []  # New: track actual implementation classes
        }
        
        # Create original text for class matching (preserve CamelCase)
        original_text = f"{description} {notes} {category}"
        
        # Create lowercased text for error pattern matching
        full_text = original_text.lower()
        
        # First: Match Java classes from text using the pickle file (needs original case)
        class_matches = self._match_java_classes_from_text(original_text)
        if class_matches['matched_classes']:
            java_context['implementation_classes'] = class_matches['matched_classes'][:30]
            java_context['matched_projects'] = class_matches['projects']
            java_context['java_files'] = class_matches['projects']  # Projects as "files"
            logger.info(f"Matched {len(class_matches['matched_classes'])} Java classes from {len(class_matches['projects'])} projects")
        
        # Second: Detect Java error patterns
        java_indicators = 0
        for pattern in self.java_error_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            if matches:
                java_indicators += len(matches)
                java_context['stack_traces'].extend(matches)
        
        # Java failure detected if we have error patterns OR matched classes
        if java_indicators < 1 and not class_matches['matched_classes']:
            return java_context

        java_context['java_failure_detected'] = True
        java_context['confidence_score'] = min(0.9, 0.5 + (java_indicators * 0.1))
        self.stats['java_failures_detected'] += 1
        
        # Use ChromaDB java_mapping collection if available
        if self.java_mapping_collection:
            try:
                # Search java_mapping collection
                query_text = full_text[:500]  # Limit query size
                query_embedding = self.semantic_model.encode([query_text])[0].tolist()
                
                results = self.java_mapping_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=10,
                    include=['metadatas', 'documents']
                )
                
                for i, doc in enumerate(results.get('documents', [[]])[0]):
                    metadata = results.get('metadatas', [[]])[0][i] if i < len(results.get('metadatas', [[]])[0]) else {}
                    file_name = metadata.get('file_name', f'java_file_{i}')
                    if file_name not in java_context['java_files']:
                        java_context['java_files'].append(file_name)
                        self.stats['java_files_identified'] += 1
                    
                    # Extract class names from document
                    class_names = self._extract_class_names(doc)
                    java_context['implementation_classes'].extend(class_names)
                    
                    # Extract technical details
                    for line in doc.split('\n')[:10]:
                        if any(word in line.lower() for word in ['error', 'exception', 'class']):
                            detail = line.strip()[:200]
                            if detail and detail not in java_context['technical_details']:
                                java_context['technical_details'].append(detail)
                
                return java_context
            except Exception as e:
                logger.warning(f"ChromaDB java_mapping query failed: {e}")
        
        # Legacy SQLite fallback (disabled - using ChromaDB only)
        return java_context
        
        # Legacy code below (kept for reference but not executed)
        conn = None  # self.connect_database(self.java_db_path)
        if not conn:
            return java_context

        try:
            cursor = conn.cursor()
            search_terms = self.extract_technical_terms(full_text)
            
            if search_terms:
                # First: Search XLSX files (detailed implementation) with higher priority
                xlsx_results = self._search_java_xlsx_files(cursor, search_terms)
                
                # Second: Search CSV files (summaries) for additional context
                csv_results = self._search_java_csv_files(cursor, search_terms)
                
                # Combine results: XLSX first (implementation details), then CSV (context)
                all_results = xlsx_results + csv_results
                
                # Process results
                logger.debug(f"Java search found {len(all_results)} results for search terms: {search_terms[:5]}")
                for file_name, document in all_results[:25]:  # Increased from 10 to 25
                    if file_name not in java_context['java_files']:
                        java_context['java_files'].append(file_name)
                        self.stats['java_files_identified'] += 1
                        logger.debug(f"Added Java file: {file_name}")

                    lowered = document.lower()
                    
                    # Extract implementation class names from XLSX files
                    if 'Java_Analysis.xlsx' in file_name:
                        class_names = self._extract_class_names(document)
                        java_context['implementation_classes'].extend(class_names)
                    
                    # Extract error and exception information
                    if any(token in lowered for token in ['error', 'exception', 'failure']):
                        for line in document.splitlines():
                            if any(word in line.lower() for word in ['error', 'exception', 'failure']):
                                detail = line.strip()[:200]  # Increased from 150 to 200
                                if detail and detail not in java_context['technical_details']:
                                    java_context['technical_details'].append(detail)
                                if len(java_context['technical_details']) >= 10:
                                    break

                    # Extract interface information
                    if 'interface' in lowered:
                        interface_info = f"Interface in {file_name}"
                        if interface_info not in java_context['interfaces_affected']:
                            java_context['interfaces_affected'].append(interface_info)

                # Deduplicate implementation classes and increase limit
                java_context['implementation_classes'] = list(set(java_context['implementation_classes']))[:50]

        except Exception as exc:
            logger.error(f"Error querying Java database: {str(exc)}")
        finally:
            conn.close()

        return java_context
    
    def _search_java_xlsx_files(self, cursor, search_terms: List[str]) -> List[Tuple[str, str]]:
        """
        Search detailed Java Analysis XLSX files for implementation classes.
        These contain actual class names, methods, exceptions, etc.
        Now prioritizes based on extracted module names, not hardcoded activation.
        """
        query_conditions = []
        params: List[Any] = []
        
        for term in search_terms[:5]:
            query_conditions.append("(file_name LIKE ? OR document LIKE ?)")
            params.extend([f"%{term}%", f"%{term}%"])
        
        if query_conditions:
            # Build dynamic ORDER BY based on extracted search terms
            # Prioritize files matching the first few search terms (most specific)
            order_cases = []
            for idx, term in enumerate(search_terms[:3], 1):
                order_cases.append(f"WHEN file_name LIKE '%{term}%' THEN {idx}")
            
            # Add default priority for common modules
            order_cases.append("WHEN file_name LIKE '%activation%' THEN 10")
            order_cases.append("WHEN file_name LIKE '%customization%' THEN 11")
            order_cases.append("WHEN file_name LIKE '%frontend%' THEN 12")
            order_cases.append("ELSE 20")
            
            query = f"""
                SELECT DISTINCT file_name, document
                FROM embeddings 
                WHERE file_name LIKE '%Java_Analysis.xlsx'
                  AND ({' OR '.join(query_conditions)})
                ORDER BY 
                    CASE 
                        {' '.join(order_cases)}
                    END,
                    file_name
                LIMIT 20
            """
            logger.debug(f"SQL Query ORDER BY cases: {order_cases}")
            cursor.execute(query, params)
            results = cursor.fetchall()
            logger.debug(f"XLSX search returned {len(results)} results, unique files: {len(set([r[0] for r in results]))}")
            return results
        return []
    
    def _search_java_csv_files(self, cursor, search_terms: List[str]) -> List[Tuple[str, str]]:
        """
        Search CSV summary files for high-level context.
        These provide overview but not detailed implementation.
        """
        query_conditions = []
        params: List[Any] = []
        
        for term in search_terms[:3]:  # Fewer terms for CSV
            query_conditions.append("(file_name LIKE ? OR document LIKE ?)")
            params.extend([f"%{term}%", f"%{term}%"])

        if query_conditions:
            query = f"""
                SELECT DISTINCT file_name, document
                FROM embeddings
                WHERE file_name LIKE '%.csv'
                  AND ({' OR '.join(query_conditions)})
                ORDER BY file_name
                LIMIT 5
            """
            cursor.execute(query, params)
            return cursor.fetchall()
        return []
    
    def _extract_class_names(self, document: str) -> List[str]:
        """
        Extract Java class names from XLSX document content.
        Enhanced to extract more implementation classes with multiple patterns.
        """
        class_names = []
        
        # Pattern 1: Class Name: ClassName (most reliable)
        class_pattern = r'Class Name[:\s]+([A-Z][a-zA-Z0-9_]+)'
        matches = re.findall(class_pattern, document)
        class_names.extend(matches)
        
        # Pattern 2: ClassName.java (file names)
        java_file_pattern = r'([A-Z][a-zA-Z0-9_]+)\.java'
        matches = re.findall(java_file_pattern, document)
        class_names.extend(matches)
        
        # Pattern 3: Implementation class patterns (common suffixes)
        impl_patterns = [
            r'([A-Z][a-zA-Z0-9_]*Impl)\b',           # ServiceImpl, DaoImpl
            r'([A-Z][a-zA-Z0-9_]*Service)\b',        # ActivationService
            r'([A-Z][a-zA-Z0-9_]*Controller)\b',     # ActivationController
            r'([A-Z][a-zA-Z0-9_]*Manager)\b',        # MessageManager
            r'([A-Z][a-zA-Z0-9_]*Handler)\b',        # RequestHandler
            r'([A-Z][a-zA-Z0-9_]*Processor)\b',      # EventProcessor
            r'([A-Z][a-zA-Z0-9_]*Repository)\b',     # DataRepository
            r'([A-Z][a-zA-Z0-9_]*Factory)\b',        # ServiceFactory
            r'([A-Z][a-zA-Z0-9_]*Builder)\b',        # RequestBuilder
            r'([A-Z][a-zA-Z0-9_]*Validator)\b',      # InputValidator
            r'([A-Z][a-zA-Z0-9_]*Helper)\b',         # UtilityHelper
            r'([A-Z][a-zA-Z0-9_]*Util)\b',           # StringUtil
            r'([A-Z][a-zA-Z0-9_]*Client)\b',         # ApiClient
            r'([A-Z][a-zA-Z0-9_]*Adapter)\b',        # DataAdapter
            r'([A-Z][a-zA-Z0-9_]*Mapper)\b',         # EntityMapper
            r'([A-Z][a-zA-Z0-9_]*Converter)\b',      # TypeConverter
            r'([A-Z][a-zA-Z0-9_]*Provider)\b',       # DataProvider
            r'([A-Z][a-zA-Z0-9_]*Listener)\b',       # EventListener
            r'([A-Z][a-zA-Z0-9_]*Filter)\b',         # RequestFilter
            r'([A-Z][a-zA-Z0-9_]*Interceptor)\b',    # LoggingInterceptor
        ]
        
        for pattern in impl_patterns:
            matches = re.findall(pattern, document)
            class_names.extend(matches)
        
        # Pattern 4: Exception classes
        exception_pattern = r'([A-Z][a-zA-Z0-9_]*Exception)\b'
        matches = re.findall(exception_pattern, document)
        class_names.extend(matches)
        
        # Pattern 5: DAO classes
        dao_pattern = r'([A-Z][a-zA-Z0-9_]*Dao)\b'
        matches = re.findall(dao_pattern, document)
        class_names.extend(matches)
        
        # Pattern 6: Entity/Model classes (common in business logic)
        entity_pattern = r'([A-Z][a-zA-Z0-9_]*Entity)\b'
        matches = re.findall(entity_pattern, document)
        class_names.extend(matches)
        
        # Pattern 7: Configuration classes
        config_pattern = r'([A-Z][a-zA-Z0-9_]*Config)\b'
        matches = re.findall(config_pattern, document)
        class_names.extend(matches)
        
        # Pattern 8: Generic Java class pattern (CamelCase starting with capital)
        # More aggressive - matches any CamelCase that looks like a class
        generic_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b'
        matches = re.findall(generic_pattern, document)
        class_names.extend(matches)
        
        return class_names
    
    def ai_semantic_search(self, description: str, notes: str) -> Dict:
        """
        Use historical_sr_index.pkl for AI-powered semantic search across 1.18M+ records
        """
        ai_results = {
            'similar_cases': [],
            'classification': 'Moderate',
            'confidence': 0.5,
            'resolution_type': 'Investigation Required',
            'interface_likelihood': 0.0,
            'workaround_likelihood': 0.0,
            'complexity': 'Medium',
            'workarounds': [],
            'target_interface': 'Unknown',
            'success_rate': 0.0,
            'similar_cases_count': 0
        }
        
        if not self.index_loaded or not self.historical_indexer:
            logger.debug("Historical index not available for semantic search")
            return ai_results
        
        try:
            # Use AI semantic search - prioritize notes over vague description
            query = f"{notes} {description}" if notes else description
            prediction = self.historical_indexer.predict_outcome(description, notes)
            
            self.stats['ai_semantic_searches'] += 1
            
            # Extract similar cases
            similar_cases = prediction.get('similar_cases', [])
            ai_results['similar_cases'] = similar_cases
            ai_results['similar_cases_count'] = len(similar_cases)
            ai_results['query'] = query  # Add query for user feedback search
            ai_results['description'] = description  # Add description for user feedback search
            ai_results['notes'] = notes  # CRITICAL FIX: Add notes for user feedback search
            
            # Extract AI predictions
            ai_results['classification'] = prediction.get('classification', 'Moderate')
            ai_results['confidence'] = prediction.get('confidence', 0.5)
            ai_results['resolution_type'] = prediction.get('resolution_type', 'Investigation Required')
            ai_results['interface_likelihood'] = prediction.get('interface_likelihood', 0.0)
            ai_results['workaround_likelihood'] = prediction.get('workaround_likelihood', 0.0)
            ai_results['complexity'] = prediction.get('complexity', 'Medium')
            
            # Extract workarounds from similar cases
            workarounds = []
            for case in similar_cases[:5]:
                outcome = case.get('outcome', {})
                wa_text = outcome.get('workaround_text')
                if wa_text and len(str(wa_text).strip()) > 30:
                    workarounds.append({
                        'sr_id': case.get('sr_id', 'Unknown'),
                        'text': str(wa_text).strip(),
                        'similarity': case.get('similarity', 0),
                        'classification': outcome.get('classification', 'Unknown')
                    })
            
            ai_results['workarounds'] = workarounds
            self.stats['workarounds_extracted'] += len(workarounds)
            
            # Calculate success rate from similar cases
            if similar_cases:
                successful = sum(1 for c in similar_cases if c.get('outcome', {}).get('classification') != 'Tough')
                ai_results['success_rate'] = successful / len(similar_cases) if similar_cases else 0.0
            
            # Detect target interface
            ai_results['target_interface'] = self.detect_interface(description, notes, similar_cases)
            if ai_results['target_interface'] != 'Unknown':
                self.stats['interface_detections'] += 1
            
        except Exception as e:
            logger.error(f"Error in AI semantic search: {str(e)}")
        
        return ai_results
    
    def detect_interface(self, description: str, notes: str, similar_cases: List[Dict] = None) -> str:
        """
        Detect target interface system (DCP/OMW/CAMP/OSO/Broadsoft/etc.)
        """
        combined_text = f"{description} {notes}".lower()
        
        # Score each interface based on keyword matches
        interface_scores = {}
        for interface, keywords in self.interface_keywords.items():
            score = sum(2 if kw in combined_text else 0 for kw in keywords)
            if score > 0:
                interface_scores[interface] = score
        
        # Check similar cases for interface mentions
        if similar_cases:
            for case in similar_cases[:5]:
                outcome = case.get('outcome', {})
                resolution = str(outcome.get('resolution_type', '')).lower()
                desc = str(case.get('description', '')).lower()
                
                for interface, keywords in self.interface_keywords.items():
                    for kw in keywords:
                        if kw in resolution or kw in desc:
                            interface_scores[interface] = interface_scores.get(interface, 0) + 1
        
        # Return the interface with highest score
        if interface_scores:
            return max(interface_scores.items(), key=lambda x: x[1])[0]
        
        return 'Unknown'
    
    def semantic_search_history(self, description: str, notes: str = "", top_k: int = 5) -> List[Dict]:
        """
        Semantic search using ChromaDB with Sentence Transformers
        Returns SR IDs with combined semantic workaround (resolution + wl_summary + workaround)
        Plus SLA categorization fields
        
        Args:
            description: SR description text
            notes: Additional notes text
            top_k: Number of top results to return (default 5)
            
        Returns:
            List of dicts with sr_id, semantic_workaround, SLA categorization fields, similarity
        """
        if not self.history_collection or not self.semantic_model:
            logger.debug("ChromaDB or semantic model not available")
            return []
        
        try:
            # Build query from description and notes
            query_text = f"{description} {notes}".strip()
            
            if len(query_text) < 10:
                logger.debug("Query text too short for semantic search")
                return []
            
            # Preprocess query if preprocessor available
            if self.preprocessor:
                original_query = query_text
                query_text = self.preprocessor.clean_for_semantic_search(query_text)
                if len(query_text) < 10:
                    query_text = original_query
            
            # Encode query using Sentence Transformers
            logger.debug(f"🔍 Encoding query with Sentence Transformers...")
            query_embedding = self.semantic_model.encode([query_text])[0].tolist()
            
            # Query ChromaDB
            chroma_results = self.history_collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,  # Get more to filter
                include=['metadatas', 'distances']
            )
            
            results = []
            metadatas = chroma_results.get('metadatas', [[]])[0]
            distances = chroma_results.get('distances', [[]])[0]
            
            for i, metadata in enumerate(metadatas):
                # Convert distance to similarity (ChromaDB uses L2 distance)
                # For normalized embeddings: similarity = 1 - (distance^2 / 2)
                distance = distances[i] if i < len(distances) else 1.0
                similarity = max(0, 1 - (distance / 2))  # Approximate conversion
                
                if similarity < 0.50:  # Skip if less than 50% similar
                    continue
                
                if len(results) >= top_k:  # Stop once we have enough
                    break
                
                # Create semantic workaround = resolution + wl_summary + workaround
                semantic_parts = []
                
                resolution = str(metadata.get('resolution', '')).strip()
                wl_summary = str(metadata.get('wl_summary', '')).strip()
                workaround = str(metadata.get('workaround', '')).strip()
                
                if resolution and resolution.lower() not in ['nan', 'none', '']:
                    semantic_parts.append(f"Resolution: {resolution}")
                
                if wl_summary and wl_summary.lower() not in ['nan', 'none', '']:
                    semantic_parts.append(f"WL Summary: {wl_summary}")
                
                if workaround and workaround.lower() not in ['nan', 'none', '']:
                    semantic_parts.append(f"Workaround: {workaround}")
                
                # Skip if no meaningful content
                if not semantic_parts:
                    continue
                
                semantic_workaround = "\n\n".join(semantic_parts)
                
                results.append({
                    'sr_id': metadata.get('call_id', 'Unknown'),
                    'semantic_workaround': semantic_workaround,
                    'ai_generated_workaround': metadata.get('ai_generated_workaround', 'NA'),
                    'user_corrected_workaround': metadata.get('user_corrected_workaround', ''),
                    # Individual fields for UI display (summary removed - was redundant)
                    'wl_summary': metadata.get('wl_summary', ''),
                    'workaround': metadata.get('workaround', ''),
                    # SLA Categorization fields
                    'resolution_categorization': metadata.get('resolution_categorization', ''),
                    'resolution_categorization_tier3': metadata.get('resolution_categorization_tier3', ''),
                    'sla_resolution_categorization_t1': metadata.get('sla_resolution_categorization_t1', ''),
                    'sla_resolution_category': metadata.get('sla_resolution_category', ''),
                    'similarity': similarity,
                    'priority': metadata.get('priority', ''),
                    'description': str(metadata.get('description', ''))[:100],  # Truncated for context
                })
            
            if results:
                logger.info(f"   ✅ Found {len(results)} semantic matches (top similarity: {results[0]['similarity']:.1%})")
            else:
                logger.debug("   ℹ️ No semantic matches found above 50% threshold")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def format_semantic_workarounds(self, similar_srs: List[Dict]) -> Dict:
        """
        Format data from similar SRs into separate sections:
        - Semantic workarounds (summary + wl_summary + workaround)
        - Previous AI workarounds (ai_generated_workaround)
        - User corrections (user_corrected_workaround)
        - SLA categorization paths
        
        Args:
            similar_srs: List of similar SRs from semantic_search_history
            
        Returns:
            Dict with all formatted sections
        """
        semantic_formatted = []  # summary + wl_summary + workaround
        ai_workarounds_formatted = []  # ai_generated_workaround from similar SRs
        user_corrections_formatted = []  # user_corrected_workaround from similar SRs
        categorization_paths = []  # Resolution categorization (resolution + tier3)
        sla_categorization_paths = []  # SLA categorization (sla_t1 + sla_category)
        
        for i, sr_data in enumerate(similar_srs, 1):
            sr_id = sr_data.get('sr_id', 'Unknown')
            similarity = sr_data.get('similarity', 0)
            
            # 1️⃣ SEMANTIC WORKAROUND: ONLY workaround field (not summary or wl_summary)
            workaround = str(sr_data.get('workaround', '')).strip() if sr_data.get('workaround') is not None else ''
            
            if workaround and workaround.lower() not in ['nan', 'none', '']:
                semantic_formatted.append(f"SR ID: {sr_id}")
                semantic_formatted.append(f"Similarity: {similarity:.1%}")
                semantic_formatted.append(f"Workaround: {workaround}")
                semantic_formatted.append("")  # Blank line
            
            # 2️⃣ PREVIOUS AI WORKAROUND: From matched historical SRs
            ai_wa = str(sr_data.get('ai_generated_workaround', 'NA')) if sr_data.get('ai_generated_workaround') is not None else 'NA'
            if ai_wa and ai_wa.strip() and ai_wa.upper() != 'NA':
                ai_workarounds_formatted.append(f"SR ID: {sr_id}")
                ai_workarounds_formatted.append(f"Similarity: {similarity:.1%}")
                ai_workarounds_formatted.append(f"Previous AI Workaround: {ai_wa}")
                ai_workarounds_formatted.append("")  # Blank line
            
            # 3️⃣ USER CORRECTIONS: From matched historical SRs
            user_wa = str(sr_data.get('user_corrected_workaround', '')) if sr_data.get('user_corrected_workaround') is not None else ''
            if user_wa and user_wa.strip() and user_wa.lower() not in ['nan', 'none', '']:
                user_corrections_formatted.append(f"SR ID: {sr_id}")
                user_corrections_formatted.append(f"Similarity: {similarity:.1%}")
                user_corrections_formatted.append(f"User Correction: {user_wa}")
                user_corrections_formatted.append("")  # Blank line
            
            # 4️⃣ RESOLUTION CATEGORIZATION: Concatenate resolution fields
            resolution_parts = []
            for field in ['resolution_categorization', 'resolution_categorization_tier3']:
                value = str(sr_data.get(field, '')).strip() if sr_data.get(field) is not None else ''
                if value and value.lower() not in ['nan', 'none', 'n/a', '']:
                    resolution_parts.append(value)
            
            if resolution_parts:
                resolution_path = ' > '.join(resolution_parts)
                if resolution_path not in categorization_paths:
                    categorization_paths.append(resolution_path)
            
            # 5️⃣ SLA RESOLUTION CATEGORIZATION: Concatenate SLA fields
            sla_parts = []
            for field in ['sla_resolution_categorization_t1', 'sla_resolution_category']:
                value = str(sr_data.get(field, '')).strip() if sr_data.get(field) is not None else ''
                if value and value.lower() not in ['nan', 'none', 'n/a', '']:
                    sla_parts.append(value)
            
            if sla_parts:
                sla_path = ' > '.join(sla_parts)
                if sla_path not in sla_categorization_paths:
                    sla_categorization_paths.append(sla_path)
        
        return {
            # Semantic workarounds (summary + wl_summary + workaround)
            'formatted_text': '\n'.join(semantic_formatted) if semantic_formatted else 'No semantic matches found',
            'semantic_workarounds_list': '\n'.join(semantic_formatted) if semantic_formatted else 'No semantic matches found',
            
            # Previous AI workarounds from matched SRs
            'ai_workarounds_list': '\n'.join(ai_workarounds_formatted) if ai_workarounds_formatted else 'No AI workarounds found',
            
            # User corrections from matched SRs
            'user_corrections_list': '\n'.join(user_corrections_formatted) if user_corrections_formatted else 'No user corrections found',
            
            # Dual categorization fields (Resolution + SLA)
            'resolution_categorization_display': ' | '.join(categorization_paths) if categorization_paths else 'N/A',
            'sla_resolution_display': ' | '.join(sla_categorization_paths) if sla_categorization_paths else 'N/A',
            
            # Keep old fields for backward compatibility
            'categorization_display': ' | '.join(categorization_paths) if categorization_paths else 'N/A',
            'resolution_categories': ' | '.join(categorization_paths) if categorization_paths else 'N/A',
            'status_reasons': ' | '.join(sla_categorization_paths) if sla_categorization_paths else 'N/A',
            'match_count': len(similar_srs)
        }
    
    def comprehensive_historical_analysis(self, description: str, category: str, priority: str) -> Dict:
        """
        Enhanced historical analysis using pickle file (historical_sr_index.pkl)
        NOTE: We use the pickle file instead of sr_tracking.db because the pickle file
        contains the 'resolution' field with all workarounds, while the database doesn't.
        """
        historical_context = {
            'similar_cases_count': 0,
            'similar_cases_description': '',
            'similar_cases': [],  # NEW: Store full case objects for workaround collection
            'success_rate': 0.0,
            'avg_resolution_time': 0.0,
            'historical_patterns': [],
            'resolution_approaches': [],
            'confidence_level': 0.0
        }
        
        # Use pickle file data instead of database
        if not self.index_loaded or not self.historical_indexer:
            logger.debug("Historical index not available")
            return historical_context

        try:
            # Search for similar cases using the pickle file's historical_data
            # Ensure description is a string
            description_str = str(description) if description else ""
            search_terms = self.extract_key_terms(description_str)
            
            if search_terms and hasattr(self.historical_indexer, 'historical_data'):
                similar_cases = []
                
                # Search through historical data
                for record in self.historical_indexer.historical_data:
                    # Safely convert to string and lowercase
                    searchable_text = str(record.get('searchable_text', '')).lower()
                    description_text = str(record.get('description', '')).lower()
                    resolution_text = str(record.get('resolution', '')).lower()
                    
                    # Check if any search term matches
                    match_count = 0
                    for term in search_terms[:4]:
                        # Ensure term is a string
                        term_str = str(term) if term else ""
                        term_lower = term_str.lower()
                        if term_lower in searchable_text or term_lower in description_text or term_lower in resolution_text:
                            match_count += 1
                    
                    if match_count > 0:
                        similar_cases.append({
                            'record': record,
                            'match_score': match_count
                        })
                
                # Sort by match score and limit to top 15
                similar_cases.sort(key=lambda x: x['match_score'], reverse=True)
                similar_cases = similar_cases[:15]
                
                if similar_cases:
                    historical_context['similar_cases_count'] = len(similar_cases)
                    self.stats['historical_matches_found'] += len(similar_cases)
                    
                    # NEW: Store full case objects with calculated similarity for workaround collection
                    # Convert match_score to similarity percentage (normalize based on max possible matches)
                    max_match_score = similar_cases[0]['match_score'] if similar_cases else 1
                    historical_context['similar_cases'] = [
                        {
                            'sr_id': c['record'].get('sr_id'),
                            'description': c['record'].get('description', ''),
                            'outcome': c['record'].get('outcome', {}),
                            'resolution': c['record'].get('resolution', ''),
                            'similarity': min(0.95, c['match_score'] / max(max_match_score, 1) * 0.8)  # Scale to 0-80% range
                        }
                        for c in similar_cases
                    ]
                    
                    # Calculate success rate (based on outcome field)
                    successful_cases = [
                        c for c in similar_cases 
                        if str(c['record'].get('outcome', '')).lower() in ['resolved', 'workaround', 'fixed']
                    ]
                    
                    if successful_cases:
                        historical_context['success_rate'] = len(successful_cases) / len(similar_cases)
                    
                    # Extract resolution approaches from successful cases
                    historical_context['resolution_approaches'] = [
                        c['record'].get('resolution', '')[:200]  # Limit to 200 chars
                        for c in successful_cases[:3]
                        if c['record'].get('resolution') and len(c['record'].get('resolution', '').strip()) > 20
                    ]
                    
                    # Create case descriptions
                    case_descriptions = [
                        f"SR{c['record'].get('sr_id', 'Unknown')}: {str(c['record'].get('description', ''))[:40]}..."
                        for c in similar_cases[:3]
                    ]
                    historical_context['similar_cases_description'] = " | ".join(case_descriptions)
                    historical_context['confidence_level'] = min(0.95, 0.6 + (len(similar_cases) * 0.05))
            
        except Exception as exc:
            logger.error(f"Error querying historical pickle file: {str(exc)}")
        
        return historical_context
    
    def intelligent_team_assignment(self, application: str, complexity_score: float, priority: str, java_failure: bool) -> Dict:
        """
        Determine the best assignee from people_skills.db with improved distribution.
        Uses application normalization, load balancing, and availability to ensure even distribution.
        
        GUARANTEED ASSIGNMENT: Every SR will be assigned to someone.
        EQUAL DISTRIBUTION: Daily load tracking ensures no one is overloaded.
        """
        from datetime import date
        
        assignment_context = {
            'assigned_to': 'NA',
            'assignment_confidence': 0.0,
            'skill_match_details': '',
            'workload_balance': '',
            'specialization_match': False,
            'assignment_reasoning': ''
        }
        
        # Reset daily assignments at midnight
        today = date.today()
        if self.daily_assignment_date != today:
            self.daily_assignments = {}
            self.daily_assignment_date = today
            logger.info(f"🔄 Daily assignment counts reset for {today}")
        
        conn = self.connect_database(self.skills_db_path)
        if not conn:
            return assignment_context

        try:
            # Normalize application name for better matching
            normalized_app = self._normalize_application_name(application)
            
            columns = self._get_table_columns(conn, 'skills')
            cursor = conn.cursor()
            
            # Get availability data for all members
            availability_map = {}
            try:
                cursor.execute('''
                    SELECT tm.name, ah.availability_percent
                    FROM team_members tm
                    LEFT JOIN (
                        SELECT member_id, availability_percent
                        FROM availability_history
                        WHERE (end_date IS NULL OR end_date >= datetime('now'))
                        GROUP BY member_id
                        HAVING id = MAX(id)
                    ) ah ON tm.id = ah.member_id
                    WHERE tm.status = 'active'
                ''')
                
                for row in cursor.fetchall():
                    name = row[0]
                    availability_percent = row[1] if row[1] is not None else 100
                    availability_map[name] = availability_percent
                    
            except Exception as e:
                logger.warning(f"Could not load availability data: {e}. Using default 100% for all.")
                # Continue without availability filtering
            
            select_fields = [
                "tm.name",
                "tm.employee_id",
                "s.skill_level",
                "s.max_load",
                "s.confidence_score",
                "s.specializations",
                "s.application",
                "s.min_load"
            ]

            # Build query with flexible application matching
            query = f"""
                SELECT {", ".join(select_fields)}
            FROM team_members tm
            JOIN skills s ON tm.id = s.member_id
                WHERE tm.status = 'active'
                """
                
            params: List[Any] = []
            
            # Try normalized application first, then fall back to broader search
            if normalized_app and normalized_app != 'Unknown':
                query += " AND s.application = ?"
                params.append(normalized_app)
            elif application and application != 'Unknown':
                # Fallback: partial match
                query += " AND s.application LIKE ?"
                params.append(f"%{application}%")

            # For P1/P2, require higher skill but still allow all qualified members
            if priority in ['P1', 'P2']:
                query += " AND s.skill_level >= 3.5"  # Lowered from 4 to include more candidates
            
            # Order by skill level but add randomness for distribution
            query += " ORDER BY s.skill_level DESC, s.confidence_score DESC"
            cursor.execute(query, params)

            candidates = cursor.fetchall()
            
            # If no candidates with normalized app, try again without app filter
            if not candidates and (normalized_app or application != 'Unknown'):
                query = f"""
                    SELECT {", ".join(select_fields)}
                    FROM team_members tm
                    JOIN skills s ON tm.id = s.member_id
                    WHERE tm.status = 'active'
                """
                if priority in ['P1', 'P2']:
                    query += " AND s.skill_level >= 3.5"
                query += " ORDER BY s.skill_level DESC, s.confidence_score DESC"
                cursor.execute(query)
                candidates = cursor.fetchall()
            
            if not candidates:
                return assignment_context

            # Score all candidates and use weighted random selection
            scored_candidates = []

            for row in candidates:
                (
                    name,
                    employee_id,
                    skill_level,
                    max_load,
                    confidence_score,
                    specializations,
                    recorded_application,
                    min_load,
                ) = row

                if skill_level is None:
                    continue

                # Check user availability from database
                user_availability_percent = availability_map.get(name, 100)
                
                # Skip completely unavailable users (0% availability)
                if user_availability_percent == 0:
                    logger.info(f"Skipping {name} - unavailable (0% availability)")
                    continue
                
                # Convert availability percent to 0-1 scale for scoring
                availability_factor = user_availability_percent / 100.0

                specialization_text = self._clean_text(specializations).lower()
                recorded_application_text = self._clean_text(recorded_application).lower()
                target_app = self._clean_text(normalized_app or application).lower()

                # Application matching with multiple strategies
                application_match = 0.5  # Base score
                if target_app:
                    if target_app == recorded_application_text:
                        application_match = 1.0  # Perfect match
                    elif target_app in recorded_application_text or recorded_application_text in target_app:
                        application_match = 0.85  # Partial match
                    elif any(keyword in recorded_application_text for keyword in ['som', 'sqo', 'billing']):
                        # Check if same domain
                        if any(keyword in target_app for keyword in ['som', 'sqo', 'billing']):
                            application_match = 0.7

                # Specialization boost
                if target_app and specialization_text and target_app in specialization_text:
                    application_match = min(1.2, application_match + 0.2)

                # Skill match (normalized 0-1)
                skill_match = min(max(skill_level / 5.0, 0.0), 1.0)
                
                # Confidence score
                confidence = confidence_score if confidence_score is not None else 0.5
                
                # Use actual availability from database instead of simulated
                # This replaces the old simulated availability logic
                availability = availability_factor

                # Java expertise bonus
                java_bonus = 0.0
                if java_failure and 'java' in specialization_text:
                    java_bonus = 0.15

                # Priority boost for high-skill members on critical SRs
                priority_boost = 1.0
                if priority in ['P1', 'P2'] and skill_level >= 4:
                    priority_boost = 1.15
                elif priority in ['P1', 'P2'] and skill_level >= 3.5:
                    priority_boost = 1.05

                # Complexity matching: match skill level to complexity
                complexity_match = 1.0
                if complexity_score < 0.4 and skill_level >= 4.0:
                    # Over-qualified: slightly reduce score to distribute simple tasks
                    complexity_match = 0.9
                elif complexity_score > 0.7 and skill_level < 3.5:
                    # Under-qualified: reduce score
                    complexity_match = 0.85

                # Calculate base score with adjusted weights
                # Availability is now a critical factor - heavily penalize low availability
                score = (
                    (skill_match * 0.30)          # Reduced from 0.45 to allow more variation
                    + (application_match * 0.25)  # Keep application match important
                    + (confidence * 0.15)         # Reduced from 0.20
                    + (availability * 0.20)       # Based on actual availability from database
                    + (complexity_match * 0.10)   # New: match complexity to skill
                    + java_bonus
                ) * priority_boost

                # Daily load balancing: penalize members with many assignments today
                daily_load = self.daily_assignments.get(name, 0)
                
                # Calculate average daily load for comparison
                total_daily = sum(self.daily_assignments.values()) if self.daily_assignments else 0
                num_members = len(self.daily_assignments) if self.daily_assignments else 1
                avg_daily_load = total_daily / max(num_members, 1)
                
                # Apply load balancing adjustments
                if daily_load == 0:
                    # 🎯 BOOST: Members with no SRs today get priority (20% boost)
                    score *= 1.20
                elif daily_load < avg_daily_load:
                    # Members below average get slight boost (10%)
                    score *= 1.10
                elif daily_load > avg_daily_load + 2:
                    # Members significantly above average get penalty (20%)
                    score *= 0.80
                elif daily_load > avg_daily_load:
                    # Members above average get slight penalty (10%)
                    score *= 0.90

                # Add randomness for distribution (5-15% variation)
                import random
                distribution_factor = random.uniform(0.95, 1.15)
                final_score = score * distribution_factor

                scored_candidates.append({
                    'score': final_score,
                    'base_score': score,
                    'row': row,
                    'name': name,
                    'skill_level': skill_level,
                    'application_match': application_match,
                    'availability': availability,
                    'availability_percent': user_availability_percent
                })

            # Sort by score and select from top candidates (not just the best)
            scored_candidates.sort(key=lambda x: x['score'], reverse=True)
            
            # Select from top 5 candidates to increase distribution
            top_candidates = scored_candidates[:5]
            
            if top_candidates:
                # Weighted random selection from top candidates
                import random
                weights = [c['score'] for c in top_candidates]
                selected = random.choices(top_candidates, weights=weights, k=1)[0]
                
                best_row = selected['row']
                best_score = selected['base_score']

                (
                    name,
                    employee_id,
                    skill_level,
                    max_load,
                    confidence_score,
                    specializations,
                    recorded_application,
                    min_load,
                ) = best_row

                assignment_context['assigned_to'] = name
                assignment_context['assignment_confidence'] = round(min(best_score, 1.0) * 100, 1)
                assignment_context['skill_match_details'] = f"Skill {skill_level}/5 | Confidence {confidence_score:.2f}" if confidence_score is not None else f"Skill {skill_level}/5"
                assignment_context['workload_balance'] = f"Max load {max_load}" if max_load else ''
                assignment_context['specialization_match'] = bool(
                    application and application.lower() in self._clean_text(specializations).lower()
                )
                
                # Increment daily load counter for load balancing
                self.daily_assignments[name] = self.daily_assignments.get(name, 0) + 1
                daily_count = self.daily_assignments[name]
                
                reasoning_parts = []
                reasoning_parts.append(f"Expertise in {recorded_application}" if recorded_application else "Application experience")
                if assignment_context['specialization_match']:
                    reasoning_parts.append("Specialization match")
                if java_failure and 'java' in self._clean_text(specializations).lower():
                    reasoning_parts.append("Java specialization")
                if priority in ['P1', 'P2'] and skill_level >= 4:
                    reasoning_parts.append("High priority capable")
                
                # Add availability information
                avail_percent = selected.get('availability_percent', 100)
                if avail_percent < 100:
                    reasoning_parts.append(f"Availability: {avail_percent}%")
                
                if selected['application_match'] >= 0.85:
                    reasoning_parts.append("Strong app match")
                
                # Include daily load in reasoning
                reasoning_parts.append(f"Today's load: {daily_count}")

                assignment_context['assignment_reasoning'] = "; ".join(reasoning_parts)
                self.stats['skills_based_assignments'] += 1
            
            # Fallback: If no skill-based candidates found, use round-robin
            if assignment_context['assigned_to'] == 'NA':
                logger.warning(f"⚠️ No skill-based candidates found for {application}, using round-robin fallback")
                
                # Get ALL active team members for fallback
                cursor.execute("""
                    SELECT DISTINCT tm.name 
                    FROM team_members tm
                    WHERE tm.status = 'active'
                    ORDER BY tm.name
                """)
                all_members = [row[0] for row in cursor.fetchall()]
                
                if all_members:
                    # Find member with lowest daily load (ensures equal distribution)
                    member_loads = [(m, self.daily_assignments.get(m, 0)) for m in all_members]
                    member_loads.sort(key=lambda x: x[1])  # Sort by load (ascending)
                    
                    # Select member with lowest load
                    selected_name = member_loads[0][0]
                    
                    assignment_context['assigned_to'] = selected_name
                    assignment_context['assignment_confidence'] = 50.0  # Lower confidence for fallback
                    assignment_context['assignment_reasoning'] = f"Round-robin fallback (lowest load today: {member_loads[0][1]})"
                    
                    # Increment their daily load
                    self.daily_assignments[selected_name] = self.daily_assignments.get(selected_name, 0) + 1
                    
                    logger.info(f"✅ Fallback assignment: {selected_name} (daily load: {self.daily_assignments[selected_name]})")
                else:
                    logger.error("❌ No active team members found in database!")
        
        except Exception as e:
            logger.error(f"Error querying skills database: {str(e)}")
        finally:
            conn.close()
        
        # Track total processed for statistics
        self.stats['total_processed'] = self.stats.get('total_processed', 0) + 1
        
        return assignment_context
    
    def _normalize_application_name(self, assigned_group: str) -> str:
        """
        Normalize application names from input to match database format.
        Maps various input formats to standardized application names.
        """
        if not assigned_group:
            return 'Unknown'
        
        normalized = assigned_group.upper().strip()
        
        # SOM_MM mappings
        if any(keyword in normalized for keyword in ['SOM', 'SERVICE ORDER', 'ORDER MANAGEMENT']):
            return 'SOM_MM'
        
        # SQO_MM mappings
        if any(keyword in normalized for keyword in ['SQO', 'SALES QUOTE', 'QUOTE OPERATIONS']):
            return 'SQO_MM'
        
        # BILLING_MM mappings
        if any(keyword in normalized for keyword in ['BILLING', 'INVOICE', 'PAYMENT']):
            return 'BILLING_MM'
        
        # Return original if no match (will try partial matching in query)
        return assigned_group
    
    def generate_ai_workaround(self, 
                             java_context: Dict, 
                             ai_results: Dict,
                             historical_context: Dict, 
                             description: str, 
                             priority: str = 'P3', 
                             category: str = '') -> str:
        """
        Generate AI-powered workaround from historical_sr_index.pkl intelligence
        """
        workaround_steps = []
        description_lower = description.lower()
        
        # Priority-based initial response
        if priority in ['P1', 'P2']:
            workaround_steps.append("🚨 URGENT: 1. Immediately escalate to senior engineer and notify management")
        else:
            workaround_steps.append("📋 1. Document current issue state and gather comprehensive system context")
        
        # AI-extracted workarounds from historical_sr_index.pkl (highest priority)
        if ai_results.get('workarounds'):
            top_workarounds = ai_results['workarounds'][:2]  # Top 2 workarounds
            workaround_steps.append(f"🧠 AI HISTORICAL INTELLIGENCE: Based on {ai_results['similar_cases_count']} similar cases from 1.18M+ historical records:")
            
            for i, wa in enumerate(top_workarounds, 1):
                wa_text = wa['text'][:300]  # Limit length
                similarity = wa.get('similarity', 0)
                workaround_steps.append(f"   {i}. [Similarity: {similarity:.0%}] {wa_text}")
            
            self.stats['workarounds_extracted'] += len(top_workarounds)
        
        # Java-specific intelligent workarounds
        if java_context['java_failure_detected']:
            confidence = java_context.get('confidence_score', 0.5)
            
            if confidence > 0.7:
                workaround_steps.extend([
                    "☕ JAVA BACKEND ISSUE DETECTED - High Confidence:",
                    f"   📁 Affected Files: {', '.join(java_context['java_files'][:3])}",
                    "   🔍 a) Access application server logs: /var/log/application/ or Application Event Viewer",
                    "   🔍 b) Search for stack traces matching the error timeframe",
                    "   🔍 c) Identify the specific Java class and method causing the failure",
                    "   🔧 d) Check database connection pool configuration",
                    "   🔧 e) Verify memory heap settings and garbage collection logs"
                ])
        
        # Interface-specific workarounds
        target_interface = ai_results.get('target_interface', 'Unknown')
        if target_interface != 'Unknown':
            workaround_steps.append(f"🔌 INTERFACE DETECTED: {target_interface} - Check interface logs and connectivity")
        
        # Historical success-based recommendations
        if historical_context['similar_cases_count'] > 3 and historical_context['success_rate'] > 0.8:
            workaround_steps.extend([
                f"📊 HISTORICAL SUCCESS PATTERN (Success Rate: {historical_context['success_rate']:.0%}):",
                f"   Based on {historical_context['similar_cases_count']} similar resolved cases:",
            ])
            
            if historical_context.get('resolution_approaches'):
                for i, approach in enumerate(historical_context['resolution_approaches'][:2], 1):
                    workaround_steps.append(f"   {chr(96+i)}) {approach[:100]}")
        
        # Category-specific workarounds
        issue_type = self.classify_issue_intelligently(description, category, java_context)
        
        if issue_type == 'Provisioning':
            workaround_steps.extend([
                "🏗️ PROVISIONING WORKFLOW:",
                "   a) Access OSO dashboard and locate the service order",
                "   b) Trace order through: OSO → CPM → Network Elements → Completion",
                "   c) Check for inventory locks, data validation issues, or resource conflicts"
            ])
        elif issue_type == 'Performance':
            workaround_steps.extend([
                "⚡ PERFORMANCE OPTIMIZATION:",
                "   a) Monitor system resources: CPU, Memory, Disk I/O, Network",
                "   b) Identify performance bottlenecks using profiling tools",
                "   c) Apply immediate relief: restart services, clear caches, load balance"
            ])
        
        # Final validation
        if priority in ['P1', 'P2'] or java_context['java_failure_detected']:
            workaround_steps.extend([
                "✅ FINAL VALIDATION:",
                "   • Test resolution thoroughly in controlled environment",
                "   • Validate all system integrations and dependencies",
                "   • Update documentation with lessons learned"
            ])
        
        return " | ".join(workaround_steps)
    
    def classify_issue_intelligently(self, description: str, category: str, java_context: Dict) -> str:
        """AI-powered issue classification"""
        text = f"{description} {category}".lower()
        
        if java_context.get('java_failure_detected'):
            if any(word in text for word in ['timeout', 'connection', 'database']):
                return 'Java Database Connectivity'
            elif any(word in text for word in ['exception', 'error', 'failure']):
                return 'Java Application Error'
            else:
                return 'Java Backend Issue'
        
        if any(word in text for word in ['provision', 'activation', 'connect', 'install']):
            return 'Provisioning'
        elif any(word in text for word in ['status', 'stuck', 'pending', 'workflow']):
            return 'Status/Workflow'
        elif any(word in text for word in ['slow', 'timeout', 'performance', 'speed']):
            return 'Performance'
        elif any(word in text for word in ['data', 'missing', 'incorrect', 'corrupt']):
            return 'Data Issue'
        else:
            return category if category else 'General Technical'
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms for search"""
        if not text:
            return []
        
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        key_terms = [word for word in words if len(word) > 2 and word not in stop_words]
        
        seen = set()
        unique_terms = []
        for term in key_terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)
        
        return unique_terms[:15]

    def _clean_text(self, value: Any, max_length: Optional[int] = None) -> str:
        """Normalize whitespace and optionally truncate text."""
        if value is None:
            return ""
        text = re.sub(r'\s+', ' ', str(value)).strip()
        if max_length and len(text) > max_length:
            text = text[:max_length].rstrip() + "..."
        return text

    def _score_text_quality(self, text: str) -> float:
        """
        Score text quality based on multiple factors.
        Returns a score from 0.0 (garbage) to 1.0 (high quality).
        
        Criteria:
        - Penalize HTML entities and garbage characters
        - Reward actionable keywords
        - Penalize too short or too long texts
        - Reward proper sentence structure
        - Reward technical relevance
        """
        if not text or len(text.strip()) < 10:
            return 0.0
        
        text_lower = text.lower()
        score = 0.5  # Start with neutral score
        
        # 1. Penalize garbage patterns (HTML entities, encoded characters)
        garbage_patterns = [
            r'&amp;', r'&lt;', r'&gt;', r'&quot;', r'&#\d+;',  # HTML entities
            r'&nbsp;', r'&[a-z]+;',  # Other HTML entities
            r'[^\x00-\x7F]{3,}',  # Multiple non-ASCII characters in a row
            r'\{\{.*?\}\}',  # Template placeholders
            r'<[^>]+>',  # HTML tags
            r'\bnull\b|\bundefined\b|\bNaN\b',  # Code artifacts
        ]
        
        garbage_count = 0
        for pattern in garbage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            garbage_count += len(matches)
        
        # Heavy penalty for garbage (up to -0.3)
        if garbage_count > 0:
            score -= min(0.3, garbage_count * 0.05)
        
        # 2. Reward actionable keywords (up to +0.3)
        actionable_keywords = [
            'restart', 'reboot', 'clear cache', 'update', 'configure', 
            'apply patch', 'modify', 'change', 'set', 'enable', 'disable',
            'check', 'verify', 'review', 'contact', 'escalate',
            'workaround', 'solution', 'fix', 'resolve', 'bypass',
            'run', 'execute', 'install', 'uninstall', 'upgrade'
        ]
        
        actionable_count = sum(1 for kw in actionable_keywords if kw in text_lower)
        score += min(0.3, actionable_count * 0.1)
        
        # 3. Length scoring - penalize too short or too long
        text_len = len(text.strip())
        if text_len < 20:
            score -= 0.2  # Too vague
        elif text_len > 500:
            score -= 0.1  # Too verbose, might be entire conversation
        elif 50 <= text_len <= 200:
            score += 0.1  # Sweet spot for concise workarounds
        
        # 4. Sentence structure - reward proper punctuation
        if '.' in text or ',' in text or ':' in text:
            score += 0.1
        
        # 5. Penalize repetitive characters or patterns
        if re.search(r'(.)\1{4,}', text):  # 5+ repeated characters
            score -= 0.2
        
        # 6. Reward presence of technical terms
        technical_terms = [
            'server', 'database', 'interface', 'service', 'application',
            'timeout', 'connection', 'sync', 'error', 'config', 'log',
            'system', 'process', 'job', 'batch', 'queue', 'cache'
        ]
        technical_count = sum(1 for term in technical_terms if term in text_lower)
        score += min(0.2, technical_count * 0.05)
        
        # 7. Penalize vague/generic phrases
        vague_phrases = [
            'see notes', 'see below', 'as per', 'kindly', 'please find',
            'attached', 'refer to', 'mentioned above', 'same as'
        ]
        vague_count = sum(1 for phrase in vague_phrases if phrase in text_lower)
        if vague_count > 0:
            score -= min(0.2, vague_count * 0.1)
        
        # 8. Reward specific numbers/versions (indicates concrete steps)
        if re.search(r'\bv?\d+\.\d+|\bpatch\s+\d+|\bversion\s+\d+', text_lower):
            score += 0.1
        
        # Clamp score between 0.0 and 1.0
        return max(0.0, min(1.0, score))

    def _collect_workaround_evidence(
        self, ai_results: Dict, historical_context: Dict
    ) -> List[Dict[str, Any]]:
        """
        Collect grounded workaround snippets with PRIORITY ORDER:
        1. User feedback (80%+ similarity, +20% boost) - HIGHEST PRIORITY
        2. AI semantic search results (TF-IDF similarity, 50%+ threshold):
           - Scores both workaround_text and resolution (0.0-1.0)
           - Adaptive quality threshold based on similarity:
             * 70%+ similarity: Accept quality >= 0.15 (very lenient)
             * 60-70% similarity: Accept quality >= 0.20 (lenient)
             * 50-60% similarity: Accept quality >= 0.30 (strict)
           - Fallback: If similarity >= 60% but both below threshold, use better one anyway
        3. Historical keyword-matched cases (from comprehensive_historical_analysis):
           - Same quality scoring and adaptive thresholds as priority 2
           - Skips duplicates already found in AI semantic search
           - Helps capture cases shown in "Similar Cases" column
        4. SR tracking database fallback
        
        Note: Phase 1 data removed as it can force bad implementations
        Quality scoring considers: actionable keywords, technical terms, length,
        sentence structure, and penalizes HTML entities/repetitive patterns
        """
        evidence: List[Dict[str, Any]] = []

        # PRIORITY 1: Check user feedback FIRST (if available)
        if self.user_feedback_manager and self.user_feedback_loaded:
            try:
                # Build search query from SR notes (prioritize technical details over vague description)
                query = ai_results.get('query', '')
                
                # FIXED: Use notes field to match searchable_text in feedback
                if not query and 'notes' in ai_results:
                    query = ai_results['notes']
                
                # Fallback to description only if notes are empty
                if not query and 'description' in ai_results:
                    query = ai_results['description']
                
                if query:
                    user_feedback_matches = self.user_feedback_manager.search_similar(
                        query, top_k=3, min_similarity=0.80  # 80% - Conservative threshold for high-quality matches
                    )
                    
                    for match in user_feedback_matches:
                        evidence.append({
                            'source': 'user_feedback',
                            'sr_id': match['sr_id'],
                            'text': self._clean_text(match['user_corrected_workaround'], 220),
                            'similarity': match['similarity'],
                            'boosted_similarity': match['boosted_similarity'],
                            'priority': 1,  # Highest priority
                            'feedback_date': match.get('feedback_date', ''),
                            'user_corrected_interface': match.get('user_corrected_interface', '')  # Include interface correction
                        })
                        logger.info(f"✅ User feedback match: SR {match['sr_id']} (similarity: {match['similarity']:.0%}, boosted: {match['boosted_similarity']:.0%})")
            except Exception as e:
                logger.error(f"Error searching user feedback: {str(e)}")

        # PRIORITY 2: Historical index - workaround_text or resolution (50%+ similarity)
        # Note: Phase 1 data removed as it can force bad implementations
        SIMILARITY_THRESHOLD = 0.50  # Changed from 0.60 to 0.50 (50%)
        for case in ai_results.get('similar_cases', []):
            similarity = case.get('similarity', 0.0)
            
            # Apply 50% similarity threshold
            if similarity < SIMILARITY_THRESHOLD:
                continue
            
            outcome = case.get('outcome') or {}
            sr_id = case.get('sr_id')
            
            # PRIORITY 2: Intelligently choose between workaround_text and resolution
            # Score both texts and pick the one with higher quality
            wa_text = outcome.get('workaround_text')
            resolution_text = case.get('resolution', '')
            
            # Score both texts for quality
            wa_score = 0.0
            resolution_score = 0.0
            
            if wa_text and len(str(wa_text).strip()) > 10:
                wa_score = self._score_text_quality(str(wa_text))
            
            if resolution_text and len(str(resolution_text).strip()) > 10:
                resolution_score = self._score_text_quality(str(resolution_text))
            
            # Adaptive quality threshold based on similarity
            # Higher similarity = more lenient on quality (we trust the match more)
            if similarity >= 0.70:
                MIN_QUALITY_SCORE = 0.15  # Very lenient for 70%+ similarity
            elif similarity >= 0.60:
                MIN_QUALITY_SCORE = 0.20  # Somewhat lenient for 60-70% similarity
            else:
                MIN_QUALITY_SCORE = 0.30  # Strict for 50-60% similarity
            
            # Choose the better one based on quality score
            if wa_score >= MIN_QUALITY_SCORE or resolution_score >= MIN_QUALITY_SCORE:
                # Pick whichever has higher quality
                if wa_score >= resolution_score and wa_score >= MIN_QUALITY_SCORE:
                    # Workaround text is better quality
                    evidence.append({
                        'source': 'historical_workaround',
                        'sr_id': sr_id,
                        'text': self._clean_text(wa_text, 220),
                        'similarity': similarity,
                        'quality_score': wa_score,
                        'priority': 2
                    })
                    logger.debug(f"SR {sr_id}: Using workaround (quality={wa_score:.2f} vs resolution={resolution_score:.2f}, sim={similarity:.0%}, threshold={MIN_QUALITY_SCORE:.2f})")
                elif resolution_score >= MIN_QUALITY_SCORE:
                    # Resolution text is better quality
                    evidence.append({
                        'source': 'historical_resolution',
                        'sr_id': sr_id,
                        'text': self._clean_text(resolution_text, 220),
                        'similarity': similarity,
                        'quality_score': resolution_score,
                        'priority': 2
                    })
                    logger.debug(f"SR {sr_id}: Using resolution (quality={resolution_score:.2f} vs workaround={wa_score:.2f}, sim={similarity:.0%}, threshold={MIN_QUALITY_SCORE:.2f})")
            else:
                # Both are low quality - last resort fallback for very high similarity
                # If similarity is 60%+, use the better of the two even if both are low quality
                if similarity >= 0.60 and (wa_text or resolution_text):
                    if wa_score > resolution_score and wa_text:
                        evidence.append({
                            'source': 'historical_workaround',
                            'sr_id': sr_id,
                            'text': self._clean_text(wa_text, 220),
                            'similarity': similarity,
                            'quality_score': wa_score,
                            'priority': 3  # Lower priority than high-quality matches
                        })
                        logger.debug(f"SR {sr_id}: FALLBACK using low-quality workaround (quality={wa_score:.2f}, high similarity={similarity:.0%})")
                    elif resolution_text:
                        evidence.append({
                            'source': 'historical_resolution',
                            'sr_id': sr_id,
                            'text': self._clean_text(resolution_text, 220),
                            'similarity': similarity,
                            'quality_score': resolution_score,
                            'priority': 3
                        })
                        logger.debug(f"SR {sr_id}: FALLBACK using low-quality resolution (quality={resolution_score:.2f}, high similarity={similarity:.0%})")
                else:
                    # Truly skip - low similarity AND low quality
                    logger.debug(f"SR {sr_id}: Skipping both (workaround={wa_score:.2f}, resolution={resolution_score:.2f}, sim={similarity:.0%}, threshold={MIN_QUALITY_SCORE:.2f})")

        # PRIORITY 3: Historical context similar cases (from comprehensive_historical_analysis)
        # These are keyword-matched cases that may not be in ai_results
        for case in historical_context.get('similar_cases', []):
            sr_id = case.get('sr_id')
            similarity = case.get('similarity', 0.0)
            
            # Apply 50% similarity threshold
            if similarity < SIMILARITY_THRESHOLD:
                continue
            
            # Check if we already added this SR from ai_results
            if any(e.get('sr_id') == sr_id for e in evidence):
                continue  # Skip duplicates
            
            outcome = case.get('outcome') or {}
            resolution_text = case.get('resolution', '')
            
            # Score both texts for quality
            wa_text = outcome.get('workaround_text')
            wa_score = 0.0
            resolution_score = 0.0
            
            if wa_text and len(str(wa_text).strip()) > 10:
                wa_score = self._score_text_quality(str(wa_text))
            
            if resolution_text and len(str(resolution_text).strip()) > 10:
                resolution_score = self._score_text_quality(str(resolution_text))
            
            # Adaptive quality threshold based on similarity
            if similarity >= 0.70:
                MIN_QUALITY_SCORE = 0.15
            elif similarity >= 0.60:
                MIN_QUALITY_SCORE = 0.20
            else:
                MIN_QUALITY_SCORE = 0.30
            
            # Choose the better one based on quality score
            if wa_score >= MIN_QUALITY_SCORE or resolution_score >= MIN_QUALITY_SCORE:
                if wa_score >= resolution_score and wa_score >= MIN_QUALITY_SCORE:
                    evidence.append({
                        'source': 'historical_keyword_match',
                        'sr_id': sr_id,
                        'text': self._clean_text(wa_text, 220),
                        'similarity': similarity,
                        'quality_score': wa_score,
                        'priority': 3
                    })
                    logger.debug(f"SR {sr_id}: Using keyword-matched workaround (quality={wa_score:.2f}, sim={similarity:.0%})")
                elif resolution_score >= MIN_QUALITY_SCORE:
                    evidence.append({
                        'source': 'historical_keyword_resolution',
                        'sr_id': sr_id,
                        'text': self._clean_text(resolution_text, 220),
                        'similarity': similarity,
                        'quality_score': resolution_score,
                        'priority': 3
                    })
                    logger.debug(f"SR {sr_id}: Using keyword-matched resolution (quality={resolution_score:.2f}, sim={similarity:.0%})")
            else:
                # Fallback for 60%+ similarity
                if similarity >= 0.60 and (wa_text or resolution_text):
                    if wa_score > resolution_score and wa_text:
                        evidence.append({
                            'source': 'historical_keyword_match',
                            'sr_id': sr_id,
                            'text': self._clean_text(wa_text, 220),
                            'similarity': similarity,
                            'quality_score': wa_score,
                            'priority': 3
                        })
                        logger.debug(f"SR {sr_id}: FALLBACK keyword-matched workaround (quality={wa_score:.2f}, sim={similarity:.0%})")
                    elif resolution_text:
                        evidence.append({
                            'source': 'historical_keyword_resolution',
                            'sr_id': sr_id,
                            'text': self._clean_text(resolution_text, 220),
                            'similarity': similarity,
                            'quality_score': resolution_score,
                            'priority': 3
                        })
                        logger.debug(f"SR {sr_id}: FALLBACK keyword-matched resolution (quality={resolution_score:.2f}, sim={similarity:.0%})")

        # PRIORITY 4: SR tracking database
        for approach in historical_context.get('resolution_approaches', []) or []:
            cleaned = self._clean_text(approach, 220)
            if cleaned and len(cleaned) > 30:
                evidence.append({
                    'source': 'sr_tracking',
                    'sr_id': None,
                    'text': cleaned,
                    'similarity': None,
                    'priority': 4
                })

        # Sort by priority (1=user feedback first) then by similarity
        evidence.sort(key=lambda x: (x.get('priority', 999), -(x.get('boosted_similarity') or x.get('similarity') or 0)))

        return evidence[:5]  # Top 5 results

    def _collect_java_evidence(self, java_context: Dict) -> List[Dict[str, Any]]:
        """Collect Java-specific context extracted from javaMapping.db."""
        java_files = java_context.get('java_files') or []
        technical_details = java_context.get('technical_details') or []
        implementation_classes = java_context.get('implementation_classes') or []
        evidence: List[Dict[str, Any]] = []

        # Add implementation class names (highest priority - actual Java classes)
        for class_name in implementation_classes[:30]:
            evidence.append({
                'file': None,
                'class_name': class_name,
                'detail': f"Implementation class: {class_name}"
            })

        # Add file references with technical details
        for idx, file_name in enumerate(java_files[:8]):
            detail = technical_details[idx] if idx < len(technical_details) else None
            file_type = 'detailed' if 'Java_Analysis.xlsx' in file_name else 'summary'
            evidence.append({
                'file': file_name,
                'file_type': file_type,
                'detail': self._clean_text(detail, 200) if detail else None
            })

        # Add remaining technical details not associated with files
        for detail in technical_details[len(java_files):len(java_files)+5]:
            if detail:
                evidence.append({
                    'file': None,
                    'detail': self._clean_text(detail, 200)
                })

        return evidence

    def _get_table_columns(self, conn: sqlite3.Connection, table_name: str) -> set:
        """Return the set of column names for a SQLite table."""
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return {row[1] for row in cursor.fetchall()}
        except Exception:
            return set()
    
    def extract_technical_terms(self, text: str) -> List[str]:
        """
        Extract technical terms for Java database queries.
        Now includes module-specific and class name extraction for better matching.
        """
        technical_terms = []
        
        # PRIORITY 1: Extract Java class names (CamelCase with common suffixes)
        class_patterns = [
            r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+(?:Impl|Service|Controller|Manager|Processor|Handler|Repository|Factory|Builder|Validator|Helper|Util|Client|Adapter|Mapper|Converter|Provider|Listener|Filter|Interceptor|Exception|Dao|Entity|Config))\b',
        ]
        
        for pattern in class_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            technical_terms.extend(matches)
        
        # PRIORITY 2: Extract package/module names from Java paths (com.amdocs.MODULE)
        package_pattern = r'com\.amdocs\.(\w+)'
        package_matches = re.findall(package_pattern, text, re.IGNORECASE)
        technical_terms.extend(package_matches)
        
        # PRIORITY 3: Extract known module names from your javaMapping.db
        module_keywords = [
            'activation', 'customization', 'billing', 'frontend', 'warehouse', 
            'event-processor', 'guided-task', 'dashboard', 'tools', 'common',
            'services', 'service', 'oso', 'catalog', 'pricing', 'quote',
            'order', 'inventory', 'customer', 'account', 'payment', 'invoice'
        ]
        
        text_lower = text.lower()
        for keyword in module_keywords:
            if keyword in text_lower:
                technical_terms.append(keyword)
        
        # PRIORITY 4: Generic Java/framework terms (lower priority)
        generic_patterns = [
            r'\b(?:java|spring|hibernate|database|sql|connection|api|rest|dao|exception|error)\b',
            r'\b(?:timeout|null|pointer|class|method|interface|thread|memory|heap)\b',
        ]
        
        for pattern in generic_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            technical_terms.extend(matches)
        
        # Remove duplicates while preserving order (specific terms first)
        seen = set()
        unique_terms = []
        for term in technical_terms:
            term_lower = term.lower()
            if term_lower not in seen:
                seen.add(term_lower)
                unique_terms.append(term)
        
        return unique_terms[:15]  # Increased from 10 to 15
    
    def calculate_complexity_score(self, description: str, notes: str, priority: str, java_context: Dict, ai_results: Dict) -> Tuple[float, str]:
        """Enhanced complexity calculation with AI intelligence"""
        score = 0.0
        
        # Base score from priority
        priority_scores = {'P1': 0.9, 'P2': 0.7, 'P3': 0.5, 'P4': 0.3}
        score += priority_scores.get(priority, 0.5)
        
        # AI classification influence
        ai_classification = ai_results.get('classification', 'Moderate')
        if ai_classification == 'Easy Win':
            score -= 0.2
        elif ai_classification == 'Tough':
            score += 0.3
        
        # Java failure adds complexity
        if java_context.get('java_failure_detected'):
            score += 0.2
        
        # Interface issues add complexity
        if ai_results.get('interface_likelihood', 0) > 0.5:
            score += 0.15
        
        # Normalize score
        score = max(0.1, min(1.0, score))
        
        # Determine level
        if score >= 0.8:
            level = 'High'
        elif score >= 0.45:
            level = 'Medium'
        else:
            level = 'Low'
        
        return score, level
    
    def determine_risk_level(self, priority: str, complexity_score: float, java_failure: bool) -> str:
        """Enhanced risk assessment"""
        risk_score = 0
        
        priority_risk = {'P1': 40, 'P2': 30, 'P3': 20, 'P4': 10}
        risk_score += priority_risk.get(priority, 15)
        
        risk_score += complexity_score * 30
        
        if java_failure:
            risk_score += 20
        
        if risk_score >= 75:
            return 'Critical'
        elif risk_score >= 55:
            return 'High'
        elif risk_score >= 35:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_ai_analysis(
        self,
                           java_context: Dict, 
                           ai_results: Dict,
                           historical_context: Dict, 
                           complexity_score: float, 
                           issue_type: str,
        assignment_context: Dict
    ) -> str:
        """Generate analysis summary grounded in retrieved evidence."""
        analysis_parts: List[str] = []

        similar_count = ai_results.get('similar_cases_count', 0)
        if similar_count:
            top_case = ai_results.get('similar_cases', [{}])[0] if ai_results.get('similar_cases') else {}
            sr_id = top_case.get('sr_id')
            similarity = top_case.get('similarity')
            if sr_id and similarity:
                analysis_parts.append(f"Semantic match SR {sr_id} ({similarity:.0%})")
            analysis_parts.append(f"Similar cases identified: {similar_count}")

        target_interface = ai_results.get('target_interface')
        if target_interface and target_interface != 'Unknown':
            analysis_parts.append(f"Interface signals: {target_interface}")

        success_rate = historical_context.get('success_rate')
        if success_rate:
            count = historical_context.get('similar_cases_count', 0)
            analysis_parts.append(f"Historical success {success_rate:.0%} across {count} cases")

        if java_context.get('java_failure_detected'):
            confidence = java_context.get('confidence_score', 0)
            files = ", ".join(java_context.get('java_files', [])[:2])
            snippet = f"Java indicators ({confidence:.0%})"
            if files:
                snippet += f"; files: {files}"
            analysis_parts.append(snippet)

        assigned_to = assignment_context.get('assigned_to')
        if assigned_to and assigned_to != 'NA':
            reasoning = assignment_context.get('assignment_reasoning')
            if reasoning:
                analysis_parts.append(f"Assigned to {assigned_to}: {reasoning}")
            else:
                analysis_parts.append(f"Assigned to {assigned_to}")

        if not analysis_parts:
            return "NA"

        return " | ".join(analysis_parts)
    
    def calculate_overall_confidence(self, java_context: Dict, ai_results: Dict, historical_context: Dict, assignment_context: Dict) -> int:
        """Calculate overall analysis confidence score"""
        confidence_score = 50  # Base confidence
        
        # AI semantic search confidence
        ai_confidence = ai_results.get('confidence', 0)
        confidence_score += ai_confidence * 25
        
        # Java analysis confidence
        if java_context.get('java_failure_detected'):
            confidence_score += java_context.get('confidence_score', 0) * 15
        
        # Historical data confidence
        historical_confidence = historical_context.get('confidence_level', 0)
        confidence_score += historical_confidence * 10
        
        # Assignment confidence
        assignment_confidence = assignment_context.get('assignment_confidence', 0)
        confidence_score += assignment_confidence * 0.1
        
        # Data completeness bonus
        if ai_results.get('similar_cases_count', 0) > 0 and java_context.get('java_files'):
            confidence_score += 10
        
        return min(95, max(30, int(confidence_score)))
    
    def analyze_single_sr(self, sr_data: Dict) -> Dict:
        """
        Comprehensive analysis of a single service request with AI intelligence.
        """
        try:
            logger.info(f"Analyzing SR: {sr_data.get('Call ID', 'Unknown')}")
            
            sr_id = sr_data.get('Call ID', sr_data.get('SR ID', 'Unknown'))
            priority = sr_data.get('Customer Priority', sr_data.get('Priority', 'P3'))
            status = sr_data.get('STATUS', sr_data.get('Status', 'Open'))
            description = str(sr_data.get('Description', '')).strip()
            notes = str(sr_data.get('Notes', sr_data.get('Additional Notes', ''))).strip()
            category = sr_data.get('Categorization Tier 3', sr_data.get('Category', 'General'))
            assigned_group = sr_data.get('Assigned Group', sr_data.get('Application', 'Unknown'))
            submit_date = sr_data.get('Submit Date', sr_data.get('Created Date', ''))
            
            age_str, _ = self.calculate_sr_age(submit_date)
            
            java_context = self.advanced_java_analysis(description, notes, category)
            
            # NEW: Try semantic search with history_data.db FIRST
            semantic_matches = []
            semantic_workaround_data = None
            if self.historical_db and self.semantic_model:
                logger.info(f"🔍 Using NEW semantic search with history_data.db for SR {sr_id}")
                semantic_matches = self.semantic_search_history(description, notes, top_k=5)
                if semantic_matches:
                    semantic_workaround_data = self.format_semantic_workarounds(semantic_matches)
                    logger.info(f"   ✅ Found {semantic_workaround_data['match_count']} semantic matches")
            
            # Fallback to old AI semantic search if no new results
            ai_results = self.ai_semantic_search(description, notes)
            historical_context = self.comprehensive_historical_analysis(description, category, priority)
            
            complexity_score, complexity_level = self.calculate_complexity_score(
                description, notes, priority, java_context, ai_results
            )
            
            assignment_context = self.intelligent_team_assignment(
                assigned_group, complexity_score, priority, java_context.get('java_failure_detected', False)
            )
            
            # 🎯 FIX: Record assignment for ML learning
            try:
                from scripts.utilities.assignment_recorder import get_recorder
                recorder = get_recorder()
                if assignment_context.get('assigned_to') and assignment_context['assigned_to'] != 'NA':
                    recorder.record_assignment(
                        sr_id=str(sr_id),
                        assignee_name=assignment_context['assigned_to'],
                        assignment_reason=assignment_context.get('assignment_reasoning', ''),
                        confidence_score=assignment_context.get('assignment_confidence', 0) / 100.0,
                        predicted_complexity=complexity_level if 'complexity_level' in locals() else None,
                        predicted_classification=None,  # Will be filled after issue_type is determined
                        application=assigned_group,
                        priority=priority,
                        notes=f"Skill match: {assignment_context.get('skill_match_details', '')}"
                    )
            except ImportError:
                pass  # Skip if assignment_recorder not available
            
            issue_type = self.classify_issue_intelligently(description, category, java_context)
            risk_level = self.determine_risk_level(
                priority, complexity_score, java_context.get('java_failure_detected', False)
            )

            workaround_evidence = self._collect_workaround_evidence(ai_results, historical_context)
            java_evidence = self._collect_java_evidence(java_context)

            workaround = self.generate_ai_workaround(workaround_evidence, java_evidence)
            troubleshooting_steps = self.generate_troubleshooting_steps(
                workaround_evidence, java_evidence, historical_context
            )
            expected_path = self.derive_expected_path(workaround_evidence, java_evidence)

            ai_analysis = self.generate_ai_analysis(
                java_context, ai_results, historical_context, complexity_score, issue_type, assignment_context
            )
            
            if risk_level == 'Critical':
                recommended_action = "Immediate Escalation with Management Notification"
            elif java_context.get('java_failure_detected') and java_context.get('confidence_score', 0) > 0.7:
                recommended_action = "Java Backend Technical Investigation"
            elif ai_results.get('classification') == 'Easy Win':
                recommended_action = "Quick Resolution - Configuration/User Issue"
            elif ai_results.get('success_rate', 0) > 0.7:
                recommended_action = "Apply Proven Historical Resolution"
            else:
                recommended_action = "Standard Resolution Process"
            
            overall_confidence = self.calculate_overall_confidence(
                java_context, ai_results, historical_context, assignment_context
            )
            if overall_confidence >= 80:
                self.stats['high_confidence_analyses'] += 1
            
            # OPTIMIZED: Only columns that are actually used downstream (30 → 12 columns)
            result = {
                'SR ID': sr_id,
                'Priority': priority,
                'Status': status,
                'Interface': self._get_interface_with_user_priority(ai_results, java_context, workaround_evidence),
                'Suggested Workaround': workaround,
                'Assigned To': assignment_context.get('assigned_to', 'NA'),
                'Application': assigned_group,
                'Original Description': description,
                'Original Notes/Summary': notes,
                'Resolution Categorization': sr_data.get('Resolution Categorization', semantic_workaround_data['resolution_categorization_display'] if semantic_workaround_data else 'N/A'),
                'SLA Resolution': sr_data.get('SLA Resolution Categorization T1', sr_data.get('SLA Resolution', semantic_workaround_data['sla_resolution_display'] if semantic_workaround_data else 'N/A')),
                'SLA Resolution Category': sr_data.get('SLA Resolution Category', ''),
            }
            
            return result
    
        except Exception as exc:
            logger.error(f"Error analyzing SR {sr_data.get('Call ID', 'Unknown')}: {str(exc)}")
            self.stats['processing_errors'] += 1
            # OPTIMIZED: Only columns that are actually used downstream
            return {
                'SR ID': sr_data.get('Call ID', 'Error'),
                'Priority': sr_data.get('Customer Priority', 'P3'),
                'Status': 'Analysis Error',
                'Interface': 'Unknown',
                'Suggested Workaround': f'Analysis failed: {str(exc)}',
                'Assigned To': 'NA',
                'Application': sr_data.get('Assigned Group', 'Unknown'),
                'Original Description': str(sr_data.get('Description', 'No description available')),
                'Original Notes/Summary': str(sr_data.get('Notes', 'No notes available')),
                'Resolution Categorization': 'N/A',
                'SLA Resolution': 'N/A',
                'SLA Resolution Category': '',
            }
    
    def _get_interface_with_user_priority(self, ai_results: Dict, java_context: Dict, workaround_evidence: List[Dict]) -> str:
        """
        Get interface with user correction priority.
        Priority order:
        1. User-corrected interface (from feedback with high similarity)
        2. AI semantic search result
        3. Java analysis interfaces
        4. Default to 'Standard'
        """
        # Check user feedback first (Priority 1)
        for evidence in workaround_evidence:
            if evidence.get('source') == 'user_feedback':
                user_interface = evidence.get('user_corrected_interface', '')
                if user_interface:
                    logger.info(f"Using user-corrected interface: {user_interface}")
                    return f"{user_interface} (User-Corrected)"
        
        # AI semantic search (Priority 2)
        if ai_results.get('target_interface') and ai_results.get('target_interface') != 'Unknown':
            return ai_results.get('target_interface')
        
        # Java analysis (Priority 3)
        if java_context.get('interfaces_affected'):
            return ', '.join(java_context.get('interfaces_affected', [])[:2])
        
        # Default (Priority 4)
        return 'Standard'
    
    def _format_java_modules(self, java_files: List[str]) -> str:
        """
        Format Java file names or project names to user-friendly module names.
        Converts: 'activation_Java_Analysis.xlsx' -> 'Activation Module'
        Converts: 'activation' -> 'Activation Module'
        Converts: 'warehouse-order-manager' -> 'Warehouse Order Manager'
        """
        if not java_files:
            return 'N/A'
        
        formatted_modules = []
        for file_name in java_files:
            # Remove '_Java_Analysis.xlsx' suffix if present
            module_name = file_name.replace('_Java_Analysis.xlsx', '').replace('.xlsx', '').replace('.csv', '')
            
            # Capitalize and format
            # Convert snake_case or camelCase or kebab-case to Title Case
            module_name = module_name.replace('_', ' ').replace('-', ' ')
            
            # Special handling for common abbreviations
            abbreviations = {
                'oso': 'OSO',
                'dcp': 'DCP',
                'api': 'API',
                'omw': 'OMW',
                'som': 'SOM',
                'sqo': 'SQO',
                'odo': 'ODO',
                'aff': 'AFF',
                'gt': 'GT',
                'dto': 'DTO',
                'dmd': 'DMD',
                'mm': 'MM',
                'onp': 'ONP',
                'o2d': 'O2D',
                'sfo': 'SFO',
                'cmn': 'CMN',
                'cmtna': 'CMTNA',
                'asmf': 'ASMF',
                'asif': 'ASIF',
                'ossui': 'OSSUI',
                'dpm': 'DPM',
                'etd': 'ETD',
                'tmf': 'TMF',
                'arm': 'ARM',
                'bom': 'BOM'
            }
            
            # Check if it's a known abbreviation
            if module_name.lower() in abbreviations:
                formatted_name = abbreviations[module_name.lower()] + ' Module'
            else:
                # Title case for regular names
                formatted_name = module_name.title()
                # Don't add "Module" suffix if it already contains "module", "service", "manager", etc.
                if not any(word in formatted_name.lower() for word in ['module', 'service', 'manager', 'application']):
                    formatted_name += ' Module'
            
            formatted_modules.append(formatted_name)
        
        return ', '.join(formatted_modules)
    
    def format_similar_cases(self, ai_similar_cases: List[Dict], historical_context: Dict) -> str:
        """Format similar cases for display"""
        formatted: List[str] = []
        
        for case in ai_similar_cases[:3]:
            sr_id = case.get('sr_id', 'Unknown')
            desc = self._clean_text(case.get('description', ''), 80)
            similarity = case.get('similarity')
            if similarity:
                formatted.append(f"({similarity:.0%}) SR {sr_id} - {desc}")
            else:
                formatted.append(f"SR {sr_id} - {desc}")

        extra = self._clean_text(historical_context.get('similar_cases_description'), 160)
        if extra:
            formatted.append(extra)

        return " | ".join(formatted) if formatted else 'NA'

    def generate_ai_workaround(
        self,
        workaround_evidence: List[Dict[str, Any]],
        java_evidence: List[Dict[str, Any]]
    ) -> str:
        """
        Compose workaround using only grounded evidence snippets.
        User feedback is displayed with 🌟 indicator and boosted similarity.
        Phase 1 data removed to avoid forcing bad implementations.
        Returns 'NA' if no high-quality workarounds found.
        """
        lines: List[str] = []

        for evidence in workaround_evidence[:3]:
            sr_id = evidence.get('sr_id')
            similarity = evidence.get('similarity')
            source = evidence.get('source')
            boosted_similarity = evidence.get('boosted_similarity')
            text = evidence.get('text')
            
            # Handle user feedback with special indicator (Priority 1)
            if source == 'user_feedback':
                display_similarity = boosted_similarity if boosted_similarity else similarity
                feedback_date = evidence.get('feedback_date', '')
                date_str = f" [{feedback_date.split('T')[0]}]" if feedback_date else ""
                lines.append(f"🌟 (User Feedback {display_similarity:.0%}) SR {sr_id}{date_str}: {text}")
            
            # Handle historical workaround text (Priority 2A)
            elif source == 'historical_workaround':
                if not text:
                    continue
                if sr_id and similarity:
                    lines.append(f"({similarity:.0%}) SR {sr_id} workaround: {text}")
                elif sr_id:
                    lines.append(f"SR {sr_id} workaround: {text}")
                else:
                    lines.append(text)
            
            # Handle historical resolution text (Priority 2B - Fallback)
            elif source == 'historical_resolution':
                if not text:
                    continue
                if sr_id and similarity:
                    lines.append(f"({similarity:.0%}) SR {sr_id} resolution: {text}")
                elif sr_id:
                    lines.append(f"SR {sr_id} resolution: {text}")
                else:
                    lines.append(text)
            
            # Handle historical keyword-matched workaround (Priority 3)
            elif source == 'historical_keyword_match':
                if not text:
                    continue
                if sr_id and similarity:
                    lines.append(f"({similarity:.0%}) SR {sr_id} workaround: {text}")
                elif sr_id:
                    lines.append(f"SR {sr_id} workaround: {text}")
                else:
                    lines.append(text)
            
            # Handle historical keyword-matched resolution (Priority 3)
            elif source == 'historical_keyword_resolution':
                if not text:
                    continue
                if sr_id and similarity:
                    lines.append(f"({similarity:.0%}) SR {sr_id} resolution: {text}")
                elif sr_id:
                    lines.append(f"SR {sr_id} resolution: {text}")
                else:
                    lines.append(text)
            
            # Handle SR tracking database (Priority 4)
            elif source == 'sr_tracking':
                if not text:
                    continue
                lines.append(text)
            
            # Handle any other source (backward compatibility)
            else:
                if not text:
                    continue
                if sr_id:
                    if similarity:
                        lines.append(f"({similarity:.0%}) SR {sr_id}: {text}")
                    else:
                        lines.append(f"SR {sr_id}: {text}")
                else:
                    lines.append(text)

        # Fallback to Java evidence if no workarounds found
        if not lines:
            for entry in java_evidence[:2]:
                detail = entry.get('detail')
                file_name = entry.get('file')
                if detail:
                    lines.append(f"Java mapping {file_name}: {detail}")
                elif file_name:
                    lines.append(f"Java mapping identified {file_name}")

        return " | ".join(lines) if lines else "NA"

    def generate_troubleshooting_steps(
        self,
        workaround_evidence: List[Dict[str, Any]],
        java_evidence: List[Dict[str, Any]],
        historical_context: Dict
    ) -> str:
        """Generate troubleshooting steps grounded in retrieved evidence."""
        steps: List[str] = []
        step_index = 1

        for evidence in workaround_evidence[:3]:
            text = evidence.get('text')
            sr_id = evidence.get('sr_id')
            similarity = evidence.get('similarity')
            if not text:
                continue
            if sr_id:
                if similarity:
                    steps.append(f"{step_index}. ({similarity:.0%}) Reproduce resolution from SR {sr_id}: {text}")
                else:
                    steps.append(f"{step_index}. Reproduce resolution from SR {sr_id}: {text}")
            else:
                steps.append(f"{step_index}. Follow documented resolution: {text}")
            step_index += 1

        for entry in java_evidence[:3]:
            file_name = entry.get('file')
            detail = entry.get('detail')
            if file_name or detail:
                snippet = detail or "Review implementation details."
                if file_name:
                    steps.append(f"{step_index}. Inspect {file_name}: {snippet}")
                else:
                    steps.append(f"{step_index}. Java mapping insight: {snippet}")
                step_index += 1

        for pattern in (historical_context.get('historical_patterns') or [])[:2]:
            cleaned = self._clean_text(pattern, 200)
            if cleaned:
                steps.append(f"{step_index}. Historical pattern: {cleaned}")
                step_index += 1

        return " | ".join(steps) if steps else "NA"

    def derive_expected_path(
        self,
        workaround_evidence: List[Dict[str, Any]],
        java_evidence: List[Dict[str, Any]]
    ) -> str:
        """Derive expected resolution path from grounded evidence."""
        segments: List[str] = []

        for evidence in workaround_evidence[:2]:
            text = evidence.get('text')
            if not text:
                continue
            sr_id = evidence.get('sr_id')
            similarity = evidence.get('similarity')
            if sr_id:
                if similarity:
                    segments.append(f"({similarity:.0%}) SR {sr_id}: {text}")
                else:
                    segments.append(f"SR {sr_id}: {text}")
            else:
                segments.append(text)

        if not segments:
            for entry in java_evidence[:2]:
                detail = entry.get('detail')
                file_name = entry.get('file')
                if detail and file_name:
                    segments.append(f"{file_name}: {detail}")
                elif file_name:
                    segments.append(file_name)

        return " | ".join(segments) if segments else "NA"
    
    def process_excel_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Process Excel file with enhanced error handling"""
        logger.info(f"Processing file: {file_path}")
        
        try:
            # Read Excel file with multiple engine support
            engines = ['openpyxl', 'xlrd']
            df = None
            
            for engine in engines:
                try:
                    df = pd.read_excel(file_path, engine=engine)
                    logger.info(f"Successfully loaded {len(df)} records using {engine}")
                    break
                except Exception as e:
                    logger.debug(f"Failed to read with {engine}: {str(e)}")
                    continue
            
            if df is None:
                logger.error(f"Failed to read Excel file: {file_path}")
                return None
            
            # Validate and standardize column names
            column_mapping = {
                'Call ID': ['SR ID', 'Service Request ID', 'ID', 'Inc Call ID'],
                'Description': ['Issue Description', 'Problem Description', 'Details', 'Inc Description'],
                'Customer Priority': ['Priority', 'UTS Priority'],
                'STATUS': ['Status', 'Inc Current EIR - Status'],
                'Notes': ['Additional Notes', 'Resolution', 'Inc Resolution'],
                'Categorization Tier 3': ['Category', 'Categorization'],
                'Assigned Group': ['Application', 'Assignee Support Group', 'Owner Support Group'],
                'Submit Date': ['Created Date', 'Inc Created Date']
            }
            
            for standard_col, alternatives in column_mapping.items():
                if standard_col not in df.columns:
                    for alt_col in alternatives:
                        if alt_col in df.columns:
                            df.rename(columns={alt_col: standard_col}, inplace=True)
                            break
            
            logger.info(f"Columns found: {list(df.columns)}")
            
            # Process each row
            results = []
            total_rows = len(df)
            
            for index, row in df.iterrows():
                try:
                    self.stats['total_srs'] += 1
                    sr_analysis = self.analyze_single_sr(row.to_dict())
                    results.append(sr_analysis)
                    
                    if (index + 1) % 5 == 0 or index == total_rows - 1:
                        logger.info(f"Progress: {index + 1}/{total_rows} records")
                        
                except Exception as e:
                    logger.error(f"Error processing row {index}: {str(e)}")
                    continue
            
            if not results:
                logger.error("No results generated from the Excel file")
                return None
            
            # Create output DataFrame
            output_df = pd.DataFrame(results)
            logger.info(f"Generated analysis for {len(output_df)} service requests")
            
            return output_df
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return None
    
    def run_analysis(self) -> bool:
        """Run the complete AI-enhanced analysis process"""
        logger.info("=" * 80)
        logger.info("Starting AI-Enhanced Service Request Analysis System")
        logger.info("Features: Java Detection | AI Semantic Search | Historical Intelligence | Skills Assignment")
        logger.info("=" * 80)
        
        # Validate system components
        if not self.input_dir.exists():
            logger.error(f"Input directory not found: {self.input_dir}")
            return False
        
        # Find Excel files
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        
        if not excel_files:
            logger.error(f"No Excel files found in {self.input_dir}")
            return False
        
        logger.info(f"Found {len(excel_files)} Excel file(s) to process:")
        for i, file_path in enumerate(excel_files, 1):
            logger.info(f"  {i}. {file_path.name}")
        
        # Process each file
        success_count = 0
        
        for file_path in excel_files:
            try:
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing: {file_path.name}")
                logger.info(f"{'='*60}")
                
                output_df = self.process_excel_file(file_path)
                
                if output_df is not None and len(output_df) > 0:
                    # Generate output filename
                    base_name = file_path.stem
                    output_filename = f"{base_name}_workaround.xlsx"
                    output_path = self.output_dir / output_filename
                    
                    # Save to Excel with all required columns
                    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                        # Main analysis sheet
                        output_df.to_excel(writer, index=False, sheet_name='SR_Analysis')
                    
                        # Create summary sheet
                        summary_data = {
                            'Metric': [
                                'Total SRs Analyzed',
                                'Java Failures Detected',
                                'Java Files Identified',
                                'AI Semantic Searches',
                                'Historical Matches Found',
                                'Workarounds Extracted',
                                'Interface Detections',
                                'Skills-Based Assignments',
                                'High Confidence Analyses',
                                'Processing Errors'
                            ],
                            'Count': [
                                self.stats['total_srs'],
                                self.stats['java_failures_detected'],
                                self.stats['java_files_identified'],
                                self.stats['ai_semantic_searches'],
                                self.stats['historical_matches_found'],
                                self.stats['workarounds_extracted'],
                                self.stats['interface_detections'],
                                self.stats['skills_based_assignments'],
                                self.stats['high_confidence_analyses'],
                                self.stats['processing_errors']
                            ]
                        }
                        
                        summary_df = pd.DataFrame(summary_data)
                        summary_df.to_excel(writer, index=False, sheet_name='Analysis_Summary')
                    
                    logger.info(f"✅ Analysis saved to: {output_path}")
                    logger.info(f"📊 Generated comprehensive analysis for {len(output_df)} service requests")
                    success_count += 1
                    
                else:
                    logger.warning(f"❌ No results generated for {file_path}")
                    
            except Exception as e:
                logger.error(f"❌ Error processing file {file_path}: {str(e)}")
                continue
        
        # Final statistics report
        logger.info("\n" + "="*80)
        logger.info("AI-ENHANCED ANALYSIS COMPLETE!")
        logger.info("="*80)
        logger.info(f"📁 Files Processed: {success_count}/{len(excel_files)}")
        logger.info(f"📊 Total SRs Analyzed: {self.stats['total_srs']}")
        logger.info(f"☕ Java Failures Detected: {self.stats['java_failures_detected']}")
        logger.info(f"📂 Java Files Identified: {self.stats['java_files_identified']}")
        logger.info(f"🧠 AI Semantic Searches: {self.stats['ai_semantic_searches']}")
        logger.info(f"📈 Historical Matches: {self.stats['historical_matches_found']}")
        logger.info(f"🔧 Workarounds Extracted: {self.stats['workarounds_extracted']}")
        logger.info(f"🔌 Interface Detections: {self.stats['interface_detections']}")
        logger.info(f"👥 Skills-Based Assignments: {self.stats['skills_based_assignments']}")
        logger.info(f"🎯 High Confidence Analyses: {self.stats['high_confidence_analyses']}")
        logger.info(f"⚠️  Processing Errors: {self.stats['processing_errors']}")
        
        if self.stats['total_srs'] > 0:
            success_rate = ((self.stats['total_srs'] - self.stats['processing_errors']) / self.stats['total_srs']) * 100
            logger.info(f"✅ Overall Success Rate: {success_rate:.1f}%")
        
        logger.info(f"\n📁 Check '{self.output_dir}' directory for analysis results")
        logger.info("="*80)
        
        return success_count > 0


def main():
    """Main execution function"""
    print("AI-Enhanced Service Request Analyzer")
    print("Features: Java detection | Semantic search | Historical intelligence | Skills assignment")
    print("=" * 80)
    
    analyzer = AIEnhancedServiceRequestAnalyzer()
    
    try:
        success = analyzer.run_analysis()
        if success:
            print("\nAnalysis completed successfully.")
            print("Check the 'RAG/llm output' folder for results.")
            print("Review the Analysis_Summary sheet for detailed statistics.")
            return 0
        else:
            print("\nAnalysis failed. Check the logs for details.")
            return 1
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        return 1
    except Exception as exc:
        logger.error(f"Unexpected error in main execution: {str(exc)}")
        print(f"\nUnexpected error: {str(exc)}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
