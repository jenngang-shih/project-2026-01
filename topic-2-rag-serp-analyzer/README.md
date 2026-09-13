---
title: RAG SERP Analyzer
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 6.27.0
app_file: app.py
pinned: false
---

<!--
The YAML block above is Hugging Face Spaces' required Space-configuration
header (only meaningful if this folder is pushed to a Space — GitHub and
every other renderer just show it as an ignorable frontmatter block, same
as this comment). Everything below is this topic's actual documentation.
-->

# Topic 2 — RAG SERP Analyzer

Full-stack prototype: a "Skill" that analyzes SERP competitor data, a RAG
pipeline over the internal writing manual, and an LLM call that combines
both into an SEO article planning proposal for "房屋二胎" (second mortgage).

## Deploy & run

### Prerequisites

- Python 3.9+ (developed against 3.14; nothing here needs a version newer
  than that, the code just hasn't been tested below 3.9's bare-generic
  typing support).
- An Azure OpenAI resource with **two deployments**: a chat model (e.g.
  `gpt-5.6-terra`) and a separate **embedding** model — topic-2's manual
  ingestion/retrieval genuinely needs the embedding one; it's not optional
  the way it was for topic 1.
- No SERP API key needed — B4 specifies a static provided fixture
  (`data/SERP_Data.json`), not a live call.

### 1. Set up the environment (from the project root, not this folder)

```bash
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your real values:

```ini
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_DEPLOYMENT=<your chat deployment name>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your embedding deployment name>
```

`.env` lives at the project root, not inside this folder — `src/llm_client.py`'s
`load_dotenv()` finds it automatically by walking up from wherever you run
the command, so this works whether you run from the project root or from
inside `topic-2-rag-serp-analyzer/`.

### 2. Ingest the manual (once, or whenever `data/Manual.txt` changes)

```bash
cd topic-2-rag-serp-analyzer
python -m src.cli --keyword "房屋二胎利率" --reingest
```

This chunks and embeds `data/Manual.txt` into a local ChromaDB collection
at `topic-2-rag-serp-analyzer/.chroma/` (gitignored — local state, rebuilt
by re-running this command, not something to commit) and then runs a full
proposal generation in the same command. Omit `--reingest` on later runs —
the collection persists locally between runs.

### 3. Run it for any keyword

```bash
python -m src.cli --keyword "your keyword here"
```

Prints the SERP analysis, retrieved manual passages, and final proposal as
JSON to stdout.

### 4. Or run the actual web frontend (satisfies B3/B14)

```bash
python app.py
```

Opens a local Gradio UI at `http://127.0.0.1:7860` — enter a keyword, see
the SERP analysis, retrieved manual passages, and proposal in separate
tabs. Auto-ingests the manual on first use, so step 2 isn't required first.

**Deploy it as a Hugging Face Space** (this is what makes it a genuine
full-stack deployment, not just a local script) — full step-by-step walkthrough
in **[`docs/huggingface-deployment.md`](docs/huggingface-deployment.md)**.
Short version: push this folder's contents plus a `data/` copy to a new
Space with SDK "gradio" (the `README.md` you're reading already has the
required Space-configuration header at the top), then set the same five
secrets as the Colab setup. Two things worth knowing before deploying:
- **Storage is ephemeral on the free tier**, same as Colab — `app.py`
  re-ingests the manual automatically on first use after every restart, so
  this doesn't need a manual step, just a few extra seconds on first load.
- **Keep the Space private unless you want it public** — a public Space
  with your Azure credentials wired in means anyone who finds it can
  trigger real (billable) Azure API calls on your account.

### Alternative: run in Google Colab, no local setup

`topic2_end_to_end_colab.ipynb` — every cell ported verbatim from `src/`.
Open it in Colab, add five secrets via the 🔑 Secrets panel
(`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`,
`AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`), grant the
notebook access to each, and run all cells top to bottom.

### Troubleshooting

- **`RuntimeError: Manual collection not found`** — run step 2 with
  `--reingest` first; this happens if you try step 3 before ever ingesting.
- **`ValidationError` on the proposal** — a live model occasionally wraps a
  string field in an object instead of returning it plain (a real issue
  this project hit once — see `docs/component-specs.md`'s run notes);
  `schemas.py`'s `ProposalOutput` has a defensive coercion for the shapes
  actually observed, but a sufficiently different malformed response will
  still raise clearly rather than silently accepting garbage.
- **`chromadb` install is slow** — it has a fairly large dependency tree;
  budget a couple of minutes for `pip install`/Colab's `!pip install` cell.

## Status

| Step | Status |
|---|---|
| Requirements categorized | ✅ `docs/problem-statement-categorized.md` (B1-B23) |
| Component specs + prompts (`build-topic-executables`) | ✅ `docs/component-specs.md`, `prompts/*.md` |
| Deterministic code (`src/`) | ✅ Built and verified against real `data/` fixtures (fixture LLM/embeddings) |
| Colab notebook | ✅ `topic2_end_to_end_colab.ipynb` — every cell ported verbatim from `src/`, verified |
| Real run against live Azure OpenAI + ChromaDB | ✅ `docs/live-run.md` + `docs/live-run/` — closes **B16** |
| B18 (architecture diagram) | ✅ `docs/component-specs.md` |
| B23 (scalability) | ✅ `docs/component-specs.md`'s "Scalability" section |
| B12 (coding-agent process documented) | ✅ `docs/coding-agent-process.md` |
| **B3/B14 — real frontend** | ✅ `app.py` — Gradio UI, deployable as a Hugging Face Space (verified locally: imports, builds, runs against Fixture clients, error paths surface correctly) |
| **B19** | ✅ **Fully closed** — deploy/run instructions above, and the code is live at [github.com/jenngang-shih/project-2026-01](https://github.com/jenngang-shih/project-2026-01) |
| B20 (demo video) | ⬜ Not started — the one remaining item across both built topics |

## Code (`src/`)

| File | Role |
|---|---|
| `schemas.py` | Pydantic contracts for every deterministic data shape and dynamic component's JSON output |
| `llm_client.py` | `AzureOpenAILLMClient` (chat) + `AzureOpenAIEmbeddingClient` (embeddings, separate deployment) + Fixture equivalents |
| `prompts.py` | Loads `prompts/*.md`, renders with runtime substitutions |
| `json_utils.py` | Shared JSON-parsing gate (used by both dynamic components) |
| `skill.py` | C2 — heading extraction + keyword distribution (deterministic) + content-gap detection (dynamic) |
| `manual_store.py` | C3/C4 — chunks + embeds `Manual.txt` into ChromaDB, retrieves by keyword |
| `orchestrator.py` | C1 — ties the above together into `generate_seo_proposal(keyword)` |
| `cli.py` | `python -m src.cli --keyword "房屋二胎利率"` |
| `app.py` (topic root, not `src/`) | Gradio web UI — `python app.py`, or deploy as a Hugging Face Space |

Verified end to end against the real `data/SERP_Data.json` and `data/Manual.txt`
(not synthetic test data) via fixture LLM/embedding clients — including one
real finding caught before it shipped: `Manual.txt` has no blank lines
between its 3 rules, so the originally-planned paragraph-chunking default
would have collapsed to one chunk covering the whole file. Fixed to
per-line chunking instead (see `component-specs.md`'s run notes).

## Architecture

Six components — see `docs/component-specs.md` for the full spec, function
signatures, error-handling requirements, orchestration diagram, and the
scalability analysis (B23):

| Component | Type | Role |
|---|---|---|
| C1 — Orchestrator | deterministic | Sequences Skill → retrieval → Proposal Generator |
| C2 — SERP Analyzer Skill | **hybrid** | Heading/keyword extraction (deterministic) + content-gap detection (dynamic — see run notes for why) |
| C3 — Manual Ingestion | deterministic | Chunks + embeds `data/Manual.txt` into ChromaDB |
| C4 — Manual Retriever | deterministic | Vector similarity search for a keyword |
| C5 — Proposal Generator | dynamic | Combines C2 + C4's output into the final proposal |
| C6 — Frontend/API | deterministic | Keyword in, rendered proposal out — `cli.py` (terminal) and `app.py` (Gradio web UI, deployable as a Hugging Face Space) |

**Backend:** Azure OpenAI (LLM + embeddings, reusing topic 1's
`AzureOpenAILLMClient` pattern) + ChromaDB (vector store) — chosen over the
source's soft suggestion of Gemini Flash + Pinecone/Qdrant (B16/B17, both
non-mandatory).

## Prompts

- `prompts/serp-content-gap-detection.md` — C2's dynamic sub-call
- `prompts/proposal-generation.md` — C5, the main synthesis call

## Two open engineering defaults (flagged, not yet decided)

Per `docs/component-specs.md`'s run notes: retrieval top-k (default 3) and
the manual-chunking strategy (default: one chunk per non-empty line, chosen
after checking `Manual.txt`'s actual shape) — neither is a sourced
requirement, both `[needs review]`.

## Live run

`docs/live-run.md` — a real Azure OpenAI + ChromaDB run, not fixture
playback. Strong gap-detection and cross-source synthesis results, plus two
honest limitations worth knowing before calling this done: keyword-count
undercounts near-variants (exact substring match only), and retrieval
hasn't actually been tested for discrimination yet (only 3 manual chunks
exist, so every query returns all of them).

## Data

Shared fixtures at project root: `data/SERP_Data.json` (5 competitor
results for "房屋二胎"), `data/Manual.txt` (internal writing manual to embed).
