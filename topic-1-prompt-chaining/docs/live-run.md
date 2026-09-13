<!--
Traceability: exercises the C1 orchestrator (docs/component-specs.md) end to
end using the C2/C3/C4a/C4b prompts in ../prompts/*.md, run live against a
real Azure OpenAI deployment via topic1_end_to_end_colab.ipynb — not a
fixture (contrast docs/sample-run.md, which is fixture-based).
-->

# Topic 1 — Live Run (Azure OpenAI, 2026-09-12)

## Provenance

| Piece | Provenance |
|---|---|
| Stage A output, Stage B (all versions), Stage C audits (all three) | **Real live model output** — an actual Azure OpenAI chat-completions call per stage, via `AzureOpenAILLMClient` running in `topic1_end_to_end_colab.ipynb` in Google Colab. Not fixture playback, not assistant-authored. |
| Intent selection | **Human decision** — the project owner reviewed Stage A's 5 real candidate intents and picked "找到適合自己裝置與玩法的遊戲體驗，並在註冊前確認介面與連線品質" (device/connection-quality fit), same category as prior runs. |
| The retry loop, JSON-schema validation, and `pass`/`fail` results | **Runtime evidence** — produced by `resume_prompt_chain` actually executing against the live Azure responses, recorded in `.sessions/4e96579f-3bc5-465f-88d6-b5b7607e5825.json`. |
| Azure deployment used | *(TBD — not recorded in the session JSON; confirm which of `gpt-5.6-terra`/`gpt-5.6-luna`/other was configured for this run)* |

Raw session file: `.sessions/4e96579f-3bc5-465f-88d6-b5b7607e5825.json` (gitignored — local run state; the files under `live-run/` below are the durable, inspectable record, same convention as `sample-run/`).

## What ran

```
start_prompt_chain("娛樂城")
  → C2 (Stage A) → 5 micro-intents, validated against StageAOutput
  → SEL: human picks intent — 找到適合自己裝置與玩法的遊戲體驗，並在註冊前確認介面與連線品質
      (device/connection-quality fit before registering)

resume_prompt_chain(session_id, selected_intent, retry_cap=3)
  → C3 (Stage B) → paragraph v1 (draft)
  → C4a (Audit)  → pass: false (5 reasons — see below)
  → C4b (Correct)→ paragraph v2
  → C4a (Audit)  → pass: false (6 reasons)
  → C4b (Correct)→ paragraph v3
  → C4a (Audit)  → pass: false (6 reasons)
  → C4b (Correct)→ paragraph v4 — retry_cap (3) exhausted; loop stops WITHOUT
                    auditing v4
  → final_pass: false; stage_b_final = v4 (never itself audited — see finding below)
```

## Result: `final_pass: false` — the retry cap was reached without a pass

Unlike the fixture-based run in `sample-run.md` (which passed on its 2nd audit), this live run's audit component kept finding new, substantive issues across all 3 cycles — each pass raised additional EEAT/YMYL concerns beyond what the previous correction had addressed:

- **Audit v1** (5 reasons): flagged an unqualified device/connection observation phrased almost as a market claim, and — more substantively — noted the paragraph gave no testing date, platform name, device/browser version, or network conditions, making its specific claims ("about one second", "video lags behind audio") unverifiable; also flagged that "smooth interface → willing to bet more" blurs UX quality into a financial-risk implication without a YMYL caveat.
- **Audit v2** (6 reasons, after Stage B added disclosure of untracked test conditions and an explicit "smoothness ≠ safety/legality" caveat): still flagged that the correction leaned on phrases like "official license verification page" and "check if you're in the legally served region" without citing any actual regulator, document, or verification method — i.e., the correction added the right *shape* of caution without any checkable substance behind it.
- **Audit v3** (6 reasons, after Stage B added an explicit "I have no gambling/payments/compliance expertise, no editorial review" disclosure): still flagged that citing "official regulator pages" and "consumer protection agency guidance" without naming a single actual jurisdiction, agency, or URL is a repeated pattern, not a one-off gap — and, more fundamentally, noted the piece never states the author's actual testing scope/methodology in a reproducible way, so no amount of hedging turns a single untracked personal test into an authoritative source.

**Reading across all three audits together**, a pattern emerges: Stage B's corrections got progressively better at *disclosing limitations* (no credentials, no reproducible methodology, no editorial review, no commercial ties) but never actually satisfied the audit's core ask — real, checkable citations (a named regulator, a named license registry, a dated source). That's arguably the audit doing its job correctly: no amount of self-aware hedging substitutes for a verifiable source when the underlying content is a first-hand, un-tracked personal account. It also suggests 3 cycles may be structurally insufficient for a keyword this YMYL-sensitive, if the honest fix requires adding externally-verifiable facts the persona (a lone player, not a research team) doesn't actually have access to.

## Finding: the returned `stage_b_final` was never itself audited

Tracing the orchestrator's loop (`orchestrator.py:100-114`) against this session's `audit_trail`: with `retry_cap=3`, the loop runs exactly 3 audit→correct pairs when every audit fails. The 3rd correction (`stage_b_output_v4_final_unaudited.txt`) is generated *after* the 3rd (final) audit, appended to `audit_trail`, and then the loop exits because `range(3)` is exhausted — **there is no 4th audit call to check that 3rd correction**. `ChainResult.stage_b_final` is simply whatever `current_paragraph` holds at that point — v4, a version whose compliance was never actually verified by the audit step at all.

This is a real gap surfaced by this live run, not something the fixture run (which passed on cycle 2, never reaching the cap) could have revealed.

**Fixed** in `orchestrator.py`'s `resume_prompt_chain` (and the notebook's ported copy): the retry `for` loop now has an `else` clause (Python's for/else — the `else` runs only when the loop completes every iteration without hitting `break`, i.e. exactly the cap-exhausted-without-passing case). When that happens, one more audit call checks the final correction before it's returned — one extra call beyond `retry_cap`, only in this case. `stage_b_final` is now always a version some audit actually evaluated, whether it ultimately passed or not. Verified against both the pass-before-cap case (unchanged: 4 audit_trail entries, passes on cycle 2) and a new cap-exhaustion test (5 corrections/audits as before, plus the bonus audit — `stage_b_final` now correctly reflects an audited version, `final_pass` reflects that bonus audit's real verdict).

## Files in `live-run/`

| File | Contents |
|---|---|
| `stage_a_output.json` | Stage A's 5 real micro-intents |
| `stage_b_output_v1_draft.txt` | Stage B's first draft, pre-audit |
| `stage_c_audit_v1.json` | 1st audit verdict (fail, 5 reasons) |
| `stage_b_output_v2.txt` | 1st correction |
| `stage_c_audit_v2.json` | 2nd audit verdict (fail, 6 reasons) |
| `stage_b_output_v3.txt` | 2nd correction |
| `stage_c_audit_v3.json` | 3rd (final) audit verdict (fail, 6 reasons) |
| `stage_b_output_v4_final_unaudited.txt` | 3rd correction — this is `stage_b_final`, generated after the last audit, never itself re-audited |

## Relationship to this topic's Deliverables

- **B16** (results of Stages A/B/C): this run is now the project's *live-model* data point for B16, alongside the fixture-based run (`sample-run.md`) and the in-session live-generated run (`iterative-record.md`).
- **B19** (Rationale): this run's honest `final_pass: false` outcome, and the unaudited-final-paragraph finding above, are more substantive evidence for B19 than a clean pass would have been — they show the audit mechanism enforcing real rigor, and surface a genuine design boundary condition (the retry-cap/audit-coverage gap) worth explicitly addressing rather than a rationale that only describes the happy path.
