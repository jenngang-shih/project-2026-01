<!--
Traceability: closes B16 for topic 3. Built entirely from a real run's
output -- topic3_end_to_end_colab_completed-run.ipynb (Colab, T4 GPU,
Llama-3-8B-Instruct base + QLoRA fine-tuned variants), not fixture or
hand-authored data. Source artifacts: topic3_report.html (full per-row HTML
report), topic3_results.csv (flat 48-row table). All quoted model output
below is copied verbatim from those artifacts, not paraphrased.
-->

# Topic 3 — Audit Report (real run, base vs. fine-tuned, 8 held-out rows)

## What this is

The 8 held-out rows (`data/split_and_gold_labels.json`) run through both
model variants -- the unmodified base Llama-3-8B-Instruct and the same
weights with the QLoRA adapter attached -- at 3 temperatures each (0.1,
0.7, 1.0), 48 calls total. Both variants use the **identical** Complex
System Prompt (`prompts/seo-diagnostic-audit.md`, B5); nothing about the
prompt changed between runs. Any difference in output is attributable to
the fine-tune, not to prompt iteration -- see `reflection.md` for why that
matters for how B18 is answered.

None of these 8 rows, or their specific content, appeared in the 12
training rows. Two of them (13, 19) are planted false SEO theories whose
*specific claims* are different from the two planted theories the model
did see in training (row 4: Meta Keywords tag; row 9: hidden white-on-white
text) -- see `data-split-and-labels.md` for why the split was deliberately
built this way.

## Structural compliance (B21)

**43/48 valid JSON = 89.6%**, not 100%. Failures split 3 base / 2
fine-tuned -- not a fine-tuning regression, and not clustered by
temperature. Interestingly, 3 of the 5 failures land on a single row (12,
the PTT-review legitimate-content row): base failed at both 0.7 and 1.0
(both "Illegal trailing comma before end of array"), fine-tuned failed
once at 0.7 (a different failure mode, "Expecting ',' delimiter"). The
other two failures -- base on row 14 ("Unbalanced braces"), fine-tuned on
row 20 ("Expecting ',' delimiter") -- are distinct malformation types
again. There's no single root cause across all 5; the pattern worth naming
is that row 12 alone accounts for 3 of the 5 failures across both variants,
and its gold judgment calls for a longer `reasons` list than most other
rows -- consistent with longer JSON arrays being where this 8B model's
formatting is least reliable, though 3 failures on one row isn't enough to
call that proven. This is the real, observed compliance rate for B21 --
not the idealized
claim the framing invites.

## Score comparison by content type (valid outputs only)

| Type | Rows | Base mean | Fine-tuned mean | Direction |
|---|---|---|---|---|
| A — Legitimate | 11, 12, 15, 20 | 64.5 (n=10) | 87.8 (n=10) | fine-tuned scores genuinely good content **higher** |
| B — YMYL overclaim | 14 | 20.0 (n=2) | 5.0 (n=3) | fine-tuned scores the risky claim **lower** |
| C — Planted false theory | 13, 19 | 13.3 (n=6) | 1.7 (n=6) | fine-tuned scores the false claim **lower**, more decisively |
| D — Keyword stuffing | 3 | 20.0 (n=3) | 10.0 (n=3) | fine-tuned scores it **lower** |

The overall mean across all valid calls (21 base, 22 fine-tuned) barely
moves (base 39.3 vs. fine-tuned 42.4) -- reporting only that number would
understate, almost hide, the
actual effect. The real pattern is a **sharpening of discrimination in
both directions at once**: fine-tuned pushes legitimate content up and
every flavor of bad/risky content down, relative to base. Base's scores
cluster in a narrower, more indecisive middle band (mostly 60s regardless
of content quality) that doesn't distinguish a real recommendation from a
YMYL-risk overclaim nearly as sharply.

## Row-by-row: what the model actually said

### Rows 13 & 19 — the planted false theories (B20's real test)

**Row 13** ("2026年最有效的SEO技巧是將關鍵字放在H1標籤內重複20次，這能顯著提升網頁的權威性與排名" -- claims repeating a keyword 20x in an H1 tag boosts ranking authority):

- Base (temps 0.1/0.7/1.0): scores 0/20/15. All three flag it, but hedge --
  *"Claim not verified: the text asserts an SEO tactic without providing
  evidence or credible sources to support it"* (0.1); *"doesn't provide
  credible evidence to support the claim"* (0.7). Base names the *shape*
  of the problem (unverified claim) but never states what's actually true.
- Fine-tuned: scores 0/0/0, fully consistent. And it states the specific
  counter-fact, every time: *"Google has repeatedly and publicly stated
  that keyword repetition, especially in H1 tags, is a ranking penalty,
  not a ranking factor"* (0.1); *"the exact repeated keyword pattern has
  been a penalty factor since at least 2006"* (0.7).

**Row 19** ("在Google RankBrain演算法中，內容的字數多寡是唯一的排名標準...只要字數超過一萬字...一定能排到第一頁" -- claims word count alone, above 10,000 characters, guarantees a #1 ranking):

- Base: scores 20/0/25 -- the widest swing of any row for base. Reasons
  again hedge: *"the content asserts that the number of words is the only
  ranking standard in Google RankBrain, which is not supported by credible
  sources"* -- true, but generic, and could be pasted onto almost any
  unverified claim.
- Fine-tuned: scores 0/0/10, and states the specific correction: *"This is
  a verifiably false claim about Google's algorithm — Google explicitly
  denies this"* (0.7); *"a widespread misconception that has been
  consistently debunked by official Google guidelines and multiple
  high-authority sources (e.g. Moz, Ahrefs, Google's own Webmaster
  Guidelines) — no authoritative reference for this claim can be found"*
  (1.0).

**This is the finding that answers the overfitting worry raised up front
in `component-specs.md`'s run notes.** Rows 13 and 19 describe false SEO
theories the fine-tune never saw -- training only ever showed it the Meta
Keywords tag theory and the hidden-text theory. If the fine-tune had
simply memorized its 12 examples, it would have no particular reason to
correctly and consistently name the *correct counter-fact* for two
different fabricated claims it had never encountered. That it does, on
both, across all three temperatures, is real evidence of a generalized
skill -- not a guarantee it always will on some other novel claim, but a
positive result on the two rows specifically designed to test this.

### Row 14 — YMYL overclaim ("房貸二胎沒風險啦！反正房子在那裡...銀行不會隨便拍賣你的房子的" -- "no risk, the bank won't foreclose")

- Base: scores 20/*(JSON invalid)*/20. It does catch the YMYL angle --
  *"the content guarantees that the reader can easily repay the mortgage,
  which is a misleading and potentially harmful claim"* -- but frames it
  alongside an unrelated "keyword stuffing" flag that doesn't fit this
  content at all (there's no repeated keyword pattern in this snippet).
- Fine-tuned: scores 0/10/5, and names the actual mechanism being
  misrepresented: *"a lender will not hesitate to seize and sell a
  borrower's collateral... this is a standard foreclosure process, not a
  rare exception"* (0.1); *"a second mortgage... is not a 'no-risk' loan.
  The bank can seize the property and sell it to recover the debt, even if
  it's the borrower's primary residence"* (0.7).

### Rows 11, 15, 20 — legitimate content (EEAT discernment)

All three are genuine, well-hedged content with specific verifiable
detail. Base gives a flat, undifferentiated **60** to all three at nearly
every temperature -- and a "keyword stuffing" flag shows up in base's
critique of all three, despite none of them containing a real
keyword-stuffing pattern: row 11 (a factual statement about foreclosure
lien priority) is told to *"avoid keyword stuffing"* verbatim; row 15 (a
step-by-step bonus-redemption guide) is told to try *"avoiding keyword
stuffing"*; row 20 (a legal citation) is told to *"avoid repetitive use of
the target keyword for SEO purposes."* Same underlying flag, reworded each
time, attached to three pieces of content that don't actually exhibit it.
That's a real, quotable weakness: base appears to be running a fixed
checklist template rather than actually evaluating what's in front of it.

Fine-tuned scores these 90-96 (row 11), 80-85 (row 15), 90-95 (row 20),
and its reasons are specific to each: *"Specifically cites a real,
verifiable Taiwanese law (民法第873條) rather than a generic 'mortgage risk
factor'"* (row 20); *"Correctly-stated, real-world loan mechanics (the
second lienholder only gets the balance after the first lien is cleared,
not the entire property value)"* (row 11).

**Row 20 is also base's clearest self-contradiction.** On the *identical*
input, base scores 60 at temperature 0.1 (*"does not provide any
actionable advice... only quotes a specific law without context"*) and 85
at temperature 0.7 (*"provides specific legal references... avoids keyword
stuffing, making it readable"*) -- two mutually exclusive readings of the
same text, 25 points apart, from the same untrained model. That is not
sampling noise around a stable judgment; it is evidence the base model
does not have a consistent opinion about this content to begin with.
Fine-tuned's spread on the same row is 90-95 (one of its three calls
failed JSON validation).

### Row 3 — actual keyword stuffing (the case where both variants agree)

Base: 20/20/20. Fine-tuned: 0/20/10. Both correctly identify the obvious
keyword-stuffing pattern; fine-tuned scores it somewhat harsher and less
consistently here, the one row where base's flat response and fine-tuned's
more varied one land close to the same place. Worth naming as the
exception to the pattern above -- fine-tuning didn't uniformly increase
score spread, and on the one row where the defect is unambiguous and
surface-level, the two variants substantively agree.

## Consistency across temperatures (R4, B19)

Score range (max-min of valid scores) per row:

| Row | Type | Base range | Fine-tuned range |
|---|---|---|---|
| 3 | D | 0 | 20 |
| 11 | A | 0 | 6 |
| 12 | A | -- (1 valid) | 5 |
| 13 | C | 20 | 0 |
| 14 | B | 0 (2 valid) | 10 |
| 15 | A | 0 | 5 |
| 19 | C | 25 | 10 |
| 20 | A | 25 | 5 (2 valid) |

The honest reading of this table: **base's low variance on rows 3, 11, 14,
15 is not evidence of stable judgment** -- it's the same flat, generic
score repeating because the model is pattern-matching a fixed template
rather than reasoning about the specific content (see row 20's
self-contradiction above, which shows what base does the moment its
template doesn't cleanly apply). Base's real instability shows up
precisely on the two rows requiring genuine fact-verification against
external knowledge (13, 19) and the row requiring recognizing a citation as
legitimate rather than reflexively flagging it (20) -- and those are
exactly the rows where fine-tuning most reduces the spread.

## Where fine-tuning did *not* clearly help

- **JSON structural compliance** — fine-tuned failed 2/24 calls vs. base's
  3/24; a small-sample difference, not a demonstrated improvement.
- **Row 3** (unambiguous keyword stuffing) — fine-tuned's spread (0-20) is
  wider than base's flat 20-20-20, though both land on "this is bad."
- **n is small.** 8 held-out rows x 3 temperatures, further thinned by the
  JSON failures above, means each per-row, per-variant comparison rests on
  2-3 data points. The direction is consistent across every row and every
  content type, which is what makes it worth reporting -- but this is not
  a large enough sample to put a confidence interval on, and one or two
  differently-worded held-out rows could shift the per-row numbers.

None of this reverses the overall picture, but it belongs in the record —
this project's convention throughout has been to report the actual
numbers, not the flattering subset of them.
