"""
Stage 3 of the pipeline (see planning.md "Architecture"): chunking.

Reads the cleaned files from cleaned_documents/ and writes one JSON file per
source to chunks/ (e.g. chunks/acc_bad_things.json). The next pipeline stage
(embedding) will load these JSON files directly.

Chunking strategy:
  Reddit (8 files) — paragraph-aware:
    Treat each blank-line-separated paragraph (= one comment / one thought) as
    the atomic unit. Pack consecutive paragraphs into a window up to 500 chars.
    If a single paragraph exceeds 500 chars (a long comment), split it at a
    sentence boundary. This avoids cutting mid-comment and prevents unrelated
    comments from sharing a chunk.

  YouTube tour (uci_housing) — sliding window, 800 chars / 100 overlap:
    Chapter headings carry context forward so the fixed window works well here.

  Official webinar (uci_official_housing) — sliding window, 500 chars / 150 overlap:
    Smaller chunks keep each retrieval hit focused on a single topic (eligibility,
    a specific housing option, application steps, etc.). Larger overlap compensates
    for the lack of natural paragraph breaks in continuous webinar prose.

Each chunk is stored as:
    {
        "source":      "acc_bad_things",   # stem of the filename
        "source_type": "reddit",           # "reddit" | "transcript"
        "chunk_index": 0,                  # 0-based position within source
        "text":        "..."
    }
"""

import json
import re
from pathlib import Path

CLEAN_DIR  = Path(__file__).parent / "cleaned_documents"
CHUNKS_DIR = Path(__file__).parent / "chunks"

YOUTUBE_TOUR     = "uci_housing"
OFFICIAL_WEBINAR = "uci_official_housing"

REDDIT_MAX          = 500
TOUR_CHUNK_SIZE     = 800
TOUR_OVERLAP        = 100
WEBINAR_CHUNK_SIZE  = 500
WEBINAR_OVERLAP     = 150

# Sentence-ending punctuation used when splitting an oversized paragraph.
_RE_SENT_END = re.compile(r"(?<=[.!?])\s+")


# ---------------------------------------------------------------------------
# Shared sliding-window chunker (transcripts)
# ---------------------------------------------------------------------------

def _nudge_boundary(text, pos, direction="left", window=40):
    """Move pos to the nearest whitespace within ±window chars."""
    if pos <= 0 or pos >= len(text) or text[pos].isspace():
        return pos
    if direction == "left":
        for i in range(pos, max(pos - window, 0), -1):
            if text[i].isspace():
                return i + 1
    else:
        for i in range(pos, min(pos + window, len(text))):
            if text[i].isspace():
                return i
    return pos


def _sliding_window_chunks(text, chunk_size, overlap):
    """Sliding-window character chunker with word-boundary nudging."""
    text = text.strip()
    if not text:
        return []
    step   = chunk_size - overlap
    chunks = []
    start  = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            end = _nudge_boundary(text, end, "left")
        raw = text[start:end].strip()
        if raw:
            chunks.append(raw)
        if end >= len(text):
            break
        next_start = _nudge_boundary(text, start + step, "right")
        if next_start <= start:
            next_start = start + step
        start = next_start
    return chunks


# ---------------------------------------------------------------------------
# Reddit paragraph-aware chunker
# ---------------------------------------------------------------------------

def _split_long_paragraph(para, max_size):
    """
    Split a paragraph that exceeds max_size at sentence boundaries.
    Falls back to word boundaries if no sentence break is found.
    """
    if len(para) <= max_size:
        return [para]

    sentences = _RE_SENT_END.split(para)
    pieces = []
    current = ""
    for sent in sentences:
        candidate = (current + " " + sent).strip() if current else sent
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                pieces.append(current)
            # Sentence itself is too long — split at word boundary.
            if len(sent) > max_size:
                pos = _nudge_boundary(sent, max_size, "left")
                pieces.append(sent[:pos].strip())
                current = sent[pos:].strip()
            else:
                current = sent
    if current:
        pieces.append(current)
    return [p for p in pieces if p]


def _paragraph_aware_chunks(text, max_size):
    """
    Pack blank-line-separated paragraphs greedily into windows ≤ max_size.
    Long individual paragraphs are first split at sentence boundaries.
    """
    raw_paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    # Expand any paragraph that exceeds max_size.
    atomic = []
    for para in raw_paras:
        atomic.extend(_split_long_paragraph(para, max_size))

    chunks  = []
    current = ""
    for para in atomic:
        sep       = "\n\n" if current else ""
        candidate = current + sep + para
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks


# ---------------------------------------------------------------------------
# Per-file dispatcher
# ---------------------------------------------------------------------------

def process_file(path):
    stem = path.stem
    text = path.read_text(encoding="utf-8")

    if stem == YOUTUBE_TOUR:
        source_type  = "transcript"
        chunk_size   = TOUR_CHUNK_SIZE
        texts        = _sliding_window_chunks(text, TOUR_CHUNK_SIZE, TOUR_OVERLAP)
    elif stem == OFFICIAL_WEBINAR:
        source_type  = "transcript"
        chunk_size   = WEBINAR_CHUNK_SIZE
        texts        = _sliding_window_chunks(text, WEBINAR_CHUNK_SIZE, WEBINAR_OVERLAP)
    else:
        source_type  = "reddit"
        chunk_size   = REDDIT_MAX
        texts        = _paragraph_aware_chunks(text, REDDIT_MAX)

    return [
        {
            "source":      stem,
            "source_type": source_type,
            "chunk_index": i,
            "text":        t,
        }
        for i, t in enumerate(texts)
    ], chunk_size


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run():
    CHUNKS_DIR.mkdir(exist_ok=True)
    cleaned_files = sorted(CLEAN_DIR.glob("*.txt"))
    if not cleaned_files:
        print(f"No cleaned files found in {CLEAN_DIR}. Run clean_documents.py first.")
        return

    total_chunks = 0
    print(f"Chunking {len(cleaned_files)} documents -> {CHUNKS_DIR}/\n")
    print(f"{'file':<45}{'type':>11}{'size':>6}{'chunks':>8}")
    print("-" * 70)

    for path in cleaned_files:
        records, chunk_size = process_file(path)
        out = CHUNKS_DIR / (path.stem + ".json")
        out.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        total_chunks += len(records)
        src_type = records[0]["source_type"] if records else "?"
        print(f"{path.name:<45}{src_type:>11}{chunk_size:>6}{len(records):>8}")

    print("-" * 70)
    print(f"{'TOTAL':<45}{'':>11}{'':>6}{total_chunks:>8}")
    print(f"\nAll chunk files written to {CHUNKS_DIR}/")


if __name__ == "__main__":
    run()
