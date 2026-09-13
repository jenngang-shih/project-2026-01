<!--
Traceability: topic-2-rag-serp-analyzer/docs/problem-statement-categorized.md, B12
  ("The full-stack system must be implemented via a Coding Agent, and the
  process/logic followed must be documented.")
Type: human/documentation deliverable — this file is the documentation B12
  itself asks for; the implementation it documents is elsewhere (src/,
  prompts/, component-specs.md).
-->

# Topic 2 — Coding-Agent Process Record (B12)

## The agent

**Claude Code**, in a single continuous session (unlike topic 1, whose build
spanned two separate sessions — see `../topic-1-prompt-chaining/docs/postmortem-topic-1.md`
for that history). Session link:
https://claude.ai/code/session_015zzyCBNPYpKZQuadESVtCs

## Process followed, in actual order

1. **Requirements categorization** (an earlier point in this project, prior
   to topic 2's build proper) — `docs/problem-statement-categorized.md`,
   B1-B23.
2. **Role review and correction.** The Role section had been copy-pasted
   from topic 1's categorized doc without changes. Reviewed on request:
   traced that text back to its actual origin (a project-wide default with
   no B-ID, not sourced from either topic's text), then tailored it to name
   topic 2's actual central tension (SERP competitive signal vs. internal
   compliance authority, tied to B22) instead of leaving topic 1's
   writing/ranking framing unchanged. Also caught and restored a dropped
   Reference bullet (**B2** — the system must weigh both sources together,
   not either in isolation) found by tracing the source paragraph sentence
   by sentence.
3. **Stack decision.** B16/B17 only *suggest* Gemini Flash + Pinecone/Qdrant
   (both explicitly soft — "建議"/"可考慮"). Given the choice, Azure OpenAI +
   ChromaDB was selected instead — reusing topic 1's already-debugged
   `AzureOpenAILLMClient` pattern rather than adding a third LLM provider.
4. **`build-topic-executables` run** (`prompts/master-prompt.md`'s
   procedure) — classified every Objective bullet as deterministic/dynamic/
   hybrid. One classification required checking real data before deciding
   rather than assuming from the requirement's wording: **B8** (content-gap
   detection) looked like it could be pure parsing, but `data/SERP_Data.json`'s
   actual shape (`{rank, title, h2, snippet, source_authority}`) has no
   pain-point field to match against — identifying an *absent* reader need
   requires semantic judgment, so the SERP Analyzer Skill was classified
   `hybrid`, not deterministic. Two engineering defaults with no sourced
   value (retrieval top-k, manual-chunking strategy) were flagged
   `[needs review]` rather than silently picked. Output:
   `docs/component-specs.md`, `prompts/serp-content-gap-detection.md`,
   `prompts/proposal-generation.md`.
5. **`src/` implementation** — `schemas.py`, `llm_client.py` (with
   `FixtureLLMClient`/`FixtureEmbeddingClient` so control flow could be
   tested without live API calls), `prompts.py`, `json_utils.py`,
   `skill.py`, `manual_store.py`, `orchestrator.py`, `cli.py`.
6. **Verification against real data, before any live call.** A fixture-based
   pipeline test run against the actual `data/SERP_Data.json` and
   `data/Manual.txt` (not synthetic test fixtures) caught two real defects
   before they shipped: `Manual.txt` has no blank lines between its 3 rules,
   so the originally-planned paragraph-level chunking default would have
   collapsed the whole manual into one chunk, destroying per-rule
   provenance — fixed to one chunk per non-empty line; and both data files
   carry a UTF-8 BOM that was leaking into chunk text and JSON parsing until
   read with `utf-8-sig`.
7. **Colab notebook generation**, ported verbatim from `src/` rather than
   hand-retyped (a lesson carried over from a real drift bug found in topic
   1's earlier notebook). Verified with a second fixture-based test that
   executes the notebook's own ported cells, not just the real `src/` files.
8. **Live run against real Azure OpenAI + ChromaDB.** Three real runtime
   errors surfaced and were fixed as they occurred, each verified with an
   automated regression check before being called resolved, not just
   reasoned about:
   - A missing `Any` import (the notebook-porting process strips each
     file's own imports to avoid duplicating them across cells, which
     silently dropped a name the real files only got away without
     importing locally because of `from __future__ import annotations`).
   - The same class of gap recurring for `field_validator` after a later
     schema change — audited every source file's full import surface after
     hitting this a second time, rather than patching one name at a time
     again.
   - A live model returning `recommended_headings`/`compliance_notes` as
     lists of single-key objects (e.g. `{"heading": "..."}`) and
     `keyword_guidance` as a multi-key object, instead of the plain strings
     the schema required — fixed at two levels: the prompt's Output-shape
     instructions were tightened with explicit "never an object" language
     and examples, and `schemas.py`'s `ProposalOutput` gained a
     `mode="before"` field validator that coerces the observed shapes into
     strings rather than crashing, as a **B21** (Technical Rigor) safety net
     for whenever a model still drifts despite the clearer prompt.
9. **B16 evidence captured** — `docs/live-run.md`, including an honest
   accounting of two real limitations the live run itself revealed
   (keyword-distribution undercounts near-variants; retrieval hasn't
   actually been tested for discrimination since only 3 manual chunks
   exist), not just the parts that went well.
10. **B23 (scalability) addressed** — a worked hypothetical-second-Skill
    diagram in `docs/component-specs.md`, explicit about what's genuinely
    additive (a new module, schema, prompt file) versus what requires a
    small, contained edit to existing code (C1's orchestrator, C5's prompt)
    — not an idealized "fully plug-and-play" claim.
11. **B19 (this topic's README) rewritten** as deploy/run documentation —
    prerequisites, environment setup, manual ingestion, running the CLI,
    the Colab alternative, and a troubleshooting section drawn from the
    real errors hit in step 8.
12. **This document**, closing B12 itself.

## What "the logic followed" means concretely

Three things ran consistently across every step above, not just as a
one-off practice:

- **Every ambiguous requirement or undocumented default was flagged, not
  silently decided** — the hybrid-Skill classification, the top-k and
  chunking defaults, the stack choice deviating from a soft suggestion, all
  recorded in `component-specs.md`'s run notes rather than assumed and left
  unstated.
- **Every code change was verified against real project data before being
  called done** — fixture tests ran against the actual `SERP_Data.json`/
  `Manual.txt`, not invented test data, and the notebook was verified by
  actually executing its ported cells, not just checked for syntax.
- **Every live-run failure was treated as information, not just noise** —
  each of the three real bugs in step 8 is documented with what caused it
  and why the fix addresses that specific cause, in `component-specs.md`'s
  run notes and this document, rather than being fixed silently and left
  untraced.

## Traceability

| Step above | Artifact(s) |
|---|---|
| 1 | `docs/problem-statement-categorized.md` |
| 2 | `docs/problem-statement-categorized.md` (Role, B2) |
| 3, 4 | `docs/component-specs.md`, `prompts/*.md` |
| 5 | `src/*.py` |
| 6 | `src/manual_store.py`'s chunking + `utf-8-sig` fixes |
| 7 | `topic2_end_to_end_colab.ipynb` |
| 8 | `src/prompts.py`, `prompts/proposal-generation.md`, `src/schemas.py`'s `ProposalOutput` validators |
| 9 | `docs/live-run.md`, `docs/live-run/` |
| 10 | `docs/component-specs.md`'s "Scalability" section |
| 11 | `README.md` |
| 12 | this file |
