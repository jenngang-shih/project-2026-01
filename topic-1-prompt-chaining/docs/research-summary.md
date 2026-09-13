<!--
Traceability:
  Source: topic-1-prompt-chaining/docs/problem-statement-categorized.md, B4
    ("Before building the chain, research and summarize: Search Intent vs.
    Micro Search Intent; EEAT and YMYL.")
  Type: human/documentation deliverable — same category as B19 (Rationale):
    supports the design decisions in component-specs.md and the prompts in
    prompts/*.md, but is not itself runtime code.
  Status: written after the chain (C1-C4b) was already built, not strictly
    before it as B4's phrasing implies — the concepts below were already
    applied in the prompt/schema design; this document makes that research
    explicit and citable rather than left implicit in prompt wording.
-->

# Topic 1 — Research Summary: Search Intent vs. Micro Search Intent, EEAT, YMYL

## 1. Search Intent vs. Micro Search Intent

**Search intent** is the underlying goal a searcher has when issuing a query —
not the literal string they typed, but what they're actually trying to
accomplish. The standard industry taxonomy (rooted in Andrei Broder's 2002
"A Taxonomy of Web Search" and widely adopted in SEO practice since) splits
intent into four broad categories:

| Category | What the searcher wants |
|---|---|
| Informational | To learn something ("what is EEAT") |
| Navigational | To reach a specific known site/page ("facebook login") |
| Transactional | To complete an action, usually a purchase or signup ("buy nike air max") |
| Commercial investigation | To compare options before a later transaction ("best running shoes 2026") |

This four-way split is useful but coarse — it tells you the *category* of
intent behind a query, not the specific *need-state* driving it. That gap
matters most for short, ambiguous, high-competition head terms: a bare
keyword like [娛樂城] doesn't map cleanly onto any single Broder category.
It's already past the informational stage (the searcher knows what an online
casino platform is), but it isn't a single transactional intent either —
different searchers issuing the identical query are actually trying to
resolve different, more specific worries.

**Micro Search Intent** is the practice of decomposing one broad/ambiguous
intent category into several distinct, narrower need-states that all sit
under the same head keyword. Where Broder's taxonomy answers "what *kind* of
thing does this searcher want," micro-intent analysis answers "which
*specific* thing, among several plausible ones, does *this* searcher want" —
informed by signals the bare keyword doesn't state outright: what stage of
the decision journey a query like this typically comes from, what a realistic
referral path into the category looks like (e.g. word-of-mouth vs. organic
comparison shopping), and what background risks or anxieties are structural
to the category itself rather than incidental to any one query.

This is the direct basis for Stage A (C2) in this topic's chain: rather than
treating [娛樂城] as one transactional/commercial intent, Stage A is required
to surface ≥4 distinct micro-intents (B8) — e.g. withdrawal-reliability
anxiety, platform-legitimacy verification, UI/UX quality (repeat-usage
concern), legal-exposure anxiety — each with its own evidence for why that
need-state exists and its own competitive rationale for why most ranking
content fails to address it (B9). The four-category taxonomy alone would
have produced one label ("transactional/commercial"); it's the micro-intent
layer that produces content-planning-usable output.

## 2. EEAT

EEAT (Experience, Expertise, Authoritativeness, Trustworthiness) is the
framework Google's own **Search Quality Rater Guidelines** — the public
document used to train human quality raters whose judgments help evaluate
(not directly rank) search results — uses to describe what separates
high-quality, trustworthy content from low-quality content. It was E-A-T
(three pillars) for years; Google added the additional "Experience" pillar
in a December 2022 guidelines update, making the current framework:

- **Experience** — has the content's creator actually used/done the thing
  they're describing? This is distinct from expertise: a first-hand player
  account of a platform's mobile UI carries experience signal even if the
  writer has no formal credentials.
- **Expertise** — does the creator have the knowledge or skill the topic
  requires?
- **Authoritativeness** — is the creator/site a known, credible source for
  this specific topic — reputation among other sources and users, not just
  self-declared authority.
- **Trustworthiness** — is the content accurate, honest, safe, and reliable?
  Google's guidelines treat this as the most important of the four, and
  treat the other three as largely existing in service of it.

EEAT is not a literal ranking algorithm input; it's a quality framework whose
signals surface indirectly through things Google's actual systems can
measure. For this topic, it matters directly at two points: Stage B (C3) is
built specifically to produce genuine *Experience* signal (first-hand sensory
detail, a two-sided assessment, not marketing copy — B11-B13), and Stage C
(C4a/C4b) audits primarily for *Authoritativeness* and *Trustworthiness*
failures — most concretely, unverifiable superlative claims ("this is the
best platform on the market") that assert authority the content hasn't
earned, as opposed to a properly-scoped first-hand claim.

## 3. YMYL

YMYL ("Your Money or Your Life") is also a Search Quality Rater Guidelines
concept: a label for topics or pages that, if the content is inaccurate or
untrustworthy, could plausibly cause real harm to a person's health,
financial stability, safety, or wellbeing. Google's guidelines hold YMYL
content to a materially higher EEAT bar than low-stakes topics, on the
reasoning that the cost of misleading content is much higher when real money,
health, or safety is on the line. Canonical YMYL examples in the guidelines
include medical/health advice, financial/investment advice, legal advice,
and pages that facilitate significant financial transactions.

[娛樂城] content is YMYL-adjacent for a direct reason: it's content about
platforms that move a reader's real money, with no consumer-protection
recourse if a platform is fraudulent or a claim is wrong (a point one of
Stage A's own micro-intents — legal-exposure anxiety — surfaces directly).
That's why Stage C's audit (B15) is scoped specifically to EEAT/YMYL
compliance rather than generic writing quality: an unqualified "best in the
market" claim isn't just weak marketing copy in this category, it's a
trust/authority claim that could plausibly influence where a reader sends
money, which is exactly the kind of claim YMYL scrutiny exists to catch.

## 4. How this maps onto the chain's design

| Research concept | Where it's applied |
|---|---|
| Micro Search Intent (vs. broad intent categories) | Stage A (C2) — `stage-a-micro-intent-modeling.md`, `StageAOutput` schema's ≥4-entry requirement (B8) |
| EEAT — Experience pillar | Stage B (C3) — `stage-b-first-hand-experience.md`'s sensory-detail/objective-critique requirement (B11) |
| EEAT — Authoritativeness/Trustworthiness pillars | Stage C audit (C4a) — `stage-c-audit.md`'s `authoritativeness_suggestions` field |
| YMYL — higher bar for money-adjacent claims | Stage C audit (C4a) — the specific check that caught the "market-best" superlative in `docs/sample-run.md` |

This closes requirement **B4**. See `component-specs.md` for how these
concepts turn into the concrete component specs, and `sample-run.md` for a
worked example of Stage C's EEAT/YMYL audit catching a real violation of the
Authoritativeness/YMYL principles described above.
