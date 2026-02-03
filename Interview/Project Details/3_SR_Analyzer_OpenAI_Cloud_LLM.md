# SR Analyzer with OpenAI API - Complete Project Documentation

## 📋 Project Overview

**Project Name:** SR Analyzer - OpenAI/ChatGPT Edition  
**Type:** Enterprise RAG Pipeline with Multi-Model Architecture  
**Tech Stack:** Python, OpenAI API (Amdocs Gateway), ChromaDB, SQLite, Flask, Sentence Transformers  
**Purpose:** Production-grade SR analysis using cloud LLM with 5-call architecture

---

## 🎯 Project Description

### Short Description (30 seconds)
"This is an enterprise-grade RAG pipeline that uses OpenAI's GPT model through Amdocs' AI gateway. It implements a sophisticated 5-LLM-call architecture for comprehensive SR analysis: semantic workaround retrieval, Java error detection with 5-source voting, activity keyword extraction, resolution generation, and skill-based assignment. The system uses ChromaDB for vector storage and includes a full Flask web application with user/admin portals."

### Detailed Description (2-3 minutes)
"This project is the production version of our SR analysis system, designed for enterprise deployment using Amdocs' OpenAI API gateway which provides $5/user/month allocation.

**The Multi-Model Architecture uses 5 sequential LLM calls:**

1. **LLM Call 1 - Semantic Workaround Retrieval:**
   - Queries ChromaDB for similar historical SRs
   - LLM evaluates and selects the best matching workaround
   - Filters out garbage responses (NA, escalated, etc.)

2. **LLM Call 2 - Java Error Detection (5-Source Voting):**
   - Analyzes 5 different sources for Java indicators
   - Resolution categories, semantic workaround, AI workarounds, user workarounds, SR text
   - Uses voting mechanism for high-confidence detection

3. **LLM Call 3a/3b - Activity Extraction:**
   - 3a: Extracts activity keywords for fuzzy database search
   - 3b: Matches keywords to actual Java class names from javaMapping.db

4. **LLM Call 4a/4b - Resolution Generation:**
   - 4a: Java-specific resolution with class paths and code fixes
   - 4b: General resolution for non-Java issues

5. **LLM Call 5 - Skill-Based Assignment:**
   - Queries people_skills.db for team capabilities
   - Considers SR priority, Java expertise, workload
   - Returns optimal assignee with reasoning

**Key Differentiators from Ollama Version:**
- Higher quality responses from GPT-4
- Structured JSON output parsing
- Parallel processing for batch SRs
- Token usage tracking and optimization
- Enterprise authentication via Amdocs gateway"

---

## 📁 File Structure

```
Abhi- SR analyzer-restructured_Open AI/
├── semantic-resolution/
│   ├── RAG/
│   │   ├── pipeline/
│   │   │   ├── multi_model_rag_pipeline_chatgpt.py  # Main 5-call pipeline
│   │   │   └── activity_name_finder.py              # PostgreSQL activity lookup
│   │   ├── vectorstore/
│   │   │   ├── vectorstore_manager.py               # ChromaDB operations
│   │   │   └── embedding_utils.py                   # Embedding generation
│   │   └── prompts/
│   │       └── prompt_templates.py                  # All 5 LLM prompts
│   │
│   ├── app/
│   │   ├── __init__.py                              # Flask app factory
│   │   ├── sr_feedback_app.py                       # Entry point
│   │   ├── routes/
│   │   │   ├── auth.py                              # Login/logout
│   │   │   ├── user.py                              # User portal
│   │   │   ├── admin.py                             # Admin portal
│   │   │   ├── team.py                              # Team management
│   │   │   └── api.py                               # REST API endpoints
│   │   └── utils/
│   │       ├── helpers.py                           # Utility functions
│   │       ├── decorators.py                        # Auth decorators
│   │       └── state.py                             # Shared state
│   │
│   ├── analyzers/
│   │   ├── batch_sr_analyser.py                     # Batch processing
│   │   ├── comprehensive_sr_analyzer.py             # Full analysis
│   │   └── sr_text_preprocessor.py                  # Text cleaning
│   │
│   ├── data/
│   │   ├── vectorstore/
│   │   │   └── chroma_db/                           # ChromaDB storage
│   │   ├── database/
│   │   │   └── javaMapping.db                       # Java class mapping
│   │   └── people_skills.db                         # Team skills
│   │
│   ├── config/
│   │   ├── settings.py                              # Configuration
│   │   └── paths.py                                 # Path constants
│   │
│   ├── tokens/
│   │   └── Tokens.xlsx                              # API token storage
│   │
│   ├── templates/
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── user/
│   │   │   └── portal.html
│   │   ├── admin/
│   │   │   ├── portal.html
│   │   │   └── batch_upload.html
│   │   └── team/
│   │       └── management.html
│   │
│   ├── team/
│   │   ├── skill_manager.py                         # Skills CRUD
│   │   └── assignment_engine.py                     # Assignment logic
│   │
│   ├── workaround/
│   │   ├── workaround_retriever.py                  # Semantic search
│   │   └── workaround_generator.py                  # AI generation
│   │
│   ├── START_MULTIMODEL_RAG.bat                     # Windows launcher
│   ├── START_MULTIMODEL_RAG.sh                      # Linux launcher
│   └── requirements.txt    
```

---

## 🛠️ Technologies Used

| Category | Technology | Purpose |
|----------|------------|---------|
| LLM | OpenAI GPT-4 (via Amdocs Gateway) | Cloud language model |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) | Text vectorization |
| Vector DB | ChromaDB | Semantic similarity search |
| Database | SQLite | Java mapping & skills |
| Database | PostgreSQL | Activity implementation lookup |
| Backend | Flask | Web application |
| API | REST + LangChain | LLM integration |
| Auth | Session-based | User management |
| Data | Pandas, OpenPyXL | Excel processing |

---

## 🔧 Key Technical Implementations

### 1. Multi-Model RAG Pipeline (5 LLM Calls)

```python
# RAG/pipeline/multi_model_rag_pipeline_chatgpt.py

class MultiModelRAGPipeline:
    """5-Call LLM Architecture for SR Analysis"""
    
    def __init__(self):
        self.llm = AmdocsOpenAILLM(api_url, token_file)
        self.vectorstore = ChromaDBManager()
        self.java_db = SQLiteHandler('javaMapping.db')
        self.skills_db = SQLiteHandler('people_skills.db')
        
    def analyze_sr(self, sr_data: Dict) -> Dict:
        # ===== LLM CALL 1: Semantic Workaround =====
        similar_srs = self.vectorstore.similarity_search(sr_data['description'])
        semantic_workaround = self.llm_call_1_semantic_workaround(
            sr_data, similar_srs
        )
        
        # ===== LLM CALL 2: Java Detection (5-Source Voting) =====
        java_result = self.llm_call_2_java_detection(
            sr_data, semantic_workaround, similar_srs
        )
        
        # ===== LLM CALL 3a/3b: Activity Extraction =====
        if java_result['is_java']:
            keywords = self.llm_call_3a_extract_keywords(sr_data)
            activity_names = self.llm_call_3b_match_activities(keywords)
        
        # ===== LLM CALL 4a/4b: Resolution Generation =====
        if java_result['is_java']:
            resolution = self.llm_call_4a_java_resolution(
                sr_data, activity_names, java_result
            )
        else:
            resolution = self.llm_call_4b_general_resolution(
                sr_data, semantic_workaround
            )
        
        # ===== LLM CALL 5: Skill-Based Assignment =====
        assignment = self.llm_call_5_assignment(
            sr_data, java_result, resolution
        )
        
        return {
            'semantic_workaround': semantic_workaround,
            'java_detected': java_result['is_java'],
            'java_confidence': java_result['confidence'],
            'ai_resolution': resolution,
            'assigned_to': assignment['assignee'],
            'assignment_reason': assignment['reason']
        }
```

### 2. Amdocs OpenAI Gateway Integration

```python
# Custom LLM class for Amdocs API Gateway
class AmdocsOpenAILLM(LLM):
    """LangChain-compatible LLM for Amdocs OpenAI Gateway"""
    
    api_url: str = "https://ai-framework1:8085/api/v1/call_llm"
    token: str = None
    
    def __init__(self, token_file: str):
        super().__init__()
        self.token = self._load_token(token_file)
        
    def _load_token(self, token_file: str) -> str:
        """Load API token from Excel file"""
        df = pd.read_excel(token_file)
        return df.iloc[0]['token']
    
    def _call(self, prompt: str, stop: List[str] = None) -> str:
        """Make API call to Amdocs gateway"""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-4',
            'messages': [
                {'role': 'system', 'content': 'You are an SR analysis expert.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_tokens': 2048
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            verify=False  # Internal network
        )
        
        return response.json()['choices'][0]['message']['content']
```

### 3. 5-Source Java Detection Voting

```python
PROMPT_JAVA_DETECTION_VOTING = """
You are a Java error detection system using 5-SOURCE VOTING mechanism.

=== SOURCE 1: RESOLUTION CATEGORIES ===
Current SR Category: {resolution_category}
Java-indicating: code, backend, application error, system error
Non-Java: data, interface, configuration, network, frontend

=== SOURCE 2: SEMANTIC WORKAROUND ===
{semantic_workaround}
Look for: *Service, *Controller, NullPointerException, com.amdocs.*

=== SOURCE 3: AI WORKAROUNDS FROM SIMILAR SRs ===
{ai_workarounds}

=== SOURCE 4: USER WORKAROUNDS FROM SIMILAR SRs ===
{user_workarounds}

=== SOURCE 5: SR TEXT ANALYSIS ===
{sr_text}

=== VOTING RULES ===
- Each source votes: JAVA, NOT_JAVA, or UNCERTAIN
- Final decision: Majority wins (3+ votes)
- Confidence = (winning_votes / 5) * 100

=== OUTPUT (JSON) ===
{{
    "source_votes": {{
        "categories": "JAVA|NOT_JAVA|UNCERTAIN",
        "semantic_workaround": "JAVA|NOT_JAVA|UNCERTAIN",
        "ai_workarounds": "JAVA|NOT_JAVA|UNCERTAIN",
        "user_workarounds": "JAVA|NOT_JAVA|UNCERTAIN",
        "sr_text": "JAVA|NOT_JAVA|UNCERTAIN"
    }},
    "is_java": true|false,
    "confidence": 0.0-1.0,
    "detected_patterns": ["pattern1", "pattern2"]
}}
"""

def llm_call_2_java_detection(self, sr_data, semantic_wa, similar_srs):
    prompt = PROMPT_JAVA_DETECTION_VOTING.format(
        resolution_category=sr_data.get('category', ''),
        semantic_workaround=semantic_wa,
        ai_workarounds=self._extract_ai_workarounds(similar_srs),
        user_workarounds=self._extract_user_workarounds(similar_srs),
        sr_text=sr_data['description'] + ' ' + sr_data.get('notes', '')
    )
    
    response = self.llm._call(prompt)
    return json.loads(response)
```

### 4. Activity Name Finder (PostgreSQL Integration)

```python
# RAG/pipeline/activity_name_finder.py

class ActivityFinder:
    """Find Java activity implementations in PostgreSQL"""
    
    def __init__(self, db_config: Dict):
        self.conn = psycopg2.connect(**db_config)
        
    def find_activity(self, keywords: List[str]) -> List[Dict]:
        """Fuzzy search for activity names"""
        results = []
        
        for keyword in keywords:
            # Use trigram similarity for fuzzy matching
            query = """
                SELECT 
                    activity_name,
                    class_name,
                    file_path,
                    similarity(activity_name, %s) as score
                FROM java_activities
                WHERE similarity(activity_name, %s) > 0.3
                ORDER BY score DESC
                LIMIT 5
            """
            
            cursor = self.conn.cursor()
            cursor.execute(query, (keyword, keyword))
            
            for row in cursor.fetchall():
                results.append({
                    'activity_name': row[0],
                    'class_name': row[1],
                    'file_path': row[2],
                    'match_score': row[3]
                })
        
        return results
```

### 5. Flask Application with Blueprints

```python
# app/__init__.py

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sr-analyzer-secret'
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.team import team_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# app/routes/admin.py
@admin_bp.route('/batch-upload', methods=['POST'])
@admin_required
def batch_upload():
    """Process batch SR upload"""
    file = request.files['file']
    df = pd.read_excel(file)
    
    pipeline = MultiModelRAGPipeline()
    results = []
    
    for _, row in df.iterrows():
        result = pipeline.analyze_sr(row.to_dict())
        results.append(result)
    
    return jsonify({'results': results, 'count': len(results)})
```

---

## 🔄 5-Call LLM Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Multi-Model RAG Pipeline                       │
│                   (5 Sequential LLM Calls)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LLM CALL 1: Semantic Workaround Retrieval                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: SR description + ChromaDB similar SRs            │    │
│  │ Task: Select best matching workaround                   │    │
│  │ Output: semantic_workaround, quality_score              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LLM CALL 2: Java Error Detection (5-Source Voting)             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Sources: Categories, Semantic WA, AI WAs, User WAs, Text│    │
│  │ Task: Vote on Java error presence                       │    │
│  │ Output: is_java, confidence, detected_patterns          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│  LLM CALL 3a: Keywords    │ │  (Skip if not Java)       │
│  Extract activity keywords│ │                           │
└───────────────────────────┘ └───────────────────────────┘
                    │
                    ▼
┌───────────────────────────┐
│  LLM CALL 3b: Activities  │
│  Match to Java classes    │
│  (uses javaMapping.db)    │
└───────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  LLM CALL 4a/4b: Resolution Generation                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 4a (Java): Include class paths, code fixes              │    │
│  │ 4b (General): Standard troubleshooting steps            │    │
│  │ Output: ai_resolution, troubleshooting_steps            │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LLM CALL 5: Skill-Based Assignment                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: SR analysis + people_skills.db                   │    │
│  │ Task: Find optimal assignee                             │    │
│  │ Output: assignee, reason, confidence                    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FINAL OUTPUT                                                    │
│  - Semantic Workaround                                          │
│  - Java Detected (Yes/No) + Confidence                          │
│  - AI Resolution                                                │
│  - Assigned To + Reason                                         │
│  - Activity Names (if Java)                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💡 Interview Questions & Answers

### Q1: Why 5 LLM calls instead of 1 comprehensive call?
**Answer:** "Breaking into 5 specialized calls provides several benefits:
1. **Focused prompts:** Each call has a specific task, reducing confusion
2. **Better accuracy:** Specialized prompts outperform general ones
3. **Debugging:** Can identify which step fails
4. **Caching:** Can cache intermediate results
5. **Parallel processing:** Some calls can run concurrently
6. **Token efficiency:** Each call uses only relevant context

The trade-off is higher latency (5 API calls), but accuracy improvement justifies it."

### Q2: Explain the 5-source voting mechanism for Java detection.
**Answer:** "Java detection is critical because it determines the resolution path. Using a single source is unreliable, so I implemented voting:

1. **Resolution Categories:** If category is 'backend' or 'code', vote JAVA
2. **Semantic Workaround:** Scan for Java patterns (Exception, .java, com.*)
3. **AI Workarounds:** Check if similar SRs had Java solutions
4. **User Workarounds:** Historical human-provided Java fixes
5. **SR Text:** Direct pattern matching in description

Each source votes independently. Majority (3+) wins. Confidence = votes/5.

This reduces false positives/negatives significantly."

### Q3: How do you handle the $5/user/month API budget?
**Answer:** "Several optimization strategies:
1. **Caching:** Cache embeddings and similar SR results
2. **Token counting:** Track usage per call, optimize prompts
3. **Batch processing:** Process multiple SRs in single sessions
4. **Selective calls:** Skip LLM calls 3a/3b if not Java
5. **Response length limits:** Set max_tokens appropriately
6. **Prompt compression:** Remove redundant context

I also built a token usage dashboard to monitor consumption."

### Q4: How does the activity name finder work with PostgreSQL?
**Answer:** "The PostgreSQL database stores Java activity implementations with:
- Activity name (e.g., 'CreateOrderActivity')
- Class name (e.g., 'com.amdocs.order.CreateOrderActivityImpl')
- File path

I use PostgreSQL's trigram similarity extension (pg_trgm) for fuzzy matching:
```sql
SELECT activity_name, similarity(activity_name, 'CreateOrder') as score
FROM java_activities
WHERE similarity(activity_name, 'CreateOrder') > 0.3
```

This finds activities even with typos or partial names."

### Q5: What's the difference between this and the Ollama version?
**Answer:** 
| Aspect | Ollama (Local) | OpenAI (Cloud) |
|--------|----------------|----------------|
| Cost | Free | $5/user/month |
| Quality | Good | Excellent |
| Latency | 2-5s | 1-2s |
| Privacy | Data stays local | Data sent to cloud |
| Offline | Yes | No |
| Architecture | Single call | 5 specialized calls |
| Output | Free text | Structured JSON |

"OpenAI version is for production where quality matters; Ollama for development/testing."

### Q6: How do you ensure JSON output from LLM?
**Answer:** "Multiple strategies:
1. **Explicit instructions:** 'Output ONLY valid JSON, no explanation'
2. **JSON schema in prompt:** Show exact expected structure
3. **Temperature:** Use low temperature (0.3) for deterministic output
4. **Validation:** Try json.loads(), retry if fails
5. **Fallback parsing:** Regex extraction if JSON fails
6. **Error handling:** Return default structure on parse failure"

### Q7: How do you handle LLM hallucinations?
**Answer:** "RAG inherently reduces hallucinations by grounding responses in retrieved context. Additional measures:
1. **Fact verification:** Cross-check generated class names against javaMapping.db
2. **Confidence scores:** Low confidence triggers manual review
3. **User feedback:** Collect corrections to identify hallucination patterns
4. **Prompt engineering:** Instruct LLM to say 'unknown' rather than guess
5. **Output validation:** Verify file paths exist before including"

---

## 🚀 How to Run

```bash
# 1. Ensure API token is in tokens/Tokens.xlsx

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize vector store (first time)
python data/vectorstore/create_vectorstore.py

# 4. Run the web application
python app/sr_feedback_app.py

# Access:
# User Portal: http://localhost:5000
# Admin Portal: http://localhost:5000/admin
```

---

## 📊 Key Metrics

- **LLM Calls per SR:** 5 (optimized path: 3 for non-Java)
- **Average Response Time:** 8-12 seconds per SR
- **Token Usage:** ~2000 tokens per SR analysis
- **Java Detection Accuracy:** 94% (with 5-source voting)
- **User Satisfaction:** 85% on generated workarounds
- **Cost per SR:** ~$0.02 (within $5/month budget for ~250 SRs)
