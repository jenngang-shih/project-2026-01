"""Loads topic 2's Role/Goal/Instructions prompt files and renders them with
the runtime substitutions each dynamic component needs (SERP context for
gap detection; the SERP analysis bundle + retrieved passages for proposal
generation). Source templates: ../prompts/*.md.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _load(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def gap_detection_prompt(keyword: str, serp_context: list[dict[str, Any]]) -> str:
    """Renders prompts/serp-content-gap-detection.md. `serp_context` is the
    deterministically-extracted {rank, title, h2, snippet} per result — not
    raw HTML, per that template's Reference section."""
    template = _load("serp-content-gap-detection.md")
    return (
        f"{template}\n\n---\nKeyword: {keyword}\n\n"
        "Extracted heading structure and snippets for the top-ranking results:\n"
        f"{json.dumps(serp_context, ensure_ascii=False, indent=2)}\n\n"
        'Respond with ONLY a JSON object: {"gaps": [{"pain_point": ..., '
        '"evidence": ..., "checked_against": [...]}, ...]}.'
    )


def proposal_prompt(
    keyword: str,
    serp_analysis: dict[str, Any],
    retrieved_passages: list[dict[str, Any]],
) -> str:
    """Renders prompts/proposal-generation.md. `retrieved_passages` may be
    an empty list — that's a legitimate input meaning C4 found nothing
    relevant, which the template's Constraints require surfacing as
    `manual_silent: true`, not silently omitting."""
    template = _load("proposal-generation.md")
    return (
        f"{template}\n\n---\nKeyword: {keyword}\n\n"
        "SERP analysis bundle (headings, keyword distribution, content gaps):\n"
        f"{json.dumps(serp_analysis, ensure_ascii=False, indent=2)}\n\n"
        "Retrieved manual passages (empty list means the manual had nothing relevant):\n"
        f"{json.dumps(retrieved_passages, ensure_ascii=False, indent=2)}\n\n"
        'Respond with ONLY a JSON object of this EXACT shape — every list item '
        'a plain string, never an object, and keyword_guidance a single plain '
        'string, never an object with its own sub-fields: '
        '{"recommended_headings": ["heading text with any citation folded in", '
        '"..."], "keyword_guidance": "one string covering all keyword-usage '
        'points", "compliance_notes": ["note text with its manual citation '
        'folded in", "..."], "manual_silent": bool}.'
    )
