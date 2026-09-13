"""C2 — SERP Analyzer Skill. Source: B5 (+B6, B7, B8, B21).

Hybrid component: extract_headings() and keyword_distribution() are pure
deterministic field reads over data/SERP_Data.json's structure;
detect_content_gaps() deterministically assembles its input then makes one
dynamic call (see docs/component-specs.md's run notes for why gap detection
specifically needs semantic judgment, not fixed-rule matching).
"""
from __future__ import annotations

from .json_utils import parse_json_response
from .llm_client import LLMClient
from .prompts import gap_detection_prompt
from .schemas import (
    ContentGap,
    ContentGapsOutput,
    HeadingExtraction,
    KeywordCount,
    SerpAnalysisBundle,
    SerpResult,
)


def extract_headings(serp_data: list[SerpResult]) -> list[HeadingExtraction]:
    """Deterministic. Source: B6. A malformed individual result (missing
    h2/title) would fail at SerpResult validation before reaching here —
    see orchestrator.load_serp_data — so this function itself can assume
    well-formed input per result."""
    return [HeadingExtraction(rank=r.rank, title=r.title, h2=r.h2) for r in serp_data]


def keyword_distribution(serp_data: list[SerpResult], keyword: str) -> list[KeywordCount]:
    """Deterministic. Source: B7. Case-insensitive substring count of
    `keyword` across each result's title + h2 + snippet combined — a
    simple, auditable heuristic; not stemming/tokenization-aware, which is
    an acceptable simplification for a prototype but worth knowing if
    keyword variants (e.g. plurals, particles) need to count too."""
    out = []
    kw = keyword.lower()
    for r in serp_data:
        haystack = " ".join([r.title, " ".join(r.h2), r.snippet]).lower()
        out.append(KeywordCount(rank=r.rank, count=haystack.count(kw)))
    return out


def detect_content_gaps(serp_data: list[SerpResult], keyword: str, llm: LLMClient) -> list[ContentGap]:
    """Hybrid. Source: B8. Deterministically assembles the dynamic call's
    input (heading structure + snippets, not raw HTML — see
    prompts/serp-content-gap-detection.md's Reference section), then
    validates the returned shape before returning it."""
    context = [
        {"rank": r.rank, "title": r.title, "h2": r.h2, "snippet": r.snippet}
        for r in serp_data
    ]
    raw = llm.complete(gap_detection_prompt(keyword, context), component="gap_detection")
    validated = ContentGapsOutput.model_validate(parse_json_response(raw))
    return validated.gaps


def analyze_serp(serp_data: list[SerpResult], keyword: str, llm: LLMClient) -> SerpAnalysisBundle:
    """C2's full entry point, called by C1. Source: B5."""
    return SerpAnalysisBundle(
        headings=extract_headings(serp_data),
        keyword_distribution=keyword_distribution(serp_data, keyword),
        gaps=detect_content_gaps(serp_data, keyword, llm),
    )
