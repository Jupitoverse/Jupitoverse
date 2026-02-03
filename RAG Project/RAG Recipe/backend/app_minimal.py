"""Minimal FastAPI app - no routes, just health. Use to verify server starts."""
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health():
    return {"status": "ok"}
