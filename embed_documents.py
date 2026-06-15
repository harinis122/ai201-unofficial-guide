"""
Stage 4 of the pipeline (see planning.md "Architecture"): embedding + vector store.

Loads all chunks from chunks/*.json, embeds their text with all-MiniLM-L6-v2
(runs locally, no API key), and stores the vectors in a persistent ChromaDB
collection at chroma_db/.

Safe to re-run: the collection is deleted and rebuilt from scratch each time so
the store never drifts out of sync with the chunks on disk.

The collection is named "uci_housing_guide" and can be queried by the retrieval
stage using the same model to embed the user's question.
"""

import json
import time
from pathlib import Path

from sentence_transformers import SentenceTransformer
import chromadb

CHUNKS_DIR  = Path(__file__).parent / "chunks"
CHROMA_DIR  = Path(__file__).parent / "chroma_db"
COLLECTION  = "uci_housing_guide"
MODEL_NAME  = "all-MiniLM-L6-v2"
BATCH_SIZE  = 64   # how many chunks to embed at once


def load_chunks():
    chunks = []
    for path in sorted(CHUNKS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        chunks.extend(data)
    return chunks


def make_id(chunk):
    """Stable, unique ID for each chunk: '<source>__<index>'."""
    return f"{chunk['source']}__{chunk['chunk_index']}"


def run():
    # ------------------------------------------------------------------ #
    # 1. Load chunks
    # ------------------------------------------------------------------ #
    chunks = load_chunks()
    if not chunks:
        print("No chunks found in chunks/. Run chunk_documents.py first.")
        return
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_DIR}/")

    # ------------------------------------------------------------------ #
    # 2. Load embedding model
    # ------------------------------------------------------------------ #
    print(f"\nLoading model: {MODEL_NAME}  (downloads once, cached after that)")
    model = SentenceTransformer(MODEL_NAME)
    print("Model ready.")

    # ------------------------------------------------------------------ #
    # 3. Set up ChromaDB — wipe and rebuild for a clean state
    # ------------------------------------------------------------------ #
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
        print(f"\nDropped existing '{COLLECTION}' collection (rebuilding from scratch).")

    collection = client.create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"Created collection '{COLLECTION}'.")

    # ------------------------------------------------------------------ #
    # 4. Embed in batches and upsert into ChromaDB
    # ------------------------------------------------------------------ #
    texts     = [c["text"]        for c in chunks]
    ids       = [make_id(c)       for c in chunks]
    metadatas = [
        {
            "source":      c["source"],
            "source_type": c["source_type"],
            "chunk_index": c["chunk_index"],
        }
        for c in chunks
    ]

    print(f"\nEmbedding {len(texts)} chunks in batches of {BATCH_SIZE}…")
    t0 = time.time()

    for start in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[start : start + BATCH_SIZE]
        batch_ids   = ids[start : start + BATCH_SIZE]
        batch_meta  = metadatas[start : start + BATCH_SIZE]

        embeddings = model.encode(
            batch_texts,
            show_progress_bar=False,
            convert_to_numpy=True,
        ).tolist()

        collection.add(
            ids=batch_ids,
            embeddings=embeddings,
            documents=batch_texts,
            metadatas=batch_meta,
        )

        done = min(start + BATCH_SIZE, len(texts))
        print(f"  {done:>4}/{len(texts)} embedded and stored")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s.")

    # ------------------------------------------------------------------ #
    # 5. Sanity check: run a test query and print the top result
    # ------------------------------------------------------------------ #
    print("\n--- Sanity check: querying 'what is ACC housing like?' ---")
    query_embedding = model.encode(["what is ACC housing like?"], convert_to_numpy=True).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    )):
        print(f"\n[{i+1}] source={meta['source']}  chunk={meta['chunk_index']}  distance={dist:.4f}")
        print(doc[:200])

    stored = collection.count()
    print(f"\nCollection '{COLLECTION}' contains {stored} vectors in {CHROMA_DIR}/")


if __name__ == "__main__":
    run()