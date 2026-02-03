#!/bin/bash
# Launch SR Feedback UI
echo "Starting SR Feedback UI..."
cd "$(dirname "$0")"
streamlit run rag/sr_feedback_ui.py

