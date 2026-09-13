<!--
Traceability:
  Source: topic-1-prompt-chaining/docs/problem-statement-categorized.md, B19
    ("A Rationale: a short technical explanation of how the prompt design
    ensures EEAT-compliant output.")
  Type: human/documentation deliverable — component-specs.md's run notes
    already flag B19 as outstanding pending real (non-fixture) audit
    behavior; this document closes it, drawing on three independent runs
    rather than design intent alone.
-->

# Topic 1 — Rationale (B19)

## What the prompt design does, mechanically

The chain enforces EEAT compliance through two coupled mechanisms, not one —
Stage B builds in the signal the audit later checks for, and Stage C checks
it against a bar specific enough to actually be enforced rather than
gestured at.

1. **Stage A (C2) scopes the problem down.** Rather than writing generically
   about [娛樂城], Stage A forces selection of one specific micro-intent
   (B7-B9) — this matters for EEAT because "Experience" and "Authoritativeness"
   are meaningless in the abstract; they only mean something relative to a
   specific claim (e.g. "this platform's mobile video lags on a weak
   connection"), which a narrow intent produces and a generic overview
   doesn't.

2. **Stage B (C3) operationalizes EEAT's Experience pillar directly in the
   prompt**, not as an afterthought: B13's persona requirement (veteran
   Taiwanese player, not an analyst/marketer) and B11's constraint (mandatory
   Sensory Details + Objective Critique) are what make "first-hand
   experience" a checkable prompt instruction rather than a vague aspiration.
   B12's "no AI disclaimers / no hollow praise" constraint exists specifically
   to suppress the generic-praise failure mode that would otherwise make
   every output look identical regardless of actual experience.

3. **Stage C's audit (C4a) operationalizes Authoritativeness/Trustworthiness
   and YMYL as a structured, per-claim verdict**, not a holistic
   good/bad rating. Its output shape requires every flagged `reason` to name
   the specific sentence/claim and the principle it violates — "reads too
   promotional" is explicitly disallowed as insufficient (see
   `stage-c-audit.md`'s Output shape constraint). This specificity
   requirement is itself the design choice that makes the audit's rigor
   *visible and comparable* across runs, rather than a single opaque
   pass/fail bit.

4. **Stage C's correction (C4b) is scoped to resolve only what's flagged**,
   preserving the rest of the paragraph — this is what keeps a compliance fix
   from drifting back into generic marketing voice, which would silently undo
   Stage B's B12/B13 work while "fixing" B15.

5. **The orchestrator's retry loop (C1)** bounds this to a fixed cost
   (`retry_cap`) and — since the fix made during this same effort — now
   guarantees that whatever content is finally returned was itself checked by
   an audit call, never just generated in response to one and handed back
   unverified (see the live-run finding below; this was a real gap, not a
   hypothetical).

## Evidence: three independent runs, not just design intent

| Run | Backend | Outcome | What it demonstrates |
|---|---|---|---|
| Fixture-based (`sample-run.md`) | Assistant-authored stand-in, replayed via `FixtureLLMClient` | Pass on audit cycle 2 | The control flow (schema validation, audit→correct→re-audit loop) executes correctly end to end against content with one deliberately planted, findable flaw. |
| In-session live-generated (`iterative-record.md`) | Assistant generating Stage A/B/C live, turn-by-turn, in this session | Pass on audit cycle 2 | The same *category* of violation (an unqualified market-wide superlative) arose organically from independent generation, not a replayed script — and was independently caught and corrected. |
| Real Azure OpenAI (`live-run.md`) | `gpt-5.6-luna`, genuinely independent model, no assistant authorship at any stage | **`final_pass: false`** — all 3 cycles failed | The audit enforced a real, escalating bar (progressively more specific demands for named regulators, license registries, reproducible methodology) that Stage B's honest-hedging corrections never satisfied — and surfaced a genuine orchestrator bug (see below), which none of the staged runs could have revealed. |

## What this shows, including the parts that don't flatter the design

**The mechanism reliably *checks* for compliance; it does not guarantee
compliance is *achieved* within a fixed retry budget.** Two of three runs
passed by the second audit cycle. The third — the only one run against a
genuinely independent model, with nothing staged — did not pass in three
cycles, and reading across its three audits shows why: Stage B's corrections
got progressively better at *disclosing limitations* (no credentials, no
reproducible testing, no editorial review) but never added an actual
verifiable fact (a named regulator, a dated source), because B13's persona —
a lone hobbyist player, not a research team — structurally doesn't have
access to one. That's a real, evidence-based tension between two of this
topic's own sourced constraints: B13 (write as a genuine individual player)
and B15/YMYL (demonstrate Authoritativeness against a money-adjacent topic).
It isn't a flaw in either prompt individually — it's what happens when both
are enforced honestly at once against sufficiently YMYL-sensitive content,
and the audit's specificity requirement (point 3 above) is exactly what
makes this tension visible across three cycles instead of hidden inside a
single pass/fail bit.

**The retry-loop completeness gap this run surfaced is the clearest example
of why a fixture-only demonstration isn't sufficient evidence on its own.**
By construction, a fixture run scripted to pass on cycle 2 never exercises
the cap-exhaustion branch — so the bug where `stage_b_final` could be a
just-generated correction that was never itself audited was invisible until
a genuinely stringent live model actually exhausted the retry budget. It's
now fixed (a `for`/`else` on the retry loop runs one bonus audit specifically
when the cap is exhausted without a pass), verified against both the normal
pass-before-cap case and a new cap-exhaustion test case — but the fact that
it took a live, non-staged failure to find it is itself part of this
rationale: design intent and a passing fixture demonstration are not the same
thing as verified behavior under real model variance.

## Summary (short form)

The chain enforces EEAT/YMYL compliance by making Experience a mandatory,
persona-bound prompt constraint in Stage B (B11-B13) and making
Authoritativeness/Trustworthiness/YMYL a structured, per-claim, machine-
checkable verdict in Stage C (B15), then looping correction against that
verdict under a bounded retry budget that — as of this fix — never returns
content it didn't itself check. Across three independent runs, this reliably
surfaces specific, citable compliance problems rather than vague style
complaints, but it does not guarantee a pass: for content whose honest
persona (B13) cannot supply the verifiable citations its own audit demands
(B15), the mechanism's correct, informative output may legitimately be "still
failing, cap reached" — and the design is built to surface that outcome
rather than force or hide it.

## Traceability

- `research-summary.md` — the Search Intent/Micro-Intent and EEAT/YMYL theory
  this design is built from (B4)
- `component-specs.md` — the architecture and control-flow specs (C1-C4b)
- `sample-run.md`, `iterative-record.md`, `live-run.md` — the three
  evidentiary runs cited above (B16, B17)
