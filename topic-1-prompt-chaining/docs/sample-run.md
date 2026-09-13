<!--
Traceability: exercises the C1 orchestrator (docs/component-specs.md) end to
end using the C2/C3/C4a/C4b prompts in ../prompts/*.md.
-->

# Topic 1 — Sample Run (2026-09-12)

## Provenance (read this before citing anything below as evidence)

| Piece | Provenance |
|---|---|
| Orchestrator code (`src/orchestrator.py`, `schemas.py`, `llm_client.py`, `prompts.py`) | **Application-generated artifact** — real Python, executed for real (see commands below), not pseudocode. |
| Stage A output (`sample-run/stage_a_output.json`) | **AI-generated proposal** — written by the assistant directly acting as Stage A's LLM, following `prompts/stage-a-micro-intent-modeling.md` verbatim. **Not** a live call through `AnthropicLLMClient` — `.env`'s `ANTHROPIC_API_KEY` is still a placeholder, so no such call is currently possible. |
| Intent selection | **Human decision** — genuinely made by the project owner mid-conversation (not simulated), choosing intent `[2]` (game-UI immersion / cross-device usability) from Stage A's real output. |
| Stage B v1, Stage C audit v1/v2, Stage B v2 | **AI-generated proposal**, same basis as Stage A — the assistant acting as each component's LLM, one file per call, not fabricated after the fact to fit a narrative. Stage B v1 deliberately includes one realistic EEAT flaw (an unqualified "market-best" superlative) so the audit/correction loop has something genuine to catch, rather than trivially passing on the first attempt. |
| The retry loop, JSON-schema validation, and final `pass: true` result | **Runtime evidence** — produced by actually running `resume_prompt_chain` against the fixtures above through `FixtureLLMClient`, not asserted by hand. |

This run demonstrates the mechanism (the orchestrator's control flow, the schema contracts, the audit→correct→re-audit loop) working correctly. It does **not** demonstrate live-model behavior — that requires a real `ANTHROPIC_API_KEY` and a re-run through `AnthropicLLMClient` instead of `FixtureLLMClient`.

## What ran

```
start_prompt_chain("娛樂城")
  → C2 (Stage A) → 4 micro-intents, validated against StageAOutput
  → SEL: human picks intent [2] — 遊戲介面沉浸感與跨裝置操作體驗需求

resume_prompt_chain(session_id, intents[2])
  → C3 (Stage B) → paragraph v1 (contains one deliberate EEAT flaw)
  → C4a (Audit)  → pass: false, 2 reasons (unqualified superlative claim)
  → C4b (Correct)→ paragraph v2 (superlative rescoped to first-hand claim)
  → C4a (Audit)  → pass: true, 0 reasons
  → loop stops (pass achieved on cycle 2 of the 3-cycle cap)
```

Full audit trail is preserved in `.sessions/<session_id>.json` (gitignored —
local run state, not a committed artifact; the fixture files under
`sample-run/` are the durable, inspectable record).

## Reproducing this run

```bash
# from topic-1-prompt-chaining/, with the project .venv active
python -c "
from src.llm_client import FixtureLLMClient
from src.orchestrator import start_prompt_chain, resume_prompt_chain
llm = FixtureLLMClient({'stage_a': [open('docs/sample-run/stage_a_output.json', encoding='utf-8').read()]})
req = start_prompt_chain('娛樂城', llm)
# ... pick req.stage_a_intents[2], then supply stage_b/stage_c_audit/stage_c_correction
# fixtures from docs/sample-run/ to resume_prompt_chain, as done for this run.
"
```

## Final accepted paragraph (Stage B v2, post-correction)

See `sample-run/stage_b_output_v2.txt` for the full text. This is the version
that fed into a `pass: true` audit and is what `ChainResult.stage_b_final`
returns.

## Relationship to this topic's Deliverables

- **B16** (results of Stages A/B/C): the fixture files in `sample-run/` plus
  the printed audit trail together are that result, for this one sample run.
- **B17** (Iterative Record): this run happened as manual, inspectable
  turns (this doc), which is a substitute for — not equivalent to — the
  sourced requirement's shared ChatGPT/Claude/Gemini conversation link. A real
  submission still needs that link from an actual chat session.
- **B18/B19** (Architecture Diagram / Rationale): the diagram in
  `component-specs.md` covers the mechanism; B19's rationale write-up is still
  outstanding (documentation, not code — see that file's run notes).

## Known gap

None of this has gone through a live model yet. The next real step is
setting `ANTHROPIC_API_KEY` in `.env` and re-running via `cli.py` (below) with
`AnthropicLLMClient`, to see whether the prompts hold up against an actual
model rather than the assistant's own hand-authored stand-in responses.
