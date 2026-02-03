"""
Run RAG Recipe. Execute: python run.py (from any directory, or double-click START_APP.bat)
"""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import uvicorn
uvicorn.run(
    "backend.app:app",
    host="127.0.0.1",
    port=8000,
    reload=True,
)
