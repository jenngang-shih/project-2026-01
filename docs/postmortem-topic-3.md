<!--
Traceability: not a sourced requirement — a postmortem of topic 3's build,
requested to extract what's reusable for topic 4, same convention as
docs/postmortem-topic-1.md and docs/postmortem-topic-2.md.
-->

# Topic 3 — Postmortem

## What actually happened, in order

1. Two upfront decisions were made explicitly by the project owner, not
   silently defaulted: **literal QLoRA fine-tuning** over a lighter
   prompt-engineering-only approach (despite no ground-truth labels
   existing yet for the fine-tune to train on), and **Llama-3-8B-Instruct**
   as the model. A third — **Colab/T4 instead of Kaggle Kernels** — was
   requested explicitly as a named exception, not a silent substitution.
2. Before building the train/held-out split, read all 20 rows of the real
   dataset individually rather than trusting the source's own framing.
   This surfaced two things the source text didn't mention: a second,
   more consequential axis beyond `Category` (a self-derived content-type
   taxonomy — legitimate / YMYL-overclaim / planted-false-theory /
   keyword-stuffing), and **four** planted false SEO theories in the data,
   not the one example the source names.
3. Built the split with a deliberate, explained departure from a plain
   stratified draw: an even 2/2 split for the planted-false-theory type,
   with **different specific false claims** in training vs. held-out
   (Meta Keywords tag / hidden text in training; H1-repetition /
   word-count-only ranking in held-out) — specifically so a later
   comparison could test generalization, not memorization.
4. Produced the 12 gold training labels by acting directly as the
   deployed model's own persona (a teacher-student / distillation setup),
   and explained the full methodology transparently when asked
   ("did you use stratified learning, etc.") rather than a one-line answer.
5. Wrote `component-specs.md` naming the two-phase (train-once /
   per-request) architecture, flagging every undefaulted hyperparameter
   `[needs review]`, and — before any run happened — explicitly naming
   the real risk: "12 training examples is a very small fine-tuning set...
   overfitting risk is genuinely high."
6. Built the full 27-cell Colab notebook authored directly (not ported
   from a `src/` package, since the deliverable itself is the notebook).
7. The first live run surfaced three real, sequential problems:
   - A gated Hugging Face repo (403) — an account/license issue, not a
     code bug; remediation given, resolution left to the project owner.
   - `apply_chat_template`'s return type not being consistent across
     `transformers` versions — fixed at both call sites, verified,
     documented, committed, pushed.
   - A CUDA OOM during training on the T4 — root-caused to a missing
     `prepare_model_for_kbit_training` call (no gradient checkpointing),
     fixed, verified, documented, committed, pushed.
8. The fixed notebook ran successfully end-to-end: training loss declined
   smoothly (2.51 → 1.99 → 1.62) over 3 epochs on the 12 examples, and
   Phase B completed all 48 base-vs-fine-tuned diagnostic calls across the
   8 held-out rows at 3 temperatures each.
9. Analyzed the real output rigorously rather than eyeballing a truncated
   summary: pulled the full untruncated HTML report, computed per-type
   score means and JSON validity, and — importantly — **caught two of my
   own drafting errors before publishing** (see "What didn't work" below).
10. Wrote the Audit Report (B16) and Reflection (B18) from the verified
    real data, including an explicit reframe: B18 asks how *prompt design*
    improved output quality, but the same prompt was used unchanged for
    both variants here — fine-tuning was the actual lever, and the
    reflection says so rather than stretching the answer to fit the
    literal question.
11. Folded the completed-run notebook, HTML report, and results CSV into
    the repo; gitignored the 53MB adapter directory (reproducible, not
    worth versioning); updated both READMEs.

## Grade: A-

**What earns it:**
- **Real generalization evidence, not an assumed one.** The fine-tune
  correctly and consistently named the specific counter-fact for two
  planted false theories it never trained on (different claims than the
  two it did see) — a legitimate answer to the overfitting risk flagged
  before training even started, not an after-the-fact rationalization.
- **A found, reported, quoted self-contradiction in the base model**
  (row 20 scored 60 and 85, on identical input, across two temperatures) —
  the kind of finding that only shows up when you read the actual output
  rather than trusting a summary statistic.
- **Reading the real 20-row dataset before splitting or labeling it**
  caught a real discrepancy (4 planted theories, not 1) the source text
  itself got wrong — the same "check real data before classifying"
  discipline topic 2's postmortem already named as reusable, applied
  successfully again here.
- **Every engineering default and every risk was flagged before the
  run that could have confirmed or refuted it**, not adjusted
  retroactively to look prescient.

**What keeps it from an unqualified A:**
1. **Two of the three live-run bugs were foreseeable, not surprises.**
   `prepare_model_for_kbit_training` before attaching LoRA to a 4-bit
   model, and the version-sensitivity of `apply_chat_template`'s return
   type, are both well-documented parts of the standard QLoRA recipe —
   this is a real gap in the first draft, not bad luck, and it cost the
   project owner three separate live-error round trips to Colab to
   surface. Unlike topic 2's Hugging Face Space failures (genuinely
   platform-specific and hard to predict in advance), these were
   knowable ahead of time.
2. **I made two real drafting errors writing the Audit Report** — a
   direct quote spliced from two different temperature outputs presented
   as one continuous quote, and a claim that fine-tuned output
   misapplied a "keyword stuffing" flag that, on checking, it never
   actually made. Both were caught and fixed only because of a deliberate
   re-verification pass against the full untruncated HTML report before
   publishing, not because the first draft was careful enough on its own.
   Working from a truncated pandas printout the first time through is
   what created the opening for both errors.
3. **The evidence base is real but small**: 8 held-out rows x 3
   temperatures, thinned further by JSON validation failures, means each
   per-row comparison rests on 2-3 data points. Both B16 and B18 say this
   plainly, but it bears repeating here: this is a directionally
   consistent, honestly-reported result, not a large-sample one.
4. **The gated-repo resolution was never confirmed back.** The notebook
   subsequently ran, so it evidently got resolved somehow (license
   accepted, or another path), but which of the offered remediations the
   project owner actually took was never explicitly stated or asked
   after — a minor gap in the record, not a technical problem.

## What worked

1. **Reading the real data before splitting or labeling it**, the same
   discipline reconfirmed from topic 2 — found the true content-type
   taxonomy and the "4 not 1" planted-theory count, neither visible from
   the source text alone.
2. **Naming the overfitting risk before running anything**, then treating
   the actual result as a real test of that stated concern rather than
   either dismissing it or declaring victory. The held-out generalization
   finding is credible specifically because the risk was on the record
   first.
3. **Being transparent about methodology when asked directly** — the
   stratified-split and teacher-student/distillation explanation was
   given in full, not summarized to "yes, basically."
4. **A verification pass on the Audit Report before publishing it** —
   re-extracting the full untruncated model output and cross-checking
   every quote caught two real errors that a plausible-sounding first
   draft would otherwise have shipped unnoticed.
5. **Root-causing both live-run bugs, not just patching them** — each fix
   is documented in `component-specs.md`'s run notes with an explanation
   of the underlying mechanism, not just "changed X to Y."

## What didn't work / friction worth avoiding on topic 4

1. **No pre-flight checklist against the standard recipe for the
   technique being used.** QLoRA has a well-known set of required steps
   (`prepare_model_for_kbit_training`, gradient checkpointing,
   `use_cache` toggling); the first-draft notebook was missing one of
   them, and it took a live OOM to surface it. If topic 4's LangGraph
   work has an equivalent "known correct recipe" (a standard
   multi-agent-loop pattern, a standard checkpointing approach), check
   the draft against it explicitly before the first live run, rather than
   treating the live run as the primary way such gaps get found.
2. **Quoting model output from a truncated pandas printout is a real
   trap.** Pandas silently truncates string columns (`...`), and building
   an analysis from that truncated view risks stitching together partial
   fragments as if they were complete, accurate quotes. **Standing rule
   for topic 4 and beyond: always pull the full untruncated text (the
   raw JSON, or an HTML/dict rendering) before quoting model output in
   any report, never the default DataFrame print.**
3. **Each live-run fix required a full round trip through the project
   owner's own Colab session** (three separate times this topic) — real
   latency, unavoidable for anything that genuinely needs GPU + gated
   model weights, but worth asking upfront on topic 4 whether more of its
   logic can be verified locally/offline first, if its runtime also needs
   a live environment neither of us can execute directly.
4. **The gated-repo resolution path was left unconfirmed.** Worth
   explicitly asking "which fix did you end up using?" rather than
   silently inferring resolution from the run succeeding, next time a
   similar account-side blocker comes up.

## Directly reusable for topic 4

- **"Read the real data before classifying, splitting, or defaulting
  anything"** — now confirmed as a working discipline across all three
  topics built so far (topic 2's `SERP_Data.json`/`Manual.txt`, topic 3's
  20-row CSV). Apply it to topic 4's own data (it also uses
  `data/Manual.txt`, per the root README) the same way.
- **"Flag every risk and every engineering default before the run that
  could confirm or refute it, then report the real outcome honestly
  either way"** — the pattern that made this topic's overfitting-risk
  finding credible; apply it to whatever topic 4's own unproven design
  choices turn out to be (a LangGraph negotiation loop has plenty of
  candidates: max negotiation rounds, what counts as a stalemate, etc.).
- **New this topic: always re-verify quoted model output against
  full, untruncated source text before publishing a report built from
  it** — a lesson earned by catching two self-introduced errors, not one
  to relearn on topic 4.
- **New this topic: check a technique's standard, well-documented recipe
  explicitly before the first live run**, rather than relying on a live
  failure to surface a foreseeable gap.
- **The catch-diagnose-fix-verify-document-commit-push cycle** for live
  errors, now exercised across all three topics' live runs — keep using
  it unchanged for whatever topic 4's own live-run surprises turn out to
  be.

## Open items

None outstanding for topic 3's own deliverables — see
`topic-3-local-llm-seo-diagnostics/README.md`. Two loose ends worth
closing whenever convenient, not blocking:
1. Confirm which gated-repo remediation the project owner actually used
   (license approval wait, or a model switch), purely for the record.
2. The project-wide open item from topic 2's postmortem — deciding
   whether to move the git working copy outside OneDrive's sync scope —
   is still undecided and still applies to topic 4's work too.
