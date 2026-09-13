# Topic 4 — Multi-Agent Conflict Resolution

Two AI agents with deliberately opposed goals — an SEO Content Planner
chasing click-through, a YMYL Compliance Auditor enforcing legal/compliance
rules — negotiate through a real, stateful `langgraph.graph.StateGraph`
until they converge on a compromise, or honestly exhaust their iteration
budget without one.

## Status

| Step | Status |
|---|---|
| Requirements categorized | ✅ `docs/problem-statement-categorized.md` (B1-B19) |
| Component specs + prompts (`build-topic-executables`) | ✅ `docs/component-specs.md`, `prompts/planner.md`, `prompts/auditor.md` |
| `src/` implementation | ✅ real `langgraph.StateGraph`, async Azure OpenAI calls, retry/backoff (B19), schema-validated agent output |
| Colab notebook | ✅ `topic4_end_to_end_colab.ipynb` — 25 cells, executed end-to-end (Fixture backend) as part of building it, not just syntax-checked |
| Real run against Azure OpenAI | ⬜ Not started — needs you |
| Postmortem | ⬜ Not started — write from the real run |

## Backend decision

`docs/architecture.md` had a stale, pre-topic-1 note about a Llama-based
model for this topic; asked directly, the project owner chose **Azure
OpenAI for both agents**, consistent with topics 1-2 — see
`docs/problem-statement-categorized.md`'s run notes for the full reasoning
and `docs/architecture.md`'s "Resolved" section for the supersession.

## Real finding: `data/Manual.txt` doesn't cover this scenario

Manual.txt (the "company's internal manual" B5 references) is entirely
mortgage/interest-rate-specific — no casino-related rule exists in it at
all. B10's forced-conflict phrases (穩賺不賠/保證出金) are used as their own
explicit fixture rule, not force-fit from a document that doesn't address
this content category. Manual.txt is still loaded as Agent B's
general-purpose reference (a mortgage-content run would be governed by its
real rules), just not the source of this specific scenario's conflict. See
`docs/component-specs.md`'s run notes.

## Architecture

Real `langgraph.graph.StateGraph`, not hand-rolled — see
`docs/component-specs.md` for the full spec, function signatures, and
orchestration diagram:

| Component | Type | Role |
|---|---|---|
| G1 — State Schema | deterministic | `NegotiationState` TypedDict + `PlannerOutput`/`AuditVerdict` pydantic schemas |
| G2 — Planner Node (Agent A) | dynamic | Generates/revises the SEO outline, addressing the Auditor's specific feedback on revision rounds |
| G3 — Auditor Node (Agent B) | dynamic | Blocklist check + Manual.txt judgment, constructive revision suggestions |
| G4 — Decision Node | deterministic | Routes to converged / exhausted / back-to-Planning; updates `history` |
| G5 — Graph Orchestrator | hybrid | The actual `StateGraph` wiring + async retry/backoff fault tolerance (B19) |
| G6 — Output Renderer | deterministic | Graph diagram (from the compiled graph's own introspection), state log, final output |

## Run it

```bash
python -m src.cli                                    # B9/B10's exact scenario
python -m src.cli --keyword "房屋二胎利率" --category Mortgage \
    --required-terms "全台最低利" --max-iterations 3   # a different scenario
```

Or step through `topic4_end_to_end_colab.ipynb` in Colab — it has a
Fixture-backed dry run (no API key needed) before the real Azure OpenAI
cell.

## What's left

1. Run the notebook (or `src.cli`) against real Azure OpenAI — the one
   real live-verification step remaining.
2. Write a postmortem from the real run's output, same convention as
   topics 1-3.
