# 📚 SR-Analyzer User & Admin Guide

> **Complete Guide for Using the SR Feedback System**

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [User Portal Guide](#user-portal-guide)
4. [Admin Portal Guide](#admin-portal-guide)
5. [Understanding AI Workarounds](#understanding-ai-workarounds)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## 🎯 System Overview

### What is SR-Analyzer?

SR-Analyzer is an **AI-powered Service Request analysis system** that:

- 🔍 **Searches** 1.18M+ historical SRs to find similar issues
- 🤖 **Generates** intelligent workarounds using GPT-4.1
- 🎯 **Detects** Java/backend errors automatically
- 👥 **Assigns** SRs to team members based on skills
- 📝 **Learns** from user feedback to improve suggestions

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    SR-ANALYZER WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1️⃣  ADMIN uploads Excel file with SRs                        │
│        └── OR system fetches from Outlook (Windows only)        │
│                         ↓                                        │
│   2️⃣  SEMANTIC SEARCH finds similar historical SRs              │
│        └── Uses AI embeddings on 1.18M+ records                 │
│                         ↓                                        │
│   3️⃣  5-LLM PIPELINE analyzes each SR:                          │
│        • LLM 1: Extract workaround from matches                 │
│        • LLM 2: Detect if Java/backend error (voting)           │
│        • LLM 3: Extract Java activity names                     │
│        • LLM 4: Generate resolution steps                       │
│        • LLM 5: Assign to team member                           │
│                         ↓                                        │
│   4️⃣  USER views SR and AI workaround                           │
│        └── Provides feedback or corrections                     │
│                         ↓                                        │
│   5️⃣  SYSTEM LEARNS from feedback                               │
│        └── Improves future suggestions                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Operating System** | Windows 10/11, Linux, or macOS |
| **Python** | Version 3.10, 3.11, or 3.12 |
| **API Tokens** | `tokens/Tokens.xlsx` with valid API tokens |
| **Network** | Access to `ai-framework1:8085` |

### First Time Setup

#### Windows

```cmd
cd semantic-resolution
First_time_MultiModel.bat
```

#### Linux/Mac

```bash
cd semantic-resolution
chmod +x First_time_MultiModel.sh
./First_time_MultiModel.sh
```

This will:
1. ✅ Check Python version (3.10-3.12 required)
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Verify databases and vector stores
5. ✅ Start the application

### Regular Startup

#### Windows

```cmd
cd semantic-resolution
START_MULTIMODEL_RAG.bat
```

#### Linux/Mac

```bash
cd semantic-resolution
./START_MULTIMODEL_RAG.sh
```

### Access Points

| Portal | URL | Credentials |
|--------|-----|-------------|
| **User Portal** | http://localhost:5000 | None required (or Azure AD) |
| **Admin Portal** | http://localhost:5000/admin | `admin` / `admin123` |

---

## 👤 User Portal Guide

### Accessing the Portal

1. Open your browser
2. Navigate to **http://localhost:5000**
3. Login with your credentials (if required)

### Searching for an SR

1. **Enter SR ID** in the search box (e.g., `CAS123456789`)
2. Click **Search** or press Enter
3. System will display:
   - SR Details (description, priority, status)
   - Similar Historical SRs (with similarity scores)
   - **AI-Generated Workaround**

### Understanding the Results

#### SR Details Panel
```
┌─────────────────────────────────────────┐
│ SR ID: CAS123456789                     │
│ Priority: P2                            │
│ Application: SOM_MM                     │
│ Age: 3 business days                    │
│ Status: Open                            │
└─────────────────────────────────────────┘
```

#### Similar SRs Panel
```
┌─────────────────────────────────────────┐
│ Similar Historical SRs:                 │
│                                         │
│ 📋 CAS987654321 (85% match)            │
│    "Network timeout connecting to..."   │
│                                         │
│ 📋 CAS555666777 (72% match)            │
│    "Connection pool exhausted..."       │
└─────────────────────────────────────────┘
```

#### AI Workaround Panel
```
┌─────────────────────────────────────────┐
│ 🤖 AI-Generated Workaround:            │
│                                         │
│ 1. Check database connection pool       │
│ 2. Verify ValidateAddress service       │
│ 3. Review logs for exceptions           │
│ 4. Restart affected services            │
│                                         │
│ Confidence: HIGH                        │
│ Java Error: Yes                         │
│ Assigned To: John Smith                 │
│                                         │
│ [👍 Helpful] [👎 Not Helpful]          │
└─────────────────────────────────────────┘
```

### Providing Feedback

#### Voting on Workarounds

1. **👍 Helpful** - Click if the workaround was useful
2. **👎 Not Helpful** - Click if the workaround was incorrect

#### Submitting Corrections

If the AI workaround is wrong or incomplete:

1. Click **"Provide Correction"**
2. Enter the **correct workaround** in the text box
3. Click **Submit Feedback**

Your corrections help the system learn and improve future suggestions!

### Viewing Your SRs

1. Click **"My SRs"** in the navigation
2. See all SRs assigned to you
3. View their status and workarounds

### Setting Your Availability

1. If you're a team member, you'll see an **Availability** section
2. Set your availability percentage (0-100%)
3. Choose type: Full Day, Half Day, or Unavailable
4. Provide a reason (optional)

---

## 🔐 Admin Portal Guide

### Accessing the Admin Portal

1. Navigate to **http://localhost:5000/admin**
2. Login with credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

### Admin Dashboard

The dashboard shows:
- **Historical SR Count**: Total SRs in database
- **User Corrections**: Number of user feedback entries
- **Upload Count**: Number of uploads processed
- **LLM Usage**: API costs and token usage

### Uploading Excel Files

#### Step 1: Prepare Your File

Your Excel file should have these columns:

| Column | Required | Description |
|--------|----------|-------------|
| Call ID (or SR ID) | ✅ | SR identifier |
| Description | ✅ | Issue description |
| Notes | Optional | Additional details |
| Priority | Optional | P1, P2, P3, P4 |
| Application | Optional | SOM_MM, SQO_MM, etc. |
| Submit Date | Optional | Date SR was created |

#### Step 2: Upload

1. Click **"Upload Excel"**
2. Select your `.xlsx` or `.xls` file
3. Click **"Process"**

#### Step 3: Processing

The system will:
1. 📊 Clean and validate data
2. 🔍 Run semantic search for each SR
3. 🤖 Execute 5-LLM pipeline
4. 💾 Merge results to database
5. 📁 Save output file

**Processing time**: ~15-30 seconds per SR

#### Step 4: Download Results

1. Go to **"Reports"** section
2. Find your file: `Admin_Upload_YYYYMMDD_HHMMSS.xlsx`
3. Click to download

### Understanding the Output

The output Excel contains:

| Column | Description |
|--------|-------------|
| SR ID | Service Request ID |
| Description | Original description |
| Notes | Original notes |
| Priority | P1-P4 |
| Application | Application area |
| Is Java Error | Yes/No |
| Confidence | HIGH/MEDIUM/LOW/VERY_LOW |
| Activity Names | Java activities found |
| AI Workaround | Generated resolution |
| Semantic Workaround | Historical match |
| Assigned To | Team member name |
| Similar SR IDs | Matching historical SRs |
| Similarity Score | Match percentage |

### Viewing Statistics

1. Click **"Statistics"** or **"Stats"**
2. View:
   - Total SRs processed
   - LLM API costs
   - Token usage
   - Processing times

### Managing Team

1. Go to **Team Skills** section
2. View team members and their:
   - Skill levels by application
   - Current availability
   - Workload capacity
3. Update `People.xlsx` to add/modify team members

### Email Fetching (Windows Only)

> ⚠️ **Windows Only**: This feature requires Outlook desktop app.

1. Ensure Outlook is running and logged in
2. Click **"Fetch from Email"**
3. System will download today's SR report
4. Automatically process the attachment

---

## 🤖 Understanding AI Workarounds

### How Workarounds Are Generated

```
STEP 1: SEMANTIC SEARCH
├── Query: Current SR description + notes
├── Database: 1.18M+ historical SRs
├── Method: Vector similarity (all-MiniLM-L6-v2)
└── Output: Top 10 similar SRs with workarounds

STEP 2: JAVA DETECTION (5-Source Voting)
├── Source 1: Resolution categories (0.5x weight)
├── Source 2: Semantic workaround (1.5x weight)
├── Source 3: AI workarounds (1.0x weight)
├── Source 4: User workarounds (1.0x weight)
├── Source 5: Current SR content (2.0x weight) ← Most important
└── Output: Is Java Error? (Yes/No) + Confidence

STEP 3: ACTIVITY EXTRACTION (if Java)
├── Extract: CamelCase activity names
├── Validate: Against PostgreSQL database
├── Retry: Up to 2 times with alternatives
└── Output: Validated activity names + classes

STEP 4: RESOLUTION GENERATION
├── If Java: Use code context + activities
├── If Non-Java: Use historical patterns
├── Anti-hallucination: Only use verified info
└── Output: Step-by-step resolution

STEP 5: ASSIGNMENT
├── Check: Team availability (skip 0%)
├── Match: Skill level to SR complexity
├── Balance: Workload distribution
└── Output: Assigned team member
```

### Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **HIGH** | ≥80% voting agreement, 3+ sources | Trust the result |
| **MEDIUM** | ≥67% agreement, 3+ sources | Review briefly |
| **LOW** | ≥60% agreement | Verify manually |
| **VERY_LOW** | <60% agreement | Manual review needed |

### Anti-Hallucination Rules

The AI follows strict rules to prevent fabricated information:

1. ✅ Only use file paths from provided context
2. ✅ Only use class names that were validated
3. ✅ Quote exact text from SR when possible
4. ✅ Mark unknown items as `[NEEDS INVESTIGATION]`

---

## 🔧 Troubleshooting

### Common Issues

#### "No Python found"
```
Solution: Install Python 3.10-3.12 from python.org
```

#### "ChromaDB not found"
```
Error: Semantic search will NOT work

Solution: 
1. Check if data/vectorstore/chromadb_store exists
2. If missing, contact admin to restore from backup
```

#### "Tokens.xlsx not found"
```
Solution:
1. Create tokens/Tokens.xlsx
2. Add columns: Email, Token
3. Add your API tokens (one per row)
```

#### "LLM API timeout"
```
Solutions:
1. Check network connection to ai-framework1:8085
2. Verify API tokens are not exhausted
3. Try again in a few minutes
```

#### "No workaround generated"
```
Possible causes:
1. SR description too short (<50 chars)
2. No similar historical SRs found
3. All tokens exhausted

Solutions:
1. Add more details to SR
2. Try different search terms
3. Add more tokens to Tokens.xlsx
```

### Checking System Status

1. Open Admin Portal
2. Go to Statistics
3. Check:
   - ChromaDB record count (should be 1M+)
   - Token availability
   - Recent error count

---

## ❓ FAQ

### General

**Q: How accurate are the AI workarounds?**
> A: Accuracy depends on historical data quality. The system uses 1.18M+ real SRs and user feedback to continuously improve. HIGH confidence workarounds are typically 85%+ accurate.

**Q: How long does processing take?**
> A: ~15-30 seconds per SR. Batch uploads of 50 SRs take ~10-15 minutes.

**Q: Can I use this on Linux?**
> A: Yes! Everything works except the Outlook email fetcher. Use manual Excel upload instead.

### User Portal

**Q: Why can't I find my SR?**
> A: The SR must be uploaded by an admin first. Ask your admin to upload today's SR report.

**Q: Does my feedback actually help?**
> A: Yes! Your corrections are stored and used in the 5-source voting system, improving future suggestions.

### Admin Portal

**Q: What Excel format should I use?**
> A: `.xlsx` or `.xls` files. Ensure columns include at minimum: Call ID (or SR ID) and Description.

**Q: How many tokens do I need?**
> A: Each token has a $4/day limit. For 50 SRs/day, 1-2 tokens is enough. The system auto-rotates to the next token when one is exhausted.

**Q: How do I add team members?**
> A: Update `People.xlsx` in the project root, then run:
```python
from team.people_skills_database import PeopleSkillsDatabase
PeopleSkillsDatabase().load_people_from_excel()
```

---

## 📞 Support

For issues not covered in this guide:

1. Check the [README.md](README.md) for technical details
2. Review [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) for architecture
3. Contact your system administrator

---

*Last Updated: January 2026*
