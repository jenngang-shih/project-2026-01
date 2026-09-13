<!--
Traceability: topic-3-local-llm-seo-diagnostics/docs/problem-statement-categorized.md
  Supports B12 (12 rows for fine-tuning/training), B17 (strict train/audit
  separation, zero overlap), and is the direct input to Phase A's QLoRA
  fine-tune. Machine-readable output: data/split_and_gold_labels.json.
-->

# Topic 3 — Train/Held-out Split and Gold Labels

## Why not a plain random split

The 20 rows split 10/10 by `Category` (Casino/Mortgage), but reading all 20
rows individually turned up a second, more consequential axis the given
column doesn't capture: **content type**. A plain random 12/8 draw — even
stratified only by Category — could still land all the genuinely bad
content in one set and all the good content in the other, or put every
planted false theory in the same set, none held out to test against.

## Type taxonomy (self-derived, not in the source data)

| Type | Count | Rows | What it is |
|---|---|---|---|
| A — Legitimate | 11 | 1,5,6,8,10,11,12,15,17,18,20 | Accurate, appropriately hedged, no violations |
| B — YMYL overclaim | 3 | 2,7,14 | Guarantee/overclaim language ("guaranteed profit," "guaranteed approval") |
| C — Planted false SEO theory | 4 | 4,9,13,19 | A deliberately incorrect SEO claim |
| D — Keyword stuffing | 2 | 3,16 | Naked, unnatural keyword repetition |

**B9 in the categorized doc only names one planted-theory example** (Meta
Keywords, row 4) as an illustrative case. Reading the full dataset found
three more: row 9 (white-on-white hidden text — an actual banned black-hat
technique, not just outdated advice), row 13 (claims repeating a keyword
20× in an H1 tag boosts authority), and row 19 (claims word count alone,
regardless of quality, guarantees a #1 ranking).

## Split methodology

**Stratified on Category × Type**, targeting the overall 60/40 (12/8) ratio
within each type, then hand-adjusted to land exactly 6 Casino/6 Mortgage in
training and 4/4 in held-out.

**Deliberate exception for Type C (planted false theories): an even 2/2
split with non-overlapping specific claims in each set**, not the
proportional ~60/40 every other type got. Reasoning: if all 4 planted-theory
rows went to training, held-out would have zero examples to test whether
fine-tuning actually improved error-detection (B20) — the comparison B16
needs would be untestable. If all 4 went to held-out, training would get no
explicit signal for this specific skill. Splitting with **different**
specific claims in each set tests whether the fine-tune generalizes to
catching false SEO theories broadly, not whether it memorized these two
particular ones:
- Training sees: row 4 (Meta Keywords), row 9 (hidden text)
- Held-out tests: row 13 (H1 keyword repetition), row 19 (word-count-only ranking)

**Final split:**
- **Train (12)**: 1, 2, 4, 5, 6, 7, 8, 9, 10, 16, 17, 18
- **Held-out (8)**: 3, 11, 12, 13, 14, 15, 19, 20

## Gold label construction

**Score scale: 0-100.** B6 requires a `Score` field but doesn't specify a
range — an engineering default, not a sourced requirement, flagged the
same way topic 1/2's undocumented defaults were. Chosen over a coarser
1-10 scale so a base-vs-fine-tuned score comparison in the Audit Report
(B16) has room to show a meaningful shift, not just a 1-2-point wobble.

**Method**: for each of the 12 training rows, I acted directly as the
persona B5 wants the deployed model to eventually adopt (a Google official
SEO quality reviewer) and produced a `{score, reasons, actionable_advice}`
verdict — the same shape the fine-tuned model must learn to produce. This
is a teacher-student / distillation setup: a stronger, more capable model
(this session) produces the reference targets a smaller local model
(Llama-3-8B-Instruct) is fine-tuned to imitate. Every label is fully
inspectable and correctable before use — see
`data/split_and_gold_labels.json` for all 12 in full, or spot-check a few
here:

- **Row 2** (severe YMYL violation — "guaranteed 100% profit"): scored 8/100,
  reasons cite the specific false/misleading-claim pattern and its real
  financial-harm risk, not just "sounds too good to be true."
- **Row 4** (planted Meta Keywords theory): scored 10/100, reasons state
  the actual fact being contradicted (Google confirmed this isn't a ranking
  factor, publicly, since 2009) rather than a vague "this seems wrong."
- **Row 18** (cites an official government data source instead of asserting
  its own numbers): scored 90/100 — deliberately held up as the
  Authoritativeness pattern rows 2 and 7 fail to follow, both in the reason
  text and by scoring it among the highest in the set.

## Files

- `data/split_and_gold_labels.json` — machine-readable: full snippet text,
  category, self-derived type tag, and (for training rows) the gold label,
  for all 20 rows in one place. Built by a script that reads the CSV fresh
  each time, not retyped, to avoid transcription drift.
