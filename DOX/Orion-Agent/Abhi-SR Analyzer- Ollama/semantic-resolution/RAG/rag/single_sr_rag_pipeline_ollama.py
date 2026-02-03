"""
Single SR Analysis RAG Pipeline with Ollama
Intelligent Service Request Analysis using Local LLM via Ollama - Single SR Input

Context Sources:
1. javaMapping.db - Java class metadata
2. comcast_code.db (FAISS) - Backend code semantic search  
3. clean_history_data.db - Historical SR semantic search (preprocessed)
4. User Input - Manual SR details
"""

import os
import sys
import json
import sqlite3
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# Import workaround-based Java analyzer
from workaround_java_analyzer import WorkaroundJavaAnalyzer

# Import feedback storage system
try:
    from feedback_storage import WorkaroundFeedbackStorage
    FEEDBACK_STORAGE_AVAILABLE = True
except ImportError:
    FEEDBACK_STORAGE_AVAILABLE = False
    print("[WARN] WorkaroundFeedbackStorage not available")

# Import resolution mapping retriever
try:
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from resolution_mapping_retriever import ResolutionMappingRetriever
    RESOLUTION_MAPPING_AVAILABLE = True
except ImportError:
    RESOLUTION_MAPPING_AVAILABLE = False
    print("[WARN] ResolutionMappingRetriever not available")

# Import activity finder
try:
    from activity_name_finder import find_activity
    ACTIVITY_FINDER_AVAILABLE = True
except ImportError:
    ACTIVITY_FINDER_AVAILABLE = False
    print("[WARN] activity_name_finder not available")

# 🆕 Import improved activity finder
try:
    from improved_activity_finder import ImprovedActivityFinder
    IMPROVED_ACTIVITY_FINDER_AVAILABLE = True
except ImportError:
    IMPROVED_ACTIVITY_FINDER_AVAILABLE = False
    print("[WARN] ImprovedActivityFinder not available - using legacy regex extraction")

# 🆕 Import SR text preprocessor
try:
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False
    print("[WARN] SRTextPreprocessor not available - semantic search will use raw text")


class OllamaAnalyzer:
    """Ollama LLM Handler - Works with any Ollama model"""
    
    def __init__(self, model_name: str = "qwen2.5-coder:14b-instruct-q8_0"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.api_url = f"{self.base_url}/api/generate"
        
    def check_ollama_running(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def list_available_models(self) -> List[str]:
        """List all available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def load_model(self) -> bool:
        """Verify Ollama and model availability"""
        print(f"[*] Checking Ollama setup...")
        
        if not self.check_ollama_running():
            print("[ERROR] Ollama is not running!")
            print("[TIP] Start Ollama: Open terminal and run 'ollama serve'")
            return False
        
        print("[OK] Ollama is running")
        
        models = self.list_available_models()
        if not models:
            print("[WARN] No models found in Ollama")
            print("[TIP] Pull a model: ollama pull deepseek-coder")
            return False
        
        print(f"[INFO] Available models: {', '.join(models)}")
        
        model_found = any(self.model_name in model for model in models)
        if not model_found:
            print(f"[WARN] Model '{self.model_name}' not found")
            print(f"[TIP] Pull it: ollama pull {self.model_name}")
            print(f"      Or use one of: {', '.join(models)}")
            return False
        
        print(f"[OK] Model '{self.model_name}' is ready")
        return True
    
    def generate_response(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.3) -> str:
        """Generate response from Ollama model"""
        try:
            formatted_prompt = f"""You are an expert SR analysis system. Analyze service requests and provide INTELLIGENT, DETAILED technical solutions based on provided context.

{prompt}

Provide your analysis in a structured format with clear sections."""

            payload = {
                "model": self.model_name,
                "prompt": formatted_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_p": 0.95
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=2400)  # 40 minutes for complex analysis (handles concurrent model loading)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '').strip()
            else:
                print(f"[WARN] Ollama API error: {response.status_code}")
                return f"Error: API returned {response.status_code}"
                
        except Exception as e:
            print(f"[ERROR] Error generating response: {e}")
            return f"Error: {str(e)}"


class VectorstoreHandler:
    """Handle all vectorstore queries - Java Code, Java Metadata, Historical SRs"""
    
    def __init__(self, java_db_path: Path, comcast_code_db_path: Path, history_db_path: Path):
        self.java_db_path = java_db_path
        self.comcast_code_db_path = comcast_code_db_path
        self.history_db_path = history_db_path
        
        print("[*] Loading Sentence Transformer model for semantic search...")
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("[OK] Model loaded")
        
        # 🆕 Initialize preprocessor
        self.preprocessor = SRTextPreprocessor() if PREPROCESSOR_AVAILABLE else None
        
        self.comcast_code_data = None
        if comcast_code_db_path.exists():
            self._load_comcast_code_db()
        
        self.history_data = None
        if history_db_path.exists():
            self._load_history_db()
    
    def _load_comcast_code_db(self):
        """Load comcast_code.db FAISS vectorstore"""
        try:
            print(f"[*] Loading comcast_code.db from {self.comcast_code_db_path}...")
            
            embeddings_path = self.comcast_code_db_path / "embeddings.npy"
            embeddings = np.load(embeddings_path)
            
            documents_path = self.comcast_code_db_path / "documents.pkl"
            with open(documents_path, 'rb') as f:
                documents = pickle.load(f)
            
            metadatas_path = self.comcast_code_db_path / "metadatas.pkl"
            with open(metadatas_path, 'rb') as f:
                metadatas = pickle.load(f)
            
            config_path = self.comcast_code_db_path / "config.json"
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.comcast_code_data = {
                'embeddings': embeddings,
                'documents': documents,
                'metadatas': metadatas,
                'config': config
            }
            
            print(f"[OK] comcast_code.db loaded")
            print(f"     Total files: {config['total_files']}")
            print(f"     Total chunks: {config['total_chunks']}")
            print(f"     Modules: {len(config['modules'])}")
            
        except Exception as e:
            print(f"[WARN] Error loading comcast_code.db: {e}")
            self.comcast_code_data = None
    
    def _load_history_db(self):
        """Load history_data.db"""
        try:
            print(f"[*] Loading history_data.db from {self.history_db_path}...")
            with open(self.history_db_path, 'rb') as f:
                self.history_data = pickle.load(f)
            
            print(f"[OK] history_data.db loaded")
            print(f"     Total records: {self.history_data.get('total_records', 0)}")
            print(f"     Model: {self.history_data.get('model_name', 'unknown')}")
            
        except Exception as e:
            print(f"[WARN] Error loading history_data.db: {e}")
            self.history_data = None
    
    def get_java_metadata_context(self) -> str:
        """Get Java class metadata from javaMapping.db"""
        try:
            conn = sqlite3.connect(self.java_db_path)
            cursor = conn.cursor()
            
            java_context = "🔧 JAVA BACKEND METADATA (javaMapping.db):\n\n"
            
            query = """
            SELECT 
                class_name,
                package,
                full_qualified_name,
                file_path,
                class_type,
                annotations,
                project
            FROM java_classes
            ORDER BY project, package, class_name
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                java_context += f"Available Java Classes ({len(rows)} total):\n\n"
                for row in rows[:50]:  # Top 50 for context efficiency
                    class_name, package, fqn, file_path, class_type, annotations, project = row
                    java_context += f"  • {class_name} ({class_type})\n"
                    java_context += f"    Package: {package}\n"
                    java_context += f"    Path: {file_path}\n"
                    if annotations:
                        java_context += f"    Annotations: {annotations}\n"
                    java_context += "\n"
                
                java_context += f"... and {len(rows) - 50} more classes\n"
            else:
                java_context += "  No Java classes found in database.\n"
            
            conn.close()
            
            java_context += "\n📌 USE THIS FOR: Quick reference of Java class names, packages, and file paths.\n"
            
            return java_context
            
        except Exception as e:
            print(f"[WARN] Error reading javaMapping.db: {e}")
            return "🔧 JAVA BACKEND METADATA: Not accessible\n"
    
    def search_java_code_semantically(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """Search comcast_code.db for similar code snippets"""
        if not self.comcast_code_data:
            print("   [WARN] comcast_code.db not loaded")
            return []
        
        try:
            print(f"   [SEARCH] Searching Java code for: '{query_text[:60]}...'")
            
            query_embedding = self.semantic_model.encode([query_text])[0]
            
            similarities = cosine_similarity(
                [query_embedding],
                self.comcast_code_data['embeddings']
            )[0]
            
            top_indices = similarities.argsort()[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                similarity = float(similarities[idx])
                if similarity < 0.50:  # 50% threshold
                    continue
                
                results.append({
                    'similarity': similarity,
                    'code': self.comcast_code_data['documents'][idx],
                    'metadata': self.comcast_code_data['metadatas'][idx],
                    'source': 'comcast_code.db'
                })
            
            print(f"   [SEARCH] Found {len(results)} code matches")
            return results
            
        except Exception as e:
            print(f"   [WARN] Error searching Java code: {e}")
            return []
    
    def search_historical_srs(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """Search clean_history_data.db for similar historical SRs"""
        if not self.history_data:
            print("   [WARN] clean_history_data.db not loaded")
            return []
        
        try:
            print(f"   [SEARCH] Searching historical SRs for: '{query_text[:60]}...'")
            
            # 🆕 PREPROCESS QUERY (if database is preprocessed)
            db_is_preprocessed = self.history_data.get('preprocessed', False)
            if db_is_preprocessed and self.preprocessor:
                original_query = query_text
                query_text = self.preprocessor.clean_for_semantic_search(query_text)
                print(f"   [PREPROCESSED] Query cleaned for matching")
            
            query_embedding = self.semantic_model.encode([query_text])[0]
            
            similarities = cosine_similarity(
                [query_embedding],
                self.history_data['embeddings']
            )[0]
            
            top_indices = similarities.argsort()[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                similarity = float(similarities[idx])
                if similarity < 0.50:  # 50% threshold
                    continue
                
                metadata = self.history_data['metadata'][idx]
                
                # Build workaround text (Description + Workaround only, no summaries)
                workaround_parts = []
                if metadata.get('workaround'):
                    workaround_parts.append(f"Workaround: {metadata['workaround']}")
                if metadata.get('ai_generated_workaround') and metadata['ai_generated_workaround'] != 'NA':
                    workaround_parts.append(f"AI Generated: {metadata['ai_generated_workaround']}")
                if metadata.get('user_corrected_workaround') and metadata['user_corrected_workaround'] != 'NA':
                    workaround_parts.append(f"User Corrected: {metadata['user_corrected_workaround']}")
                
                workaround_text = "\n\n".join(workaround_parts) if workaround_parts else "Not available"
                
                results.append({
                    'similarity': similarity,
                    'sr_id': metadata.get('call_id', 'Unknown'),
                    'workaround': workaround_text,
                    'resolution_category': metadata.get('resolution_categorization', 'Unknown'),
                    'status_reason': metadata.get('status_reason', 'Unknown'),
                    'description': metadata.get('description', '')[:200],
                    'source': 'history_data.db'
                })
            
            print(f"   [SEARCH] Found {len(results)} historical SR matches")
            return results
            
        except Exception as e:
            print(f"   [WARN] Error searching historical SRs: {e}")
            return []


class SingleSRAnalysisPipeline:
    """Single SR RAG Pipeline for SR Analysis"""
    
    def __init__(self, ollama_model: str = "qwen2.5-coder:14b-instruct-q8_0"):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "llm output"
        
        # Database paths
        self.java_db = Path(__file__).parent.parent.parent / "vector store" / "javaMapping.db"
        self.comcast_code_db = Path(__file__).parent.parent.parent / "vector store" / "comcast_code.db"
        self.history_db = Path(__file__).parent.parent.parent / "vector store" / "clean_history_data.db"
        
        self._verify_databases()
        
        # Initialize components
        self.analyzer = OllamaAnalyzer(ollama_model)
        self.vectorstore = VectorstoreHandler(self.java_db, self.comcast_code_db, self.history_db)
        self.workaround_analyzer = WorkaroundJavaAnalyzer()
        
        # Initialize feedback storage
        if FEEDBACK_STORAGE_AVAILABLE:
            try:
                self.feedback_storage = WorkaroundFeedbackStorage()
                print("[OK] Feedback storage loaded")
            except Exception as e:
                print(f"[WARN] Could not load feedback storage: {e}")
                self.feedback_storage = None
        else:
            self.feedback_storage = None
        
        # Initialize resolution mapping retriever
        if RESOLUTION_MAPPING_AVAILABLE:
            try:
                self.resolution_retriever = ResolutionMappingRetriever()
                print("[OK] Resolution mapping retriever loaded")
            except Exception as e:
                print(f"[WARN] Could not load resolution mapping: {e}")
                self.resolution_retriever = None
        else:
            self.resolution_retriever = None
        
        # 🆕 Initialize improved activity finder
        self.improved_activity_finder = None
        if IMPROVED_ACTIVITY_FINDER_AVAILABLE:
            try:
                self.improved_activity_finder = ImprovedActivityFinder(
                    self.vectorstore,
                    self.java_db
                )
                print("[OK] Improved activity finder loaded")
            except Exception as e:
                print(f"[WARN] Could not load improved activity finder: {e}")
                self.improved_activity_finder = None
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _verify_databases(self):
        """Verify all databases exist"""
        if not self.java_db.exists():
            print(f"[WARN] javaMapping.db not found at: {self.java_db}")
        else:
            print(f"[OK] javaMapping.db found")
        
        if not self.comcast_code_db.exists():
            print(f"[WARN] comcast_code.db not found at: {self.comcast_code_db}")
        else:
            print(f"[OK] comcast_code.db found")
        
        if not self.history_db.exists():
            print(f"[WARN] history_data.db not found at: {self.history_db}")
        else:
            print(f"[OK] history_data.db found")
    
    def get_user_input(self) -> Optional[Dict]:
        """Get SR details from user input"""
        print("\n" + "="*80)
        print("SINGLE SR INPUT")
        print("="*80)
        print("Please enter the following details for your Service Request:\n")
        
        try:
            sr_id = input("SR ID (e.g., CAS123456): ").strip()
            if not sr_id:
                print("[ERROR] SR ID is required!")
                return None
            
            priority = input("Priority (High/Medium/Low) [Medium]: ").strip() or "Medium"
            
            resolution_category = input("Resolution Category (Code/Data/Interface/Configuration/etc.) [Unknown]: ").strip() or "Unknown"
            
            status_reason = input("Status Reason (Automation/Customer Approved/etc.) [Unknown]: ").strip() or "Unknown"
            
            print("\nDescription (press Enter twice when done):")
            description_lines = []
            while True:
                line = input()
                if line == "":
                    if description_lines and description_lines[-1] == "":
                        break
                    description_lines.append(line)
                else:
                    description_lines.append(line)
            description = "\n".join(description_lines).strip()
            
            if not description:
                print("[ERROR] Description is required!")
                return None
            
            print("\nAdditional Notes (optional, press Enter twice when done):")
            notes_lines = []
            while True:
                line = input()
                if line == "":
                    if not notes_lines or notes_lines[-1] == "":
                        break
                    notes_lines.append(line)
                else:
                    notes_lines.append(line)
            notes = "\n".join(notes_lines).strip()
            
            sr_data = {
                'SR ID': sr_id,
                'Priority': priority,
                'Resolution Category': resolution_category,
                'Status Reason': status_reason,
                'Description': description,
                'Notes': notes or description
            }
            
            print("\n" + "="*80)
            print("SR INPUT SUMMARY")
            print("="*80)
            print(f"SR ID: {sr_id}")
            print(f"Priority: {priority}")
            print(f"Resolution Category: {resolution_category}")
            print(f"Status Reason: {status_reason}")
            print(f"Description: {description[:100]}{'...' if len(description) > 100 else ''}")
            print("="*80)
            
            confirm = input("\nProceed with analysis? (y/n) [y]: ").strip().lower()
            if confirm and confirm != 'y':
                print("[CANCELLED] Analysis cancelled by user")
                return None
            
            return sr_data
            
        except KeyboardInterrupt:
            print("\n[CANCELLED] Input cancelled by user")
            return None
        except Exception as e:
            print(f"[ERROR] Error getting user input: {e}")
            return None
    
    def analyze_single_sr(self, sr_data: Dict, java_metadata_context: str = None) -> Dict:
        """Analyze a single service request using LLM with optimized context"""
        
        sr_id = sr_data.get('SR ID', sr_data.get('Call ID', 'Unknown'))
        priority = sr_data.get('Priority', 'Medium')
        description = str(sr_data.get('Description', ''))
        notes = str(sr_data.get('Notes', ''))
        resolution_category = str(sr_data.get('Resolution Category', sr_data.get('Resolution Categorization', 'Unknown')))
        status_reason = str(sr_data.get('Status Reason', 'Unknown'))
        
        print(f"\n[*] Analyzing SR: {sr_id} (Priority: {priority})")
        print(f"    Resolution Category: {resolution_category}")
        print(f"    Status Reason: {status_reason}")
        
        # Step 1: Check for semantic workaround in input
        semantic_workaround_input = str(sr_data.get('Semantic Workaround', ''))
        has_input_semantic = (
            semantic_workaround_input and
            semantic_workaround_input.lower() not in ['not available', 'nan', 'none', '']
        )
        
        # Step 2: Search vectorstores
        query_text = f"{description} {notes}".strip()
        
        # Search historical SRs (only if no input semantic workaround)
        historical_matches = []
        if not has_input_semantic:
            print("   [RAG] No input semantic workaround - searching historical SRs...")
            historical_matches = self.vectorstore.search_historical_srs(query_text, top_k=5)
        else:
            print("   [RAG] Using input semantic workaround")
        
        # Extract semantic workaround from historical matches if not provided in input
        if not has_input_semantic and historical_matches:
            # Get the best semantic workaround from top match
            top_match = historical_matches[0]
            semantic_workaround_input = top_match.get('workaround', '')
            if semantic_workaround_input and len(semantic_workaround_input) > 20:
                print(f"   [RAG] Using semantic workaround from top match (SR {top_match.get('sr_id', 'Unknown')}, {top_match.get('similarity', 0):.1%} similarity)")
            else:
                semantic_workaround_input = ''
        
        # Load Java metadata context if not provided
        if java_metadata_context is None:
            print("   [DB] Loading Java metadata context...")
            java_metadata_context = self.vectorstore.get_java_metadata_context()
        
        # Note: Java code search will happen AFTER activity detection (Step 3.5)
        
        # Step 2.5: Query resolution_mapping.db with similar SR categories
        resolution_mapping_context = ""
        if self.resolution_retriever and historical_matches:
            print("   [MAPPING] Querying resolution_mapping.db...")
            
            # Collect all categories from similar SRs
            categories_to_query = []
            for match in historical_matches:
                cat = match.get('resolution_category', '')
                if cat and cat.lower() not in ['unknown', 'nan', 'none', '']:
                    categories_to_query.append(cat)
            
            # Add current SR category
            if resolution_category.lower() not in ['unknown', 'nan', 'none', '']:
                categories_to_query.append(resolution_category)
            
            # Query resolution mapping
            if categories_to_query:
                # Search with combined query
                query_text = " ".join(set(categories_to_query))
                try:
                    mapping_results = self.resolution_retriever.search(query_text, top_k=3)
                    
                    if mapping_results:
                        resolution_mapping_context = "📚 **RESOLUTION MAPPING GUIDELINES** (resolution_mapping.db):\n\n"
                        for idx, result in enumerate(mapping_results, 1):
                            data = result['data']
                            resolution_mapping_context += f"Match #{idx} (Similarity: {result['similarity']:.0%}):\n"
                            resolution_mapping_context += f"  Categories: {data.get('Resolution Categorization T2', 'N/A')} / {data.get('Resolution Category Tier 3', 'N/A')}\n"
                            resolution_mapping_context += f"  Total Occurrences: {data.get('Total Occurrences', 'N/A')}\n"
                            resolution_mapping_context += f"  Most Common Workaround: {data.get('Most Common Workaround', 'N/A')}\n"
                            resolution_mapping_context += f"  Workaround Guideline: {data.get('Workaround Guideline', 'N/A')}\n"
                            resolution_mapping_context += f"  Suggested Workaround: {data.get('Suggested Workaround', 'N/A')}\n\n"
                        
                        resolution_mapping_context += "⚠️ **USE FOR INSPIRATION ONLY - Generate your own detailed steps!**\n\n"
                        print(f"   [MAPPING] Found {len(mapping_results)} matching guidelines")
                    else:
                        print("   [MAPPING] No matching guidelines found")
                except Exception as e:
                    print(f"   [WARN] Error querying resolution mapping: {e}")
            else:
                print("   [MAPPING] No valid categories to query")
        else:
            print("   [MAPPING] Resolution mapping not available")
        
        # Step 3: Workaround-Based Java Error Detection
        print("   [DETECT] Running workaround-based Java error detection...")
        try:
            detection_result = self.workaround_analyzer.analyze(
                sr_data={
                    'Description': description,
                    'Notes': notes,
                    'Resolution Category': resolution_category,
                    'Status Reason': status_reason,
                    'Semantic Workaround': semantic_workaround_input
                },
                similar_srs=historical_matches
            )
            
            print(f"   [DETECT] Java Error: {'YES' if detection_result['is_java_error'] else 'NO'}")
            print(f"   [DETECT] Confidence: {detection_result['confidence']}")
            print(f"   [DETECT] Votes: Java={detection_result['java_votes']}, Non-Java={detection_result['non_java_votes']}, Unknown={detection_result['unknown_votes']}")
            print(f"   [DETECT] Issue Type: {detection_result['issue_type']}")
            
            # Print evidence for debugging
            print(f"   [DETECT] Evidence ({len(detection_result['evidence'])} items):")
            if detection_result['evidence']:
                for evidence in detection_result['evidence'][:10]:  # Show first 10
                    print(f"            {evidence}")
            else:
                print(f"            ⚠ No evidence collected")
            
            # Step 3.5: If Java error, find activity and search specific Java code
            java_file = "N/A"
            java_path = "N/A"
            activity_info = {}
            activity_result = {}  # 🆕 Store improved finder result
            java_code_matches = []
            
            if detection_result['is_java_error']:
                # 🆕 Use IMPROVED activity finder (5 methods combined)
                if self.improved_activity_finder:
                    print("   [ACTIVITY] Using IMPROVED activity finder (5 methods)...")
                    activity_result = self.improved_activity_finder.find_activity(
                        sr_data={'Description': description, 'Notes': notes, 'Semantic Workaround': semantic_workaround_input},
                        historical_matches=historical_matches
                    )
                    
                    print(f"   [ACTIVITY] Result: {activity_result['activity_name'] or 'None'}")
                    print(f"   [ACTIVITY] Confidence: {activity_result['confidence']}")
                    print(f"   [ACTIVITY] Methods: {activity_result['methods_used']}")
                    
                    # Use result if confidence is not Low
                    if activity_result['activity_name'] and activity_result['confidence'] in ['High', 'Medium']:
                        # Get file info from improved finder
                        java_file = activity_result.get('impl_class') or "N/A"
                        java_path = activity_result.get('file_path') or "N/A"
                        
                        # If path not found locally, try PostgreSQL lookup
                        if java_path == "N/A" and ACTIVITY_FINDER_AVAILABLE:
                            try:
                                db_result = find_activity(activity_result['activity_name'])
                                if db_result.get('success'):
                                    activity_info = db_result
                                    java_file = db_result['impl_file_name']
                                    java_path = db_result['impl_path']
                                    print(f"   [ACTIVITY] DB lookup found: {java_path}")
                            except Exception as e:
                                print(f"   [WARN] DB lookup failed: {e}")
                        
                        # Search Java code with specific class/activity name
                        search_query = activity_result.get('impl_class') or activity_result['activity_name']
                        print(f"   [RAG] Searching Java code for: {search_query}...")
                        java_code_matches = self.vectorstore.search_java_code_semantically(
                            search_query,
                            top_k=5
                        )
                        print(f"   [RAG] Found {len(java_code_matches)} code matches")
                    else:
                        print(f"   [ACTIVITY] Low confidence or not found - will use generic search")
                
                # Fallback to legacy regex extraction
                elif ACTIVITY_FINDER_AVAILABLE:
                    print("   [ACTIVITY] Fallback: Using legacy regex extraction...")
                    activity_names = self.workaround_analyzer.extract_activity_names(
                        sr_data={'Description': description, 'Notes': notes, 'Semantic Workaround': semantic_workaround_input},
                        similar_srs=historical_matches
                    )
                    
                    if activity_names:
                        print(f"   [ACTIVITY] Found potential activities: {', '.join(activity_names[:3])}")
                        for activity_name in activity_names[:3]:
                            try:
                                result = find_activity(activity_name)
                                if result.get('success'):
                                    activity_info = result
                                    java_file = result['impl_file_name']
                                    java_path = result['impl_path']
                                    class_name = result['class_name']
                                    print(f"   [ACTIVITY] Found implementation: {java_path}")
                                    
                                    java_code_matches = self.vectorstore.search_java_code_semantically(
                                        class_name,
                                        top_k=5
                                    )
                                    print(f"   [RAG] Found {len(java_code_matches)} code matches for {class_name}")
                                    break
                            except Exception as e:
                                print(f"   [WARN] Could not find activity '{activity_name}': {e}")
                    else:
                        print("   [ACTIVITY] No activity names found")
            
            # If no Java error OR activity not found, search with generic description
            if not java_code_matches:
                if detection_result['is_java_error']:
                    print("   [RAG] No activity found - searching Java code with SR description...")
                else:
                    print("   [RAG] Not a Java error - searching Java code with SR description...")
                java_code_matches = self.vectorstore.search_java_code_semantically(query_text, top_k=3)
            
            # Debug input data
            print(f"   [DEBUG] Input: desc_len={len(description)}, notes_len={len(notes)}, code_matches={len(java_code_matches)}, hist_matches={len(historical_matches)}")
            
        except Exception as e:
            print(f"   [ERROR] Detector crashed: {e}")
            import traceback
            traceback.print_exc()
            # Create default detection result
            detection_result = {
                'is_java_error': False,
                'confidence': 'UNKNOWN',
                'java_votes': 0,
                'non_java_votes': 0,
                'unknown_votes': 5,
                'votes': {},
                'evidence': [f'Detection failed: {str(e)}'],
                'issue_type': 'Unknown'
            }
            java_file = 'N/A'
            java_path = 'N/A'
            activity_info = {}
            activity_result = {}  # 🆕 Initialize for fallback
            java_code_matches = []
            
            # Fallback: search with description
            print("   [RAG] Searching Java code with SR description (fallback)...")
            java_code_matches = self.vectorstore.search_java_code_semantically(query_text, top_k=3)
        
        # Step 4: Build context sections
        java_code_context = self._build_java_code_context(java_code_matches)
        historical_context = self._build_historical_context(historical_matches, has_input_semantic, semantic_workaround_input)
        detection_evidence_context = self._build_detection_evidence_context(detection_result)
        
        # Step 5: Generate AI Analysis with CONDITIONAL PROMPT
        print("   [LLM] Generating intelligent AI analysis...")
        
        # 🔀 ROUTE BASED ON JAVA ERROR DETECTION
        if detection_result['is_java_error']:
            # ============================================================
            # CASE 1: JAVA ERROR - Full technical analysis with all contexts
            # ============================================================
            analysis_prompt = f"""You are a JAVA ERROR EXPERT. Analyze this Java error and provide a precise, technical fix.

===== SERVICE REQUEST =====
SR ID: {sr_id}
Priority: {priority}
Resolution Category: {resolution_category}
Description: {description}
Notes: {notes}

===== CONTEXT #1: JAVA BACKEND METADATA =====
{java_metadata_context[:2000]}

===== CONTEXT #2: JAVA CODE MATCHES =====
{java_code_context[:2000]}

===== CONTEXT #3: HISTORICAL SOLUTIONS =====
{historical_context[:1500]}

===== CONTEXT #4: RESOLUTION GUIDELINES =====
{resolution_mapping_context[:1000] if resolution_mapping_context else "Not available"}

===== CONTEXT #5: DETECTION RESULT =====
Confidence: {detection_result.get('confidence', 'Unknown')}
Issue Type: {detection_result.get('issue_type', 'Unknown')}
Evidence: {chr(10).join(['  ' + str(e) for e in detection_result.get('evidence', [])[:10]])}

===== CONTEXT #6: ACTIVITY IDENTIFIED =====
Activity: {activity_result.get('activity_name', 'N/A')}
Class: {activity_result.get('impl_class', 'N/A')}
Path: {activity_result.get('file_path', 'N/A')}
Confidence: {activity_result.get('confidence', 'N/A')}

===== YOUR TASK =====
1. Confirm Java error with exact evidence (quote error text from SR)
2. Identify exact Java file/class using Context #1, #2, #6
3. Generate 5-12 specific fix steps:
   - Use exact file paths from contexts
   - Include commands with expected output
   - Add code changes if needed (reference Context #2 for actual code)
   - Add verification steps
4. Use patterns from Context #3 if similar Java errors were fixed before

===== OUTPUT FORMAT =====

**JAVA ERROR ANALYSIS:**
- Is Java Error: Yes
- Confidence: [Very High/High/Medium/Low] - [Why based on evidence]
- Java File: [Exact name from contexts OR "N/A"]
- Java Path: [Exact path from contexts OR "N/A"]
- Evidence: [Quote exact error text from SR]
- Issue Type: Java

**AI WORKAROUND:**
1. [Specific technical step with exact path/command/expected result]
2. [Next step...]
[... 5-12 steps total based on complexity]

**TROUBLESHOOTING STEPS:**
1. [Investigation - where to look, what logs]
2. [Analysis - what to check in code/config]
3. [Resolution - exact fix with commands]
4. [Verification - how to confirm fix worked]
5. [Escalation - when to escalate and to whom]

Analyze now:
"""
        
        else:
            # ============================================================
            # CASE 2: NON-JAVA ERROR - ALWAYS SUMMARIZE, THEN EXTEND
            # ============================================================
            analysis_prompt = f"""You are an INTELLIGENT SR RESOLVER. This is NOT a Java error. Your task is to:
1) Summarize and adapt any known semantic/historical workaround, then
2) Extend it with additional intelligent steps using all contexts.

===== SERVICE REQUEST =====
SR ID: {sr_id}
Priority: {priority}
Resolution Category: {resolution_category}
Status Reason: {status_reason}
Description: {description}
Notes: {notes}

===== SEMANTIC WORKAROUND / HISTORICAL MATCHES =====
{historical_context[:2500]}

===== RESOLUTION GUIDELINES =====
{resolution_mapping_context[:1000] if resolution_mapping_context else "Not available"}

===== DETECTION RESULT =====
Issue Type: {detection_result.get('issue_type', 'Unknown')}
Evidence: {chr(10).join(['  ' + str(e) for e in detection_result.get('evidence', [])[:5]])}

===== YOUR TASK =====

**STEP 1 - ALWAYS SUMMARIZE THE KNOWN PATTERN**

From the semantic workaround / historical matches above, extract the BEST pattern that actually solved the issue:
- ACTIONS (what was done)
- SYSTEMS (PS, OSO, CLIPS, DB, etc.)
- DATA (IP ranges, VLANs, project IDs, task names, etc.)
- SEQUENCE (order of steps)

Then:
- Rewrite this pattern as the **first 2-5 steps** of your AI WORKAROUND.
- Adapt with THIS SR's specific data (read description/notes to find IDs, IPs, tasks, etc.).
- If the workaround text is very generic, say so briefly, but still summarize what little pattern it contains.

**STEP 2 - ADD INTELLIGENT EXTRA STEPS**

After summarizing the known pattern:
- Add further steps using:
  - Issue type from detection
  - Other historical patterns (if different SRs show useful extra checks)
  - Resolution guidelines for this category
- Include:
  - Investigation steps (where to look, what logs/queries)
  - Resolution steps (specific actions with data)
  - Verification steps (how to confirm fix)
  - Escalation criteria

===== OUTPUT FORMAT =====

**ANALYSIS:**
- Is Java Error: No
- Issue Type: {detection_result.get('issue_type', 'Unknown')}
- Confidence: [Very High/High/Medium/Low] - [Why]
- Comment on semantic workaround: [e.g. "Specific and actionable" / "Generic but indicates data cleanup" / "Too vague"]

**AI WORKAROUND:**
- Steps 1-N: **Summary/adaptation of known semantic/historical workaround pattern**
- Remaining steps: **Additional intelligent steps based on issue type, history, and guidelines**

1. [Summarized/adapted step from semantic/historical pattern]
2. [Summarized/adapted step...]
3. [Summarized/adapted step...]
4. [Extra intelligent step...]
5. [Extra intelligent step...]
[Continue up to ~8-12 total steps depending on complexity]

**TROUBLESHOOTING STEPS:**
1. [Investigation step]
2. [Analysis step]
3. [Resolution step]
4. [Verification step]
5. [Escalation criteria]

🎯 IMPORTANT:
- Always use **only** the specific values (IPs, ranges, IDs, paths) that actually appear in the SR description/notes or in the semantic/historical context.
- Any concrete examples in THIS PROMPT (like IP ranges or field names used as illustrations) are **for reference only**.
  → Do NOT copy those example values into your answer unless they ALSO appear in the SR or historical context.
- If Context #3 shows a pattern like "update ipAddressRange in PS and retry", you must:
  → Extract the pattern (update a config field in PS + retry),
  → But ONLY use the real ipAddressRange / field values found in THIS SR's data or history.

Analyze now:
"""
        
        # Send to LLM
        ai_response = self.analyzer.generate_response(analysis_prompt, max_tokens=1024, temperature=0.2)
        
        # Step 6: Parse LLM Response (using workaround-based detection results)
        print("   [Parse] Extracting analysis from LLM response...")
        
        # 🐛 DEBUG: Log raw response (first 500 chars)
        print(f"   [DEBUG] Raw LLM response (first 500 chars):\n{ai_response[:500]}")
        print(f"   [DEBUG] Response length: {len(ai_response)} characters")
        
        # Use workaround-based detection results
        is_java_error = "Yes" if detection_result['is_java_error'] else "No"
        
        # Combine for output
        if java_file != "N/A" and java_path != "N/A":
            java_failure_path = f"{java_path} (Class: {java_file})"
        elif java_path != "N/A":
            java_failure_path = java_path
        elif java_file != "N/A":
            java_failure_path = java_file
        else:
            java_failure_path = detection_result.get('issue_type', 'N/A')
        
        # 🆕 Enhanced extraction with multiple fallback methods
        ai_workaround = self._extract_ai_workaround(ai_response)
        
        # 🆕 More lenient validation (20 chars minimum instead of 50)
        if not ai_workaround or len(ai_workaround.strip()) < 20:
            print(f"   [WARN] Extracted AI workaround too short ({len(ai_workaround) if ai_workaround else 0} chars)")
            print(f"   [WARN] Using full response as fallback")
            # Use the full response as fallback
            ai_workaround = ai_response.strip() if ai_response and len(ai_response.strip()) > 20 else "[LLM Analysis Incomplete] Manual solution required."
        
        # 🆕 Clean up malformed step numbering
        ai_workaround = self._clean_step_numbering(ai_workaround)
        
        # Extract Troubleshooting Steps
        troubleshooting_steps = self._extract_section(ai_response, "TROUBLESHOOTING STEPS:", "END")
        if not troubleshooting_steps or len(troubleshooting_steps) < 50:
            troubleshooting_steps = "1. Review error logs\n2. Check service status\n3. Verify configuration\n4. Test in staging\n5. Escalate if needed"
        
        # 🆕 Clean up malformed step numbering in troubleshooting
        troubleshooting_steps = self._clean_step_numbering(troubleshooting_steps)
        
        # Build semantic workaround output
        if has_input_semantic:
            semantic_workaround_output = semantic_workaround_input
        elif historical_matches:
            semantic_workaround_output = "\n\n".join([
                f"Match #{idx} - SR {match['sr_id']} ({match['similarity']:.0%} similarity):\n"
                f"Resolution Categorization: {match['resolution_category']}\n"
                f"SLA Resolution: {match['status_reason']}\n\n"
                f"{match['workaround']}"
                for idx, match in enumerate(historical_matches, 1)
            ])
        else:
            semantic_workaround_output = "Not available"
        
        # 🆕 Get vote information for this SR's workarounds
        original_votes = {'upvotes': 0, 'downvotes': 0, 'score': 0}
        ai_votes = {'upvotes': 0, 'downvotes': 0, 'score': 0}
        user_corrected_votes = {'upvotes': 0, 'downvotes': 0, 'score': 0}
        
        if self.feedback_storage:
            try:
                original_votes = self.feedback_storage.get_votes(sr_id, 'original')
                ai_votes = self.feedback_storage.get_votes(sr_id, 'ai')
                user_corrected_votes = self.feedback_storage.get_votes(sr_id, 'user_corrected')
            except Exception as e:
                print(f"   [WARN] Could not fetch vote data: {e}")
        
        # Compile result
        result = {
            'SR ID': sr_id,
            'Priority': priority,
            'Resolution Category': resolution_category,
            'Status Reason': status_reason,
            'Java Failure Detected': is_java_error,
            'Java Failure Path': java_failure_path.strip(),
            'Match Similarity': f"{java_code_matches[0]['similarity']:.0%}" if java_code_matches else "N/A",
            'Semantic Workaround': semantic_workaround_output,
            'Semantic Workaround Upvotes': original_votes['upvotes'],
            'Semantic Workaround Downvotes': original_votes['downvotes'],
            'Semantic Workaround Score': original_votes['score'],
            'AI Workaround': ai_workaround.strip(),
            'AI Workaround Upvotes': ai_votes['upvotes'],
            'AI Workaround Downvotes': ai_votes['downvotes'],
            'AI Workaround Score': ai_votes['score'],
            'User Corrected Workaround': sr_data.get('User Corrected Workaround', 'N/A'),
            'User Corrected Upvotes': user_corrected_votes['upvotes'],
            'User Corrected Downvotes': user_corrected_votes['downvotes'],
            'User Corrected Score': user_corrected_votes['score'],
            'Troubleshooting Steps': troubleshooting_steps.strip(),
            'Original Notes': notes,
            'Original Summary': description
        }
        
        print(f"   [OK] Analysis complete for {sr_id}")
        print(f"        Java Error: {is_java_error}")
        if is_java_error == "Yes":
            print(f"        Java Details: {java_failure_path.strip()}")
        
        return result
    
    def _build_java_code_context(self, matches: List[Dict]) -> str:
        """Build Java code context from semantic search results"""
        if not matches:
            return "No relevant Java code found in semantic search.\n"
        
        context = "🔍 **RELEVANT JAVA CODE SNIPPETS** (from comcast_code.db):\n\n"
        context += "These are actual code snippets from the backend that match your SR description.\n"
        context += "Use these to understand implementation details and provide accurate file references.\n\n"
        
        for idx, match in enumerate(matches, 1):
            metadata = match['metadata']
            context += f"{'='*60}\n"
            context += f"Match #{idx} - Similarity: {match['similarity']:.0%}\n"
            context += f"File: {metadata.get('file_path', 'Unknown')}\n"
            context += f"Module: {metadata.get('module', 'Unknown')}\n"
            context += f"{'='*60}\n"
            context += f"Code:\n{match['code'][:500]}\n"  # Truncate for context size
            context += f"{'='*60}\n\n"
        
        context += "📌 **USE THIS FOR**: Finding exact file paths, understanding implementation, identifying error patterns in actual code.\n\n"
        
        return context
    
    def _build_historical_context(self, matches: List[Dict], has_input: bool, input_text: str) -> str:
        """Build historical context with vote-based priority"""
        if has_input:
            context = "📚 **SEMANTIC WORKAROUND FROM INPUT**:\n\n"
            context += input_text + "\n\n"
            context += "⚠️ **MANDATORY**: This is a PROVEN solution. Extract the pattern (actions + systems + data) and adapt it with current SR's specific values!\n"
            return context
        
        if not matches:
            return "No historical matches found. Generate solution based on SR description and Java context.\n"
        
        # 🆕 Enrich matches with vote scores
        if self.feedback_storage:
            for match in matches:
                sr_id = match['sr_id']
                # Get votes for original workaround type (from historical data)
                votes = self.feedback_storage.get_votes(sr_id, 'original')
                match['vote_score'] = votes['score']
                match['votes'] = votes
        else:
            # No feedback storage - use default neutral votes
            for match in matches:
                match['vote_score'] = 0
                match['votes'] = {'upvotes': 0, 'downvotes': 0, 'score': 0}
        
        # 🆕 Sort by weighted combination: 70% similarity + 30% normalized vote score
        # Normalize vote score to 0-1 range (assuming scores typically range from -10 to +10)
        def calculate_priority(match):
            similarity_weight = 0.7
            vote_weight = 0.3
            # Normalize vote score from [-10, 10] to [0, 1]
            normalized_vote = (match['vote_score'] + 10) / 20.0
            normalized_vote = max(0, min(1, normalized_vote))  # Clamp to [0, 1]
            return (match['similarity'] * similarity_weight) + (normalized_vote * vote_weight)
        
        matches_sorted = sorted(matches, key=calculate_priority, reverse=True)
        
        context = "📚 **HISTORICAL SR MATCHES** (ranked by similarity + user feedback):\n\n"
        context += "These are PROVEN solutions from similar past SRs.\n"
        
        # Add voting legend if feedback is available
        if self.feedback_storage:
            context += "\n🎯 **VOTING LEGEND:**\n"
            context += "- 👍 Upvotes = Users found this solution helpful\n"
            context += "- 👎 Downvotes = Users found this solution unhelpful\n"
            context += "- Score = Upvotes - Downvotes (higher is better)\n"
            context += "- High score (>5) = HIGHLY VALIDATED - Prioritize this pattern!\n"
            context += "- Positive score (>0) = VALIDATED - Good solution\n"
            context += "- Negative score (<0) = PROBLEMATIC - Use with caution or avoid\n\n"
        
        context += "⚠️ **MANDATORY**: Extract ACTION PATTERNS from HIGH-SCORE matches and adapt them with current SR's specific data!\n\n"
        
        for idx, match in enumerate(matches_sorted, 1):
            context += f"{'='*60}\n"
            context += f"Match #{idx} - SR {match['sr_id']}\n"
            context += f"Similarity: {match['similarity']:.0%}\n"
            
            # Add vote information with visual indicators
            if self.feedback_storage:
                score = match['vote_score']
                upvotes = match['votes']['upvotes']
                downvotes = match['votes']['downvotes']
                
                # Add emoji indicator based on score
                if score > 5:
                    score_indicator = "⭐ **HIGHLY VALIDATED**"
                elif score > 0:
                    score_indicator = "✅ **USER VALIDATED**"
                elif score == 0 and (upvotes > 0 or downvotes > 0):
                    score_indicator = "⚖️ **MIXED FEEDBACK**"
                elif score < 0:
                    score_indicator = "⚠️ **PROBLEMATIC - USE CAUTION**"
                else:
                    score_indicator = "📊 **NOT YET RATED**"
                
                context += f"Feedback: 👍 {upvotes} | 👎 {downvotes} | Score: {score:+d} {score_indicator}\n"
            
            context += f"Resolution Category: {match['resolution_category']}\n"
            context += f"Status Reason: {match['status_reason']}\n"
            context += f"Description: {match['description']}\n\n"
            context += f"Historical Workaround:\n{match['workaround'][:800]}\n"  # Truncate
            context += f"{'='*60}\n\n"
        
        context += "📌 **ACTION REQUIRED**: Find the common pattern across HIGH-SCORE workarounds. Identify: What was DONE (action), WHERE (system), WHAT DATA (values), and SEQUENCE. Apply same pattern to current SR.\n\n"
        
        return context
    
    def _build_detection_evidence_context(self, detection_result: Dict) -> str:
        """Build detection evidence context from intelligent detector"""
        if not detection_result['evidence']:
            return "No evidence collected."
        
        context = "Detection Evidence:\n"
        for evidence in detection_result['evidence']:
            context += f"{evidence}\n"
        
        return context
    
    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        """Extract section from AI response"""
        try:
            start_idx = text.lower().find(start_marker.lower())
            if start_idx == -1:
                return ""
            
            end_idx = text.lower().find(end_marker.lower(), start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            section = text[start_idx:end_idx].strip()
            section = section.replace(start_marker, "").replace(end_marker, "").strip()
            section = section.lstrip(':').lstrip('-').strip()
            
            return section[:2000]  # Limit length
            
        except:
            return ""
    
    def _extract_ai_workaround(self, text: str) -> str:
        """
        Enhanced AI workaround extraction with multiple fallback methods
        
        Tries multiple extraction strategies in order:
        1. Standard format: "AI WORKAROUND:" section
        2. Alternative headers: "WORKAROUND:", "SOLUTION:", "FIX:"
        3. Numbered steps at the start
        4. Full response as last resort
        """
        if not text or len(text.strip()) < 20:
            return ""
        
        # Strategy 1: Try standard "AI WORKAROUND:" header
        workaround = self._extract_section(text, "AI WORKAROUND:", "TROUBLESHOOTING STEPS:")
        if workaround and len(workaround.strip()) >= 20:
            print(f"   [Extract] Method 1: Found 'AI WORKAROUND:' section ({len(workaround)} chars)")
            return workaround
        
        # Strategy 2: Try alternative headers
        alternative_headers = [
            ("WORKAROUND:", "TROUBLESHOOTING"),
            ("SOLUTION:", "TROUBLESHOOTING"),
            ("FIX:", "TROUBLESHOOTING"),
            ("RESOLUTION:", "TROUBLESHOOTING"),
            ("RECOMMENDED ACTIONS:", "TROUBLESHOOTING")
        ]
        
        for start_marker, end_marker in alternative_headers:
            workaround = self._extract_section(text, start_marker, end_marker)
            if workaround and len(workaround.strip()) >= 20:
                print(f"   [Extract] Method 2: Found '{start_marker}' section ({len(workaround)} chars)")
                return workaround
        
        # Strategy 3: Check if response starts with numbered steps (common LLM format)
        lines = text.strip().split('\n')
        if lines and (lines[0].strip().startswith('1.') or lines[0].strip().startswith('1)')):
            print(f"   [Extract] Method 3: Using numbered steps format ({len(text)} chars)")
            return text.strip()[:2000]
        
        # Strategy 4: Use first paragraph if it's substantial
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if paragraphs and len(paragraphs[0]) >= 50:
            print(f"   [Extract] Method 4: Using first paragraph ({len(paragraphs[0])} chars)")
            return paragraphs[0][:2000]
        
        # Strategy 5: Last resort - use full response if it's reasonable length
        if len(text.strip()) >= 50:
            print(f"   [Extract] Method 5: Using full response ({len(text)} chars)")
            return text.strip()[:2000]
        
        print(f"   [Extract] Failed: All extraction methods returned insufficient content")
        return ""
    
    def _clean_step_numbering(self, text: str) -> str:
        """Clean up malformed step numbering from LLM output"""
        if not text:
            return text
        
        import re
        
        # Remove patterns like "Step 1**", "Step 21.", "**Step 3**"
        text = re.sub(r'Step\s*\d+\*+', '', text)  # Remove "Step 1**"
        text = re.sub(r'\*\*Step\s*\d+\*\*', '', text)  # Remove "**Step 3**"
        text = re.sub(r'Step\s*\d+\s*\*\*', '', text)  # Remove "Step 1 **"
        
        # Fix patterns like "Step 21. " to just "1. "
        text = re.sub(r'Step\s*(\d)(\d+)\.', r'\2.', text)  # "Step 21." → "1."
        text = re.sub(r'Step\s+(\d+)\.', r'\1.', text)  # "Step 1." → "1."
        
        # Remove bold markers from step labels like "1. **Investigation**:"
        text = re.sub(r'(\d+\.)\s*\*\*([^*]+)\*\*:', r'\1', text)  # "1. **Investigation**:" → "1."
        
        # Remove orphaned asterisks
        text = re.sub(r'\*\*(?!\w)', '', text)  # Remove "**" not followed by word
        text = re.sub(r'(?<!\w)\*\*', '', text)  # Remove "**" not preceded by word
        
        # Clean up multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove empty lines that only have whitespace
        lines = text.split('\n')
        lines = [line if line.strip() else '' for line in lines]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def _extract_value(self, text: str, marker: str) -> str:
        """Extract value after a marker"""
        try:
            start_idx = text.lower().find(marker.lower())
            if start_idx == -1:
                return "N/A"
            
            start_idx = start_idx + len(marker)
            end_idx = text.find('\n', start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            value = text[start_idx:end_idx].strip()
            value = value.lstrip(':').lstrip('-').strip()
            value = value.split('[')[0].strip()
            
            return value if value else "N/A"
            
        except:
            return "N/A"


if __name__ == '__main__':
    print("="*80)
    print("SINGLE SR ANALYSIS WITH RAG (Ollama)")
    print("="*80)
    print()
    
    # Initialize pipeline
    pipeline = SingleSRAnalysisPipeline()
    
    # Get SR input from user
    sr_data = pipeline.get_user_input()
    
    if sr_data:
        # Analyze SR
        result = pipeline.analyze_single_sr(sr_data)
        
        print("\n" + "="*80)
        print("ANALYSIS RESULT")
        print("="*80)
        print(f"SR ID: {result['SR ID']}")
        print(f"Java Error: {result['Java Failure Detected']}")
        print(f"Java Path: {result['Java Failure Path']}")
        print(f"\nAI Workaround:\n{result['AI Workaround']}")
        print(f"\nTroubleshooting:\n{result['Troubleshooting Steps']}")
        print("="*80)
    else:
        print("\n[EXIT] No SR data provided")
