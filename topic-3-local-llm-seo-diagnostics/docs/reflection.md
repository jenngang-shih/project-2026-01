<!--
Traceability: closes B18 for topic 3. Draws on the real run analyzed in
audit-report.md (topic3_end_to_end_colab_completed-run.ipynb), plus the
already-recorded decisions in problem-statement-categorized.md,
data-split-and-labels.md, and component-specs.md's run notes.
-->

# Topic 3 — Reflection: Local LLM Strengths/Weaknesses, and a Reframe of B18's Own Question

## B18 asks about prompt design; this project's answer has to be about fine-tuning instead

B18 literally asks how *prompt design* was used to improve the local
model's output quality. That's not quite what happened here, and it's
worth stating plainly rather than stretching the answer to fit the
question: the user chose **literal QLoRA fine-tuning** over lighter
prompt-engineering at the very start of this topic, explicitly, over the
lighter alternative. The Complex System Prompt
(`prompts/seo-diagnostic-audit.md`, B5) is **identical** for the base and
fine-tuned runs in `audit-report.md` -- not iterated, not A/B tested, not
varied at all. The lever this project actually pulled to improve output
quality was the fine-tune, not the prompt. So this reflection answers B18
as "what improved output quality, and how" with fine-tuning substituted
for prompt design where the source assumed the latter -- a deviation
that's a direct consequence of the fine-tuning-vs-prompting choice already
recorded, not a new one.

## Strength: Chinese-language comprehension was never the bottleneck

Across all 48 calls, both variants correctly read and reasoned about
Traditional Chinese content -- extracting the right keyword, correctly
identifying which specific claim in a Mortgage or Casino snippet was the
one at issue, and writing fluent English analysis of Chinese input (the
audit prompt's JSON-shape instruction requests reasons/advice without
specifying a language, and both variants defaulted to English). Neither
variant ever misread the content or answered about the wrong claim. For an
8B open-weight model, this is worth stating as a real, unremarkable-only-
because-it-worked baseline: Llama-3-8B-Instruct's multilingual pretraining
was sufficient for this task's actual language demands, and Chinese-input
comprehension was not where the interesting differences between base and
fine-tuned showed up.

## Weakness (base): a fixed critique template, not genuine content evaluation

The clearest, most reproducible weakness in the **base** model, found
across the held-out rows (`audit-report.md`'s full detail):

1. **A recurring "keyword stuffing" flag on content that doesn't have that
   pattern.** Rows 11, 15, and 20 -- a factual statement, a step-by-step
   guide, and a legal citation, none containing repeated keywords -- each
   got some version of an "avoid keyword stuffing" note from base. That's
   not base misreading the content; it's base running something closer to
   a fixed checklist (keyword stuffing / EEAT / YMYL / claim-verification,
   checked off regardless of fit) than actually evaluating what's in front
   of it.
2. **A literal self-contradiction on identical input.** Row 20, run twice
   at different temperatures, got a 60 ("does not provide any actionable
   advice... only quotes a specific law without context") and an 85
   ("provides specific legal references... avoids keyword stuffing, making
   it readable") from the same untrained model on the same text. Low
   variance elsewhere in base's output (a flat 60 repeated across several
   different rows) turns out not to mean stable judgment -- it means the
   template applies the same way regardless of content, and the one time
   it visibly doesn't, base contradicts itself by 25 points.
3. **Hedged, generic language on the planted false theories**, rather than
   naming what's actually true. Base's critique of both planted-theory
   rows says, in effect, "this claim isn't verified" -- correct, but this
   phrasing would fit almost any unverified claim in any domain. It never
   states the specific counter-fact.

## How the fine-tune changed this, using only 12 examples

The fine-tuned variant's advice text is specific to each row's actual
content (a concrete PTT-review detail, a specific bonus-redemption step, a
named legal article), not a recurring generic flag, and -- on the two
planted-theory rows -- it states the correcting fact directly ("keyword
repetition in H1 tags has been a ranking penalty since at least 2006";
"Google explicitly denies [word count as sole ranking factor]") rather
than a generic hedge.

**The strongest single piece of evidence this generalized rather than
memorized**: rows 13 and 19 (held-out) describe false SEO theories
different from the two the fine-tune actually saw in training (row 4:
Meta Keywords tag; row 9: hidden white-on-white text) --
`data-split-and-labels.md` built the split this way specifically to test
this. The fine-tune correctly and consistently named the right counter-fact
for both novel claims. Twelve examples is genuinely a small fine-tuning
set, and the concern raised about it up front (`component-specs.md`'s run
notes: "overfitting risk is genuinely high") was a reasonable one to raise
-- but the held-out result argues against pure memorization, at least on
this specific skill and this sample.

**What this likely is, mechanistically**: the same Complex System Prompt
was already asking for EEAT/YMYL judgment and independent fact-verification
before any fine-tuning happened -- base had access to the same
instructions. The most likely explanation is that the 12 gold-labeled
examples taught the model to actually *follow* that framing with
confidence and specificity, rather than teaching it EEAT/YMYL judgment
from nothing. That's a narrower, more defensible claim than "fine-tuning
taught this model SEO expertise," and it's the honest one: this project's
prompt design (B5's persona, B6's JSON shape) was already doing real work
before the fine-tune; the fine-tune's contribution was getting the model
to reliably act on it instead of falling back on generic instruction-tuned
habits.

## What didn't clearly improve

- **JSON structural compliance** (B21) — fine-tuned failed 2/24 vs. base's
  3/24. Directionally slightly better, but on this sample size that's not
  a demonstrated fix, and 3 of the 5 total failures (across both variants)
  land on one row (12) rather than tracking the fine-tune/base split
  cleanly. Formatting reliability at this model size looks like it's driven
  more by output length/complexity than by which variant is generating it.
- **Row 3** (the one unambiguous keyword-stuffing case) — fine-tuned's
  score spread (0-20) is wider than base's flat 20-20-20. Fine-tuning
  didn't uniformly tighten consistency; it tightened it specifically on
  the rows that needed genuine judgment, and left the already-easy case
  slightly noisier.

## If this were extended past 12 training examples

The clearest next step suggested by this run, not attempted here: more
training examples per content type (currently 2-3 each), especially more
YMYL-overclaim examples (only 3 in the entire 20-row dataset, 1 of them
held out) and more planted-false-theory examples beyond the 4 that exist
in this dataset at all. The generalization result on rows 13/19 is
encouraging at n=2 held-out rows; it is not a claim that this holds at
scale, and a real production version of this system would need a larger,
more varied gold-labeled set before the QLoRA fine-tune's reliability could
be trusted the way the base Complex System Prompt already can be, on its
own, for the parts of the task it already handles adequately.
