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
| Colab notebook (Phase A + Phase B) | ✅ `topic3_end_to_end_colab.ipynb` — 27 cells; torch-free logic (data, prompt rendering, JSON validation) verified locally; model/training/generation cells not yet run (need GPU + accepted Llama-3 license) |
| Real run on Colab T4 | ⬜ Not started — needs you |
| Audit Report (B16), Reflection (B18) | ⬜ Not started — write these from the real run's output |

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

## What's left

1. Run the notebook on Colab (T4 GPU, `HF_TOKEN` secret, Llama-3 license
   accepted) — the one real live-verification step remaining.
2. Write the Audit Report (B16) and Reflection (B18) from the actual
   output — including an honest account if the fine-tune's small training
   set (12 examples) shows real overfitting, not just the cases where it helps.
