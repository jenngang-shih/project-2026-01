"""Pydantic schemas for topic 2's deterministic data shapes and the JSON
output of its two dynamic components (C2's gap-detection sub-call, C5's
Proposal Generator).

Traceability: docs/component-specs.md; each schema's docstring cites the
categorized-requirement bullet IDs (docs/problem-statement-categorized.md)
that define its shape. Same design as topic 1's schemas.py: every model here
is a pure data contract — constructing one either succeeds or raises
pydantic.ValidationError, no side effects, no I/O.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, field_validator


class SerpResult(BaseModel):
    """One competitor's SERP entry, exactly as shaped in data/SERP_Data.json.
    Source: B4 (Reference — the fixed input data for this task)."""

    rank: int
    title: str
    h2: List[str] = Field(default_factory=list)
    snippet: str = ""
    source_authority: str = ""


class HeadingExtraction(BaseModel):
    """C2's deterministic heading-structure output, one per SERP result.
    Source: B6."""

    rank: int
    title: str
    h2: List[str]


class KeywordCount(BaseModel):
    """C2's deterministic keyword-distribution output, one per SERP result.
    Source: B7. `count` and `matched_segments` are from segmented-keyword
    matching (jieba), not exact-substring matching — see
    docs/component-specs.md's run notes for why exact-substring was
    replaced: on the real fixture, only 1 of 5 competitors ever contained
    the keyword as one contiguous string, even though the other 4 clearly
    cover the same topic using natural word-order variants
    ("二胎房貸利率" vs. "房屋二胎利率")."""

    rank: int
    count: int
    matched_segments: List[str] = Field(
        default_factory=list,
        description="Which of the keyword's segmented terms were found, for auditability — "
        "not just the final count.",
    )


class ContentGap(BaseModel):
    """One entry in C2's dynamic gap-detection output. Source: B8."""

    pain_point: str
    evidence: str
    checked_against: List[int] = Field(default_factory=list)


class ContentGapsOutput(BaseModel):
    """Output of C2's dynamic gap-detection call
    (prompts/serp-content-gap-detection.md). Source: B8.

    No minimum-count validator (unlike topic 1's StageAOutput requiring
    >=4 micro-intents) — B8 has no analogous "at least N" requirement;
    zero gaps is a legitimate result, not a validation failure.
    """

    gaps: List[ContentGap] = Field(default_factory=list)


class SerpAnalysisBundle(BaseModel):
    """C2's full output: headings + keyword distribution + gaps, assembled
    by analyze_serp() in skill.py. Source: B5 (+B6, B7, B8)."""

    headings: List[HeadingExtraction]
    keyword_distribution: List[KeywordCount]
    gaps: List[ContentGap]


class RetrievedPassage(BaseModel):
    """One passage returned by C4's retriever. Source: B11."""

    text: str
    score: float
    source_line_range: str


def _coerce_string_list(v: object) -> object:
    """Defensive coercion for recommended_headings/compliance_notes,
    tied to a real failure: despite the prompt asking for plain strings,
    a live Azure run once returned each item as a single-key object instead
    (e.g. {"heading": "..."} or {"note": "..."}) — presumably because the
    prompt's own instructions ask each item to "cite" its source, and the
    model chose to represent that as a structured field rather than folding
    it into the string's own text. The prompt (proposal-generation.md) was
    tightened to say explicitly not to do this — this validator is the B21
    (Technical Rigor) safety net for whenever a model still does anyway,
    not a substitute for the prompt fix. Only unwraps the specific shape
    actually observed (a dict); a genuinely different malformed shape
    (not a str, not a dict) is left as-is for pydantic's normal
    string_type ValidationError to catch and report clearly.
    """
    if not isinstance(v, list):
        return v
    out = []
    for item in v:
        if isinstance(item, dict):
            out.append("; ".join(str(val) for val in item.values()) if item else "")
        else:
            out.append(item)
    return out


def _coerce_string(v: object) -> object:
    """Same defensive coercion as _coerce_string_list, for keyword_guidance
    specifically (a single string, not a list) — a live run once returned
    this as a multi-key object (e.g. {"primary_keyword": ..., ...}) rather
    than the one required string. Joins every value into one readable
    string rather than guessing which key was "the" answer."""
    if isinstance(v, dict):
        return "; ".join(f"{k}: {val}" for k, val in v.items())
    return v


class ProposalOutput(BaseModel):
    """Output of C5, the Proposal Generator
    (prompts/proposal-generation.md). Source: B13 (+B14, B22).

    `manual_silent` is the schema-level home for the self-check both
    prompts.py's proposal_prompt() and the prompt template itself require:
    if C4 returned no relevant passages, this must be True rather than the
    model quietly inventing compliance guidance it wasn't actually given.
    """

    recommended_headings: List[str]
    keyword_guidance: str
    compliance_notes: List[str] = Field(default_factory=list)
    manual_silent: bool = False

    @field_validator("recommended_headings", "compliance_notes", mode="before")
    @classmethod
    def _coerce_headings_and_notes(cls, v: object) -> object:
        return _coerce_string_list(v)

    @field_validator("keyword_guidance", mode="before")
    @classmethod
    def _coerce_keyword_guidance(cls, v: object) -> object:
        return _coerce_string(v)
