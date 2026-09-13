<!--
Traceability: topic-2-rag-serp-analyzer/docs/problem-statement-categorized.md, B20
  ("A ~3-minute demo video showing usage, how the Skill processes SERP
  data, and how RAG ensures output compliance.")
Type: human/documentation deliverable — a script to record from, not the
  recording itself (B20 needs an actual video, which is your action).
-->

# Topic 2 — 3-Minute Demo Script

Built around the actual verified live run (`docs/live-run.md`, keyword
房屋二胎利率) — every number and quote below is real output, not invented for
the demo. Before recording: run the Space once, let it fully finish
generating (don't switch tabs mid-generation), so you're narrating over
completed, real results the whole time.

**Total: ~3:00.** Timestamps are a pace guide, not a hard cue — talk
naturally, don't rush to hit them exactly.

---

## [0:00–0:15] Intro — before clicking Generate

**Screen:** the Space, keyword field showing `房屋二胎利率`

**Say:**
> "This is a RAG-powered SEO SERP Analyzer. You give it one keyword, and
> it does two things at once: analyzes what's actually ranking right now,
> and cross-checks that against an internal compliance manual — then
> produces an article-planning proposal an editor could act on directly.
> Let's walk through what happens when I click Generate."

**Do:** click **Generate proposal**, wait for it to finish.

---

## [0:15–0:55] SERP Analysis tab — the "Skill"

**Screen:** switch to the **SERP analysis** tab

**Say:**
> "First is the 'Skill' — it analyzes the top 5 competitor results for
> 房屋二胎利率. Two different things happen here. Extracting headings and
> counting keyword usage is plain deterministic code — no AI, just parsing
> the actual titles and headers out of the search data. But finding
> *content gaps* — things none of the five competitors address at all —
> that needs real judgment, so that specific piece is a live AI call.
>
> And look what it actually found: the real total cost of a second
> mortgage beyond the advertised rate — setup fees, account fees, penalty
> fees — and what actually happens if you default: lien priority against
> the first mortgage, foreclosure risk. It checked all five results
> individually and explained *why* each one misses this, not just a
> generic label."

**Optional detail if you have time:** point out `keyword_distribution` —
only Rank 1 shows a count, which is a real, visible limitation (exact
substring match, not semantic) worth being upfront about rather than
hiding.

---

## [0:55–1:35] Retrieved Manual Passages tab — the RAG half

**Screen:** switch to **Retrieved manual passages**

**Say:**
> "Second half is RAG. There's a small internal compliance manual — three
> rules about what this kind of financial content is and isn't allowed to
> say. The system embeds that manual into a vector database, and for any
> keyword, retrieves the passages actually relevant to it — you can see
> the similarity score and exactly which line of the manual each one came
> from.
>
> This matters because it means compliance isn't the AI 'remembering'
> rules — it's grounded, retrieved evidence, every single run."

---

## [1:35–2:40] Proposal tab — where both sources actually combine

**Screen:** switch to **Proposal**

**Say:**
> "This is where it comes together. The proposal generator gets *both*
> the SERP analysis and the retrieved manual passages, and it has to
> actually use both — not lean on one and mention the other in passing.
>
> Look at this compliance note specifically:" — **[read the third
> compliance note aloud]** — "it takes the competitor pattern of '24-hour
> disbursement' and 'low rates' from the SERP data, and applies the exact
> prohibition from the manual that this content can't promise 'guaranteed
> approval' or 'lowest rate nationwide.' That's not a template response —
> that's the system resolving a real conflict between what ranks and
> what's compliant, and it cites the specific manual line every time it
> makes a compliance claim.
>
> And this is genuinely live output from Azure OpenAI, generated just now
> — not scripted or cached."

---

## [2:40–3:00] Close

**Say:**
> "So: deterministic parsing where parsing is enough, one live AI call
> only where real judgment is needed, RAG-grounded compliance instead of
> memorized rules, and a final proposal that has to draw from both sources
> at once. That's the RAG SERP Analyzer."

---

## Notes for recording

- If you want to show more technical depth, `docs/component-specs.md` has
  the architecture diagram — could be a 10-second cutaway ("here's the
  actual data flow") between the SERP and RAG sections.
- The "real, not scripted" line in the Proposal section is worth keeping —
  it's honest and it's a real differentiator worth stating plainly, not
  something to cut for time.
- If you re-run before recording and get a different (still real) result,
  that's fine — narrate what you actually see rather than reciting this
  script's exact numbers verbatim.
