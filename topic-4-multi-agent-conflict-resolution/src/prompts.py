"""Loads the Role/Goal/Instructions prompt files for topic 4 and renders
them with the runtime state each node needs. Source templates:
../prompts/planner.md, ../prompts/auditor.md.

Same convention as topic 1's prompts.py: the template's own prose
placeholders like {keyword} are plain string-replaced (safe — they're
single words, no risk of colliding with the Output shape section's
literal JSON braces), while structured values (history, required terms,
the current outline) are appended as a labeled runtime-data block after
the template rather than substituted inline — str.format() would choke on
the template's own literal `{"outline": [...], ...}` example.
"""
from __future__ import annotations

import json
from pathlib import Path

from .schemas import NegotiationState

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def planner_prompt(state: NegotiationState) -> str:
    template = _load("planner.md")
    template = template.replace("{keyword}", state["keyword"]).replace("{category}", state["category"])

    lines = [
        template,
        "\n---",
        f"Keyword: {state['keyword']}   Category: {state['category']}",
        "Required high-CTR terms for this run:",
        _json(state["required_ctr_terms"]),
    ]
    if state["iteration"] == 0:
        lines.append("\nThis is round 0 — no prior feedback yet, no history to avoid repeating.")
    else:
        last = state["history"][-1]
        lines.append(f"\nThis is round {state['iteration']} — a revision.")
        lines.append("Prior round's revision suggestions to address:")
        lines.append(_json(last["audit_verdict"]["revision_suggestions"]))
        lines.append("\nFull history so far (do not repeat a rejected approach):")
        lines.append(_json(state["history"]))
    lines.append(
        "\nRespond with ONLY a JSON object: "
        '{"outline": [string, ...], "keywords_used": [string, ...], "rationale": string}.'
    )
    return "\n".join(lines)


def auditor_prompt(state: NegotiationState) -> str:
    template = _load("auditor.md")

    lines = [
        template,
        "\n---",
        f"Category: {state['category']}",
        "Outline to audit:",
        _json(state["outline"]),
        "\nForbidden terms for this run (hard fail, zero tolerance):",
        _json(state["forbidden_terms"]),
        "\nCompliance manual (may not apply to this category — say so if not):",
        state["compliance_reference"],
        "\nRespond with ONLY a JSON object: "
        '{"passed": bool, "issues": [string, ...], "revision_suggestions": [string, ...]}.',
    ]
    return "\n".join(lines)
