"""
Start RAG Recipe server. Run: python start_server.py
Writes logs to server_log.txt. Server runs at http://127.0.0.1:8000
"""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

# Redirect stdout/stderr to see startup errors
log_file = ROOT / "server_log.txt"
with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"ROOT={ROOT}\ncwd={os.getcwd()}\n")
    try:
        f.write("Importing backend.app...\n")
        f.flush()
        from backend.app import app
        f.write("App imported OK.\n")
        f.flush()
    except Exception as e:
        f.write(f"Import error: {e}\n")
        import traceback
        traceback.print_exc(file=f)
        sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("Starting uvicorn on 127.0.0.1:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
