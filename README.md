# SEOFUN AI/SEO Assessment — 2026-01

Four independently-runnable AI/SEO prototypes built against `docs/problem-statement.md`.
See `docs/architecture.md` for how they relate and
[`Four-topic project execution narrative.md`](./Four-topic%20project%20execution%20narrative.md)
for the complete cross-topic account — requirements, decisions, prompt/response
evidence, results, and limitations for all four topics, written per
`prompts/project-construction-meta-prompt.md`'s actual intended use (not a build
plan; see `docs/postmortem-topic-1.md` for why) now that all four topics have
real, evidence-backed results to report.

**Repository:** https://github.com/jenngang-shih/project-2026-01

## Topics
1. [`topic-1-prompt-chaining`](./topic-1-prompt-chaining/README.md) — Micro-intent
   modeling → first-hand-experience simulation → EEAT/YMYL self-audit prompt chain.
2. [`topic-2-rag-serp-analyzer`](./topic-2-rag-serp-analyzer/README.md) — SERP Analyzer
   skill + RAG over the internal writing manual, full-stack demo.
3. [`topic-3-local-llm-seo-diagnostics`](./topic-3-local-llm-seo-diagnostics/README.md) —
   Local LLM (Kaggle) SEO content auditor with JSON-structured scoring.
4. [`topic-4-multi-agent-conflict-resolution`](./topic-4-multi-agent-conflict-resolution/README.md) —
   LangGraph Planner/Auditor negotiation loop for traffic-vs-compliance conflicts.

## Data
Shared fixtures used across topics live in [`data/`](./data):
- `SERP_Data.json` — simulated SERP results for topic 2's Content Gap analysis.
- `Manual.txt` — internal writing/compliance manual, used for RAG (topic 2) and as the
  compliance rules the Auditor agent enforces (topic 4).
- `SEO 診斷測試數據樣本.csv` — 20 labeled content snippets (12 for training/tuning,
  8 held out for audit) for topic 3, including deliberately planted SEO
  misinformation and keyword-stuffing examples.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # then fill in real values; .env is gitignored
```

## Status
- **Topic 1** — built and evidence-backed: deterministic orchestrator + prompts,
  a fixture run, an in-session live-generated run, and a real Azure OpenAI live
  run; all sourced deliverables (B4, B16-B19) closed. See
  `topic-1-prompt-chaining/README.md` for the full index, and
  `docs/postmortem-topic-1.md` for what's reusable from it.
- **Topic 2** — built and evidence-backed: deterministic orchestrator + prompts
  (Azure OpenAI + ChromaDB backend), verified against real project data, a
  real Azure live run (`topic-2-rag-serp-analyzer/docs/live-run.md`), and a
  Gradio frontend (`app.py`, deployed live as a Hugging Face Space). All
  sourced deliverables except B20 (demo video, needs direct human action)
  are closed — see `topic-2-rag-serp-analyzer/README.md` for the full index,
  and `docs/postmortem-topic-2.md` for what worked, what didn't, and what's
  reusable for topics 3-4.
- **Topic 3** — built and evidence-backed: QLoRA fine-tune of
  Llama-3-8B-Instruct on Colab/T4 (a flagged exception to Kaggle, not
  silent), a real completed run (`topic-3-local-llm-seo-diagnostics/docs/
  topic3_end_to_end_colab_completed-run.ipynb`) comparing base vs.
  fine-tuned on 8 held-out rows, and an Audit Report (B16) + Reflection
  (B18) written from that run's actual output — see
  `topic-3-local-llm-seo-diagnostics/README.md` for the full index.
- **Topic 4** — built and evidence-backed: a real `langgraph.StateGraph`
  (Planner/Auditor negotiation loop, Azure OpenAI backend chosen over an
  old stale note suggesting a local Llama model), and a real completed run
  (`topic-4-multi-agent-conflict-resolution/docs/
  topic4_end_to_end_colab_completed_run.ipynb`) — B9/B10's forced conflict
  reproduced, a genuine rejection-and-revision cycle, converged in 2
  rounds — see `topic-4-multi-agent-conflict-resolution/README.md` for the
  full index and `docs/postmortem-topic-4.md` for what worked, what
  didn't, and what's still untested (the exhausted path, B19's
  fault-tolerance logic).

All four topics now have real, evidence-backed results — the postmortems
(`docs/postmortem-topic-{1,2,3,4}.md`) are the fastest way to see what
worked and what's reusable across them. Build order followed
`docs/architecture.md`'s suggested pipeline: Topic 1 → Topic 2 → Topic 3 →
Topic 4.
