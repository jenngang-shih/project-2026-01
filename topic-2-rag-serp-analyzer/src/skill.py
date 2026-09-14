"""C2 — SERP Analyzer Skill. Source: B5 (+B6, B7, B8, B21).

Hybrid component: extract_headings() and keyword_distribution() are pure
deterministic field reads over data/SERP_Data.json's structure;
detect_content_gaps() deterministically assembles its input then makes one
dynamic call (see docs/component-specs.md's run notes for why gap detection
specifically needs semantic judgment, not fixed-rule matching).
"""
from __future__ import annotations

import jieba

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

# Filters out single-character segments jieba tends to isolate as their own
# tokens -- punctuation, particles ("的", "了"), connectors. Real Chinese
# content words are almost always 2+ characters, so this is a cheap,
# effective way to avoid counting a stray single-character coincidence as
# a keyword match, without a stopword list to maintain.
_MIN_SEGMENT_LEN = 2


def _segment(text: str) -> list[str]:
    return [seg for seg in jieba.cut(text) if len(seg.strip()) >= _MIN_SEGMENT_LEN]


def extract_headings(serp_data: list[SerpResult]) -> list[HeadingExtraction]:
    """Deterministic. Source: B6. A malformed individual result (missing
    h2/title) would fail at SerpResult validation before reaching here —
    see orchestrator.load_serp_data — so this function itself can assume
    well-formed input per result."""
    return [HeadingExtraction(rank=r.rank, title=r.title, h2=r.h2) for r in serp_data]


def keyword_distribution(serp_data: list[SerpResult], keyword: str) -> list[KeywordCount]:
    """Deterministic. Source: B7. Segments the *keyword* into its component
    terms (jieba — e.g. "房屋二胎利率" -> ["房屋", "二胎", "利率"]), then
    counts each segment's raw substring occurrences in each result's
    title+h2+snippet — see docs/component-specs.md's run notes for why
    exact-substring on the *whole* keyword was replaced.

    Only the keyword is segmented, deliberately — the haystack is matched
    as plain substrings, not re-segmented and compared token-for-token.
    Tried segmenting both sides first; it under-matched real compound
    words (jieba tokenizes "低利率" as one token, so a standalone "利率"
    segment would never equal it, even though "利率" is plainly a
    substring of "低利率"). Substring-matching each keyword segment against
    the raw haystack avoids that mismatch entirely while still fixing the
    original problem (no longer requiring the full multi-word keyword to
    appear as one contiguous string).

    `matched_segments` names which keyword segments were found, for
    auditability — a reader can see *why* a result scored the way it did,
    not just the final number."""
    keyword_segments = _segment(keyword) or [keyword]  # fall back to the whole
    # string if segmentation yields nothing (e.g. a keyword shorter than
    # _MIN_SEGMENT_LEN, or pure punctuation) rather than matching zero terms
    out = []
    for r in serp_data:
        haystack = " ".join([r.title, " ".join(r.h2), r.snippet])
        matched = [seg for seg in keyword_segments if seg in haystack]
        count = sum(haystack.count(seg) for seg in matched)
        out.append(KeywordCount(rank=r.rank, count=count, matched_segments=matched))
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
