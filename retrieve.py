"""
Stage 5a of the pipeline (see planning.md "Architecture"): retrieval.

Provides a single public function:

    retrieve(query, k=5) -> list[dict]

Each returned dict contains:
    {
        "text":         str,   # chunk text
        "source":       str,   # filename stem, e.g. "heard_bad_things_about_acc"
        "source_type":  str,   # "reddit" or "transcript"
        "chunk_index":  int,   # position of this chunk within its source document
        "distance":     float, # cosine distance (lower = more relevant)
    }

The model and ChromaDB collection are loaded once on first call and reused for
subsequent queries (module-level singletons).
"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION = "uci_housing_guide"
MODEL_NAME = "all-MiniLM-L6-v2"

_model      = None
_collection = None


def _load():
    global _model, _collection
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_collection(COLLECTION)


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return the top-k most relevant chunks for *query*."""
    _load()

    embedding = _model.encode([query], convert_to_numpy=True).tolist()
    results = _collection.query(
        query_embeddings=embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text":        text,
            "source":      meta["source"],
            "source_type": meta["source_type"],
            "chunk_index": meta["chunk_index"],
            "distance":    dist,
        })
    return chunks


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "What is ACC housing like?"
    print(f"Query: {query!r}\n")
    for i, chunk in enumerate(retrieve(query), 1):
        print(f"[{i}] {chunk['source']}  chunk={chunk['chunk_index']}  dist={chunk['distance']:.4f}")
        print(chunk["text"])
        print()