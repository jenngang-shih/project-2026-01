"""Gradio app — the frontend/API layer (C6) for topic 2's RAG SERP Analyzer.
Built to deploy on a Hugging Face Space, but runs anywhere `python app.py`
does. Wraps the existing src/ orchestrator unchanged — this file adds no
new business logic, only a UI around generate_seo_proposal().

Run locally:
    python app.py

Deploy to Hugging Face Spaces (SDK: gradio):
    Push this folder's contents (app.py, requirements.txt, README.md, src/,
    prompts/, data/) to a new Space, then set these as Space secrets
    (Settings -> Repository secrets — never committed as a file):
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_EMBEDDING_DEPLOYMENT.
"""
from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

from src.llm_client import AzureOpenAIEmbeddingClient, AzureOpenAILLMClient
from src.manual_store import ingest_manual
from src.orchestrator import generate_seo_proposal

DATA_DIR = Path(__file__).resolve().parent / "data"
PERSIST_DIR = Path(__file__).resolve().parent / ".chroma"

# Falls back to this folder's own data/ if the shared project-root data/
# doesn't exist alongside it (e.g. when only this topic's folder is what
# got pushed to the Space, not the whole multi-topic project).
if not DATA_DIR.exists():
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_llm: AzureOpenAILLMClient | None = None
_embed: AzureOpenAIEmbeddingClient | None = None


def _clients() -> tuple[AzureOpenAILLMClient, AzureOpenAIEmbeddingClient]:
    """Lazily constructs the Azure clients on first use, not at import
    time — a missing/placeholder secret then surfaces as a clear in-app
    error the first time someone clicks "Generate," inside Gradio's own
    error surface, rather than crashing the whole app before it can even
    render (which would show nothing but a blank Space)."""
    global _llm, _embed
    if _llm is None:
        _llm = AzureOpenAILLMClient()
    if _embed is None:
        _embed = AzureOpenAIEmbeddingClient()
    return _llm, _embed


def _ensure_manual_ingested(embed: AzureOpenAIEmbeddingClient) -> None:
    """Hugging Face Spaces' free-tier storage is ephemeral, same caveat as
    Colab — re-ingest automatically on first use after each restart rather
    than requiring a separate manual step the way the CLI's --reingest
    flag does."""
    if not PERSIST_DIR.exists() or not any(PERSIST_DIR.iterdir()):
        ingest_manual(str(DATA_DIR / "Manual.txt"), embed, persist_dir=str(PERSIST_DIR))


def run(keyword: str, top_k: int) -> tuple[str, str, str]:
    if not keyword or not keyword.strip():
        raise gr.Error("Enter a keyword first.")

    llm, embed = _clients()
    _ensure_manual_ingested(embed)

    try:
        result = generate_seo_proposal(
            keyword.strip(),
            str(DATA_DIR / "SERP_Data.json"),
            llm,
            embed,
            top_k=int(top_k),
            persist_dir=str(PERSIST_DIR),
        )
    except RuntimeError as exc:
        # C1's own error-handling contract (component-specs.md) already
        # raises a clear RuntimeError for a missing/malformed SERP file or
        # an uninitialized manual collection — surface that text directly
        # rather than letting Gradio show a generic traceback.
        raise gr.Error(str(exc)) from exc

    return (
        json.dumps(result.serp_analysis, ensure_ascii=False, indent=2),
        json.dumps(result.retrieved_passages, ensure_ascii=False, indent=2),
        json.dumps(result.proposal, ensure_ascii=False, indent=2),
    )


with gr.Blocks(title="RAG SERP Analyzer") as demo:
    gr.Markdown(
        "# RAG SERP Analyzer\n"
        "Enter a keyword to generate an SEO article planning proposal — "
        "combining competitor SERP analysis (the \"Skill\") with the "
        "internal writing manual's compliance guidance (RAG). "
        "Backend: Azure OpenAI + ChromaDB."
    )
    with gr.Row():
        keyword_in = gr.Textbox(label="Keyword", value="房屋二胎利率", scale=3)
        # max=3 matches data/Manual.txt's current 3 chunks (one per
        # compliance rule, per-line chunking — see component-specs.md's
        # run notes); raise this if the manual grows.
        top_k_in = gr.Slider(label="Manual passages to retrieve (top_k)", minimum=1, maximum=3, step=1, value=3, scale=1)
    run_btn = gr.Button("Generate proposal", variant="primary")

    with gr.Tab("Proposal"):
        proposal_out = gr.Code(label="proposal", language="json")
    with gr.Tab("SERP analysis"):
        serp_out = gr.Code(label="serp_analysis", language="json")
    with gr.Tab("Retrieved manual passages"):
        passages_out = gr.Code(label="retrieved_passages", language="json")

    run_btn.click(run, inputs=[keyword_in, top_k_in], outputs=[serp_out, passages_out, proposal_out])

if __name__ == "__main__":
    demo.launch()
