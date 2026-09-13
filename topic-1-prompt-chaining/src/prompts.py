"""Loads the Role/Goal/Instructions prompt files for topic 1 and renders them
with the runtime substitutions each stage needs (selected intent, prior
paragraph, audit reasons). Source templates: ../prompts/*.md.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load(name: str, *, keyword: str | None = None) -> str:
    """Loads a prompt template and, if given, substitutes every literal
    {keyword} placeholder with the actual keyword for this run. Plain
    string replacement (not str.format) deliberately — several templates
    contain unrelated literal `{...}` (e.g. the Output shape's
    `{intent, evidence, competitive_rationale}`), which str.format would try
    to interpret as format fields and fail on."""
    text = (PROMPTS_DIR / name).read_text(encoding="utf-8")
    if keyword is not None:
        text = text.replace("{keyword}", keyword)
    return text


def stage_a_prompt(keyword: str) -> str:
    template = _load("stage-a-micro-intent-modeling.md", keyword=keyword)
    return (
        f"{template}\n\n---\nKeyword for this run: {keyword}\n\n"
        'Respond with ONLY a JSON object: {"intents": [{"intent": ..., '
        '"evidence": ..., "competitive_rationale": ...}, ...]} with at '
        "least 4 entries."
    )


def stage_b_prompt(selected_intent: dict[str, Any], keyword: str) -> str:
    template = _load("stage-b-first-hand-experience.md", keyword=keyword)
    return (
        f"{template}\n\n---\nSelected micro-intent for this run:\n"
        f"{json.dumps(selected_intent, ensure_ascii=False, indent=2)}\n\n"
        "Respond with ONLY the paragraph text, no JSON wrapper."
    )


def stage_c_audit_prompt(paragraph: str, keyword: str) -> str:
    template = _load("stage-c-audit.md", keyword=keyword)
    return (
        f"{template}\n\n---\nParagraph to audit:\n{paragraph}\n\n"
        'Respond with ONLY a JSON object: {"pass": bool, "reasons": [...], '
        '"authoritativeness_suggestions": [...]}.'
    )


def stage_c_correction_prompt(paragraph: str, reasons: list[str]) -> str:
    template = _load("stage-c-correction.md")
    reasons_block = "\n".join(f"- {r}" for r in reasons)
    return (
        f"{template}\n\n---\nParagraph to revise:\n{paragraph}\n\n"
        f"Audit reasons to resolve:\n{reasons_block}\n\n"
        "Respond with ONLY the revised paragraph text, no JSON wrapper."
    )
