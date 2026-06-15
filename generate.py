"""
Stage 5b of the pipeline (see planning.md "Architecture"): grounded generation.

Usage:
    python3 generate.py "Is ACC housing worth it compared to off-campus?"

Flow:
    1. retrieve() fetches the top-5 most relevant chunks from ChromaDB.
    2. Those chunks (and only those chunks) are passed to Groq as context.
    3. llama-3.3-70b-versatile answers using only what is in the chunks.
    4. If the chunks don't contain enough relevant information, the model says so.
"""

import os
import sys
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Human-readable labels for each source document.
# Imported by main.py (CLI) and app.py (Gradio UI) for display.
SOURCE_LABELS = {
    "uci_housing_megathread_2022_2023":         "r/UCI Housing Megathread (2022–2023)",
    "uci_housing_megathread_2023_2024":         "r/UCI Housing Megathread (2023–2024)",
    "are_the_acc_apartments_really_that_bad":   "r/Are the ACC apartments really that bad?",
    "acc_vs_offcampus_housing_advice":          "r/ACC vs off-campus housing advice",
    "heard_bad_things_about_acc":               "r/I've heard bad things about ACC — is off campus better?",
    "any_ideas_on_tackling_off_campus_housing": "r/Any ideas on tackling off-campus housing?",
    "what_apartment_communities_dont_suck":     "r/What apartment communities don't suck?",
    "why_choose_acc_over_residence_halls":      "r/Why choose ACC apartments over residence halls?",
    "uci_housing":                              "YouTube: UCI Housing Tour (Non-Dorms) — Pros & Cons",
    "uci_official_housing":                     "YouTube: UCI Official Continuing Student Housing Webinar",
}

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about UCI continuing student housing options.

You may ONLY use information that is explicitly stated in the context chunks provided. Each chunk is labeled with its source.

Rules you must follow:
- Do not use any knowledge from outside the provided chunks. If you know something about UCI housing that is not in the chunks, do not say it.
- You may draw conclusions that are directly supported by the text (e.g. if a chunk says "ACC is cheap and close to campus", you may say those are advantages). Do not go beyond what the text supports.
- Do not fabricate details, statistics, prices, or opinions that do not appear in the chunks.
- If the chunks are about a completely different topic than the question and contain nothing relevant, respond with exactly: "I don't have enough information on that."
- If only part of the question can be answered, answer that part and note what you couldn't find.
- Cite the source of each piece of information in parentheses, e.g. (source: heard_bad_things_about_acc).
- Be concise and direct."""


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Chunk {i} | source: {chunk['source']}]\n{chunk['text']}")
    return "\n\n".join(parts)


def ask(question: str) -> dict:
    """Return {"answer": str, "sources": list[str]} for the given question."""
    chunks = retrieve(question, k=5)
    # Drop transcript chunks with high cosine distance — these are usually
    # mid-sentence fragments that happened to land near the query by accident.
    chunks = [c for c in chunks if not (c["source_type"] == "transcript" and c["distance"] > 0.45)]
    if not chunks:
        return {"answer": "I don't have enough information on that.", "sources": []}

    context = format_context(chunks)

    user_message = f"""Context chunks retrieved from UCI housing documents:

{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.0,
    )

    answer = response.choices[0].message.content

    # Deduplicated source list in retrieval order
    seen = set()
    sources = []
    for c in chunks:
        if c["source"] not in seen:
            seen.add(c["source"])
            sources.append(c["source"])

    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    if not question:
        print("Usage: python3 generate.py \"your question here\"")
        sys.exit(1)

    print(f"Question: {question}\n")
    print("Retrieving chunks...")
    chunks = retrieve(question, k=5)
    print(f"Top sources: {[c['source'] for c in chunks]}\n")
    print("Answer:")
    print("-" * 60)

    result = ask(question)
    print(result["answer"])
    print("\nSources:", result["sources"])