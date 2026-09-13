# Topic 3 — Local LLM SEO Diagnostics

A 24/7, no-external-data-leak SEO content audit system: Llama-3-8B-Instruct,
fine-tuned via QLoRA, framed as a "Google official SEO quality reviewer,"
producing structured `{score, reasons, actionable_advice}` JSON verdicts —
including catching deliberately planted false SEO theories in the test data.

## Status

| Step | Status |
|---|---|
| Requirements categorized | ✅ `docs/problem-statement-categorized.md` (B1-B21) |
| Train/held-out split + gold labels | ✅ `docs/data-split-and-labels.md`, `data/split_and_gold_labels.json` |
| Component specs + prompt (`build-topic-executables`) | ✅ `docs/component-specs.md`, `prompts/seo-diagnostic-audit.md` |
| Colab notebook (Phase A + Phase B) | ✅ `topic3_end_to_end_colab.ipynb` — 27 cells; two real bugs found and fixed on the first live run (see `docs/component-specs.md` run notes) |
| Real run on Colab T4 | ✅ `docs/topic3_end_to_end_colab_completed-run.ipynb`, `docs/topic3_report.html`, `docs/topic3_results.csv` — QLoRA fine-tune (loss 2.51→1.99→1.62) + 48 base-vs-fine-tuned diagnostic calls on the 8 held-out rows |
| Audit Report (B16), Reflection (B18) | ✅ `docs/audit-report.md`, `docs/reflection.md` — written from the real run's actual output, including where fine-tuning did and didn't help |

Also see [`docs/lineage.md`](docs/lineage.md) for a node-by-node walkthrough
(problem statement → split/labels → fine-tune, including the three real
live-run bugs on the path → per-row results → report) suited to explaining
this to someone who already knows the domain, and
[`../docs/postmortem-topic-3.md`](../docs/postmortem-topic-3.md) for what
worked, what didn't, and what's reusable for topic 4.

For a non-technical audience, three companion pieces:
- **["Show Your Work"](https://claude.ai/code/artifact/78ef724f-e31f-4668-a3c3-687672b3cebd)**
  (Claude Artifact, private by default — share from the page itself) — a
  13-slide click-through walkthrough, plain conversational language, no
  domain or technical background assumed.
- **[`Show Your Work.pptx`](Show%20Your%20Work.pptx)** — the same 13 slides
  as a downloadable file, opens directly in Google Slides (File → Import
  slides) or PowerPoint/Keynote.
- **["Prove It First"](https://claude.ai/code/artifact/2b3effdc-707f-491e-945a-4965d30ff6aa)**
  (Claude Artifact) and **[`One-Pager.pdf`](One-Pager.pdf)** — a one-page
  written summary covering the same ground, for a reader who wants a
  leave-behind rather than a live presentation.

## Platform/model exception

B3/B15 name **Kaggle Kernels**; this deploys on **Colab with a T4 GPU**
instead, per explicit direction — flagged in
`docs/problem-statement-categorized.md`'s run notes, not a silent
substitution. Model: **Llama-3-8B-Instruct** (gated on Hugging Face —
you'll need to accept Meta's license and provide an `HF_TOKEN` Colab
secret; see the notebook's own intro cell for exact steps).

## Architecture

Two phases — see `docs/component-specs.md` for the full spec, function
signatures, error-handling requirements, and orchestration diagram:

| Component | Phase | Type | Role |
|---|---|---|---|
| T1 — Data Split | A (done) | deterministic | Stratified 12/8 split, Category × content-type, fixed seed |
| T2 — Gold Label Synthesis | A (done) | dynamic | Teacher-student: this session as the reviewer persona, 12 targets |
| T3 — QLoRA Fine-tune | A | deterministic (training) | Fine-tunes Llama-3-8B-Instruct on the 12 gold-labeled examples |
| R1 — Orchestrator | B | deterministic | Batches the 8 held-out rows across both model variants |
| R2 — Diagnostic Inference | B | dynamic | The actual audit call — EEAT/YMYL judgment + independent fact-verification |
| R3 — JSON Validation Gate | B | deterministic | Defensive extraction + schema validation (handles fenced/chatty output, not just clean JSON) |
| R4 — Consistency Harness | B | hybrid | 3 calls per row/variant at 3 temperatures (B8) |
| R5 — Post-processing | B | deterministic | HTML report + DataFrame (B14) |

## Data

`data/split_and_gold_labels.json` — all 20 rows from the shared
`data/SEO 診斷測試數據樣本.csv` fixture, with the stratified split and the 12
training gold labels. Full methodology, including a real finding (4 planted
false-theory rows exist, not the 1 named in the source) in
`docs/data-split-and-labels.md`.

## Real run results

The fine-tune generalized on the sharpest test available: rows 13 and 19
(held out) plant *different* false SEO theories than the two the model
trained on, and the fine-tuned variant correctly named the specific
counter-fact for both, consistently across all 3 temperatures — evidence
against pure memorization of the 12 training examples, not proof it holds
at scale. Base's most reproducible weakness was a fixed "keyword stuffing"
critique template applied even to content without that pattern, including
one literal self-contradiction on identical input (row 20, 60 vs. 85
across two temperatures). JSON structural compliance (B21) came in at
89.6% (43/48), not the idealized 100%. Full detail, all scores, and
verbatim quoted model output: `docs/audit-report.md`;
what this says about the local model and about B18's own "prompt design"
framing: `docs/reflection.md`.

## What's left

Nothing outstanding for this topic's own deliverables. The LoRA adapter
weights (`docs/llama3-seo-audit-adapter/`, ~53MB) are gitignored —
reproducible by re-running the notebook's fine-tune cell, not versioned.
