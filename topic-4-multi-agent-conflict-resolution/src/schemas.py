"""Data shapes for topic 4: the two agents' validated output (G2/G3's
output schemas in docs/component-specs.md) and the LangGraph state itself
(G1). Pydantic models validate each LLM call's output before it's allowed
into the graph's state; the state itself is a plain TypedDict, which is
what langgraph.graph.StateGraph expects and merges node return values into.
"""
from __future__ import annotations

from typing import List, Literal, Optional, TypedDict

from pydantic import BaseModel, field_validator, model_validator


class PlannerOutput(BaseModel):
    """Agent A's (SEO Content Planner) validated output. `outline` and
    `keywords_used` must be non-empty — an empty outline or a draft that
    claims to use no keywords at all isn't a real attempt at the brief,
    it's a malformed response that happens to parse as valid JSON."""

    outline: List[str]
    keywords_used: List[str]
    rationale: str

    @field_validator("outline", "keywords_used")
    @classmethod
    def _non_empty_list(cls, v: List[str], info) -> List[str]:
        if not v:
            raise ValueError(f"{info.field_name} must not be empty")
        return v

    @field_validator("rationale")
    @classmethod
    def _non_empty_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("rationale must not be empty")
        return v


class AuditVerdict(BaseModel):
    """Agent B's (YMYL Compliance Auditor) validated output. `issues` and
    `revision_suggestions` must be empty exactly when `passed` is true and
    non-empty exactly when it's false — a fail with no stated reason, or a
    pass with lingering issues, is a malformed response, not a valid edge
    case (docs/component-specs.md's G3 spec)."""

    passed: bool
    issues: List[str]
    revision_suggestions: List[str]

    @model_validator(mode="after")
    def _issues_match_passed(self) -> "AuditVerdict":
        if self.passed and (self.issues or self.revision_suggestions):
            raise ValueError("passed=true must not carry issues or revision_suggestions")
        if not self.passed and not (self.issues and self.revision_suggestions):
            raise ValueError("passed=false must carry non-empty issues and revision_suggestions")
        return self


class HistoryEntry(TypedDict):
    """One completed round, kept so a later Planner call can see what it
    already tried and why it was rejected — the concrete mechanism behind
    B17's "does State fully carry prior context" criterion."""

    iteration: int
    outline: dict  # PlannerOutput.model_dump()
    audit_verdict: dict  # AuditVerdict.model_dump()


class NegotiationState(TypedDict):
    """The full LangGraph state (G1). Every field a node reads or writes
    is named here explicitly — langgraph merges each node's returned dict
    into this state, so this is the one place the whole shape is visible
    at a glance."""

    keyword: str
    category: str
    required_ctr_terms: List[str]
    forbidden_terms: List[str]
    compliance_reference: str
    outline: Optional[dict]  # PlannerOutput.model_dump(), current round
    audit_verdict: Optional[dict]  # AuditVerdict.model_dump(), current round
    iteration: int
    max_iterations: int
    history: List[HistoryEntry]
    status: Literal["in_progress", "converged", "exhausted"]
