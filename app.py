"""
Gradio web UI for the UCI Housing Unofficial Guide.
Run with: python3 app.py
"""

import gradio as gr
from generate import ask, SOURCE_LABELS

EXAMPLES = [
    "What do students say about the wifi at ACC apartments?",
    "How does Camino del Sol compare to other ACC communities?",
    "What should I know about parking at Plaza Verde?",
    "Is ACC housing worth it compared to living off campus?",
    "What are the cheapest ACC housing options?",
]


def handle_query(question: str):
    if not question.strip():
        return "", "", ""
    result = ask(question)
    sources = "\n".join(
        f"• {SOURCE_LABELS.get(s, s)}" for s in result["sources"]
    )
    chunk_parts = []
    for i, c in enumerate(result.get("chunks", []), 1):
        label = SOURCE_LABELS.get(c["source"], c["source"])
        chunk_parts.append(
            f"**Chunk {i} — {label}** (distance: {c['distance']:.4f})\n\n{c['text']}"
        )
    chunks_md = "\n\n---\n\n".join(chunk_parts) or "No chunks retrieved."
    return result["answer"], sources or "No sources retrieved.", chunks_md


with gr.Blocks(title="UCI Continuing Student Housing Unofficial Guide") as demo:
    gr.Markdown(
        """
        # 🏠 UCI Continuing Student Housing Unofficial Guide
        Ask anything about UCI continuing student housing — ACC communities, off-campus options,
        costs, noise, parking, and more. Answers are grounded entirely in student Reddit discussions
        and official UCI housing documentation. No hallucination — if the documents don't cover it,
        the system will say so.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            question = gr.Textbox(
                label="Your question",
                placeholder="e.g. What are students saying about mold at ACC apartments?",
                lines=2,
            )
            with gr.Row():
                submit_btn = gr.Button("Ask", variant="primary")
                clear_btn  = gr.Button("Clear")

            gr.Examples(
                examples=EXAMPLES,
                inputs=question,
                label="Example questions",
            )

        with gr.Column(scale=3):
            answer_box = gr.Textbox(
                label="Answer",
                lines=10,
                interactive=False,
            )
            sources_box = gr.Textbox(
                label="Sources used",
                lines=4,
                interactive=False,
            )
            with gr.Accordion("View retrieved chunks", open=False):
                chunks_box = gr.Markdown()

    submit_btn.click(handle_query, inputs=question, outputs=[answer_box, sources_box, chunks_box])
    question.submit(handle_query, inputs=question, outputs=[answer_box, sources_box, chunks_box])
    clear_btn.click(lambda: ("", "", ""), outputs=[question, answer_box, sources_box])

demo.launch(theme=gr.themes.Soft())