# SR Feedback System - User Guide

## 🎯 Overview

The SR Feedback System allows users to rate workarounds (upvote/downvote) and uses this feedback to improve future AI-generated solutions. High-voted workarounds get priority in the RAG pipeline.

## 📦 Components

1. **feedback_storage.py** - SQLite database handler for storing votes
2. **rag_pipeline_ollama.py** - Enhanced RAG pipeline with feedback integration
3. **sr_feedback_ui.py** - Streamlit web UI for viewing and rating workarounds
4. **run_feedback_ui.bat/sh** - Launch scripts for the UI

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install streamlit
```

### Step 2: Run the Feedback UI

**Windows:**
```bash
run_feedback_ui.bat
```

**Linux/Mac:**
```bash
chmod +x run_feedback_ui.sh
./run_feedback_ui.sh
```

Or directly:
```bash
streamlit run rag/sr_feedback_ui.py
```

### Step 3: Load SR Analysis Results

1. The UI will open in your browser (usually http://localhost:8501)
2. Upload an Excel file from the sidebar or select from recent outputs
3. Browse through the SR boxes

### Step 4: Provide Feedback

For each workaround box:
- Click **👍** to upvote if the solution is helpful
- Click **👎** to downvote if the solution is unhelpful
- The score updates in real-time

## 📊 Output Box Format

```
┌─────────────────────────────────────────┐
│ 📊 SR-123              [85%]            │
├─────────────────────────────────────────┤
│ 📋 Resolution Categorization: Data Issue│
│ 🎯 SLA Resolution: Resolved             │
├─────────────────────────────────────────┤
│ 💡 Original Workaround: [text]          │
│    👍 5  👎 2  Score: +3 ✅ Validated   │
│                                         │
│ 🤖 AI Workaround: [text]               │
│    👍 12  👎 1  Score: +11 🔥 Highly... │
│                                         │
│ 🌟 User Correction: [text]             │
│    👍 0  👎 0  Score: 0 📊 Not Rated    │
└─────────────────────────────────────────┘
```

## 🗄️ Database Storage

Votes are stored in: `vector store/workaround_feedback.db`

### Database Schema

**workaround_feedback** table:
- `sr_id`: Service Request ID
- `workaround_type`: 'original', 'ai', or 'user_corrected'
- `workaround_text`: First 500 characters (for reference)
- `upvotes`: Count of upvotes
- `downvotes`: Count of downvotes
- `score`: Computed as (upvotes - downvotes)
- `created_at`: First vote timestamp
- `last_updated`: Latest vote timestamp

**vote_history** table (optional):
- Individual vote events for tracking and analytics

## 🤖 How Feedback Improves AI

### 1. Priority Ranking

In `_build_historical_context()`, historical matches are sorted by:
- **70% similarity score** (semantic match)
- **30% normalized vote score** (user validation)

High-voted workarounds appear first in the context sent to the LLM.

### 2. Vote Indicators

The LLM receives visual indicators:
- **🔥 Score > 5**: "HIGHLY VALIDATED - Prioritize this pattern!"
- **✅ Score > 0**: "USER VALIDATED - Good solution"
- **⚖️ Score = 0** (with votes): "MIXED FEEDBACK"
- **⚠️ Score < 0**: "PROBLEMATIC - Use with caution or avoid"

### 3. Instruction to LLM

The prompt explicitly tells the LLM:
> "Extract ACTION PATTERNS from HIGH-SCORE matches and adapt them with current SR's specific data!"

## 📈 Analytics & Insights

### View Statistics

In the UI sidebar, you can see:
- Total workarounds rated
- Total upvotes/downvotes
- Average score
- Best and worst workarounds

### Export Data

```python
from feedback_storage import WorkaroundFeedbackStorage

storage = WorkaroundFeedbackStorage()
storage.export_to_csv("feedback_data.csv")
```

### Get Top Workarounds

```python
top_10 = storage.get_top_workarounds(limit=10, min_votes=5)

for w in top_10:
    print(f"{w['sr_id']}: Score {w['score']} ({w['upvotes']}↑ {w['downvotes']}↓)")
```

### Get Bottom Workarounds (for improvement)

```python
bottom_10 = storage.get_bottom_workarounds(limit=10)

for w in bottom_10:
    print(f"{w['sr_id']}: Score {w['score']} - Needs review!")
```

## 🔧 API Usage

### Record Votes Programmatically

```python
from feedback_storage import WorkaroundFeedbackStorage

storage = WorkaroundFeedbackStorage()

# Upvote
storage.upvote("SR-123", "ai", "Check PS config...")

# Downvote
storage.downvote("SR-456", "original", "Manual fix required")
```

### Get Votes

```python
# Get votes for a specific workaround
votes = storage.get_votes("SR-123", "ai")
print(f"Upvotes: {votes['upvotes']}")
print(f"Downvotes: {votes['downvotes']}")
print(f"Score: {votes['score']}")

# Get all votes for an SR
all_votes = storage.get_all_votes_for_sr("SR-123")
for w_type, votes in all_votes.items():
    print(f"{w_type}: {votes['score']}")
```

## 🎨 Customization

### Change Vote Weight

In `rag_pipeline_ollama.py`, adjust the weights in `_build_historical_context()`:

```python
def calculate_priority(match):
    similarity_weight = 0.7  # Change this
    vote_weight = 0.3        # Change this
    # ...
```

### Add User Tracking

When recording votes, pass a `user_id`:

```python
storage.upvote("SR-123", "ai", "...", user_id="john.doe@company.com")
```

### Change Score Thresholds

Modify the emoji indicators in `_build_historical_context()`:

```python
if score > 5:  # Change threshold
    score_indicator = "⭐ **HIGHLY VALIDATED**"
```

## 🐛 Troubleshooting

### Database Not Found

If you see "Feedback storage not available":
1. Check that `feedback_storage.py` is in the `rag/` folder
2. The database will be created automatically on first run

### UI Not Loading

1. Ensure Streamlit is installed: `pip install streamlit`
2. Check the port (default: 8501) isn't blocked
3. Try: `streamlit run rag/sr_feedback_ui.py --server.port 8502`

### Votes Not Updating

1. Click the button again (sometimes needs double-click)
2. Check the terminal for error messages
3. Verify database file permissions

## 📝 Best Practices

1. **Rate Consistently**: Apply the same criteria when voting
2. **Rate Both Good and Bad**: Negative feedback is as valuable as positive
3. **Review Top/Bottom**: Periodically check the highest and lowest rated workarounds
4. **Export Data**: Back up your feedback data regularly
5. **Clean Up**: Remove duplicate or test votes from the database

## 🔒 Data Privacy

- All votes are stored locally in SQLite
- No data is sent to external servers
- User IDs (if used) are optional and stored only locally

## 📊 Example Workflow

1. **Run Analysis**: `python rag_pipeline_ollama.py`
2. **Review Results**: Open `llm output/*.xlsx`
3. **Launch UI**: `run_feedback_ui.bat`
4. **Rate Workarounds**: Vote on solutions
5. **Re-run Analysis**: Next analysis will use feedback
6. **Iterate**: Continuously improve!

## 🚀 Advanced: Batch Vote Import

If you have historical feedback data:

```python
import pandas as pd
from feedback_storage import WorkaroundFeedbackStorage

storage = WorkaroundFeedbackStorage()

# Load from CSV
feedback_df = pd.read_csv("historical_feedback.csv")

for _, row in feedback_df.iterrows():
    for _ in range(row['upvotes']):
        storage.upvote(row['sr_id'], row['type'], row['text'])
    for _ in range(row['downvotes']):
        storage.downvote(row['sr_id'], row['type'], row['text'])
```

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **SQLite Docs**: https://www.sqlite.org/docs.html
- **RAG Pipeline**: See `rag_pipeline_ollama.py` documentation

---

**Questions?** Check the code comments or raise an issue!

