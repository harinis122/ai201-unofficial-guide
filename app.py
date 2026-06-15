"""
Gradio web UI for the UCI Housing Unofficial Guide.
Run with: python3 app.py
"""

import gradio as gr
from generate import ask

SOURCE_LABELS = {
    "uci_housing_megathread_2022_2023":      "r/UCI Housing Megathread (2022–2023)",
    "uci_housing_megathread_2023_2024":      "r/UCI Housing Megathread (2023–2024)",
    "are_the_acc_apartments_really_that_bad":"r/Are the ACC apartments really that bad?",
    "acc_vs_offcampus_housing_advice":       "r/ACC vs off-campus housing advice",
    "heard_bad_things_about_acc":            "r/I've heard bad things about ACC — is off campus better?",
    "any_ideas_on_tackling_off_campus_housing": "r/Any ideas on tackling off-campus housing?",
    "what_apartment_communities_dont_suck":  "r/What apartment communities don't suck?",
    "why_choose_acc_over_residence_halls":   "r/Why choose ACC apartments over residence halls?",
    "uci_housing":                           "YouTube: UCI Housing Tour (Non-Dorms) — Pros & Cons",
    "uci_official_housing":                  "YouTube: UCI Official Continuing Student Housing Webinar",
}

EXAMPLES = [
    "What do students say about the wifi at ACC apartments?",
    "How does Camino del Sol compare to other ACC communities?",
    "What should I know about parking at Plaza Verde?",
    "Is ACC housing worth it compared to living off campus?",
    "What are the cheapest ACC housing options?",
]


def handle_query(question: str):
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(
        f"• {SOURCE_LABELS.get(s, s)}" for s in result["sources"]
    )
    return result["answer"], sources or "No sources retrieved."


with gr.Blocks(title="UCI Housing Guide") as demo:
    gr.Markdown(
        """
        # 🏠 UCI Housing Unofficial Guide
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

    submit_btn.click(handle_query, inputs=question, outputs=[answer_box, sources_box])
    question.submit(handle_query, inputs=question, outputs=[answer_box, sources_box])
    clear_btn.click(lambda: ("", "", ""), outputs=[question, answer_box, sources_box])

demo.launch(theme=gr.themes.Soft())