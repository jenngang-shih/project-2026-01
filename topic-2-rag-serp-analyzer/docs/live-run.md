<!--
Traceability: exercises the C1 orchestrator (docs/component-specs.md) end to
end using the C2/C4/C5 prompts and code in ../src/ and ../prompts/*.md, run
live against real Azure OpenAI (chat + embeddings) and a real ChromaDB
collection via topic2_end_to_end_colab.ipynb in Google Colab — not a
fixture. Closes B16 for topic 2.
-->

# Topic 2 — Live Run (Azure OpenAI + ChromaDB, 2026-09-12)

## Provenance

| Piece | Provenance |
|---|---|
| SERP analysis (headings, keyword distribution, content gaps), retrieved manual passages, proposal | **Real live output** — an actual Azure OpenAI chat-completion call for gap detection, one for proposal generation, and real Azure OpenAI embedding calls for manual ingestion + retrieval, via `topic2_end_to_end_colab.ipynb` running in Google Colab against a real ChromaDB collection. Not fixture playback, not assistant-authored. |
| Deterministic pieces (heading extraction, keyword counting, chunking, orchestration) | **Application-generated artifact** — the same `src/*.py` code as this repo, ported verbatim into the notebook and executed for real. |
| Raw evidence | `docs/live-run/executed_notebook.ipynb` — the actual downloaded, already-executed Colab notebook (every cell's real output embedded), not a fixture or a re-typed transcript. `serp_analysis.json`, `retrieved_passages.json`, and `proposal.json` are extracted from its final cell's output for easier inspection without opening the notebook. |

## What ran

```
Keyword: 房屋二胎利率

C2 (SERP Analyzer Skill, hybrid)
  → extract_headings()        — deterministic, 5/5 results
  → keyword_distribution()    — deterministic, exact-substring count
  → detect_content_gaps()     — dynamic (live Azure call) → 2 gaps found

C3 (Manual Ingestion, offline/once) → 3 chunks (one per compliance rule) embedded into Chroma

C4 (Manual Retriever)
  → embed(keyword) + similarity search → 3/3 passages retrieved (all chunks — see Limitations)

C5 (Proposal Generator, dynamic, live Azure call)
  → combines C2 + C4 output → final proposal, schema-valid on this run
```

## Result: a genuinely strong run, with two honest limitations

**What worked well, and is worth calling real evidence, not just "it ran":**

- **Gap detection was substantive, not generic.** The model found two distinct, well-evidenced pain points — (1) actual total borrowing cost beyond the nominal rate (setup/account/agent/penalty fees, APR, total repayment), and (2) what happens if the borrower defaults (lien seniority vs. the first mortgage, foreclosure risk, negotiation options) — and for each one, explicitly checked all 5 competitor results and gave a specific reason each misses it. Notably, it correctly distinguished Rank 2's "被騙了怎麼辦" (recourse for being scammed) from genuine repayment default, rather than treating any risk-adjacent heading as covering the gap. See `serp_analysis.json`.
- **The Proposal Generator did real cross-source synthesis, not concatenation.** `proposal.json`'s third compliance note explicitly takes Rank 3's "24hr disbursement" and Rank 4's "low rate" as competitive patterns worth referencing, then states they must not be extended into "guaranteed approval" or "lowest rate nationwide" language — directly implementing the prompt's "if a compliance rule and a competitive tactic conflict, compliance wins" instruction. This is direct evidence for **B22** (Prompt Precision), not just an assertion that the prompt asks for it.
- **Schema compliance held.** Every field came back as the required plain string/list of strings, citations folded into the text itself — the prompt-tightening (and/or the defensive `field_validator` coercion) worked; this run doesn't by itself prove which one did the work, since the printed output is post-validation either way.

**Two real, visible limitations — worth naming rather than glossing over:**

1. **`keyword_distribution` is nearly all zeros** (`serp_analysis.json`), and that's not a fluke — the deterministic counter does exact substring matching, so "二胎房貸利率" or "銀行二胎利率" in a competitor's heading don't count toward "房屋二胎利率" even though they're clearly the same topic. B7 asks the system to "identify keyword distribution across competitor content" — the current implementation technically does that, but in a way that undercounts real usage badly enough to be visibly misleading on this exact run.
2. **Retrieval hasn't actually been tested for discrimination.** With only 3 manual chunks total and `top_k=3`, every query returns all 3 regardless of relevance — the near-identical similarity scores (0.78-0.79 in `retrieved_passages.json`) reflect that, not a real ranking. This component's actual retrieval behavior won't be observable until the manual has more content than any single query needs.

## Relationship to this topic's Deliverables

- **B16** (results): closed by this run — real, evidence-backed output from all three components (C2, C4, C5), not simulated.
- **B21** (Technical Rigor): the dict-wrapped-string bug this pipeline hit and recovered from on an earlier attempt (see `component-specs.md`'s run notes) is itself B21 evidence — the system's error handling was exercised for real, not just designed for.
- **B22** (Prompt Precision): the compliance-overrides-competitive-tactic behavior in `proposal.json` is direct, specific evidence, not an inference from the prompt's wording alone.
- **Still open**: B3/B14 (a real frontend beyond the CLI), B12/B19 (process documentation + an actual git repo + run instructions), B20 (demo video), B23 (scalability — never demonstrated with a second Skill).
