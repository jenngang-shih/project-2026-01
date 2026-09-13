"""Pydantic schemas validating the JSON-shaped output of each dynamic
component in the topic-1 prompt chain.

Traceability: docs/component-specs.md; each schema's docstring cites the
categorized-requirement bullet IDs (docs/problem-statement-categorized.md)
that define its "Output shape".

Every model in this file is a pure data contract: constructing one either
succeeds and returns a validated instance, or raises `pydantic.ValidationError`
(a plain Python exception) if the input doesn't match the shape/constraints
declared below. None of them perform I/O or mutate anything outside the
instance being built — orchestrator.py relies on that: it feeds each dynamic
component's raw JSON through `Model.model_validate(...)` and treats a raised
ValidationError as "stop, don't proceed on unverified data" (ties to B21 —
Logical Consistency).
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, field_validator


class MicroIntent(BaseModel):
    """Schema for one entry in Stage A's output — a single micro-intent.

    Declares the `{intent, evidence, competitive_rationale}` shape
    `prompts.stage_a_prompt()` asks the LLM to return per entry (Output shape
    for B9). All three fields are required strings; missing or wrong-typed
    data raises `pydantic.ValidationError` on construction. No side effects —
    a plain, validated data container.
    """

    intent: str
    evidence: str
    competitive_rationale: str


class StageAOutput(BaseModel):
    """Output of C2 — Stage A: Micro-Intent Modeling. Source: B7 (+ B8, B9).

    Wraps the full list of micro-intents. `intents: List[MicroIntent]` gives
    nested validation for free — pydantic validates every element against
    `MicroIntent`'s schema too, so one malformed intent fails the whole
    `StageAOutput`, not just that entry.
    """

    intents: List[MicroIntent]

    @field_validator("intents")
    @classmethod
    def at_least_four(cls, v: List[MicroIntent]) -> List[MicroIntent]:
        """Enforces B8 (Stage A must cover >=4 distinct micro-intents) — a
        constraint plain type-checking can't express (`List[MicroIntent]`
        alone would accept a list of length 1). Runs automatically right
        after the basic type-check on `intents` passes.

        `cls` (not `self`): pydantic v2 validators are classmethods, since
        validation happens during construction, before an instance fully
        exists.

        Output/side effect: returns `v` unchanged when the length check
        passes (a validator must return the value it wants kept); otherwise
        raises `ValueError`, which pydantic re-raises as part of a
        `ValidationError` on the whole model — this is what propagates up to
        orchestrator.py's `StageAOutput.model_validate(...)` call and stops
        the run with a clear cause rather than silently accepting too few
        intents. No I/O.
        """
        if len(v) < 4:
            raise ValueError(f"B8 requires >=4 micro-intents, got {len(v)}")
        return v


class StageBOutput(BaseModel):
    """Output of C3 — Stage B: First-hand Experience. Source: B10 (+ B11-13).

    Deliberately the simplest schema here: just `paragraph: str`, no custom
    validation. Stage B's real constraints (B11 sensory detail + objective
    critique, B12 no AI disclaimers/hollow praise, B13 veteran-player
    persona) are all qualitative properties of the text's *content* — not
    something a type schema can mechanically check. That's why they're
    enforced instead by Stage C's audit (`AuditVerdict`, below) actually
    reading the text, not by this schema.
    """

    paragraph: str


class AuditVerdict(BaseModel):
    """Output of C4a — Stage C Audit. Source: B15 (check half).

    The structured verdict orchestrator.py's retry loop branches on
    (`if verdict.passed: break`).
    """

    # Accessed in Python as `.passed` (can't be `.pass` — reserved keyword),
    # but read/written over JSON as "pass" via this alias, matching the exact
    # key stage_c_audit_prompt() instructs the LLM to return.
    passed: bool = Field(alias="pass")
    # Specific EEAT/YMYL violation explanations; defaults to an empty list if
    # the LLM omits the key rather than failing validation outright. Expected
    # empty when `passed` is True.
    reasons: List[str] = Field(default_factory=list)
    # Suggested improvements to the Authoritativeness signal specifically
    # (B15's "improve its Authoritativeness signal" wording), same
    # default-empty pattern as `reasons`.
    authoritativeness_suggestions: List[str] = Field(default_factory=list)

    # Lets the model ALSO be constructed with the real field name (passed=)
    # in addition to the alias (pass=) — used by orchestrator.py's
    # `AuditVerdict(**{"pass": False})`, which needs a dict key since
    # `pass=False` as a literal keyword argument would be a SyntaxError.
    model_config = {"populate_by_name": True}


class StageCCorrection(BaseModel):
    """Output of C4b — Stage C Correction. Source: B15 (correct half) + B14.

    Structurally identical to StageBOutput: wraps the single revised
    `paragraph: str`. No custom validation, for the same reason — whether the
    revision actually resolved the audit's flagged `reasons` is a qualitative
    judgment made by the *next* audit pass (C4a again), not something this
    schema checks.
    """

    paragraph: str
