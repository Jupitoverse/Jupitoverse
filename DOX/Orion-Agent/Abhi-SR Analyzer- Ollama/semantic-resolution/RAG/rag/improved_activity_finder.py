"""
Improved Activity Name Finder
Multi-method activity detection without extra LLM calls

Methods:
1. Improved Regex Patterns
2. Keyword Matching (from CamelCase split)
3. Semantic Search (comcast_code.db)
4. Historical Pattern Extraction
5. Class Index Lookup (comcast_java_classes.pkl)

Features:
- Confidence scoring (High/Medium/Low)
- Multiple evidence aggregation
- Pre-built activity index for fast lookup
"""

import re
import sqlite3
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ImprovedActivityFinder:
    """
    Improved activity name finding using 5 methods combined.
    NO extra LLM calls - pure Python processing.
    
    Usage:
        finder = ImprovedActivityFinder(vectorstore_handler, java_db_path)
        result = finder.find_activity(sr_data, historical_matches)
        
        # result = {
        #     'activity_name': 'ValidateAddress',
        #     'impl_class': 'ValidateAddressImpl',
        #     'file_path': 'customization/src/.../ValidateAddressImpl.java',
        #     'confidence': 'High',
        #     'methods_used': 'regex, keyword, semantic',
        #     'all_candidates': [...]
        # }
    """
    
    def __init__(self, vectorstore_handler, java_db_path: Path, class_index_path: Path = None):
        """
        Initialize with vectorstore handler and database paths.
        
        Args:
            vectorstore_handler: VectorstoreHandler instance for semantic search
            java_db_path: Path to javaMapping.db
            class_index_path: Path to comcast_java_classes.pkl (optional)
        """
        self.vectorstore = vectorstore_handler
        self.java_db_path = java_db_path
        self.class_index_path = class_index_path or Path("vector store/comcast_java_classes.pkl")
        
        # Pre-build indices at startup
        print("[ACTIVITY FINDER] Building activity index...")
        self.activity_index = self._build_activity_index()
        self.class_index = self._load_class_index()
        print(f"[ACTIVITY FINDER] Index built: {len(self.activity_index.get('all_activities', []))} activities")
    
    def _build_activity_index(self) -> Dict:
        """
        Build searchable activity index from javaMapping.db.
        Run ONCE at startup, not per SR.
        
        Returns:
            {
                'by_name': {"validateaddress": {class_name, activity_name, package, file_path}},
                'by_keyword': {"address": ["ValidateAddress", "UpdateAddress", ...]},
                'all_activities': ["ValidateAddress", "CreateOrder", ...],
                'name_to_impl': {"ValidateAddress": "ValidateAddressImpl"}
            }
        """
        activity_index = {
            'by_name': {},
            'by_keyword': {},
            'all_activities': [],
            'name_to_impl': {}
        }
        
        try:
            if not self.java_db_path.exists():
                logger.warning(f"javaMapping.db not found at {self.java_db_path}")
                return activity_index
            
            conn = sqlite3.connect(self.java_db_path)
            cursor = conn.cursor()
            
            # Get all classes
            cursor.execute("""
                SELECT class_name, package, full_qualified_name, file_path, class_type, annotations 
                FROM java_classes
            """)
            rows = cursor.fetchall()
            
            for row in rows:
                class_name, package, fqn, file_path, class_type, annotations = row
                
                if not class_name:
                    continue
                
                # Extract activity name (remove Impl suffix)
                if class_name.endswith('Impl'):
                    activity_name = class_name[:-4]
                elif class_name.endswith('Service'):
                    activity_name = class_name[:-7] if len(class_name) > 7 else class_name
                else:
                    activity_name = class_name
                
                # Store in by_name index (lowercase key for case-insensitive lookup)
                activity_index['by_name'][activity_name.lower()] = {
                    'class_name': class_name,
                    'activity_name': activity_name,
                    'package': package or '',
                    'file_path': file_path or '',
                    'class_type': class_type or '',
                    'fqn': fqn or ''
                }
                
                # Also store with class name as key
                activity_index['by_name'][class_name.lower()] = {
                    'class_name': class_name,
                    'activity_name': activity_name,
                    'package': package or '',
                    'file_path': file_path or '',
                    'class_type': class_type or '',
                    'fqn': fqn or ''
                }
                
                activity_index['name_to_impl'][activity_name] = class_name
                
                if activity_name not in activity_index['all_activities']:
                    activity_index['all_activities'].append(activity_name)
                
                # Build keyword index (split CamelCase)
                keywords = self._extract_keywords(activity_name)
                for keyword in keywords:
                    if keyword not in activity_index['by_keyword']:
                        activity_index['by_keyword'][keyword] = []
                    if activity_name not in activity_index['by_keyword'][keyword]:
                        activity_index['by_keyword'][keyword].append(activity_name)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to build activity index: {e}")
        
        return activity_index
    
    def _extract_keywords(self, name: str) -> List[str]:
        """
        Extract keywords from CamelCase name.
        
        Examples:
            "ValidateAddress" -> ["validate", "address"]
            "CreateOrderService" -> ["create", "order", "service"]
        """
        words = re.findall(r'[A-Z][a-z]+', name)
        return [w.lower() for w in words if len(w) > 2]
    
    def _load_class_index(self) -> Dict:
        """Load existing class index from comcast_java_classes.pkl"""
        try:
            if self.class_index_path.exists():
                with open(self.class_index_path, 'rb') as f:
                    data = pickle.load(f)
                return data.get('class_index', {})
        except Exception as e:
            logger.warning(f"Could not load class index: {e}")
        return {}
    
    def find_activity(self, sr_data: Dict, historical_matches: List[Dict]) -> Dict:
        """
        Find activity name using 5 methods combined.
        
        Args:
            sr_data: SR data with Description, Notes, Semantic Workaround
            historical_matches: List of similar historical SRs
        
        Returns:
            {
                'activity_name': str or None,
                'impl_class': str or None,
                'file_path': str or None,
                'confidence': 'High'/'Medium'/'Low',
                'methods_used': str,
                'all_candidates': list
            }
        """
        description = str(sr_data.get('Description', ''))
        notes = str(sr_data.get('Notes', ''))
        semantic = str(sr_data.get('Semantic Workaround', ''))
        text = f"{description} {notes} {semantic}"
        
        result = {
            'activity_name': None,
            'impl_class': None,
            'file_path': None,
            'confidence': 'Low',
            'methods_used': '',
            'all_candidates': []
        }
        
        candidates = []
        
        # ========== METHOD 1: Improved Regex ==========
        regex_matches = self._find_by_regex(text)
        for match in regex_matches:
            candidates.append({
                'name': match,
                'confidence': 0.9,
                'method': 'regex'
            })
        
        # ========== METHOD 2: Keyword Matching ==========
        keyword_matches = self._find_by_keywords(text)
        for match, score in keyword_matches:
            candidates.append({
                'name': match,
                'confidence': score,
                'method': 'keyword'
            })
        
        # ========== METHOD 3: Semantic Search ==========
        if self.vectorstore:
            semantic_matches = self._find_by_semantic_search(text)
            for match, score in semantic_matches:
                candidates.append({
                    'name': match,
                    'confidence': score,
                    'method': 'semantic'
                })
        
        # ========== METHOD 4: Historical Pattern ==========
        historical_found = self._find_from_historical(historical_matches)
        for match in historical_found:
            candidates.append({
                'name': match,
                'confidence': 0.7,
                'method': 'historical'
            })
        
        # ========== METHOD 5: Class Index Lookup ==========
        class_matches = self._find_by_class_index(text)
        for match in class_matches:
            candidates.append({
                'name': match,
                'confidence': 0.85,
                'method': 'class_index'
            })
        
        # ========== AGGREGATE & RANK ==========
        result['all_candidates'] = candidates
        
        if not candidates:
            return result
        
        # Score aggregation - same activity from multiple methods = higher confidence
        activity_scores = {}
        for candidate in candidates:
            name = candidate['name']
            if name not in activity_scores:
                activity_scores[name] = {'score': 0, 'methods': []}
            activity_scores[name]['score'] += candidate['confidence']
            if candidate['method'] not in activity_scores[name]['methods']:
                activity_scores[name]['methods'].append(candidate['method'])
        
        # Sort by score
        ranked = sorted(activity_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        if ranked:
            best_name, best_info = ranked[0]
            
            # Get implementation details from index
            impl_info = self.activity_index['by_name'].get(best_name.lower(), {})
            
            result['activity_name'] = best_name
            result['methods_used'] = ', '.join(best_info['methods'])
            
            if impl_info:
                result['impl_class'] = impl_info.get('class_name')
                result['file_path'] = impl_info.get('file_path')
            
            # Determine confidence level
            if best_info['score'] >= 1.5 or len(best_info['methods']) >= 2:
                result['confidence'] = 'High'
            elif best_info['score'] >= 0.7:
                result['confidence'] = 'Medium'
            else:
                result['confidence'] = 'Low'
        
        return result
    
    def _find_by_regex(self, text: str) -> List[str]:
        """
        Find activities using improved regex patterns.
        """
        matches = []
        
        patterns = [
            # Pattern 1: Explicit "Activity: Name" or "activity name: Name"
            r'[Aa]ctivity[\s:]+([A-Z][a-zA-Z]+)',
            
            # Pattern 2: CamelCase with action verbs at start
            r'\b((?:Validate|Create|Update|Delete|Process|Check|Get|Set|Add|Remove|Find|Search|Load|Save|Send|Receive|Submit|Cancel|Approve|Reject)[A-Z][a-zA-Z]+)\b',
            
            # Pattern 3: CamelCase with action verbs at end
            r'\b([A-Z][a-z]+(?:Validate|Create|Update|Delete|Process|Check)[A-Z]?[a-zA-Z]*)\b',
            
            # Pattern 4: CamelCase with domain keywords
            r'\b([A-Z][a-zA-Z]+(?:Address|Order|Customer|Account|Service|Payment|Product|Inventory|Shipment|Billing|Invoice|Quote|Contract)(?:Impl)?)\b',
            
            # Pattern 5: "SomethingImpl" pattern
            r'\b([A-Z][a-zA-Z]{3,}Impl)\b',
            
            # Pattern 6: Activity mentioned in error context
            r'(?:error in|failed at|exception in|at)\s+([A-Z][a-zA-Z]+(?:Impl|Service|Activity))',
            
            # Pattern 7: Quoted activity names
            r'["\']([A-Z][a-zA-Z]+(?:Impl|Service|Activity)?)["\']',
        ]
        
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            for match in found:
                # Normalize: remove "Impl" suffix for activity name
                if isinstance(match, tuple):
                    match = match[0]
                clean_name = match[:-4] if match.endswith('Impl') else match
                
                # Validate against known activities
                if clean_name.lower() in self.activity_index['by_name']:
                    matches.append(clean_name)
                elif match.lower() in self.activity_index['by_name']:
                    matches.append(match)
                elif clean_name and clean_name[0].isupper():
                    # Accept even if not in index (could be new activity)
                    matches.append(clean_name)
        
        return list(set(matches))
    
    def _find_by_keywords(self, text: str) -> List[Tuple[str, float]]:
        """
        Find activities by keyword matching.
        
        Example:
            "address validation failing" -> finds "ValidateAddress"
            "order creation error" -> finds "CreateOrder"
        """
        matches = []
        text_lower = text.lower()
        
        # Extract words from text
        words = set(re.findall(r'\b[a-z]{3,}\b', text_lower))
        
        # Also check for partial word matches (validation -> validate)
        word_stems = set()
        for word in words:
            word_stems.add(word)
            if word.endswith('ion'):
                word_stems.add(word[:-3] + 'e')  # validation -> validate
            if word.endswith('ing'):
                word_stems.add(word[:-3])  # creating -> creat
            if word.endswith('ed'):
                word_stems.add(word[:-2])  # created -> creat
            if word.endswith('s'):
                word_stems.add(word[:-1])  # orders -> order
        
        # Score each activity by keyword overlap
        for activity_name in self.activity_index['all_activities']:
            activity_keywords = set(self._extract_keywords(activity_name))
            
            if not activity_keywords:
                continue
            
            # Count matching keywords (including stems)
            overlap = word_stems & activity_keywords
            
            if overlap:
                score = len(overlap) / len(activity_keywords)
                if score >= 0.5:  # At least 50% keyword match
                    matches.append((activity_name, score * 0.8))  # Max 0.8 confidence
        
        # Sort by score, deduplicate
        matches.sort(key=lambda x: x[1], reverse=True)
        seen = set()
        unique = []
        for name, score in matches:
            if name not in seen:
                seen.add(name)
                unique.append((name, score))
        
        return unique[:5]
    
    def _find_by_semantic_search(self, text: str) -> List[Tuple[str, float]]:
        """
        Use comcast_code.db semantic search to find relevant activities.
        """
        matches = []
        
        try:
            # Search code vectorstore
            code_matches = self.vectorstore.search_java_code_semantically(text, top_k=10)
            
            for match in code_matches:
                file_path = match.get('metadata', {}).get('file_path', '')
                similarity = match.get('similarity', 0)
                
                # Extract class name from file path
                if '/' in file_path:
                    filename = file_path.split('/')[-1]
                    if filename.endswith('.java'):
                        class_name = filename[:-5]
                        activity_name = class_name[:-4] if class_name.endswith('Impl') else class_name
                        
                        # Only include if similarity is decent
                        if similarity >= 0.5:
                            matches.append((activity_name, similarity * 0.75))
        except Exception as e:
            logger.warning(f"Semantic search failed: {e}")
        
        # Deduplicate
        seen = set()
        unique_matches = []
        for name, score in matches:
            if name not in seen:
                seen.add(name)
                unique_matches.append((name, score))
        
        return unique_matches[:5]
    
    def _find_from_historical(self, historical_matches: List[Dict]) -> List[str]:
        """
        Find activities mentioned in similar historical SRs.
        """
        matches = []
        
        for sr in historical_matches[:3]:
            workaround = str(sr.get('workaround', ''))
            description = str(sr.get('description', ''))
            text = f"{workaround} {description}"
            
            # Use regex to find activities in historical data
            found = self._find_by_regex(text)
            matches.extend(found)
        
        return list(set(matches))
    
    def _find_by_class_index(self, text: str) -> List[str]:
        """
        Direct lookup in class_index (from comcast_java_classes.pkl).
        """
        matches = []
        
        if not self.class_index:
            return matches
        
        # Extract potential class names (CamelCase)
        class_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b'
        potential = re.findall(class_pattern, text)
        
        for class_name in potential:
            if class_name in self.class_index:
                # Found exact match in class index
                activity_name = class_name[:-4] if class_name.endswith('Impl') else class_name
                matches.append(activity_name)
        
        return list(set(matches))


# Convenience function for backward compatibility
def find_activity_improved(sr_data: Dict, historical_matches: List[Dict], 
                           vectorstore=None, java_db_path: Path = None) -> Dict:
    """
    Standalone function to find activity using improved methods.
    
    Args:
        sr_data: SR data dict
        historical_matches: List of similar SRs
        vectorstore: Optional VectorstoreHandler
        java_db_path: Optional path to javaMapping.db
    
    Returns:
        Activity result dict
    """
    if java_db_path is None:
        java_db_path = Path(__file__).parent.parent.parent / "vector store" / "javaMapping.db"
    
    finder = ImprovedActivityFinder(vectorstore, java_db_path)
    return finder.find_activity(sr_data, historical_matches)


if __name__ == "__main__":
    # Test the finder
    print("Testing ImprovedActivityFinder...")
    
    test_cases = [
        {"Description": "ValidateAddress activity is throwing NullPointerException", "Notes": ""},
        {"Description": "Customer address validation failing with null error", "Notes": ""},
        {"Description": "Order creation failed in production", "Notes": "CreateOrder"},
        {"Description": "Error in payment processing", "Notes": "PaymentServiceImpl line 45"},
    ]
    
    java_db = Path(__file__).parent.parent.parent / "vector store" / "javaMapping.db"
    
    if java_db.exists():
        finder = ImprovedActivityFinder(None, java_db)
        
        for test in test_cases:
            print(f"\nInput: {test['Description'][:50]}...")
            result = finder.find_activity(test, [])
            print(f"  Activity: {result['activity_name']}")
            print(f"  Class: {result['impl_class']}")
            print(f"  Confidence: {result['confidence']}")
            print(f"  Methods: {result['methods_used']}")
    else:
        print(f"javaMapping.db not found at {java_db}")

