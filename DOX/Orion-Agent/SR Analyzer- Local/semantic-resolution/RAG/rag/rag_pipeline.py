"""
SR Analysis RAG Pipeline with DeepSeek Coder V2 Lite
Intelligent Service Request Analysis using Local LLM

This pipeline:
1. Reads Excel files with service requests and semantic workarounds
2. Analyzes each SR using javaMapping.db and people_skills.db
3. Uses DeepSeek Coder V2 Lite for intelligent analysis
4. Generates comprehensive output with Java detection and skills-based assignment
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class DeepSeekAnalyzer:
    """DeepSeek Coder V2 Lite Model Handler"""
    
    def __init__(self, model_cache_dir: Path):
        self.model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
        self.cache_dir = model_cache_dir
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the DeepSeek model from local cache"""
        print(f"🤖 Loading DeepSeek Coder V2 Lite from cache...")
        print(f"📁 Cache: {self.cache_dir}")
        print(f"🖥️  Device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(self.cache_dir),
                trust_remote_code=True,
                local_files_only=True  # Force offline mode
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                str(self.cache_dir),
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto",
                low_cpu_mem_usage=True,
                local_files_only=True  # Force offline mode
            )
            
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print(f"💡 Please run 'python download_deepseek_model.py' first!")
            return False
    
    def generate_response(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.3) -> str:
        """Generate response from DeepSeek model"""
        try:
            # Format prompt for instruction following
            formatted_prompt = f"""You are an expert SR analysis system. Analyze the following service request data and provide intelligent insights.

{prompt}

Provide your analysis in a structured format."""

            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.95,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (remove the prompt)
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()
            
            return response
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return f"Error: {str(e)}"


class DatabaseHandler:
    """Handle database queries for Java mapping and people skills"""
    
    def __init__(self, java_db_path: Path, skills_db_path: Path):
        self.java_db_path = java_db_path
        self.skills_db_path = skills_db_path
    
    def query_java_mapping(self, sr_description: str) -> Dict:
        """Query javaMapping.db for Java backend analysis"""
        try:
            conn = sqlite3.connect(self.java_db_path)
            cursor = conn.cursor()
            
            # Get all Java files and classes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Search for Java-related patterns
            java_patterns = [
                'Exception', 'Error', 'java.', 'NullPointer', 'SQLException',
                'IOException', 'RuntimeException', 'StackTrace', 'backend',
                'service', 'controller', 'repository'
            ]
            
            detected_patterns = []
            for pattern in java_patterns:
                if pattern.lower() in sr_description.lower():
                    detected_patterns.append(pattern)
            
            # Try to find specific Java files
            java_files = []
            if detected_patterns:
                # Search in tables for Java file information
                for table in tables:
                    try:
                        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 10")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            row_str = str(row).lower()
                            if any(pattern.lower() in row_str for pattern in detected_patterns):
                                java_files.append({
                                    'table': table[0],
                                    'data': str(row)[:200]  # First 200 chars
                                })
                    except:
                        pass
            
            conn.close()
            
            return {
                'detected_patterns': detected_patterns,
                'java_files': java_files[:5],  # Top 5 matches
                'has_java_error': len(detected_patterns) > 0
            }
            
        except Exception as e:
            print(f"⚠️  Warning: Error querying Java database: {e}")
            return {'detected_patterns': [], 'java_files': [], 'has_java_error': False}
    
    def get_best_assignee(self, sr_description: str, priority: str, java_failure: bool) -> Dict:
        """Query people_skills.db for optimal assignment"""
        try:
            conn = sqlite3.connect(self.skills_db_path)
            cursor = conn.cursor()
            
            # Get all team members with skills
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Try to find team members table
            team_members = []
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info({table[0]})")
                    columns = cursor.fetchall()
                    column_names = [col[1] for col in columns]
                    
                    # Look for relevant columns
                    if any(col in ['name', 'skill', 'expertise'] for col in column_names):
                        cursor.execute(f"SELECT * FROM {table[0]}")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            team_members.append({
                                'table': table[0],
                                'data': row,
                                'columns': column_names
                            })
                except:
                    pass
            
            conn.close()
            
            # Simple assignment logic based on priority and Java failure
            if java_failure:
                assigned_to = "Senior Java Developer"
            elif priority in ['P1', 'P2']:
                assigned_to = "Senior Support Engineer"
            else:
                assigned_to = "Support Engineer L2"
            
            return {
                'assigned_to': assigned_to,
                'reason': f"Java failure: {java_failure}, Priority: {priority}",
                'available_members': len(team_members)
            }
            
        except Exception as e:
            print(f"⚠️  Warning: Error querying skills database: {e}")
            return {
                'assigned_to': 'Support Engineer',
                'reason': 'Default assignment',
                'available_members': 0
            }


class SRAnalysisPipeline:
    """Main RAG Pipeline for SR Analysis"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "llm output"
        self.model_dir = Path(__file__).parent / "models" / "deepseek_coder_v2_lite"
        
        # Database paths
        self.java_db = Path(__file__).parent.parent.parent / "vector store" / "javaMapping.db"
        self.skills_db = Path(__file__).parent.parent.parent / "vector store" / "people_skills.db"
        
        # Initialize components
        self.analyzer = DeepSeekAnalyzer(self.model_dir)
        self.db_handler = DatabaseHandler(self.java_db, self.skills_db)
        self.results = []
        
        # Create directories
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def find_input_excel(self) -> Optional[Path]:
        """Find Excel file in input directory"""
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        
        if not excel_files:
            print(f"❌ No Excel files found in: {self.input_dir}")
            return None
        
        if len(excel_files) > 1:
            print(f"⚠️  Multiple Excel files found. Using: {excel_files[0].name}")
        
        return excel_files[0]
    
    def read_excel_input(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Read and validate input Excel file"""
        try:
            df = pd.read_excel(file_path)
            print(f"✅ Read {len(df)} service requests from: {file_path.name}")
            print(f"📋 Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            
            # Validate required columns
            required_cols = ['SR ID', 'Priority', 'Description', 'Semantic Workaround']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                # Try alternative column names
                alt_mapping = {
                    'SR ID': ['Call ID', 'ID', 'Ticket ID'],
                    'Description': ['Issue', 'Problem', 'Summary'],
                    'Semantic Workaround': ['Workaround', 'Similar Cases']
                }
                
                for req_col, alternatives in alt_mapping.items():
                    if req_col in missing_cols:
                        for alt in alternatives:
                            if alt in df.columns:
                                df.rename(columns={alt: req_col}, inplace=True)
                                missing_cols.remove(req_col)
                                break
            
            if missing_cols:
                print(f"⚠️  Missing columns: {missing_cols}")
                print(f"Available columns: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error reading Excel file: {e}")
            return None
    
    def analyze_single_sr(self, sr_data: Dict) -> Dict:
        """Analyze a single service request"""
        
        sr_id = sr_data.get('SR ID', 'Unknown')
        priority = sr_data.get('Priority', 'P3')
        description = str(sr_data.get('Description', ''))
        notes = str(sr_data.get('Notes', sr_data.get('Summary', '')))
        semantic_workaround = str(sr_data.get('Semantic Workaround', 'Not available'))
        
        print(f"\n🔍 Analyzing SR: {sr_id} (Priority: {priority})")
        
        # Step 1: Java Backend Analysis
        print("   ☕ Analyzing Java backend...")
        java_analysis = self.db_handler.query_java_mapping(description + " " + notes)
        
        # Step 2: Skills-Based Assignment
        print("   👤 Determining optimal assignment...")
        assignment = self.db_handler.get_best_assignee(
            description, 
            priority, 
            java_analysis['has_java_error']
        )
        
        # Step 3: Generate AI Analysis using DeepSeek
        print("   🤖 Generating AI analysis...")
        
        analysis_prompt = f"""
SERVICE REQUEST ANALYSIS

SR ID: {sr_id}
Priority: {priority}

Description: {description}

Notes: {notes}

Semantic Workaround (from similar cases): {semantic_workaround}

Java Analysis:
- Detected Patterns: {', '.join(java_analysis['detected_patterns']) if java_analysis['detected_patterns'] else 'None'}
- Java Error Present: {java_analysis['has_java_error']}

TASK: Provide intelligent analysis with:
1. AI Workaround: Enhanced workaround based on semantic workaround and current context
2. Troubleshooting Steps: Step-by-step resolution guide
3. Java Failure Analysis: If Java error detected, specify class name and path
4. Key Insights: Important observations

Format your response clearly with sections.
"""
        
        ai_response = self.analyzer.generate_response(analysis_prompt, max_tokens=1024)
        
        # Parse AI response for structured data
        ai_workaround = self._extract_section(ai_response, "AI Workaround", "Troubleshooting")
        troubleshooting_steps = self._extract_section(ai_response, "Troubleshooting", "Java Failure")
        
        # Determine Java failure details
        java_failure_detected = "Yes" if java_analysis['has_java_error'] else "No"
        java_failure_path = "N/A"
        
        if java_analysis['has_java_error'] and java_analysis['java_files']:
            # Extract path from first matching file
            java_failure_path = java_analysis['java_files'][0].get('table', 'Unknown path')
        
        # Compile result
        result = {
            'SR ID': sr_id,
            'Priority': priority,
            'Assigned To': assignment['assigned_to'],
            'Java Failure Detected': java_failure_detected,
            'Java Failure Path': java_failure_path,
            'Semantic Workaround': semantic_workaround,
            'AI Workaround': ai_workaround if ai_workaround else semantic_workaround,
            'Troubleshooting Steps': troubleshooting_steps if troubleshooting_steps else "Standard troubleshooting workflow",
            'Original Notes': notes,
            'Original Summary': description
        }
        
        print(f"   ✅ Analysis complete for {sr_id}")
        
        return result
    
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
            # Remove the marker itself
            section = section.replace(start_marker, "").strip()
            section = section.lstrip(':').strip()
            
            return section[:500]  # Limit length
            
        except:
            return ""
    
    def process_all_srs(self, df: pd.DataFrame):
        """Process all SRs one by one"""
        print(f"\n{'='*80}")
        print(f"🚀 Starting SR Analysis Pipeline")
        print(f"{'='*80}")
        print(f"📊 Total SRs to process: {len(df)}")
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing SRs"):
            try:
                sr_data = row.to_dict()
                result = self.analyze_single_sr(sr_data)
                self.results.append(result)
                
            except Exception as e:
                print(f"\n❌ Error processing SR {row.get('SR ID', idx)}: {e}")
                # Add error result
                self.results.append({
                    'SR ID': row.get('SR ID', f'SR_{idx}'),
                    'Priority': row.get('Customer Priority', row.get('Priority', 'Unknown')),
                    'Assigned To': 'Error - Requires Review',
                    'Java Failure Detected': 'Error',
                    'Java Failure Path': 'N/A',
                    'Semantic Workaround': str(row.get('Semantic Workaround', '')),
                    'AI Workaround': f'Error during analysis: {str(e)}',
                    'Troubleshooting Steps': 'Manual review required',
                    'Original Notes': str(row.get('Notes', '')),
                    'Original Summary': str(row.get('Description', ''))
                })
        
        print(f"\n✅ Processed {len(self.results)} service requests")
    
    def save_results(self, input_filename: str):
        """Save results to Excel file"""
        try:
            # Create output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{Path(input_filename).stem}_analysis_{timestamp}.xlsx"
            output_path = self.output_dir / output_filename
            
            # Convert results to DataFrame
            results_df = pd.DataFrame(self.results)
            
            # Save to Excel
            results_df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"\n{'='*80}")
            print(f"✅ SUCCESS! Analysis complete")
            print(f"{'='*80}")
            print(f"📁 Output file: {output_path}")
            print(f"📊 Total SRs analyzed: {len(self.results)}")
            print(f"☕ Java failures detected: {sum(1 for r in self.results if r['Java Failure Detected'] == 'Yes')}")
            print(f"\n💡 Next Steps:")
            print(f"   1. Review the analysis in: {output_path.name}")
            print(f"   2. Use this for RAG pipeline integration")
            print(f"   3. Process feedback and iterate")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None
    
    def run(self):
        """Main pipeline execution"""
        print("\n" + "="*80)
        print("🎯 SR Analysis RAG Pipeline with DeepSeek Coder V2 Lite")
        print("="*80)
        
        # Load model
        if not self.analyzer.load_model():
            print("\n❌ Failed to load DeepSeek model. Exiting...")
            return False
        
        # Find input file
        input_file = self.find_input_excel()
        if not input_file:
            print("\n💡 Please place an Excel file in:", self.input_dir)
            return False
        
        # Read input
        df = self.read_excel_input(input_file)
        if df is None:
            return False
        
        # Process all SRs
        self.process_all_srs(df)
        
        # Save results
        output_path = self.save_results(input_file.name)
        
        return output_path is not None


def main():
    """Entry point"""
    try:
        pipeline = SRAnalysisPipeline()
        success = pipeline.run()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

