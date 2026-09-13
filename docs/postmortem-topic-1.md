<!--
Traceability: not a sourced deliverable — a cross-session postmortem of
topic 1's build, requested to extract what's reusable for kickstarting and
completing topics 2-4. Synthesized from two sources: this project's own
files, and the full local session transcripts for both Claude Code sessions
that touched topic 1 (~/.claude/projects/<project>/*.jsonl — session
a3b13fa0-c7c8-41c1-a6d4-269cf3c441dd, 2026-09-12 00:38-07:29, and session
38ea916b-aae3-4876-b0ca-50850b37c23b, same day, continuing from there).
-->

# Topic 1 — Postmortem

## What actually happened, in order

**Session 1 (`a3b13fa0`, 00:38–07:29)** did far more than build topic 1:

1. Reviewed the fresh scaffold, found and fixed a live secret sitting
   unprotected in a root-level `Authentication-code.md` (moved into gitignored
   `.env` as `AUTH_CODE` — identity still unconfirmed, see Open Items),
   fixed a root `README.md` that was accidentally a byte-for-byte duplicate
   of a topic-4 stub, and renamed a stale `-qwen` folder suffix.
2. Determined that `project-construction-meta-prompt.md` is **not a build
   plan** — it's a documentation template for a project the meta-prompt
   assumes is already finished (with specific metrics, a specific tech stack,
   a specific model-selection narrative) that doesn't match this scaffold at
   all. Correctly redirected to build from `docs/problem-statement.md` +
   `docs/architecture.md` instead, keeping the meta-prompt only for the
   eventual final write-up.
3. Ran `categorize-topic-requirement` (from `prompts/master-prompt.md`) for
   **all four topics**, not just topic 1 — `problem-statement-categorized.md`
   already exists for topics 2, 3, and 4. Fixed two bugs in the procedure
   itself (a stale input path, an incomplete category list) after finding
   them on topic 1, before they could recur on 2-4.
4. Designed and added a second reusable procedure, `build-topic-executables`,
   to `master-prompt.md` — classifies each objective as
   `deterministic`/`dynamic`/`hybrid`/`human`, emits a Role/Goal/Instructions
   prompt per dynamic component and a function spec per deterministic one.
   **Only run against topic 1 so far** — this is directly reusable for 2-4.
5. Ran it for topic 1, produced the four `prompts/*.md` templates and
   `component-specs.md`; caught and flagged two real ambiguities (micro-intent
   selection rule, retry-cap value) rather than silently deciding them.
6. Worked through two rounds of human correction on topic 1 specifically
   (a persona-edit that broke via HTML comment; a miscommunicated "UI
   validation" instruction that got clarified into the SEL human-checkpoint
   design) — resolved by asking rather than guessing.
7. Wrote the real deterministic code (`src/*.py`), set up the venv, and did
   the first genuinely-executed (fixture-based) run end to end, producing
   `docs/sample-run.md` with a clear provenance table (what's AI-simulated vs.
   actually-executed-code vs. a real human decision) and catching a real bug
   (`.env` was never actually being loaded despite `python-dotenv` being a
   listed dependency).

**Session 2 (`38ea916b`, this one)** picked up from there: fixed the
`.env`-loading question further, added Azure OpenAI as a second backend, hit
and fixed a real `max_tokens`→`max_completion_tokens` API error, built and
iterated a Colab notebook, genericized the hardcoded keyword across all four
templates, ran a real live Azure model end to end (which failed all 3 audit
cycles — informative, not a failure), found and fixed a real orchestrator bug
the live run exposed (the final correction could be returned without ever
being re-audited), closed out B4/B17/B19, packaged the folder, and produced
two audience-facing explainers plus this postmortem.

## What worked

1. **The problem-statement → categorize → build-executables → code pipeline
   holds up.** Two clean, reusable procedures now exist in `master-prompt.md`,
   refined on topic 1's real friction rather than in the abstract. Topics 2-4
   already have step one done; only `build-topic-executables` remains before
   any code gets written for them.
2. **Traceability discipline paid for itself later.** Every artifact citing
   its B-ID, every deviation from a sourced requirement flagged rather than
   silently decided (`component-specs.md`'s run notes, each prompt's header
   comment) is exactly what made it possible, sessions later, to audit "are
   B4/B16-19 actually satisfied" with a real answer instead of a guess.
3. **Provenance-labeled runs, not just "it works" claims.** `sample-run.md`'s
   table (AI-simulated / actually-executed-code / human-decision) meant a
   later live run could be meaningfully compared against it instead of
   conflated with it.
4. **Live testing found what fixture testing structurally couldn't.** Both
   real bugs this project found (the `.env`-not-loading gap, and the
   unaudited-final-paragraph gap) were only discoverable by actually running
   the system for real — a fixture run, by construction, never exercises the
   failure paths a genuinely independent model eventually reaches.
5. **Treating the spec documents as fixable, not fixed.** `master-prompt.md`
   itself got debugged mid-use (path bugs, incomplete category list) before
   being run again on topics 2-4 — meaning those runs won't inherit the same
   defects topic 1's first pass hit.

## What didn't work / friction worth avoiding on 2-4

1. **The original scaffold had real, uncaught mismatches** — misnamed
   folders, a duplicated stub README, a meta-prompt describing a different,
   more-advanced project than what existed. Worth a similar sanity pass
   before starting topic 2: check its README, folder naming, and whether the
   meta-prompt's assumed stack for topic 2 (Azure+Chroma) still conflicts
   with `problem-statement.md`'s own suggestion (Gemini Flash +
   Pinecone/Qdrant) — **this was flagged as a soft, undecided ambiguity in
   session 1 and was never actually resolved.** Decide it before building,
   not mid-build.
2. **The `AUTH_CODE` secret has now survived two full sessions unidentified
   and unrotated.** It was a stopgap fix in session 1 ("rename once you know
   what service it is"); nobody has since. Worth actually resolving before
   topic 2, which will likely need its own real vector-DB/API credentials.
3. **Prompt template edits are fragile to blunt find/replace.** Twice now — once
   by manual edit (session 1, Stage B's Role got broken via an accidental
   HTML comment) and once by an automated keyword-genericization pass (this
   session, the intentionally-preserved 娛樂城 worked-example got overwritten
   to `{keyword}` too) — a template ended up silently different from what
   was intended. Worth double-checking template diffs by eye after any bulk
   edit, not just trusting the edit succeeded.
4. **B4-style "research before building" constraints are easy to do after
   the fact instead of before.** Topic 1's B4 (research Search Intent vs.
   Micro-Intent, EEAT/YMYL) was written well after the chain was built, not
   before, as its literal wording implied — self-flagged, not corrected. If
   topics 2-4 have an equivalent pre-build constraint, do it first this time.
5. **Numeric engineering defaults chosen without a sourced rationale are
   genuinely provisional, not just formalities.** The retry-cap default (3)
   was a placeholder from the start; only a real live run revealed both that
   3 isn't always enough for YMYL-heavy content *and* a real bug at the
   cap's boundary. Watch for the equivalent in 2-4 (retrieval top-k / chunk
   size for topic 2, confidence thresholds for topic 3 — topic 4 is already
   better-specified here, with an explicit sourced max-iterations rule).
6. **Topic-level `README.md` stubs stayed stale for the entire build.** Topic
   1's README said "Pending elaboration" through both sessions and dozens of
   real artifacts, only fixed in a late packaging pass. Update it
   incrementally as topics 2-4 progress, not as a final cleanup step.
7. **A "closed" session isn't actually unrecoverable.** `iterative-record.md`
   currently states session 1's history "cannot serve as part of this
   record" since its link wasn't captured before closing — that undersells
   what's true. The session transcript itself is sitting locally at
   `~/.claude/projects/<project-slug>/a3b13fa0-....jsonl` and was fully
   recoverable for this postmortem. Worth correcting that doc, and worth
   remembering generally: local JSONL transcripts under that path are a real
   source of truth across sessions on this machine, not just the current
   one — check there before assuming lost context is actually lost.

## Directly reusable for topics 2, 3, 4

- **Categorization is already done** for all three
  (`topic-{2,3,4}-*/docs/problem-statement-categorized.md` exist) — start
  each at `build-topic-executables`, not step one.
- **`build-topic-executables` itself**, live in `prompts/master-prompt.md`,
  tested and refined on topic 1.
- **The documentation architecture as a template**, not just topic-1
  content: `component-specs.md` (architecture + Mermaid + run notes),
  a pre-build research doc if a B4-equivalent constraint exists, a
  provenance-labeled `sample-run.md`-style doc for every real run, a
  `rationale.md`-style evidence-based writeup once real runs exist, an
  `iterative-record.md`-style session-link pointer, and `README.md` as a
  live deliverables index kept current throughout, not patched at the end.
- **The provenance-labeling convention** (AI-simulated / actually-executed /
  human-decision) for any future run documentation.
- **The pluggable `LLMClient` Protocol pattern** (`AnthropicLLMClient` /
  `AzureOpenAILLMClient` / `FixtureLLMClient`) — directly adaptable, though
  topics 2 and 3 will need their own additions (embeddings client for 2,
  local-runtime client for 3).
- **The Colab-notebook generator pattern** (a script that reads real source
  files off disk and embeds them verbatim, rather than hand-retyping) if
  topics 2-4 also want a portable demo.

## Open items worth deciding before topic 2 starts

1. Identify and rotate the `AUTH_CODE` secret in `.env`.
2. Decide topic 2's actual stack (the meta-prompt's Azure+Chroma vs.
   `problem-statement.md`'s Gemini Flash+Pinecone/Qdrant suggestion) —
   flagged in session 1, never resolved.
3. Correct `topic-1-prompt-chaining/docs/iterative-record.md`'s claim that
   session 1's history is unrecoverable, now that it demonstrably isn't.
