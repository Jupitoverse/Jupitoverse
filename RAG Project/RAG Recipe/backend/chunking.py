"""Chunking / text splitter logic: character, recursive, sentence. Returns chunks + spans for UI visualization."""
import re
from typing import List, Dict, Any, Tuple

from config import CHUNKING_OPTIONS


def _character_split(text: str, chunk_size: int, overlap: int) -> List[str]:
    if chunk_size <= 0:
        return [text] if text else []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap if overlap < chunk_size else end
        if start >= len(text):
            break
    return chunks


def _recursive_split(text: str, chunk_size: int, overlap: int) -> List[str]:
    separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
    return _split_with_separators(text.strip(), separators, chunk_size, overlap)


def _split_with_separators(
    text: str, separators: List[str], chunk_size: int, overlap: int
) -> List[str]:
    if not text:
        return []
    if chunk_size >= len(text):
        return [text]
    sep = separators[0] if separators else ""
    if not sep:
        return _character_split(text, chunk_size, overlap)
    parts = text.split(sep) if sep else [text]
    # Rejoin with separator for recursive (except for "" case)
    if sep:
        parts = [p + (sep if i < len(parts) - 1 else "") for i, p in enumerate(parts)]
    chunks = []
    current = ""
    for i, p in enumerate(parts):
        if len(current) + len(p) <= chunk_size:
            current += p
        else:
            if current:
                chunks.append(current)
            current = p
            if len(current) > chunk_size:
                sub = _split_with_separators(current, separators[1:], chunk_size, overlap)
                chunks.extend(sub[:-1] if len(sub) > 1 else sub)
                current = sub[-1] if len(sub) > 1 and len(sub[-1]) <= chunk_size else ""
                if len(current) > chunk_size:
                    small = _character_split(current, chunk_size, overlap)
                    chunks.extend(small[:-1])
                    current = small[-1] if small else ""
        if current and len(current) >= chunk_size:
            chunks.append(current)
            # Overlap: keep last `overlap` chars as start of next
            current = current[-overlap:] if overlap > 0 else ""
    if current:
        chunks.append(current)
    return chunks


def _sentence_split(text: str, chunk_size: int, overlap: int) -> List[str]:
    # chunk_size/overlap here = number of sentences per chunk / overlap in sentences
    pattern = r'(?<=[.!?])\s+'
    sentences = re.split(pattern, text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return [text] if text else []
    chunks = []
    for i in range(0, len(sentences), max(1, chunk_size - overlap)):
        seg = sentences[i : i + chunk_size]
        if seg:
            chunks.append(" ".join(seg))
    return chunks


def chunk_text(
    text: str,
    splitter_id: str,
    chunk_size: int,
    chunk_overlap: int,
) -> List[str]:
    """Return list of text chunks for the given splitter and parameters."""
    opts = CHUNKING_OPTIONS.get(splitter_id, CHUNKING_OPTIONS["character"])
    chunk_size = max(opts.get("min_chunk_size", 20), min(opts.get("max_chunk_size", 2000), chunk_size))
    chunk_overlap = max(opts.get("min_overlap", 0), min(opts.get("max_overlap", 500), chunk_overlap))
    if splitter_id == "recursive":
        return _recursive_split(text, chunk_size, chunk_overlap)
    if splitter_id == "sentence":
        return _sentence_split(text, chunk_size, chunk_overlap)
    return _character_split(text, chunk_size, chunk_overlap)


def chunk_preview(
    text: str,
    splitter_id: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Dict[str, Any]:
    """
    Return chunks, metrics, and spans for UI visualization.
    Spans: list of { "type": "chunk"|"overlap", "text", "chunk_index" } in order,
    so the frontend can render color-coded text (chunk #1, overlap, chunk #2, ...).
    """
    chunks = chunk_text(text, splitter_id, chunk_size, chunk_overlap)
    total_chars = len(text)
    num_chunks = len(chunks)
    avg_size = round(total_chars / num_chunks, 1) if num_chunks else 0

    # Build spans for visual: chunk regions and overlap regions in document order.
    # For character splitter: next chunk starts at (prev_end - overlap), so overlap = text[prev_end - overlap : prev_end].
    spans: List[Dict[str, Any]] = []
    if splitter_id == "character":
        start = 0
        for i, c in enumerate(chunks):
            end = start + len(c)
            # Unique part of this chunk (before overlap with next)
            overlap_len = chunk_overlap if (i + 1 < len(chunks)) else 0
            unique_end = end - overlap_len
            if start < unique_end:
                spans.append({"type": "chunk", "text": text[start:unique_end], "chunk_index": i + 1})
            if overlap_len > 0 and unique_end < end:
                ot = text[unique_end:end]
                spans.append({"type": "overlap", "text": ot, "chunk_index": i + 1})
            start = end - overlap_len
    else:
        consumed = 0
        for i, c in enumerate(chunks):
            pos = text.find(c, consumed) if c else consumed
            if pos == -1:
                pos = consumed
            start, end = pos, pos + len(c)
            if start > consumed and consumed < len(text):
                overlap_text = text[consumed:start]
                if overlap_text.strip():
                    spans.append({"type": "overlap", "text": overlap_text, "chunk_index": i})
            spans.append({"type": "chunk", "text": c, "chunk_index": i + 1})
            consumed = end

    return {
        "chunks": chunks,
        "metrics": {
            "total_characters": total_chars,
            "number_of_chunks": num_chunks,
            "average_chunk_size": avg_size,
        },
        "spans": spans,
    }
