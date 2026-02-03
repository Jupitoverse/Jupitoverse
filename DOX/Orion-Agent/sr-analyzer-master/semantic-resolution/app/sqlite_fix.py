#!/usr/bin/env python3
"""
SQLite Fix for ChromaDB on older Linux systems
This MUST be imported BEFORE any chromadb imports

ChromaDB requires SQLite >= 3.35.0, but many Linux systems have older versions.
This module replaces the built-in sqlite3 with pysqlite3-binary.
"""

import sys

try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    print("[OK] SQLite fix applied - using pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, use system sqlite3

