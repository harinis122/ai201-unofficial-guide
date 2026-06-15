"""
Backend entry point for the UCI Housing Unofficial Guide.

Run this file to build the full pipeline and start an interactive CLI:
    python3 main.py

For the Gradio web UI instead, run:
    python3 app.py  (assumes the pipeline has already been built)

Pipeline stages
---------------
Stage 1 — clean_documents.py  : strip Reddit boilerplate and transcript timestamps
Stage 2 — chunk_documents.py  : split cleaned text into chunks (paragraph-aware for
                                 Reddit, sliding window for transcripts)
Stage 3 — embed_documents.py  : embed every chunk with all-MiniLM-L6-v2 and store
                                 vectors in ChromaDB

Query stages (run on every question)
--------------------------------------
Stage 4 — retrieve.py         : embed the question, find top-5 closest chunks in ChromaDB
Stage 5 — generate.py         : pass those chunks to Groq (llama-3.3-70b-versatile)
                                 and return a grounded answer with source attribution
"""

from pathlib import Path

import clean_documents
import chunk_documents
import embed_documents
from retrieve import retrieve
from generate import ask, SOURCE_LABELS

CHROMA_DIR = Path(__file__).parent / "chroma_db"


# ---------------------------------------------------------------------------
# Pipeline build (stages 1–3)
# ---------------------------------------------------------------------------

def build_pipeline():
    """
    Run clean → chunk → embed.

    Skips automatically if the vector store already exists. Delete chroma_db/
    and re-run to force a full rebuild from the raw documents.
    """
    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        print("Vector store already exists — skipping pipeline build.")
        print("(Delete chroma_db/ and re-run to rebuild from scratch.)\n")
        return

    print("=" * 60)
    print("Stage 1: Cleaning raw documents")
    print("=" * 60)
    clean_documents.run()

    print("\n" + "=" * 60)
    print("Stage 2: Chunking cleaned documents")
    print("=" * 60)
    chunk_documents.run()

    print("\n" + "=" * 60)
    print("Stage 3: Embedding chunks and storing in ChromaDB")
    print("=" * 60)
    embed_documents.run()

    print("\nPipeline build complete.\n")


# ---------------------------------------------------------------------------
# Query (stages 4–5)
# ---------------------------------------------------------------------------

def query(question: str) -> dict:
    """
    Given a question, retrieve the top-5 relevant chunks and generate a
    grounded answer via Groq.

    Returns the same dict as generate.ask():
        {"answer": str, "sources": list[str]}
    """
    return ask(question)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    build_pipeline()

    print("UCI Housing Unofficial Guide")
    print("Ask anything about UCI continuing student housing.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            question = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = query(question)

        print("\nAnswer:")
        print("-" * 60)
        print(result["answer"])

        if result["sources"]:
            print("\nSources:")
            for s in result["sources"]:
                print(f"  • {SOURCE_LABELS.get(s, s)}")
        print()