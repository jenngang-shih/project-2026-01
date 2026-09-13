<!--
Traceability: not a sourced requirement — a postmortem of topic 2's build,
requested to extract what's reusable for topics 3-4, same convention as
docs/postmortem-topic-1.md. Synthesized from this session's own context —
unlike topic 1, topic 2's entire build happened in one continuous session,
so there was no cross-session recovery step needed here.
-->

# Topic 2 — Postmortem

## What actually happened, in order

Continuing directly from topic 1 in the same session:

1. Switched context to topic 2; found its requirements already categorized
   (from an earlier point in the project) but the topic README still a
   stale stub.
2. Reviewed a Role section the user had copy-pasted from topic 1's
   categorized doc — traced it back to its actual origin (a project-wide
   default with no B-ID, not sourced from either topic's text), tailored
   it to topic 2's real tension (SERP signal vs. compliance authority),
   and restored a dropped Reference bullet (**B2**) found by re-reading the
   source paragraph sentence by sentence.
3. Decided the backend (Azure OpenAI + ChromaDB) over the source's soft
   suggestion (Gemini Flash + Pinecone/Qdrant).
4. Ran `build-topic-executables`: checked `data/SERP_Data.json`'s actual
   shape before classifying **B8** (content-gap detection) — it looked
   parseable but actually needs semantic judgment, so the SERP Analyzer
   Skill was classified `hybrid`, not deterministic.
5. Built `src/`, verified against the real `data/SERP_Data.json` and
   `data/Manual.txt` (not synthetic test data) before any live call —
   caught two real defects this way: a UTF-8 BOM leaking into parsed text,
   and a chunking default that would have collapsed the whole manual into
   one chunk (`Manual.txt` has no blank lines between its 3 rules).
6. Built and verified the Colab notebook (verbatim source porting) — hit a
   missing `Any` import from the porting process stripping each file's own
   `from __future__ import annotations`, fixed it, then hit the same class
   of gap again for `field_validator` after a later schema change.
7. Ran the notebook live against real Azure OpenAI + ChromaDB — hit a
   third real issue: the model returned `recommended_headings`/
   `compliance_notes` as dict-wrapped strings instead of plain ones. Fixed
   at two layers (tightened prompt + a defensive `field_validator`
   coercion), verified against the exact malformed shape reported.
8. Captured B16 evidence from a real downloaded, already-executed notebook
   (`docs/live-run.md` + `docs/live-run/`), including two limitations the
   run itself made visible (keyword-count undercounting, retrieval never
   exercising real discrimination).
9. Addressed **B23** (scalability) with a worked hypothetical-Skill
   diagram, explicit about what's genuinely additive vs. what needs a
   small touch (C1, C5) — not an idealized "fully plug-and-play" claim.
10. Wrote **B12**'s process record and boosted the README into real
    deploy/run documentation.
11. Built `app.py` (Gradio), verified it locally against Fixture clients
    including edge cases (empty keyword, missing data file).
12. Set up git for the whole project, hit a real file silently vanishing
    from disk after a successful commit+push (git-inside-a-OneDrive-synced-
    folder), recovered it via `git checkout HEAD -- <path>`, then pushed to
    a real GitHub repo.
13. Deployed to Hugging Face Spaces — hit two genuine platform-specific
    failures in sequence: a `pydantic` version ceiling conflicting with
    gradio's own `mcp`-extra pin (fixed by relaxing our floor), then a
    `@spaces.GPU`-not-found runtime error from the Space being provisioned
    with GPU/ZeroGPU hardware instead of CPU (fixed in Space settings).
14. Wrote the B20 demo script from the verified live run, then revised it
    against a second, independently confirmed live run (a screenshot of
    the deployed Space) — generalized two content-specific callouts into
    patterns to point at, since the two runs found the same *kind* of
    result with different exact wording each time.

## Grade: A-, same tier as topic 1, for different reasons

**What earns it:**
- **B21 (Technical Rigor)** — arguably stronger evidence than topic 1's
  equivalent: three real bugs caught by testing against actual project
  data *before* shipping, plus one caught live in production and fixed at
  two layers (prompt + defensive coercion), verified against the exact
  reported malformed shape — a genuine catch-diagnose-fix-verify cycle.
- **B22 (Prompt Precision)** — the compliance-overrides-competitive-tactic
  behavior appeared independently across two separate live runs with
  different specific wording each time. That's reproducibility evidence
  for the underlying behavior, not one lucky pass.
- **B12/B18/B19** — substantive, not checkbox docs: a real deploy
  walkthrough that caught two genuine platform-specific failures with
  verified fixes, and a live GitHub repo.

**What keeps it from an unqualified A:**
1. **The exact same class of bug (missing shared import when porting to
   the notebook) recurred three times this topic**, despite being a known
   lesson from topic 1's `schemas.py` drift. Each instance was fixed
   correctly, but the underlying fragility of the porting approach itself
   (relies on manually auditing which names are used, not something
   structurally immune to drift) was never actually fixed.
2. **`keyword_distribution`'s exact-substring limitation was flagged,
   shown to be visibly misleading in a real run, and left unfixed anyway**
   — a legitimate scope call for a prototype, but a decision not to fix,
   not a technical wall, and worth being clear about which one it is.
3. **Retrieval has never actually been tested for discrimination** — the
   manual is still 3 lines/chunks, so `top_k=3` returns everything
   regardless of relevance every time; C4's real value over "just return
   the whole manual" has zero evidence either way.
4. **B23's answer is a plausibility argument, not a demonstration** — a
   well-reasoned hypothetical, but nobody's actually added a second Skill
   to prove it holds.

**Worth naming, not true of topic 1**: the actual AI/RAG mechanism worked
close to correctly on the first real attempt. Nearly all the friction this
time showed up in *infrastructure* — git-inside-OneDrive silently losing a
file, two separate Hugging Face Space deploy failures — which took more
iteration cycles than the prompt/schema logic did.

## What worked

1. **Testing against real project data before any live call** — same
   lesson topic 1's postmortem already named, reconfirmed here: both real
   pre-ship defects (the BOM, the chunking assumption) were found this way,
   not by reasoning about the code in the abstract.
2. **A two-layer fix pattern for live-model drift** — tighten the prompt
   *and* add a defensive schema coercion for the specific shape observed.
   More mature than "just fix the prompt": the coercion is a safety net for
   whenever a model drifts again in a similar way, which is realistic to
   expect from any live model, not a one-time fluke to patch away.
3. **Checking real data before classifying or defaulting**, not just
   inferring from requirement wording — the B8 hybrid classification and
   the chunking-strategy default both came from actually looking at
   `SERP_Data.json`/`Manual.txt`'s real shape first.
4. **Being honest about B23 rather than overclaiming** — a diagram that
   shows the real coupling point (C5) alongside what's genuinely additive
   is more useful and more credible than an idealized "fully modular" claim
   would have been.
5. **Using multiple independent live runs as evidence**, not just one —
   the second run (confirmed via screenshot) is what actually established
   the compliance-override behavior as a pattern rather than a coincidence.

## What didn't work / friction worth avoiding on topics 3-4

1. **The notebook-porting import-drift bug recurring three times.** The
   generator strips each file's own imports to avoid duplicating them
   across cells, which means every source-file change requires manually
   re-auditing that file's full import surface against what the shared
   cell already provides. A real fix would mean the generation step
   actually *executing* each generated cell (not just compiling it) so a
   missing name fails immediately, automatically — proposed, never
   implemented. Worth doing this properly before topic 3 or 4 also gets a
   Colab notebook.
2. **A known, visibly-misleading limitation (`keyword_distribution`) was
   flagged and then left as-is** rather than either fixed or explicitly
   signed off on as acceptable scope. If topic 3/4 surface an equivalent
   "the deterministic piece technically satisfies the letter of the
   requirement but produces a misleading result on real data" situation,
   decide explicitly rather than defaulting to "flag it and move on" again.
3. **Retrieval discrimination was never actually exercised** — only 3
   chunks exist, so top-k retrieval always returns everything. Topic 4 also
   uses `Manual.txt` (per the root README's own Data section) — if it needs
   genuine retrieval-discrimination behavior demonstrated, this exact gap
   will resurface there too.
4. **Running git inside a OneDrive-synced folder caused a real file to
   silently disappear from disk after a successful commit+push.**
   Recovered cleanly via `git checkout HEAD -- <path>`, but this could
   happen to any file, at any time, for topic 3/4's work too, in this
   project's current setup. Worth deciding whether to move the working
   copy outside OneDrive's sync scope before continuing, rather than
   re-discovering this the hard way again.
5. **Deploying to a new platform (Hugging Face Spaces) surfaced two
   unpredictable-in-advance integration failures** (a dependency version
   ceiling conflict, a hardware-tier misconfiguration) that took genuine
   back-and-forth to diagnose. Expect the same category of "first deploy
   to a new platform has platform-specific gotchas" friction if topic 3's
   local-LLM runtime or topic 4's LangGraph app also target a new
   deployment surface.
6. **Repo-scope and naming decisions (standalone vs. monorepo, a repo name
   that didn't match its final scope) needed a mid-flow clarifying
   question** rather than being decided once upfront. Worth deciding the
   whole project's repo strategy explicitly before topic 3/4 also need a
   deploy target, rather than re-litigating it per topic.

## Directly reusable for topics 3, 4

- **The pluggable `LLMClient`/`EmbeddingClient` Protocol pattern**
  (`llm_client.py`), including Fixture equivalents for control-flow testing
  without live calls.
- **"Check real data before classifying or defaulting"** as a standing
  discipline — apply it to whatever topic 3/4's own ambiguous requirements
  turn out to be, the same way it correctly caught B8's real shape here.
- **The Colab-notebook verbatim-porting generator**, with the fix this
  topic never got around to: actually execute every generated cell as part
  of resyncing the notebook, not just compile it, so a missing import fails
  immediately rather than waiting for a live run to surface it.
- **The Gradio-app-on-Hugging-Face-Spaces deployment pattern** (`app.py`
  wrapping an existing orchestrator unchanged, a self-contained
  `requirements.txt`, the YAML frontmatter in `README.md`) — reusable if
  topic 3 or 4 also want a live web demo instead of just a CLI.
- **Multiple independent live runs as reproducibility evidence** for any
  B16-equivalent deliverable — one run alone doesn't show whether a
  behavior is reliable; a second, differently-generated run does.

## Open items

1. Record **B20** (demo video) — the script is ready
   (`topic-2-rag-serp-analyzer/docs/demo-script.md`); this is genuinely the
   last item for topic 2.
2. Decide whether to move the git working copy outside OneDrive's sync
   scope, given the file-loss incident.
3. Decide whether `keyword_distribution`'s exact-match limitation is worth
   improving before this gets shown to a grader, or stays a documented,
   accepted limitation.
4. Decide whether retrieval discrimination needs to be demonstrated with a
   larger manual before this topic is considered fully validated.
