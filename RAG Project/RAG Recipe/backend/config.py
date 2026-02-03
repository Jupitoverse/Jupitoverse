"""App configuration and paths."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DATA_DIR = BASE_DIR / "project_data"
ARCHIVE_DIR = BASE_DIR / "project_archive"
ARCHIVE_DAYS_BEFORE_DELETE = 10

# Per-project subdirs (created under project_data/<project_id>/)
CONFIG_FILE = "config.json"
CHROMA_DIR = "chroma"
DOCUMENTS_DIR = "documents"
EXCEL_HISTORY_DIR = "excel_history"
MONITORING_FILE = "monitoring.json"

# LLM options
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "qwen2.5:latest"
OPENAI_DEFAULT_MODEL = "gpt-4o-mini"

# Embedding options (id -> model name or config)
EMBEDDING_OPTIONS = {
    "sentence_minilm": {
        "id": "sentence_minilm",
        "name": "SentenceTransformer all-MiniLM-L6-v2",
        "type": "local",
        "model": "all-MiniLM-L6-v2",
        "dimension": 384,
        "pros": "Free, fast, good for English. No API cost.",
        "cons": "384 dim only. English-focused.",
    },
    "sentence_paraphrase": {
        "id": "sentence_paraphrase",
        "name": "SentenceTransformer paraphrase-MiniLM-L6-v2",
        "type": "local",
        "model": "paraphrase-MiniLM-L6-v2",
        "dimension": 384,
        "pros": "Best for paraphrase/similarity. Free.",
        "cons": "384 dim. Slightly slower than all-MiniLM.",
    },
    "openai_small": {
        "id": "openai_small",
        "name": "OpenAI text-embedding-3-small",
        "type": "openai",
        "model": "text-embedding-3-small",
        "dimension": 1536,
        "pros": "High quality, multi-language. Same space as GPT.",
        "cons": "API cost. Requires OpenAI key.",
    },
    "openai_ada": {
        "id": "openai_ada",
        "name": "OpenAI text-embedding-ada-002",
        "type": "openai",
        "model": "text-embedding-ada-002",
        "dimension": 1536,
        "pros": "Widely used, stable.",
        "cons": "Older. Prefer text-embedding-3-small for new projects.",
    },
}

# LLM option metadata for UI (pros/cons)
LLM_OPTIONS_META = {
    "ollama_qwen": {
        "id": "ollama_qwen",
        "name": "Ollama Qwen (Local)",
        "type": "ollama",
        "default_model": "qwen2.5:latest",
        "pros": "Free, private, no rate limits. Full control.",
        "cons": "Requires local GPU/CPU. Slower than cloud.",
    },
    "openai": {
        "id": "openai",
        "name": "OpenAI (API)",
        "type": "openai",
        "pros": "Best quality, fast. Multiple keys with $5 limit supported.",
        "cons": "Cost per token. Keys can exhaust; rotation needed.",
    },
}

# Chunking / text splitter options (for UI dropdown + pros/cons)
CHUNKING_OPTIONS = {
    "character": {
        "id": "character",
        "name": "Character Splitter",
        "description": "Split by fixed character count. Simple and fast.",
        "pros": "Predictable size, no dependencies, works on any text.",
        "cons": "Can break mid-word or mid-sentence; may hurt retrieval quality.",
        "default_chunk_size": 512,
        "default_overlap": 50,
        "min_chunk_size": 20,
        "max_chunk_size": 2000,
        "min_overlap": 0,
        "max_overlap": 500,
    },
    "recursive": {
        "id": "recursive",
        "name": "Recursive Character Splitter",
        "description": "Try to split on newlines, then paragraphs, then sentences, then words, then chars.",
        "pros": "Keeps semantic boundaries when possible. Better for documents.",
        "cons": "Slightly slower. Needs good separators for your language.",
        "default_chunk_size": 512,
        "default_overlap": 50,
        "min_chunk_size": 20,
        "max_chunk_size": 2000,
        "min_overlap": 0,
        "max_overlap": 500,
    },
    "sentence": {
        "id": "sentence",
        "name": "Sentence Splitter",
        "description": "Split on sentence boundaries (. ! ?). Overlap in sentences.",
        "pros": "Clean boundaries. Good for Q&A and summaries.",
        "cons": "Requires clear sentence punctuation. Long sentences = big chunks.",
        "default_chunk_size": 5,
        "default_overlap": 1,
        "min_chunk_size": 1,
        "max_chunk_size": 50,
        "min_overlap": 0,
        "max_overlap": 10,
    },
}
