"""
Historical Data Indexer for SR Semantic Search
Builds a searchable index from past SR data for predictions
"""

import pandas as pd
import os
import json
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


class HistoricalDataIndexer:
    """
    Indexes historical SR data for semantic search
    """
    
    def __init__(self, past_data_dir: str = "past_data"):
        self.past_data_dir = past_data_dir
        self.historical_data = []
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            stop_words='english',
            min_df=2
        )
        self.tfidf_matrix = None
        self.indexed_at = None
        
    def load_historical_data(self) -> int:
        """Load all historical Excel files from past_data directory"""
        print(f"Loading historical data from {self.past_data_dir}...")
        
        total_records = 0
        for filename in sorted(os.listdir(self.past_data_dir)):
            if filename.endswith(('.xls', '.xlsx')):
                file_path = os.path.join(self.past_data_dir, filename)
                print(f"   Loading {filename}...", end='')
                
                try:
                    # Read Excel file
                    df = pd.read_excel(file_path)
                    
                    # Skip if it's a header row issue
                    if len(df) > 0 and 'Inc ID' in str(df.iloc[0].values):
                        # Column names are in first row
                        df.columns = df.iloc[0]
                        df = df[1:].reset_index(drop=True)
                    
                    records_added = self._process_dataframe(df, filename)
                    total_records += records_added
                    print(f" OK - {records_added} records")
                    
                except Exception as e:
                    print(f" ERROR: {str(e)}")
                    continue
        
        print(f"\nTotal historical records loaded: {total_records}")
        return total_records
    
    def _process_dataframe(self, df: pd.DataFrame, source_file: str) -> int:
        """Process a dataframe and extract relevant SR information"""
        records_added = 0
        
        # Identify key columns - updated for past_data format
        id_col = self._find_column(df, ['Customer Call ID', 'Inc Call ID', 'Call ID', 'SR ID', 'Inc ID'])
        desc_col = self._find_column(df, ['Description*', 'Description', 'Summary', 'Inc Description'])
        notes_col = self._find_column(df, ['Notes', 'Resolution', 'Resolution*', 'Inc Resolution'])
        status_col = self._find_column(df, ['Status*', 'STATUS', 'Status', 'Inc Current EIR - Status'])
        priority_col = self._find_column(df, ['Customer Priority', 'Priority', 'UTS Priority'])
        group_col = self._find_column(df, ['Assigned Group*', 'Assigned Group', 'Assignee Support Group', 'Owner Support Group'])
        resolution_col = self._find_column(df, ['Resolution*', 'Resolution', 'Inc Resolution'])
        
        if not id_col or not desc_col:
            return 0
        
        for idx, row in df.iterrows():
            sr_id = str(row.get(id_col, ''))
            if not sr_id or sr_id == 'nan':
                continue
                
            # Build searchable text
            description = str(row.get(desc_col, ''))
            notes = str(row.get(notes_col, '')) if notes_col else ''
            resolution = str(row.get(resolution_col, '')) if resolution_col else ''
            
            searchable_text = f"{description} {notes} {resolution}".strip()
            
            if len(searchable_text) < 10:  # Skip very short entries
                continue
            
            # Determine outcome/classification
            outcome = self._determine_outcome(row, resolution, notes, status_col)
            
            # Extract metadata
            record = {
                'sr_id': sr_id,
                'description': description[:500],  # Limit length
                'searchable_text': searchable_text,
                'priority': str(row.get(priority_col, 'P3')) if priority_col else 'P3',
                'assigned_group': str(row.get(group_col, '')) if group_col else '',
                'status': str(row.get(status_col, '')) if status_col else '',
                'outcome': outcome,
                'source_file': source_file,
                'resolution': resolution[:500] if resolution else ''
            }
            
            self.historical_data.append(record)
            records_added += 1
        
        return records_added
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """Find column by trying multiple possible names"""
        for col_name in possible_names:
            if col_name in df.columns:
                return col_name
            # Case insensitive search
            for col in df.columns:
                if str(col).lower() == col_name.lower():
                    return col
        return None
    
    def _determine_outcome(self, row: pd.Series, resolution: str, notes: str, status_col: str) -> Dict[str, Any]:
        """Determine the outcome/classification of an SR based on resolution and notes"""
        outcome = {
            'classification': 'Unknown',
            'resolution_type': 'Unknown',
            'is_interface': False,
            'has_workaround': False,
            'workaround_text': None,
            'complexity': 'Medium'
        }
        
        # Combine all text for analysis - include description if available
        desc_col = self._find_column(pd.DataFrame([row]), ['Description*', 'Description'])
        description = str(row.get(desc_col, '')) if desc_col else ''
        full_text = f"{description} {resolution} {notes}".lower()
        
        # Extract actual Workaround column text if available
        workaround_col = self._find_column(pd.DataFrame([row]), ['Workaround', 'WA', 'Workaround Applied'])
        if workaround_col and pd.notna(row.get(workaround_col)):
            wa_text = str(row.get(workaround_col, '')).strip()
            if wa_text and len(wa_text) > 10 and wa_text.lower() not in ['nan', 'n/a', 'none', 'no', 'no wa']:
                outcome['has_workaround'] = True
                outcome['workaround_text'] = wa_text
                if outcome['resolution_type'] == 'Unknown':
                    outcome['resolution_type'] = 'Workaround Applied'
        
        # Check for interface issues (expanded keywords)
        interface_keywords = ['interface', 'integration', 'api', 'timeout', 'connection', 'sync', 
                            'handshake', 'web service', 'endpoint', 'communication', 'between']
        if any(keyword in full_text for keyword in interface_keywords):
            outcome['is_interface'] = True
            outcome['classification'] = 'Tough'
            outcome['complexity'] = 'High'
            outcome['resolution_type'] = 'Interface Issue'
        
        # Check for workarounds in text if not found in column
        if not outcome['has_workaround']:
            wa_keywords = ['workaround', 'wa applied', 'temporary fix', 'bypass', 'alternative', 'interim']
            if any(keyword in full_text for keyword in wa_keywords):
                outcome['has_workaround'] = True
                # Try to extract workaround text from resolution or notes
                if 'workaround' in resolution.lower():
                    idx = resolution.lower().find('workaround')
                    outcome['workaround_text'] = resolution[max(0, idx-20):idx+200].strip()
                elif 'workaround' in notes.lower():
                    idx = notes.lower().find('workaround')
                    outcome['workaround_text'] = notes[max(0, idx-20):idx+200].strip()
                
                if outcome['resolution_type'] == 'Unknown':
                    outcome['resolution_type'] = 'Workaround Applied'
        
        # Check for easy wins
        easy_keywords = ['user error', 'training', 'configuration', 'permission', 'cache', 'restart',
                        'password', 'access', 'settings', 'preference']
        if any(keyword in full_text for keyword in easy_keywords):
            outcome['classification'] = 'Easy Win'
            outcome['complexity'] = 'Low'
            if outcome['resolution_type'] == 'Unknown':
                outcome['resolution_type'] = 'Configuration/User Issue'
        
        # Check for Amdocs issues
        amdocs_keywords = ['amdocs', 'product issue', 'bug', 'defect', 'patch', 'hotfix', 'code fix']
        if any(keyword in full_text for keyword in amdocs_keywords):
            outcome['classification'] = 'Tough'
            outcome['complexity'] = 'High'
            if outcome['resolution_type'] == 'Unknown':
                outcome['resolution_type'] = 'Product Defect'
        
        # Check for data issues
        data_keywords = ['data issue', 'data fix', 'database', 'query', 'sql', 'corrupt', 'missing data']
        if any(keyword in full_text for keyword in data_keywords):
            if outcome['classification'] == 'Unknown':
                outcome['classification'] = 'Moderate'
            if outcome['resolution_type'] == 'Unknown':
                outcome['resolution_type'] = 'Data Issue'
        
        # Status-based classification
        if status_col and str(row.get(status_col, '')).lower() in ['closed', 'completed', 'resolved']:
            if outcome['classification'] == 'Unknown':
                outcome['classification'] = 'Moderate'
            if outcome['resolution_type'] == 'Unknown':
                outcome['resolution_type'] = 'Standard Resolution'
        
        return outcome
    
    def build_index(self):
        """Build TF-IDF index for semantic search"""
        if not self.historical_data:
            raise ValueError("No historical data loaded. Call load_historical_data() first.")
        
        print(f"\nBuilding semantic search index...")
        
        # Extract searchable texts
        texts = [record['searchable_text'] for record in self.historical_data]
        
        # Build TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.indexed_at = datetime.now()
        
        print(f"Index built with {self.tfidf_matrix.shape[0]} documents and {self.tfidf_matrix.shape[1]} features")
    
    def search_similar(self, query: str, top_k: int = 10) -> List[Tuple[Dict, float]]:
        """Search for similar historical SRs"""
        if self.tfidf_matrix is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top K results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append((self.historical_data[idx], similarities[idx]))
        
        return results
    
    def predict_outcome(self, description: str, notes: str = "") -> Dict[str, Any]:
        """Predict outcome based on similar historical cases"""
        # Prioritize notes over vague description for better semantic matching
        query = f"{notes} {description}" if notes else description
        similar_cases = self.search_similar(query, top_k=20)
        
        # Also check for direct keyword matches
        query_lower = query.lower()
        
        # Direct interface detection
        interface_keywords = ['interface', 'integration', 'api', 'timeout', 'connection', 'sync', 
                            'handshake', 'web service', 'endpoint', 'communication', 'between']
        has_interface_keyword = any(keyword in query_lower for keyword in interface_keywords)
        
        # Direct workaround detection
        wa_keywords = ['workaround', 'wa applied', 'temporary fix', 'bypass', 'alternative', 'interim']
        has_wa_keyword = any(keyword in query_lower for keyword in wa_keywords)
        
        # Direct easy win detection
        easy_keywords = ['password', 'reset', 'access', 'permission', 'training', 'user error']
        has_easy_keyword = any(keyword in query_lower for keyword in easy_keywords)
        
        if not similar_cases:
            # Use keyword-based prediction as fallback
            if has_interface_keyword:
                return {
                    'classification': 'Tough',
                    'confidence': 0.7,
                    'resolution_type': 'Interface Issue',
                    'interface_likelihood': 0.9,
                    'workaround_likelihood': 0.3,
                    'complexity': 'High',
                    'similar_cases': []
                }
            elif has_easy_keyword:
                return {
                    'classification': 'Easy Win',
                    'confidence': 0.7,
                    'resolution_type': 'Configuration/User Issue',
                    'interface_likelihood': 0.0,
                    'workaround_likelihood': 0.0,
                    'complexity': 'Low',
                    'similar_cases': []
                }
            else:
                return {
                    'classification': 'Moderate',
                    'confidence': 0.5,
                    'resolution_type': 'Investigation Required',
                    'interface_likelihood': 0.2,
                    'workaround_likelihood': 0.2,
                    'complexity': 'Medium',
                    'similar_cases': []
                }
        
        # Aggregate outcomes from similar cases
        classifications = {}
        resolution_types = {}
        interface_count = 0
        workaround_count = 0
        complexities = {}
        
        total_weight = 0
        for case, similarity in similar_cases[:10]:  # Use top 10 for prediction
            weight = similarity
            outcome = case['outcome']
            
            # Count classifications
            clf = outcome['classification']
            classifications[clf] = classifications.get(clf, 0) + weight
            
            # Count resolution types
            res_type = outcome['resolution_type']
            resolution_types[res_type] = resolution_types.get(res_type, 0) + weight
            
            # Count interface issues
            if outcome['is_interface']:
                interface_count += weight
            
            # Count workarounds
            if outcome['has_workaround']:
                workaround_count += weight
            
            # Count complexities
            comp = outcome['complexity']
            complexities[comp] = complexities.get(comp, 0) + weight
            
            total_weight += weight
        
        # Determine predictions
        if total_weight > 0:
            # Most likely classification
            classification = max(classifications.items(), key=lambda x: x[1])[0]
            confidence = classifications[classification] / total_weight
            
            # Most likely resolution type
            resolution_type = max(resolution_types.items(), key=lambda x: x[1])[0]
            
            # Interface likelihood
            interface_likelihood = interface_count / total_weight
            
            # Workaround likelihood
            workaround_likelihood = workaround_count / total_weight
            
            # Most likely complexity
            complexity = max(complexities.items(), key=lambda x: x[1])[0]
            
            # Override with keyword detection if strong signal
            if has_interface_keyword and interface_likelihood < 0.5:
                interface_likelihood = max(0.7, interface_likelihood)
                if resolution_type == 'Unknown':
                    resolution_type = 'Interface Issue'
            
            if has_wa_keyword and workaround_likelihood < 0.5:
                workaround_likelihood = max(0.6, workaround_likelihood)
            
            if has_easy_keyword and classification != 'Easy Win':
                # Consider changing classification if confidence is low
                if confidence < 0.7:
                    classification = 'Easy Win'
                    complexity = 'Low'
                    resolution_type = 'Configuration/User Issue'
        else:
            classification = 'Unknown'
            confidence = 0.0
            resolution_type = 'Unknown'
            interface_likelihood = 0.0
            workaround_likelihood = 0.0
            complexity = 'Medium'
        
        return {
            'classification': classification,
            'confidence': confidence,
            'resolution_type': resolution_type,
            'interface_likelihood': interface_likelihood,
            'workaround_likelihood': workaround_likelihood,
            'complexity': complexity,
            'similar_cases': [
                {
                    'sr_id': case['sr_id'],
                    'description': case['description'],
                    'outcome': case['outcome'],
                    'similarity': float(similarity),
                    'phase1_workaround': case.get('phase1_workaround', {})  # Include Phase 1 data
                }
                for case, similarity in similar_cases[:5]
            ]
        }
    
    def save_index(self, filepath: str = "historical_sr_index.pkl"):
        """Save the index to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'historical_data': self.historical_data,
                'vectorizer': self.vectorizer,
                'tfidf_matrix': self.tfidf_matrix,
                'indexed_at': self.indexed_at
            }, f)
        print(f"Index saved to {filepath}")
    
    def load_index(self, filepath: str = "historical_sr_index.pkl"):
        """Load index from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.historical_data = data['historical_data']
            self.vectorizer = data['vectorizer']
            self.tfidf_matrix = data['tfidf_matrix']
            self.indexed_at = data['indexed_at']
        print(f"Index loaded from {filepath}")


def build_historical_index():
    """Build and save the historical index"""
    indexer = HistoricalDataIndexer()
    
    # Load all historical data
    indexer.load_historical_data()
    
    # Build search index
    indexer.build_index()
    
    # Save to disk
    indexer.save_index()
    
    # Test with a sample query
    print("\nTesting with sample query...")
    test_result = indexer.predict_outcome(
        "User unable to create order due to timeout error",
        "Investigated and found interface issue with billing system"
    )
    
    print(f"\nPrediction Results:")
    print(f"  Classification: {test_result['classification']} (confidence: {test_result['confidence']:.2%})")
    print(f"  Resolution Type: {test_result['resolution_type']}")
    print(f"  Interface Issue Likelihood: {test_result['interface_likelihood']:.2%}")
    print(f"  Workaround Likelihood: {test_result['workaround_likelihood']:.2%}")
    print(f"  Complexity: {test_result['complexity']}")
    print(f"  Similar Cases Found: {len(test_result['similar_cases'])}")
    
    return indexer


if __name__ == "__main__":
    build_historical_index()
