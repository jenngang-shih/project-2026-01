<!--
Traceability: not a sourced requirement — a postmortem of topic 4's build,
requested to close out the project's four topics, same convention as
docs/postmortem-topic-1.md, -topic-2.md, -topic-3.md.
-->

# Topic 4 — Postmortem

## What actually happened, in order

1. Found topic 4 already categorized from an earlier point in the project
   (`docs/problem-statement-categorized.md`, B1-B19) — reviewed it against
   the source text sentence by sentence; no corrections needed, unlike
   topic 2's Role-section copy-paste issue.
2. Found a real conflict before building anything: `docs/architecture.md`
   had a stale, pre-topic-1 note — "Topic 4 uses LangGraph with a
   Llama-based model" — contradicting what topics 1-2 had since
   established (Azure OpenAI). Surfaced this explicitly as a question
   rather than silently picking either side; the project owner chose
   **Azure OpenAI for both agents**.
3. Checked `data/Manual.txt`'s actual content before writing anything that
   depended on it — found it's entirely mortgage/interest-rate-specific,
   with zero casino-related rules, even though B10's forced-conflict
   scenario is specifically about casino content. Used B10's own forbidden
   terms as an explicit fixture rule rather than force-fitting them from a
   document that doesn't cover this category — the same "check real data
   before assuming" discipline topics 2-3 already established.
4. Decided (flagged, not asked) to load Manual.txt as static text rather
   than through topic 2's ChromaDB/RAG pipeline — 3 lines has no
   retrieval-discrimination to demonstrate, a limitation topic 2's own
   postmortem already predicted would resurface here.
5. Built `docs/component-specs.md`: six components (G1 State Schema
   through G6 Output Renderer) around a **real** `langgraph.StateGraph`,
   not a hand-rolled equivalent, specifically so B12's graph visualization
   comes from the compiled graph's own `draw_mermaid()` introspection
   rather than a diagram that could silently drift from the code.
6. Wrote `prompts/planner.md` and `prompts/auditor.md`.
7. Built `src/`: `schemas.py` (cross-field-validated pydantic models —
   `passed=true` can't carry issues, `passed=false` can't carry none),
   `llm_client.py` (this project's **first async** `LLMClient` Protocol,
   since B19 asks for real asynchronous handling), `retry.py` (transient
   -error retry kept deliberately separate from schema-validation retry —
   different failure modes, different budgets), `graph.py`, `render.py`.
8. Mid-build, refactored `graph.py`'s Manual.txt loading from an
   internal `__file__`-relative path into an explicit `compliance_reference`
   parameter — a proactive design fix (portability, testability) made
   before it could cause the exact class of notebook-porting bug topic
   2's postmortem flagged, not after.
9. Verified `src/graph.py` locally against a scripted `FixtureLLMClient`
   covering three scenarios — converged, exhausted, and malformed-output
   correctly raising after one retry — before ever touching the notebook.
10. Built the Colab notebook via verbatim source-porting (topics 1-2's
    convention, not topic 3's direct-authorship one, since topic 4 has a
    real `src/` package). Embedded the prompt templates and Manual.txt as
    string constants, matching topic 2's established pattern for Colab's
    lack of local file access.
11. **Actually executed the entire generated notebook end-to-end** (every
    cell except pip-install, Colab-secrets, and the live-Azure cell, via a
    shared exec namespace with a stubbed `google.colab` module) as part of
    building it — implementing the fix topic 2's own postmortem asked for
    ("a real fix would mean the generation step actually executing each
    generated cell") rather than just noting it should happen someday.
12. Sent the notebook. The project owner caught a real bug reading it: the
    Credentials cell used `os`/`userdata`, both only imported in a
    *later* "Shared imports" cell — a genuine cell-ordering mistake my own
    verification had missed, because it skipped the Credentials cell
    entirely (it needs live Colab secrets) and never actually exercised
    its true position relative to the imports. Fixed by merging both
    cells into one, matching how topics 1-2's actual notebooks already
    did this; re-verified by exercising the merged cell for real this
    time (a stubbed `userdata.get`), not skipping it.
13. Sent the corrected notebook. The real Azure run hit a second live
    error: `BadRequestError` — the deployed model (a GPT-5-class
    reasoning deployment) rejects any non-default `temperature`,
    invalidating the original Planner-0.7/Auditor-0.1 differentiation
    (an engineering default flagged before this was known). Fixed by
    dropping the parameter entirely; documented the supersession
    explicitly rather than quietly deleting the original reasoning.
14. The real run then completed cleanly: round 0 hit B10's forced conflict
    exactly as designed, Agent B gave specific constructive feedback and
    **correctly recognized live that Manual.txt doesn't apply to Casino
    content** (confirming, dynamically, a decision made earlier from
    static analysis alone), Agent A's round-1 revision genuinely addressed
    the feedback without one-sided concession, and the negotiation
    converged in 2 rounds with zero schema/format failures.

## Grade: A-

**What earns it:**
- **A design decision confirmed live, not just assumed correct on paper.**
  Agent B's own reasoning, in the real run, explicitly stated Manual.txt's
  rules don't apply to Casino content — the exact judgment the categorized
  doc's run notes predicted would be needed, now demonstrated working, not
  just specified.
- **A genuine negotiation, not a staged one.** Round 0 actually failed
  (both forbidden terms present, as B10 configures), and round 1's fix
  reframed around verifiable process rather than either keeping the
  banned claims or stripping all appeal — directly satisfying B18's
  "genuinely balance, not one-sidedly concede" criterion with real content,
  not an idealized description of what the system is *supposed* to do.
- **The notebook-execution fix topic 2's postmortem asked for actually
  got built this time** — every generated cell runs for real (Fixture
  backend standing in for the two Colab-only cells) as part of the build
  process, closing a lesson two topics old.
- Both real live errors were root-caused, fixed with a full technical
  explanation (not a silent patch), and reverified before being called
  done — the same discipline as every prior topic's live-run fixes.

**What keeps it from an unqualified A:**
1. **The cell-ordering bug was a mistake in my own generator, and my own
   verification had a structural blind spot that let it through.** Skipping
   the Credentials cell during verification (because it needs live Colab
   secrets) meant never actually testing its real dependency on cell
   order — a check that looked rigorous ("execute every cell!") but
   specifically exempted the one cell where the bug lived. An "execute
   everything except X" verification is only as strong as being sure X
   has no bug of its own; here it did.
2. **The temperature error was a foreseeable gotcha, not purely bad luck.**
   Topic 1 had already established that this project's GPT-5-class Azure
   deployments have unusual API restrictions (`max_completion_tokens` vs.
   `max_tokens`); writing a Planner/Auditor temperature split into the
   design without checking whether the same model family also restricted
   `temperature` repeats the same category of miss topic 3's postmortem
   named for its own QLoRA gap — a known-recipe check skipped, not an
   unknowable surprise.
3. **The live evidence is real but narrow (n=1).** The exhausted
   (non-convergence) path, the "Manual.txt genuinely applies" direction
   (a mortgage-content run), and B19's async retry/fault-tolerance logic
   are all completely unexercised against a real model — verified only by
   local Fixture tests, not live evidence. One clean successful run
   demonstrates the core mechanism works; it doesn't cover the requirement
   surface B17 and B19 actually describe.

## What worked

1. **"Check the real data before building anything that depends on it,"**
   now confirmed a fourth time — Manual.txt's actual scope mismatch was
   found by reading the file, not by trusting the source text's framing
   of what "the company's internal manual" would contain.
2. **Surfacing a real, consequential fork as a question instead of picking
   a side silently** — the backend decision, especially given a stale
   contradictory note already sitting in the project's own docs that could
   have caused confusion later if left unresolved.
3. **A proactive refactor** (moving Manual.txt loading out of an internal
   `__file__`-relative path into an explicit parameter) **made before it
   caused a problem**, not after a live run surfaced it — the first time
   in this project a known failure mode was designed around ahead of time
   rather than discovered and then fixed.
4. **Actually executing the generated notebook**, not just syntax-checking
   it — this is what caught the whole class of import-drift bugs that
   recurred three times in topic 2 and never got structurally fixed there.
5. **Root-causing both live-run bugs with a full technical explanation**
   before fixing them, and reverifying after — unbroken across all four
   topics now.

## What didn't work / friction, honestly

1. **A verification step that skips the one cell most likely to have an
   ordering bug isn't full verification.** The Colab-Secrets cell was
   exempted from execution because it needs live secrets — but that's
   exactly the cell most exposed to an import-ordering mistake, since it's
   usually near the top of the notebook. Worth stubbing credentials cells
   fully enough to execute them for real in any future notebook-generation
   task, not skipping them outright.
2. **A known model-family API quirk (topic 1's `max_tokens` restriction)
   should have prompted checking for siblings** (a restricted
   `temperature`, likely other sampling-parameter restrictions on the same
   GPT-5-class deployment family) before writing a temperature-based
   design decision into component-specs.md, not after the live run
   rejected it.
3. **The live evidence base for this topic is thinner than topics 1-3's.**
   A single successful run is real and honestly reported, but a reader
   asking "does this actually handle the case where compliance rules DO
   apply, or where negotiation genuinely fails to converge?" has no live
   answer, only a Fixture-tested one. Worth running at least one more
   scenario (a mortgage-content case, or a deliberately unresolvable
   conflict with a low `max_iterations`) before considering this topic's
   evidence complete, if that matters for how this gets graded externally.

## Directly reusable, if this project continues

- **Actually executing every generated notebook cell as part of building
  it** (stub whatever needs a live credential, don't just skip it) — now
  a proven pattern, not just a lesson written down and not acted on.
- **Checking a model family's known API quirks before designing a feature
  that depends on unrestricted API parameters** — write this check into
  the process the next time any topic specs out per-call sampling
  parameters (temperature, top_p, etc.) for one of these Azure deployments.
- **The async `LLMClient` Protocol pattern** (`llm_client.py`) — if any
  future work in this project needs genuine concurrent LLM calls, this is
  the first place in the codebase that already does it correctly.

## Open items

1. Run at least one more real scenario against live Azure OpenAI — a
   mortgage-content case (to see Manual.txt's rules actually enforced,
   not just correctly declared inapplicable) and/or a low-`max_iterations`
   run (to see the `exhausted` path for real) — before treating B17/B19's
   evidence as complete.
2. Topic 2's demo video (B20) remains the one lingering open item from
   the whole project.
3. The project-wide OneDrive/git-safety question from topic 2's
   postmortem is still undecided.
4. With real, evidence-backed results now in place for all four topics,
   `prompts/project-construction-meta-prompt.md`'s actual intended use — a
   final cross-topic execution narrative — is ready to be written for the
   first time.
