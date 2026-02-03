"""
RAG Recipe - entry point. Run: python main.py
"""
import sys
import os
from pathlib import Path

# Fix Windows console encoding so uvicorn logs don't crash
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is on path and is cwd
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Now import app from backend (backend = ROOT/backend)
from backend.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
