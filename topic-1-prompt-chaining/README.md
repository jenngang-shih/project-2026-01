# Topic 1 — Prompt Chaining

Micro-Intent Modeling → First-hand Experience Simulation → EEAT/YMYL
Self-Correction, chained across 3 stages for the keyword [娛樂城] (now
generalized to any keyword — see `docs/component-specs.md`'s run notes).

## Status: all sourced deliverables closed

| ID | Deliverable | Where |
|---|---|---|
| B4 | Research summary (Search Intent vs. Micro-Intent; EEAT/YMYL) | [`docs/research-summary.md`](docs/research-summary.md) |
| B16 | Results of Stages A/B/C | Three independent runs — see below |
| B17 | Iterative Record | [`docs/iterative-record.md`](docs/iterative-record.md) |
| B18 | Architecture Diagram | [`docs/component-specs.md`](docs/component-specs.md) (Mermaid flowchart) |
| B19 | Rationale (how the design ensures EEAT compliance) | [`docs/rationale.md`](docs/rationale.md) |

Also see [`docs/lineage.md`](docs/lineage.md) for a node-by-node walkthrough
(problem statement → intents → draft → audit/correct cycles → final state)
suited to explaining this to someone who already knows the domain.

For a non-technical audience, three companion pieces:
- **["Show Your Work"](https://claude.ai/code/artifact/08386b94-cd73-426e-b40a-7ae38252f68a)**
  (Claude Artifact, private by default — share from the page itself) — a
  click-through slide deck, plain conversational language, no domain or
  technical background assumed. Built for presenting to a wide audience.
- **[`Show Your Work.pptx`](Show%20Your%20Work.pptx)** — the same 15 slides
  as a downloadable file, opens directly in Google Slides (File → Import
  slides) or PowerPoint/Keynote, for anyone who wants to edit or present it
  outside a browser.
- **["Prove It First"](https://claude.ai/code/artifact/162a940f-283f-4f61-a47e-de0d357cedc2)**
  (Claude Artifact) — a companion single-page written explainer covering the
  same ground in more depth, for a reader who wants a leave-behind rather
  than a live presentation.

## The three evidentiary runs behind B16

| Run | Backend | Result | Doc |
|---|---|---|---|
| Fixture-based | Assistant-authored stand-in, replayed deterministically | Pass, cycle 2 | [`docs/sample-run.md`](docs/sample-run.md) + [`docs/sample-run/`](docs/sample-run/) |
| In-session live-generated | Assistant generating Stage A/B/C live, turn-by-turn | Pass, cycle 2 | [`docs/iterative-record.md`](docs/iterative-record.md) |
| Real Azure OpenAI | `gpt-5.6-luna`, independent model | **`final_pass: false`** (all 3 cycles) — see `docs/rationale.md` for why this is informative, not a failure | [`docs/live-run.md`](docs/live-run.md) + [`docs/live-run/`](docs/live-run/) |

## Code

| File | Role |
|---|---|
| `src/schemas.py` | Pydantic contracts validating each stage's JSON output (deterministic gate) |
| `src/prompts.py` | Loads `prompts/*.md` templates, substitutes `{keyword}` and run-specific context |
| `src/orchestrator.py` | C1 — the deterministic control flow: Stage A → human checkpoint → Stage B → Stage C audit/correct loop |
| `src/llm_client.py` | Pluggable backends: `AnthropicLLMClient`, `AzureOpenAILLMClient`, `FixtureLLMClient` |
| `src/cli.py` | `python -m src.cli --keyword <kw> --backend anthropic\|azure` |
| `prompts/*.md` | The four Role/Goal/Instructions templates for C2/C3/C4a/C4b |
| `topic1_end_to_end_colab.ipynb` | Self-contained Colab port — same logic, Azure OpenAI backend via Colab Secrets |

## Docs (reference / design history)

| File | Role |
|---|---|
| `docs/problem-statement.md`, `docs/problem-statement-categorized.md` | Original source requirement and its B1-B22 categorization |
| `docs/component-specs.md` | Architecture, component classification, flagged engineering decisions (keyword genericization, retry-cap default, etc.) |

## Local run state (not a deliverable)

`.sessions/*.json` is gitignored local run state — raw session dumps the
orchestrator writes to when actually run. `b2af778b-...json` and
`4e96579f-...json` are kept because `iterative-record.md`/`sample-run.md` and
`live-run.md` respectively reference them as provenance; the curated,
committed evidence is the `docs/*-run/` files extracted from them, not the
raw session dumps themselves.

## Setup

```bash
# from the project root
pip install -r requirements.txt
cp .env.example .env  # fill in ANTHROPIC_API_KEY or the AZURE_OPENAI_* vars
cd topic-1-prompt-chaining
python -m src.cli --keyword 娛樂城 --backend azure
```
