# 🔧 Technical Specifications & Logic Documentation

**Document Version**: 1.1  
**Last Updated**: December 16, 2024  
**System**: Intelligent SR Analysis & Resolution System

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [RAG Pipeline Logic](#rag-pipeline-logic)
4. [Java Error Detection Algorithm](#java-error-detection-algorithm)
5. [Activity Name Extraction](#activity-name-extraction)
6. [Semantic Search Implementation](#semantic-search-implementation)
7. [Feedback & Learning System](#feedback--learning-system)
8. [Email Integration](#email-integration)
9. [SR Classification Algorithm](#sr-classification-algorithm)
10. [Database Schemas](#database-schemas)
11. [LLM Prompt Engineering](#llm-prompt-engineering)
12. [API Specifications](#api-specifications)
13. [Configuration Parameters](#configuration-parameters)
14. [Performance Tuning](#performance-tuning)

---

## 🎯 System Overview

### Architecture Pattern

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           RAG (Retrieval-Augmented Generation)                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Input SR                                                                   │
│       ↓                                                                      │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│   │ Text        │ →  │ Semantic    │ →  │ Context     │ →  │ LLM         │  │
│   │ Preprocess  │    │ Retrieval   │    │ Building    │    │ Generation  │  │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         ↓                  ↓                  ↓                  ↓           │
│   Clean Text         Similar SRs        Rich Context       AI Workaround    │
│                      + Java Files       (5 sources)        + Steps          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **LLM** | ChatGPT (GPT-4.1) | Via LangChain | Workaround generation |
| **Embeddings** | SentenceTransformer | all-MiniLM-L6-v2 | Semantic similarity |
| **Vector Store** | FAISS | Latest | Fast similarity search |
| **Databases** | SQLite + PostgreSQL | 3.x / 14+ | Metadata & mapping |
| **Web Framework** | Flask | 2.x | Admin/User portals |
| **Frontend** | HTML/CSS/JS | - | Web UI |
| **Feedback UI** | Streamlit | 1.x | Vote collection |
| **Processing** | Python | 3.10+ | Core logic |

---

## 🔩 Core Components

### 1. MultiModelLLM Class

**File**: `RAG/rag/multi_model_rag_pipeline_chatgpt.py`

```python
class MultiModelLLM:
    """
    LLM wrapper for multi-model pipeline with JSON parsing.
    Handles all communication with the ChatGPT API via AI Framework Proxy.
    
    Attributes:
        model_name: str - Default "gpt-4.1"
        api_url: str - AI Framework Proxy endpoint
        token_manager: TokenManager - Manages API tokens with rotation
    
    Methods:
        call(prompt, call_name, temperature) -> str
        parse_json_response(response) -> Dict
        get_usage_summary() -> Dict
    """
```

**Key Parameters**:
| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `max_tokens` | 2048 | 512-4096 | Maximum response length |
| `temperature` | 0.3 | 0.0-1.0 | Lower = more deterministic |
| `top_p` | 0.95 | 0.0-1.0 | Nucleus sampling |
| `timeout` | 120s | - | API timeout |

### 2. VectorstoreHandler Class

**File**: `RAG/rag/multi_model_rag_pipeline_chatgpt.py`

```python
class VectorstoreHandler:
    """
    Manages all vector store queries and semantic searches.
    
    Data Sources:
        - javaMapping.db (SQLite): Java class metadata
        - comcast_code.db (FAISS): Code embeddings
        - clean_history_data.db (Pickle): Historical SRs
    
    Methods:
        search_java_classes(query, top_k) -> List[Dict]
        search_java_code_semantically(query, top_k) -> List[Dict]
        search_history_semantically(query, top_k) -> List[Dict]
        get_java_file_content(class_name) -> str
    """
```

**Similarity Thresholds**:
| Search Type | Min Threshold | Recommended | Max Results |
|-------------|---------------|-------------|-------------|
| Historical SRs | 0.60 | 0.70 | 5 |
| Java Code | 0.50 | 0.65 | 10 |
| Class Lookup | 0.70 | 0.80 | 3 |

### 3. WorkaroundJavaAnalyzer Class

**File**: `RAG/rag/workaround_java_analyzer.py`

```python
class WorkaroundJavaAnalyzer:
    """
    Multi-source voting system for Java error detection.
    
    Detection Sources (5 voters):
        1. Category Analysis - Resolution category patterns
        2. Semantic Workaround - Java indicators in workaround text
        3. AI Workarounds - Java patterns in AI-generated solutions
        4. User Workarounds - Java patterns in human solutions
        5. Current SR - Direct analysis of description/notes
    
    Returns:
        is_java_error: bool
        confidence: str (HIGH/MEDIUM/LOW/VERY_LOW/UNKNOWN)
        votes: Dict[str, str] - Each voter's decision
        evidence: List[str] - Supporting evidence
    """
```

### 4. ImprovedActivityFinder Class

**File**: `RAG/rag/improved_activity_finder.py`

```python
class ImprovedActivityFinder:
    """
    5-method activity name extraction without extra LLM calls.
    
    Methods Used:
        1. Regex Patterns (confidence: 0.90)
        2. Keyword Matching (confidence: up to 0.80)
        3. Semantic Search (confidence: up to 0.75)
        4. Historical Mining (confidence: 0.70)
        5. Class Index Lookup (confidence: 0.85)
    
    Returns:
        activity_name: str or None
        impl_class: str or None
        file_path: str or None
        confidence: str (High/Medium/Low)
        methods_used: str - Comma-separated list
    """
```

### 5. WorkaroundFeedbackStorage Class

**File**: `RAG/rag/feedback_storage.py`

```python
class WorkaroundFeedbackStorage:
    """
    SQLite-based feedback storage with vote tracking.
    
    Schema:
        workaround_feedback: Main vote storage
        vote_history: Individual vote log
    
    Methods:
        upvote(sr_id, workaround_type, text, user_id)
        downvote(sr_id, workaround_type, text, user_id)
        get_votes(sr_id, workaround_type) -> Dict
        get_vote_score(sr_id, workaround_type) -> int
        get_top_workarounds(limit, min_votes) -> List[Dict]
        get_statistics() -> Dict
    """
```

---

## 🔄 RAG Pipeline Logic

### Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE EXECUTION FLOW                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: INPUT PROCESSING (30 seconds)                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1.1 Load Excel from RAG/input/                                   │   │
│  │ 1.2 Extract: SR ID, Description, Notes, Category                 │   │
│  │ 1.3 Preprocess text (remove noise, preserve technical content)   │   │
│  │ 1.4 Generate embedding vector (384 dimensions)                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 2: SEMANTIC SEARCH (30 seconds)                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 2.1 Search clean_history_data.db (20K+ SRs)                      │   │
│  │ 2.2 Rank by cosine similarity + vote score                       │   │
│  │ 2.3 Apply threshold filter (≥0.60)                               │   │
│  │ 2.4 Return top 5 matches with metadata                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 3: JAVA DETECTION (10 seconds)                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 3.1 Analyze 5 sources (voting system)                            │   │
│  │ 3.2 Calculate weighted confidence                                │   │
│  │ 3.3 Determine: JAVA / NON-JAVA / UNKNOWN                         │   │
│  │ 3.4 Collect evidence for reasoning                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 4: ACTIVITY EXTRACTION (30 seconds) - If Java                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 4.1 Apply 5 extraction methods                                   │   │
│  │ 4.2 Aggregate scores per candidate                               │   │
│  │ 4.3 Query MEC database for implementation class                  │   │
│  │ 4.4 Locate exact file path in javaMapping.db                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 5: CONTEXT BUILDING (30 seconds)                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 5.1 Compile similar SR workarounds                               │   │
│  │ 5.2 Add Java file metadata (if Java error)                       │   │
│  │ 5.3 Add code snippets from comcast_code.db                       │   │
│  │ 5.4 Add resolution mapping guidelines                            │   │
│  │ 5.5 Add detection analysis evidence                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 6: LLM GENERATION (30-60 seconds)                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 6.1 Build prompt from template (prompt/prompt.txt)               │   │
│  │ 6.2 Inject 5 context sources                                     │   │
│  │ 6.3 Send to ChatGPT API                                          │   │
│  │ 6.4 Parse structured response                                    │   │
│  │ 6.5 Extract: Java analysis, workaround, troubleshooting steps    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  PHASE 7: OUTPUT (10 seconds)                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 7.1 Format as Excel row                                          │   │
│  │ 7.2 Add to output DataFrame                                      │   │
│  │ 7.3 Save to RAG/llm output/                                      │   │
│  │ 7.4 Update feedback database with new workaround                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Priority Calculation Formula

```python
def calculate_priority(match: Dict, feedback_storage: WorkaroundFeedbackStorage) -> float:
    """
    Calculate priority score for semantic matches.
    
    Formula:
        priority = (similarity * SIMILARITY_WEIGHT) + (normalized_votes * VOTE_WEIGHT)
    
    Default Weights:
        SIMILARITY_WEIGHT = 0.7 (70%)
        VOTE_WEIGHT = 0.3 (30%)
    
    Vote Normalization:
        - Score = upvotes - downvotes
        - Normalized = score / max_score_in_batch (0.0 to 1.0)
        - If no votes, normalized = 0.5 (neutral)
    """
    
    SIMILARITY_WEIGHT = 0.7
    VOTE_WEIGHT = 0.3
    
    similarity = match.get('similarity', 0)
    sr_id = match.get('sr_id', '')
    
    # Get vote score
    votes = feedback_storage.get_votes(sr_id, 'ai')
    vote_score = votes.get('score', 0)
    
    # Normalize votes (sigmoid-like normalization)
    normalized_votes = (vote_score + 10) / 20  # Maps -10..+10 to 0..1
    normalized_votes = max(0, min(1, normalized_votes))  # Clamp to 0-1
    
    priority = (similarity * SIMILARITY_WEIGHT) + (normalized_votes * VOTE_WEIGHT)
    
    return priority
```

---

## ☕ Java Error Detection Algorithm

### 5-Source Voting System

```
┌─────────────────────────────────────────────────────────────────────┐
│                     JAVA ERROR DETECTION VOTING                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   SOURCE 1: Category Analysis                                       │
│   ├── Check Resolution Category for Java keywords                   │
│   ├── Check SLA Resolution Categorization T1                        │
│   ├── Keywords: "code", "backend", "application error", etc.        │
│   └── Vote: JAVA / NON_JAVA / UNKNOWN                               │
│                                                                     │
│   SOURCE 2: Semantic Workaround                                     │
│   ├── Scan for Java indicators (regex patterns)                     │
│   ├── Patterns: exceptions, packages, stack traces                  │
│   ├── Threshold: ≥3 indicators = JAVA                               │
│   └── Vote: JAVA / UNKNOWN                                          │
│                                                                     │
│   SOURCE 3: AI Workarounds                                          │
│   ├── Analyze AI-generated solutions from similar SRs               │
│   ├── Count Java indicators per SR                                  │
│   ├── Threshold: ≥3 SRs with Java indicators = JAVA                 │
│   └── Vote: JAVA / UNKNOWN                                          │
│                                                                     │
│   SOURCE 4: User Workarounds                                        │
│   ├── Analyze human-written solutions from similar SRs              │
│   ├── Count Java indicators per SR                                  │
│   ├── Threshold: ≥3 SRs with Java indicators = JAVA                 │
│   └── Vote: JAVA / UNKNOWN                                          │
│                                                                     │
│   SOURCE 5: Current SR                                              │
│   ├── Analyze Description + Notes directly                          │
│   ├── Scan for Java patterns in text                                │
│   ├── Threshold: ≥2 indicators = JAVA                               │
│   └── Vote: JAVA / UNKNOWN                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Java Indicator Patterns

```python
JAVA_INDICATORS = [
    # Java classes (CamelCase with specific suffixes)
    r'\b[A-Z][a-zA-Z0-9]*(Service|Controller|Repository|Manager|Handler|Impl|Processor)\b',
    
    # Java exceptions
    r'(Exception|Error)(?!\s*:)',
    r'NullPointerException|SQLException|IOException|ClassNotFoundException',
    
    # Java packages
    r'com\.[a-z]+\.[a-z]+',
    r'org\.amdocs',
    r'com\.amdocs',
    r'com\.comcast',
    
    # Java files
    r'\.java\b',
    
    # Java commands
    r'mvn\s+(clean\s+)?install',
    r'restart\s+(tomcat|jboss|wildfly)',
    r'systemctl\s+restart',
    
    # Java tools
    r'\b(jstack|jmap|jconsole|jvisualvm|catalina)\b',
    
    # Stack traces
    r'at\s+com\.',
    r'at\s+org\.',
    r'at\s+java\.',
]
```

### Confidence Calculation

```python
def calculate_confidence(votes: Dict[str, str]) -> Tuple[str, Dict]:
    """
    Calculate confidence level from voting results.
    
    Args:
        votes: Dict mapping source -> vote (JAVA/NON_JAVA/UNKNOWN)
    
    Returns:
        confidence: str (HIGH/MEDIUM/LOW/VERY_LOW/UNKNOWN)
        metadata: Dict with calculation details
    """
    
    java_votes = sum(1 for v in votes.values() if v == 'JAVA')
    non_java_votes = sum(1 for v in votes.values() if v == 'NON_JAVA')
    unknown_votes = sum(1 for v in votes.values() if v == 'UNKNOWN')
    
    meaningful_votes = java_votes + non_java_votes
    
    if meaningful_votes == 0:
        return 'UNKNOWN', {'reason': 'No meaningful votes'}
    
    # Determine winner
    is_java = java_votes > non_java_votes
    
    if is_java:
        winning_ratio = java_votes / meaningful_votes
    else:
        winning_ratio = non_java_votes / meaningful_votes
    
    # Confidence thresholds
    if winning_ratio >= 0.8 and meaningful_votes >= 3:
        confidence = 'HIGH'      # 80%+ agreement with 3+ voters
    elif winning_ratio >= 0.67 and meaningful_votes >= 3:
        confidence = 'MEDIUM'    # 67%+ agreement with 3+ voters
    elif winning_ratio >= 0.6 or (winning_ratio >= 0.5 and meaningful_votes >= 4):
        confidence = 'LOW'       # 60%+ agreement OR 50%+ with 4+ voters
    else:
        confidence = 'VERY_LOW'  # < 60% agreement
    
    return confidence, {
        'winning_ratio': f"{winning_ratio:.1%}",
        'java_votes': java_votes,
        'non_java_votes': non_java_votes,
        'meaningful_votes': meaningful_votes
    }
```

---

## 🔍 Activity Name Extraction

### 5-Method Combined Approach

```
┌─────────────────────────────────────────────────────────────────────┐
│                   ACTIVITY EXTRACTION METHODS                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  METHOD 1: REGEX PATTERNS (Confidence: 0.90)                        │
│  ├── Pattern: Activity:\s*([A-Z][a-zA-Z]+)                          │
│  ├── Pattern: (Validate|Create|Update|Delete)...[A-Z][a-zA-Z]+      │
│  ├── Pattern: [A-Z][a-zA-Z]+Impl                                    │
│  └── Fastest method, highest confidence when match found            │
│                                                                     │
│  METHOD 2: KEYWORD MATCHING (Confidence: up to 0.80)                │
│  ├── Split CamelCase: ValidateAddress → ["validate", "address"]     │
│  ├── Match against pre-built keyword index                          │
│  ├── Score: overlap / total_keywords                                │
│  └── Threshold: ≥50% keyword overlap                                │
│                                                                     │
│  METHOD 3: SEMANTIC SEARCH (Confidence: similarity * 0.75)          │
│  ├── Embed SR text → 384-dim vector                                 │
│  ├── Search comcast_code.db for similar code                        │
│  ├── Extract activity name from file path                           │
│  └── Threshold: ≥50% similarity                                     │
│                                                                     │
│  METHOD 4: HISTORICAL MINING (Confidence: 0.70)                     │
│  ├── Search top 3 similar historical SRs                            │
│  ├── Apply regex patterns to workarounds                            │
│  ├── Collect activity names from past resolutions                   │
│  └── Most common = likely correct                                   │
│                                                                     │
│  METHOD 5: CLASS INDEX LOOKUP (Confidence: 0.85)                    │
│  ├── Load comcast_java_classes.pkl                                  │
│  ├── Direct lookup of CamelCase names in text                       │
│  ├── Match against known class names                                │
│  └── High confidence for exact matches                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Score Aggregation

```python
def aggregate_candidates(candidates: List[Dict]) -> Dict:
    """
    Aggregate scores from multiple methods.
    
    Logic:
        - Same activity from multiple methods = higher total score
        - Final confidence based on:
            - Total score ≥ 1.5 OR ≥2 methods = HIGH
            - Total score ≥ 0.7 = MEDIUM
            - Otherwise = LOW
    """
    
    activity_scores = {}
    
    for candidate in candidates:
        name = candidate['name']
        if name not in activity_scores:
            activity_scores[name] = {'score': 0, 'methods': []}
        
        activity_scores[name]['score'] += candidate['confidence']
        
        if candidate['method'] not in activity_scores[name]['methods']:
            activity_scores[name]['methods'].append(candidate['method'])
    
    # Sort by score descending
    ranked = sorted(activity_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    
    if ranked:
        best_name, best_info = ranked[0]
        
        # Determine confidence
        if best_info['score'] >= 1.5 or len(best_info['methods']) >= 2:
            confidence = 'High'
        elif best_info['score'] >= 0.7:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'activity_name': best_name,
            'confidence': confidence,
            'methods_used': ', '.join(best_info['methods']),
            'total_score': best_info['score']
        }
    
    return {'activity_name': None, 'confidence': 'Low'}
```

---

## 🔎 Semantic Search Implementation

### Embedding Model

```python
# Model: all-MiniLM-L6-v2
# Dimensions: 384
# Max Sequence Length: 256 tokens
# Speed: ~14,000 sentences/second on CPU

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(text)  # Returns: numpy array (384,)
```

### Similarity Calculation

```python
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(query_embedding: np.ndarray, 
                         corpus_embeddings: np.ndarray) -> np.ndarray:
    """
    Calculate cosine similarity between query and corpus.
    
    Formula:
        similarity = (A · B) / (||A|| × ||B||)
    
    Range: -1.0 to 1.0 (in practice: 0.0 to 1.0 for normalized vectors)
    
    Interpretation:
        1.0 = Identical meaning
        0.7+ = Very similar
        0.5-0.7 = Related
        <0.5 = Different topics
    """
    
    # Ensure 2D shape for sklearn
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)
    
    similarities = cosine_similarity(query_embedding, corpus_embeddings)
    
    return similarities[0]  # Return 1D array of scores
```

### History Search Algorithm

```python
def search_history_semantically(self, query: str, top_k: int = 5) -> List[Dict]:
    """
    Search historical SRs using semantic similarity + vote ranking.
    
    Steps:
        1. Preprocess query text (if preprocessor available)
        2. Encode query to 384-dim vector
        3. Calculate cosine similarity with all historical embeddings
        4. Filter by threshold (≥0.60)
        5. Fetch vote scores for each match
        6. Calculate priority: (similarity * 0.7) + (normalized_votes * 0.3)
        7. Sort by priority and return top_k
    """
    
    # Preprocess query
    if self.preprocessor:
        query = self.preprocessor.clean_for_semantic_search(query)
    
    # Encode
    query_embedding = self.semantic_model.encode(query)
    
    # Calculate similarities
    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),
        self.history_embeddings
    )[0]
    
    # Get top matches above threshold
    threshold = 0.60
    matches = []
    
    for idx in np.argsort(similarities)[::-1]:  # Descending order
        if similarities[idx] < threshold:
            break
        
        sr_data = self.history_data[idx]
        sr_id = sr_data.get('sr_id', '')
        
        # Get vote score
        vote_data = self.feedback_storage.get_votes(sr_id, 'ai') if self.feedback_storage else {}
        vote_score = vote_data.get('score', 0)
        
        # Calculate priority
        normalized_votes = (vote_score + 10) / 20
        priority = (similarities[idx] * 0.7) + (normalized_votes * 0.3)
        
        matches.append({
            'sr_id': sr_id,
            'similarity': float(similarities[idx]),
            'priority': float(priority),
            'vote_score': vote_score,
            **sr_data
        })
    
    # Sort by priority and return top_k
    matches.sort(key=lambda x: x['priority'], reverse=True)
    return matches[:top_k]
```

---

## 📊 Feedback & Learning System

### Vote Schema

```sql
-- Main feedback table
CREATE TABLE workaround_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_id TEXT NOT NULL,
    workaround_type TEXT NOT NULL,  -- 'original', 'ai', 'user_corrected'
    workaround_text TEXT NOT NULL,   -- First 500 chars for reference
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    score INTEGER GENERATED ALWAYS AS (upvotes - downvotes) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sr_id, workaround_type)
);

-- Vote history (for tracking individual votes)
CREATE TABLE vote_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_id TEXT NOT NULL,
    workaround_type TEXT NOT NULL,
    vote_type TEXT NOT NULL,  -- 'upvote' or 'downvote'
    user_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for performance
CREATE INDEX idx_sr_workaround ON workaround_feedback(sr_id, workaround_type);
CREATE INDEX idx_vote_score ON workaround_feedback(score DESC, upvotes DESC);
CREATE INDEX idx_sr_id ON workaround_feedback(sr_id);
```

### Learning Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CONTINUOUS LEARNING LOOP                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. USER INTERACTS                                                  │
│     ├── Views AI workaround                                         │
│     └── Clicks 👍 (upvote) or 👎 (downvote)                         │
│                                                                     │
│  2. VOTE RECORDED                                                   │
│     ├── workaround_feedback table updated                           │
│     ├── vote_history table logged                                   │
│     └── score = upvotes - downvotes (auto-calculated)               │
│                                                                     │
│  3. NEXT SEARCH                                                     │
│     ├── Semantic similarity calculated (70% weight)                 │
│     ├── Vote score fetched (30% weight)                             │
│     └── Priority = combined score                                   │
│                                                                     │
│  4. RANKING AFFECTED                                                │
│     ├── Upvoted SRs rank higher → more exposure                     │
│     ├── Downvoted SRs rank lower → less exposure                    │
│     └── System self-improves over time                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📧 Email Integration

### Overview

The system can auto-fetch daily SR reports from Outlook and process through RAG pipeline.

**File**: `email_processing/email_fetcher.py`, `email_processing/email_to_rag_processor.py`

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     EMAIL TO RAG PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  STEP 1: OUTLOOK CONNECTION (Windows COM)                           │
│  ├── Uses win32com.client (pywin32)                                 │
│  ├── Connects to logged-in Outlook session                          │
│  ├── NO credentials needed (uses Windows session)                   │
│  └── Works with corporate Outlook/Exchange                          │
│                                                                     │
│  STEP 2: EMAIL SEARCH                                               │
│  ├── Filter by sender: SENDER_EMAIL                                 │
│  ├── Filter by subject: SUBJECT_PATTERN                             │
│  ├── Search last N days: --days-back parameter                      │
│  └── Find latest matching email                                     │
│                                                                     │
│  STEP 3: ATTACHMENT DOWNLOAD                                        │
│  ├── Filter by attachment name: ATTACHMENT_PATTERN                  │
│  ├── Download to: email_processing/downloads/email_reports/         │
│  ├── Add timestamp to filename                                      │
│  └── Return file path for RAG processing                            │
│                                                                     │
│  STEP 4: RAG PROCESSING (Optional)                                  │
│  ├── Call upload_and_merge_with_rag()                               │
│  ├── Run full RAG analysis pipeline                                 │
│  └── Save results to output/reports/                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### OutlookEmailFetcher Class

```python
class OutlookEmailFetcher:
    """
    Fetches daily SR reports from Outlook inbox.
    
    Configuration:
        SENDER_EMAIL: str - Email sender to filter
        SUBJECT_PATTERN: str - Subject line pattern
        ATTACHMENT_PATTERN: str - Attachment name pattern
    
    Methods:
        fetch_latest_report(days_back=2) -> Tuple[str, datetime]
        list_recent_emails(days_back=7) -> List[Dict]
        get_current_outlook_email() -> str
    """
```

### Email Configuration

```python
# In email_fetcher.py
SENDER_EMAIL = "GSSUTSMail@amdocs.com"        # Sender filter
SUBJECT_PATTERN = "Scheduled Report - Mukul"  # Subject filter  
ATTACHMENT_PATTERN = "mukul"                  # Attachment name filter
```

### EmailToRAGProcessor Class

```python
class EmailToRAGProcessor:
    """
    Complete pipeline: Email → Download → RAG Analysis
    
    Methods:
        fetch_from_email(days_back=2) -> bool
        run_rag_analysis(progress_callback=None) -> bool
        run_full_pipeline(days_back=2) -> Tuple[bool, str]
    """
```

### Usage Examples

```bash
# Full pipeline: Fetch + RAG
python email_processing/email_to_rag_processor.py

# Fetch only (no RAG)
python email_processing/email_to_rag_processor.py --fetch-only

# Search last 3 days
python email_processing/email_to_rag_processor.py --days-back 3

# Interactive mode
python email_processing/email_to_rag_processor.py -i
```

---

## 📈 SR Classification Algorithm

### Overview

Classifies SRs into difficulty levels: **Easy Win**, **Moderate**, or **Tough**.

**File**: `sr_feedback_app.py` (classify_sr_ticket function)

### Classification Levels

| Level | Score | Description | Typical Resolution |
|-------|-------|-------------|-------------------|
| **Easy Win** 🟢 | 1-2 | Quick fix, config change | Minutes to 1 hour |
| **Moderate** 🟡 | 3 | Standard issue, clear path | 1-4 hours |
| **Tough** 🔴 | 4-5 | Complex, needs investigation | 4+ hours |

### Classification Algorithm

```python
def classify_sr_ticket(
    description: str,
    notes: str = "",
    priority: str = "P3",
    workaround_text: str = "",
    interface_likelihood: float = 0.0,
    similar_tickets_count: int = 0,
    direct_to_interface_count: int = 0,
    resolved_with_wa_count: int = 0,
    wa_then_interface_count: int = 0
) -> dict:
    """
    Classify SR into Easy Win / Moderate / Tough
    
    Returns:
        {
            'classification': str,  # "Easy Win", "Moderate", "Tough"
            'difficulty_score': int  # 1-5
        }
    """
```

### Scoring Factors

```
┌─────────────────────────────────────────────────────────────────────┐
│                   SR CLASSIFICATION SCORING                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FACTOR 1: PRIORITY LEVEL                                           │
│  ├── P1 (Critical): +2 points (harder)                              │
│  ├── P2 (High): +1 point                                            │
│  ├── P3 (Medium): 0 points (baseline)                               │
│  └── P4 (Low): -1 point (easier)                                    │
│                                                                     │
│  FACTOR 2: EASY WIN KEYWORDS (reduces score)                        │
│  ├── "restart", "reboot", "refresh": -1 point                       │
│  ├── "config", "configuration", "setting": -1 point                 │
│  ├── "permission", "access", "role": -1 point                       │
│  └── "cache", "clear", "reset": -1 point                            │
│                                                                     │
│  FACTOR 3: TOUGH KEYWORDS (increases score)                         │
│  ├── "investigation", "RCA", "root cause": +1 point                 │
│  ├── "interface", "integration", "API": +1 point                    │
│  ├── "database", "migration", "schema": +1 point                    │
│  └── "timeout", "performance", "memory": +1 point                   │
│                                                                     │
│  FACTOR 4: INTERFACE LIKELIHOOD                                     │
│  ├── > 0.7: +2 points (likely needs interface team)                 │
│  ├── > 0.4: +1 point                                                │
│  └── <= 0.4: 0 points                                               │
│                                                                     │
│  FACTOR 5: HISTORICAL PATTERNS                                      │
│  ├── Most similar SRs resolved with WA: -1 point                    │
│  ├── Most went to interface: +1 point                               │
│  └── Mixed pattern: 0 points                                        │
│                                                                     │
│  FINAL SCORE: Sum of all factors, clamped to 1-5                    │
│                                                                     │
│  CLASSIFICATION:                                                    │
│  ├── Score 1-2: "Easy Win" 🟢                                       │
│  ├── Score 3: "Moderate" 🟡                                         │
│  └── Score 4-5: "Tough" 🔴                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Example Classification

```python
# Example 1: Easy Win
classify_sr_ticket(
    description="Please restart the application service",
    priority="P4",
    workaround_text="Restart tomcat"
)
# Result: {"classification": "Easy Win", "difficulty_score": 1}

# Example 2: Tough
classify_sr_ticket(
    description="Integration failing with timeout errors, needs RCA",
    priority="P1",
    interface_likelihood=0.8
)
# Result: {"classification": "Tough", "difficulty_score": 5}
```

---

## 💾 Database Schemas

### 1. javaMapping.db (SQLite)

```sql
CREATE TABLE java_classes (
    id INTEGER PRIMARY KEY,
    class_name TEXT NOT NULL,
    package TEXT,
    full_qualified_name TEXT,
    file_path TEXT,
    class_type TEXT,  -- 'class', 'interface', 'enum'
    annotations TEXT,
    methods TEXT,     -- JSON array of method names
    imports TEXT      -- JSON array of imports
);

-- Total: 11,795 Java classes
```

### 2. history_data.db (Pickle)

```python
# Structure: List[Dict]
{
    'sr_id': str,           # e.g., "CAS2575553"
    'description': str,     # Full SR description
    'notes': str,           # Technical notes
    'resolution_category': str,
    'sla_resolution_categorization_t1': str,
    'workaround': str,      # Combined workaround text
    'embedding': np.ndarray # 384-dim vector
}

# Total: 20,399+ historical SRs
```

### 2b. clean_history_data.db (Pickle)

```python
# Structure: Same as history_data.db but with preprocessed text
# All SR descriptions and notes cleaned using SRTextPreprocessor
{
    'sr_id': str,
    'description': str,     # CLEANED - removed customer info, IDs, timestamps
    'notes': str,           # CLEANED
    'workaround': str,
    'embedding': np.ndarray # Re-embedded after cleaning
}

# Total: 20,399+ SRs (same data, cleaner text)
# Purpose: Better semantic matching accuracy
```

### 3. comcast_code.db (FAISS)

```python
# Index: FAISS flat L2 index
# Vectors: 384 dimensions each
# Total chunks: ~500,000 code segments

# Metadata structure per chunk:
{
    'file_path': str,      # Full path to Java file
    'chunk_id': int,       # Position in file
    'start_line': int,     # Line number start
    'end_line': int,       # Line number end
    'content': str         # Actual code text
}
```

### 4. MEC Database (PostgreSQL)

```sql
CREATE TABLE activity_mapping (
    id SERIAL PRIMARY KEY,
    activity_name VARCHAR(255) NOT NULL,
    impl_class_name VARCHAR(255),
    package_name VARCHAR(500),
    file_name VARCHAR(255),
    module_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_name ON activity_mapping(activity_name);
CREATE INDEX idx_impl_class ON activity_mapping(impl_class_name);
```

### 5. people_skills.db (SQLite)

```sql
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT,
    skills TEXT,           -- JSON array: ["Java", "Python", "CMFS"]
    expertise_areas TEXT,  -- JSON array of domain expertise
    availability TEXT,     -- 'available', 'busy', 'on-leave'
    assigned_count INTEGER DEFAULT 0
);

CREATE TABLE skill_categories (
    id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,    -- e.g., "Java Backend"
    keywords TEXT,                  -- JSON array of matching keywords
    team_member_ids TEXT            -- JSON array of member IDs
);

-- Purpose: Skills-based SR assignment
```

### 6. resolution_mapping.db (SQLite/Pickle)

```python
# Structure: Category → Resolution Guidelines
{
    'category': str,           # e.g., "Backend - Order"
    'subcategory': str,
    'resolution_template': str,
    'common_causes': List[str],
    'recommended_steps': List[str],
    'embedding': np.ndarray
}

# Total: 145 resolution categories
# Purpose: Best practice guidelines per category
```

### 7. workaround_feedback.db (SQLite)

```sql
CREATE TABLE workaround_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_id TEXT NOT NULL,
    workaround_type TEXT NOT NULL,       -- 'ai', 'historical', 'resolution'
    workaround_text TEXT NOT NULL,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    score INTEGER GENERATED ALWAYS AS (upvotes - downvotes) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sr_id, workaround_type)
);

CREATE TABLE vote_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_id TEXT NOT NULL,
    workaround_type TEXT NOT NULL,
    vote_type TEXT NOT NULL,             -- 'up' or 'down'
    user_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Purpose: Track user votes for learning
```

### 8. sr_tracking.db (SQLite)

```sql
CREATE TABLE sr_processing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_id TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'pending',       -- pending, processing, completed, failed
    input_file TEXT,
    output_file TEXT,
    processing_time_seconds REAL,
    java_detected BOOLEAN,
    activity_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Purpose: Track SR processing status
```

---

## 📝 LLM Prompt Engineering

### Prompt Template Structure

**File**: `prompt/prompt.txt`

```
===== ROLE =====
Expert SR analysis system with 5 context sources.

===== CRITICAL RULES (Priority Order) =====
🔴 PRIORITY 1: Use ONLY exact file paths from context
🟡 PRIORITY 2: Quote EXACT text as evidence
🟢 PRIORITY 3: Generate NEW workaround steps

❌ FORBIDDEN: Generic steps, vague locations, copying solutions

===== 5 CONTEXT SOURCES =====
1. Java Backend Metadata (javaMapping.db)
2. Java Code Snippets (comcast_code.db)
3. Historical SR Matches (clean_history_data.db)
4. Resolution Mapping Guidelines
5. Detection Analysis Evidence

===== OUTPUT FORMAT =====
**REASONING:** (Steps 1-5 analysis)
**JAVA ERROR ANALYSIS:** (Detection results)
**AI WORKAROUND:** (5-10 numbered steps)
**TROUBLESHOOTING STEPS:** (Investigation flow)

===== QUALITY CHECKLIST =====
□ Showed reasoning?
□ Used actual paths from context?
□ Avoided generic steps?
□ Each step specific and actionable?
```

### Context Injection Format

```python
def build_prompt(sr_data: Dict, context: Dict) -> str:
    """
    Build complete prompt with all 5 context sources.
    """
    
    prompt = load_template("prompt/prompt.txt")
    
    # Inject contexts
    prompt += f"""
    
===== CONTEXT #1: JAVA BACKEND METADATA =====
{context.get('java_metadata', 'N/A')}

===== CONTEXT #2: JAVA CODE SNIPPETS =====
{context.get('java_code', 'N/A')}

===== CONTEXT #3: HISTORICAL SR MATCHES =====
{format_historical_matches(context.get('similar_srs', []))}

===== CONTEXT #4: RESOLUTION MAPPING GUIDELINES =====
{context.get('resolution_mapping', 'N/A')}

===== CONTEXT #5: DETECTION ANALYSIS =====
Is Java Error: {context.get('is_java_error', 'Unknown')}
Confidence: {context.get('confidence', 'Unknown')}
Evidence: {context.get('evidence', 'N/A')}

===== INPUT SR =====
SR ID: {sr_data.get('SR ID', 'N/A')}
Summary: {sr_data.get('Summary', 'N/A')}
Full Description: {sr_data.get('Description', 'N/A')}
Notes: {sr_data.get('Notes', 'N/A')}
Resolution Category: {sr_data.get('Resolution Category', 'N/A')}
"""
    
    return prompt
```

---

## 🔌 API Specifications

### Flask Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/` | GET | Login selection page | No |
| `/user-login` | GET/POST | User login page | No |
| `/admin-login` | GET/POST | Admin login page | No |
| `/feedback` | GET | Main feedback dashboard | User |
| `/search` | POST | Search SR by ID | User |
| `/admin/upload` | GET/POST | File upload UI | Admin |
| `/admin/process` | POST | Start RAG processing | Admin |
| `/admin/download/<id>` | GET | Download results | Admin |
| `/admin/remove-sr` | GET/POST | Remove SR from system | Admin |
| `/admin/today` | GET | Today's uploads view | Admin |
| `/skills` | GET | Team skills view | User |
| `/api/sr/<sr_id>` | GET | Get SR details (JSON) | No |
| `/api/vote` | POST | Record vote (JSON) | No |
| `/api/regenerate` | POST | Regenerate AI analysis | User |
| `/logout` | GET | Logout and clear session | No |

### API Request/Response Examples

**Search SR:**
```http
POST /search
Content-Type: application/x-www-form-urlencoded

sr_id=CAS2575553

---
Response: HTML page with SR details and workaround
```

**Record Vote (API):**
```http
POST /api/vote
Content-Type: application/json

{
    "sr_id": "CAS2575553",
    "workaround_type": "ai",
    "vote_type": "upvote"
}

---
Response:
{
    "success": true,
    "new_score": 5,
    "message": "Vote recorded"
}
```

---

## ⚙️ Configuration Parameters

### Environment Variables

```bash
# ChatGPT Configuration
CHATGPT_API_URL=https://ai-framework1:8085/api/v1/call_llm
CHATGPT_MODEL=gpt-4.1
TOKENS_FILE=Tokens.xlsx

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here

# Database Paths
HISTORY_DB_PATH=vector store/clean_history_data.db
JAVA_MAPPING_PATH=vector store/javaMapping.db

# Email Configuration (in email_fetcher.py)
SENDER_EMAIL=GSSUTSMail@amdocs.com
SUBJECT_PATTERN=Scheduled Report - Mukul
ATTACHMENT_PATTERN=mukul
CODE_DB_PATH=vector store/comcast_code.db
FEEDBACK_DB_PATH=vector store/workaround_feedback.db

# MEC Database
MEC_HOST=localhost
MEC_PORT=5432
MEC_DATABASE=mec_db
MEC_USER=admin
MEC_PASSWORD=password

# Processing Parameters
SIMILARITY_THRESHOLD=0.60
TOP_K_MATCHES=5
MAX_TOKENS=2048
TEMPERATURE=0.3
```

### Tunable Parameters

```python
# In multi_model_rag_pipeline_chatgpt.py

# Semantic Search
SIMILARITY_THRESHOLD = 0.60      # Minimum similarity to include
TOP_K_HISTORICAL = 5             # Max similar SRs to return
TOP_K_CODE = 10                  # Max code chunks to return

# Priority Calculation
SIMILARITY_WEIGHT = 0.7          # Weight for semantic similarity
VOTE_WEIGHT = 0.3                # Weight for user votes

# LLM Generation
MAX_TOKENS = 2048                # Response length limit
TEMPERATURE = 0.3                # Creativity (lower = deterministic)
TOP_P = 0.95                     # Nucleus sampling
TIMEOUT_SECONDS = 2400           # 40 minutes per SR

# Java Detection
MIN_JAVA_INDICATORS = 3          # For semantic workaround
MIN_SRS_WITH_JAVA = 3            # For AI/User workarounds
MIN_CURRENT_SR_INDICATORS = 2    # For current SR analysis

# Activity Extraction
MIN_KEYWORD_OVERLAP = 0.5        # 50% keyword match
MIN_SEMANTIC_SIMILARITY = 0.5    # For code search
HIGH_CONFIDENCE_SCORE = 1.5      # Score threshold
```

---

## 🚀 Performance Tuning

### Memory Optimization

```python
# Load embeddings lazily
class LazyEmbeddingLoader:
    def __init__(self, path):
        self.path = path
        self._embeddings = None
    
    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = np.load(self.path, mmap_mode='r')
        return self._embeddings

# Use memory mapping for large arrays
embeddings = np.load('embeddings.npy', mmap_mode='r')
```

### Batch Processing Optimization

```python
# Process SRs in batches for efficiency
BATCH_SIZE = 5

def process_batch(srs: List[Dict]) -> List[Dict]:
    # Pre-encode all queries at once
    queries = [sr['Description'] for sr in srs]
    embeddings = model.encode(queries, batch_size=BATCH_SIZE)
    
    results = []
    for sr, embedding in zip(srs, embeddings):
        # Use pre-computed embedding
        matches = search_with_embedding(embedding)
        result = process_single_sr(sr, matches)
        results.append(result)
    
    return results
```

### Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_java_class_info(class_name: str) -> Dict:
    """Cache Java class lookups"""
    conn = sqlite3.connect(JAVA_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM java_classes WHERE class_name = ?",
        (class_name,)
    )
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else {}

# Clear cache periodically
def clear_caches():
    get_java_class_info.cache_clear()
```

### Index Optimization

```python
# Pre-build activity index at startup (not per-request)
class ImprovedActivityFinder:
    _instance = None
    _activity_index = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._activity_index = cls._build_activity_index()
        return cls._instance
    
    @classmethod
    def _build_activity_index(cls):
        # Build once, reuse forever
        return build_index_from_db()
```

---

## 📈 Monitoring & Logging

### Log Levels

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('sr_analysis.log'),
        logging.StreamHandler()
    ]
)

# Log levels by component
LOGGING_CONFIG = {
    'rag_pipeline': logging.INFO,
    'java_analyzer': logging.DEBUG,
    'activity_finder': logging.INFO,
    'feedback_storage': logging.WARNING,
    'chatgpt_client': logging.INFO
}
```

### Metrics to Track

```python
# Processing metrics
METRICS = {
    'total_srs_processed': 0,
    'avg_processing_time_seconds': 0,
    'java_detection_accuracy': 0,
    'activity_extraction_success_rate': 0,
    'avg_similarity_score': 0,
    'total_upvotes': 0,
    'total_downvotes': 0,
    'feedback_ratio': 0
}
```

---

## 📚 References

- **OpenAI Documentation**: https://platform.openai.com/docs
- **LangChain Documentation**: https://python.langchain.com/docs
- **SentenceTransformers**: https://www.sbert.net/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Flask**: https://flask.palletsprojects.com/
- **Streamlit**: https://streamlit.io/

---

**Document maintained by**: Praveer Kumar Deo (praveerd@amdocs.com)  
**Last Technical Review**: December 16, 2024

