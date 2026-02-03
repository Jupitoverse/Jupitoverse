# 🔄 Multi-Model SR Analysis Pipeline - LLM Flow Documentation

> 📍 **Location:** `sr-analyzer/semantic-resolution/RAG/rag/LLM_FLOW_DOCUMENTATION.md`  
> 🔧 **Main Pipeline:** `multi_model_rag_pipeline_chatgpt.py`

## Overview

This document describes the complete flow of LLM calls that occur after a user uploads an Excel file containing Service Requests (SRs) for analysis.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER UPLOADS EXCEL FILE                           │
│                        (Service Requests Data)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PIPELINE INITIALIZATION                            │
│  • Load API Tokens from Tokens.xlsx                                         │
│  • Load Sentence Transformer Model (all-MiniLM-L6-v2)                       │
│  • Connect to Vector Stores & Databases                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │    FOR EACH SR IN EXCEL FILE    │
                    └─────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
   SEMANTIC SEARCH            LLM CALL 1-4              OUTPUT GENERATION
   (No LLM - Local)         (ChatGPT API)              (Excel Results)
```

---

## 📁 Data Sources Used

| # | Source | Type | Purpose |
|---|--------|------|---------|
| 1 | `javaMapping.db` | SQLite | Java class metadata lookup |
| 2 | `comcast_code.db` | FAISS (NumPy + Pickle) | Backend code semantic search |
| 3 | `clean_history_data.db` | ChromaDB | Historical SR semantic search |
| 4 | PostgreSQL (MEC) | Remote DB | Activity implementation validation |

---

## 🚀 Complete Flow After Excel Upload

### STEP 0: Excel Reading & Initialization

```
Input: Excel file from /RAG/input/ folder
       ├── SR ID
       ├── Priority / Customer Priority
       ├── Description
       ├── Notes
       ├── Resolution Category
       └── Status Reason
```

---

### STEP 1: Semantic Search (No LLM)

**Purpose:** Find similar historical SRs using vector embeddings

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEMANTIC SEARCH                              │
│                    (Local - No LLM)                             │
├─────────────────────────────────────────────────────────────────┤
│ Input:  SR Description + Notes                                  │
│ Process:                                                        │
│   1. Encode text using SentenceTransformer                      │
│   2. Compute cosine similarity against history embeddings       │
│   3. Return top 10 matches (threshold > 0.30)                   │
│ Output: List of historical SRs with similarity scores           │
└─────────────────────────────────────────────────────────────────┘
```

---

### STEP 2: Filter Garbage Workarounds (No LLM)

**Garbage Patterns Filtered:**
- `N/A`, `NA`, `None`, `Null`, `-`, `.`
- `Not available`, `Not applicable`
- `Escalated`, `Closed`, `Resolved`, `Fixed`
- Text < 15 characters

---

### 🤖 LLM CALL 1: Find Semantic Workaround

**Trigger:** Called ONLY if top match has similarity < 50%

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM CALL 1                                   │
│           FIND SEMANTIC WORKAROUND                              │
├─────────────────────────────────────────────────────────────────┤
│ Model:  gpt-4.1                                                 │
│ API:    https://ai-framework1:8085/api/v1/call_llm              │
├─────────────────────────────────────────────────────────────────┤
│ INPUT CONTEXT:                                                  │
│   • Current SR: ID, Description, Notes, Resolution Category     │
│   • Up to 10 historical matches with similarity scores          │
│   • Workarounds from each historical SR                         │
├─────────────────────────────────────────────────────────────────┤
│ TASK:                                                           │
│   1. Analyze current SR's core issue                            │
│   2. Find BEST matching workaround from history                 │
│   3. Ignore garbage workarounds                                 │
│   4. COMBINE best steps if multiple matches exist               │
│   5. Return "NO_MATCH" if no useful workaround found            │
├─────────────────────────────────────────────────────────────────┤
│ OUTPUT (JSON):                                                  │
│   {                                                             │
│     "matched_sr_id": "<SR ID or null>",                         │
│     "similarity_reason": "<why this matches>",                  │
│     "semantic_workaround": "<workaround text>",                 │
│     "quality_score": 0.0-1.0                                    │
│   }                                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🤖 LLM CALL 2: Java Error Detection (5-Source Voting)

**Always Called:** Yes - for every SR

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM CALL 2                                   │
│         JAVA ERROR DETECTION (5-SOURCE VOTING)                  │
├─────────────────────────────────────────────────────────────────┤
│ 5 VOTING SOURCES:                                               │
│                                                                 │
│   SOURCE 1: RESOLUTION CATEGORIES                               │
│   SOURCE 2: SEMANTIC WORKAROUND                                 │
│   SOURCE 3: AI WORKAROUNDS FROM SIMILAR SRs                     │
│   SOURCE 4: USER WORKAROUNDS FROM SIMILAR SRs                   │
│   SOURCE 5: CURRENT SR CONTENT                                  │
├─────────────────────────────────────────────────────────────────┤
│ JAVA INDICATORS CHECKED:                                        │
│   • Java classes: *Service, *Controller, *Repository, *Impl    │
│   • Exceptions: NullPointerException, SQLException, etc.        │
│   • Packages: com.amdocs.*, com.comcast.*, org.*                │
│   • Stack traces: "at com.", "at org.", "at java."              │
│   • Commands: mvn, systemctl, jstack, jmap                      │
├─────────────────────────────────────────────────────────────────┤
│ VOTING RULES:                                                   │
│   Each source votes: JAVA | NON_JAVA | UNKNOWN                  │
│   Final: is_java_error = (java_votes > non_java_votes)          │
├─────────────────────────────────────────────────────────────────┤
│ CONFIDENCE LEVELS:                                              │
│   HIGH:     ≥80% agreement with ≥3 meaningful votes             │
│   MEDIUM:   ≥67% agreement with ≥3 meaningful votes             │
│   LOW:      ≥60% agreement OR ≥50% with ≥4 voters               │
│   VERY_LOW: <60% agreement                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🤖 LLM CALL 3: Extract Activity Names (with Retry Loop)

**Trigger:** Called ONLY if `is_java_error = true`

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM CALL 3                                   │
│              EXTRACT ACTIVITY NAMES                             │
│              (With Retry Loop for Validation)                   │
├─────────────────────────────────────────────────────────────────┤
│ Max Retries: 2 (3 total attempts)                               │
├─────────────────────────────────────────────────────────────────┤
│ INPUT CONTEXT:                                                  │
│   • SR Description + Notes                                      │
│   • Semantic workaround from LLM Call 1                         │
│   • Top 3 historical workarounds                                │
│   • Java code context from comcast_code.db                      │
├─────────────────────────────────────────────────────────────────┤
│ ACTIVITY PATTERNS SEARCHED:                                     │
│   • CamelCase verbs: Validate*, Create*, Update*, Delete*       │
│   • Domain keywords: *Address, *Order, *Customer, *Payment      │
│   • Impl suffix: ValidateAddressImpl → ValidateAddress          │
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ACTIVITY VALIDATION                             │
│              (PostgreSQL via ActivityFinder)                    │
├─────────────────────────────────────────────────────────────────┤
│ For each extracted activity name:                               │
│   Query PostgreSQL for implementation class                     │
│   If FOUND ✅: Add to validated list                            │
│   If NOT FOUND ❌: Add to retry list                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🤖 LLM CALL 4a: Java Resolution

**Trigger:** Called if `is_java_error = true`

**Output:** 8-15 step AI workaround including:
- Investigation steps (logs, files to check)
- Analysis steps (root cause identification)
- Resolution steps (exact fix with commands)
- Verification steps (confirm fix worked)

---

### 🤖 LLM CALL 4b: General Resolution

**Trigger:** Called if `is_java_error = false`

**Output:** 8-15 step AI workaround for non-Java issues

---

## 📈 LLM Call Summary Per SR

| Scenario | LLM Calls | Description |
|----------|-----------|-------------|
| Non-Java (high similarity) | 2 | LLM 2, LLM 4b |
| Non-Java (low similarity) | 3 | LLM 1, LLM 2, LLM 4b |
| Java (no retry) | 3-4 | LLM 2, LLM 3, LLM 4a |
| Java (low similarity, no retry) | 4 | LLM 1, LLM 2, LLM 3, LLM 4a |
| Java (with retries) | 4-6 | LLM 1, LLM 2, LLM 3×3, LLM 4a |

---

## 🔧 Token Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN ROTATION SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│ Source: tokens/Tokens.xlsx                                      │
│                                                                 │
│ Token Rotation Logic:                                           │
│   1. Load all tokens at startup                                 │
│   2. Use current token for API calls                            │
│   3. On 429 (quota exhausted):                                  │
│      → Mark current token as exhausted                          │
│      → Rotate to next available token                           │
│      → Retry the failed call                                    │
│   4. If all tokens exhausted → Return error                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📤 Output Format

| Column | Description |
|--------|-------------|
| `SR ID` | Service Request identifier |
| `Is Java Error` | Yes/No (from 5-source voting) |
| `Confidence` | HIGH/MEDIUM/LOW/VERY_LOW |
| `Java Votes` | Count of JAVA votes (0-5) |
| `Non-Java Votes` | Count of NON_JAVA votes (0-5) |
| `Activity Names` | Validated Java activities |
| `Implementation Classes` | Corresponding *Impl classes |
| `AI Workaround` | Generated 8-15 step workaround |

---

## 🔗 API Details

| Parameter | Value |
|-----------|-------|
| **API URL** | `https://ai-framework1:8085/api/v1/call_llm` |
| **Model** | `gpt-4.1` |
| **Timeout** | 300 seconds |
| **SSL Verify** | Disabled |

---

*Last Updated: January 2025*




