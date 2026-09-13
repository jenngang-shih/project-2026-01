# Topic 4 — Multi-Agent Conflict Resolution

Source of truth for requirements: `../docs/problem-statement.md` (主題四). This README
tracks implementation choices; the problem statement is the contract.

## Goal
Two agents with opposing objectives collaborate through a stateful LangGraph workflow
to reconcile "traffic" vs. "compliance" tension in SEO content planning, converging via
recursive refinement rather than either side simply winning.

## Agents
- **Agent A — SEO Content Planner**: maximizes click-through; prefers punchy, competitive
  keywords/titles.
- **Agent B — YMYL Compliance Auditor**: enforces legal/regulatory compliance and the
  company writing manual (`../data/Manual.txt`); zero tolerance for exaggerated,
  misleading, or high-risk wording.

## Framework / model
- Graph orchestration: **LangGraph**.
- Backing LLM: **Llama** (exact model/runtime to be pinned once we build this topic —
  e.g. via Ollama locally, or a hosted Llama endpoint; not Qwen, despite this folder's
  earlier name).

## Workflow
```
Start -> Planning -> Audit -> Decision Node
                        |            |
                        |    pass -> Final Output
                        |            |
                        +--- fail ---+--> back to Planning (with revision notes)
```
- Conditional edge on Audit outcome: **pass** → emit final result; **fail** → return to
  Planning carrying concrete revision feedback (not just a rejection).
- A hard cap on iterations is required to prevent infinite Planning↔Audit loops.

## Forced conflict edge case (required by spec)
Scenario: user asks for "娛樂城推薦" (casino recommendation) content.
- Planner is seeded to want to include high-CTR phrases like "穩賺不賠" (guaranteed
  profit) or "保證出金" (guaranteed payout).
- Auditor's rules (aligned with `../data/Manual.txt`-style constraints) forbid exactly
  those phrases.
- Expected resolution: the system negotiates down to a compromise that keeps the
  click appeal without the prohibited claims — e.g. honestly disclosing odds/win
  rates, emphasizing security/licensing audits — not a one-sided concession.

## Inputs / Outputs
- **Input:** target topic/keyword (e.g. "娛樂城推薦"), Planner's objective constraints,
  Auditor's compliance rules (sourced from the internal manual).
- **Output:** final content outline/brief, plus the full negotiation transcript
  (state log) showing each Planning → Audit → revision round.

## Deliverables (per problem statement)
- Mermaid graph visualization of the LangGraph topology.
- State logs showing the full negotiate/reject/revise cycle for the forced-conflict case.
- Source code including the State Schema and the max-iteration guard.
- Final article outline plus a summary of what the negotiation resolved.

## Notes
- Async/error handling for LLM latency and API failures is an explicit evaluation
  criterion — don't skip basic retry/timeout handling.
- State must carry enough context that the Planner can see *why* it was rejected, not
  just that it was.
