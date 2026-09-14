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
| Real run against Azure OpenAI | ✅ `docs/topic4_end_to_end_colab_completed_run.ipynb` — real conflict, real rejection, real revision, converged in 2 rounds, zero schema failures |
| Postmortem | ✅ `../docs/postmortem-topic-4.md` |

Also see [`docs/lineage.md`](docs/lineage.md) for a node-by-node walkthrough
(problem statement → both real decisions → the graph build → both real
live-run bugs on the actual path → the real negotiation → final state)
suited to explaining this to someone who already knows the domain.

For a non-technical audience, three companion pieces:
- **["Show Your Work"](https://claude.ai/code/artifact/944e632f-2929-4053-8392-728bafdaeccf)**
  (Claude Artifact, private by default — share from the page itself) — a
  12-slide click-through walkthrough, plain conversational language, no
  domain or technical background assumed.
- **[`Show Your Work.pptx`](Show%20Your%20Work.pptx)** — the same 12 slides
  as a downloadable file, opens directly in Google Slides (File → Import
  slides) or PowerPoint/Keynote.
- **["Prove It First"](https://claude.ai/code/artifact/0c29675d-3b0f-4831-adef-d10b1bd1b65e)**
  (Claude Artifact) and **[`One-Pager.pdf`](One-Pager.pdf)** — a one-page
  written summary covering the same ground, for a reader who wants a
  leave-behind rather than a live presentation.

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

## Real run result

Round 0 hit B9/B10's forced conflict exactly as designed (the Planner's
draft used both banned terms directly). Agent B rejected it with specific,
constructive suggestions — and correctly recognized, live, that
`Manual.txt` doesn't apply to Casino content, confirming a decision made
earlier from static analysis alone. Agent A's round-1 revision genuinely
addressed the feedback (reframing around verifiable process, not
guarantees) rather than one-sidedly conceding — converged in 2 rounds, no
schema/format failures. Full transcript:
`docs/topic4_end_to_end_colab_completed_run.ipynb`.

**Honestly untested by this run**: the `exhausted` (non-convergence) path,
the "Manual.txt genuinely applies" direction (a mortgage-content case),
and B19's async retry/fault-tolerance logic — all verified only by local
Fixture tests, not a live model. See `../docs/postmortem-topic-4.md`'s
open items.

## What's left

Nothing blocking. See `../docs/postmortem-topic-4.md`'s open items for
optional follow-up runs that would round out the live evidence.
