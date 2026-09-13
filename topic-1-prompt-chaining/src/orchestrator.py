"""Deterministic control flow for the topic-1 prompt chain.

Source: docs/component-specs.md (C1 — Chain Orchestrator), split into two
resumable steps around the SEL human-decision checkpoint. Sessions are
persisted to disk (not just an in-memory dict) so a real process boundary
between "start" and "resume" — e.g. two separate CLI invocations, or two
separate HTTP requests in a future web wrapper — actually works.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .llm_client import LLMClient
from .prompts import (
    stage_a_prompt,
    stage_b_prompt,
    stage_c_audit_prompt,
    stage_c_correction_prompt,
)
from .schemas import AuditVerdict, StageAOutput, StageBOutput, StageCCorrection

SESSIONS_DIR = Path(__file__).resolve().parent.parent / ".sessions"


@dataclass
class IntentSelectionRequest:
    session_id: str
    stage_a_intents: list[dict[str, Any]]


@dataclass
class ChainResult:
    stage_a_intents: list[dict[str, Any]]
    selected_intent: dict[str, Any]
    stage_b_final: str
    audit_trail: list[dict[str, Any]] = field(default_factory=list)
    final_pass: bool = False


def _parse_json_response(raw: str) -> Any:
    """Deterministic parsing gate: each dynamic component is instructed to
    return JSON; this is where that contract is enforced rather than
    trusted blindly (ties to B21 — logical consistency)."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Component did not return valid JSON: {exc}\nRaw: {raw!r}") from exc


def _session_path(session_id: str) -> Path:
    return SESSIONS_DIR / f"{session_id}.json"


def _save_session(session_id: str, data: dict[str, Any]) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    _session_path(session_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _load_session(session_id: str) -> dict[str, Any]:
    path = _session_path(session_id)
    if not path.exists():
        raise ValueError(f"Unknown session_id: {session_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def start_prompt_chain(keyword: str, llm: LLMClient) -> IntentSelectionRequest:
    """Step 1 of C1 — runs Stage A (C2), pauses at the SEL human checkpoint."""
    raw = llm.complete(stage_a_prompt(keyword), component="stage_a")
    validated = StageAOutput.model_validate(_parse_json_response(raw))

    session_id = str(uuid.uuid4())
    intents = [i.model_dump() for i in validated.intents]
    _save_session(session_id, {"keyword": keyword, "stage_a_intents": intents})
    return IntentSelectionRequest(session_id=session_id, stage_a_intents=intents)


def resume_prompt_chain(
    session_id: str,
    selected_intent: dict[str, Any],
    llm: LLMClient,
    retry_cap: int = 3,
) -> ChainResult:
    """Step 2 of C1 — resumes after the human's SEL choice, runs Stage B then
    the Stage C audit/correct loop (capped at retry_cap cycles; the cap is an
    engineering default, not a sourced requirement — see component-specs.md).

    Guarantees the returned stage_b_final was itself checked by an audit call
    — never just-generated-and-handed-back unverified. Without the `else`
    clause below, a run that fails every cycle within the cap would return a
    final correction that was generated in response to the *last* audit but
    never itself re-audited (a real gap found via a live Azure run — see
    docs/live-run.md's "Finding" section for the concrete example)."""
    session = _load_session(session_id)
    if selected_intent not in session["stage_a_intents"]:
        raise ValueError("selected_intent is not one of this session's stage_a_intents")
    keyword = session["keyword"]

    raw_b = llm.complete(stage_b_prompt(selected_intent, keyword), component="stage_b")
    current_paragraph = StageBOutput(paragraph=raw_b.strip()).paragraph

    audit_trail: list[dict[str, Any]] = [{"type": "draft", "paragraph": current_paragraph}]
    verdict = AuditVerdict(**{"pass": False})
    for _ in range(retry_cap):
        raw_verdict = llm.complete(
            stage_c_audit_prompt(current_paragraph, keyword), component="stage_c_audit"
        )
        verdict = AuditVerdict.model_validate(_parse_json_response(raw_verdict))
        audit_trail.append({"type": "audit", **verdict.model_dump(by_alias=True)})
        if verdict.passed:
            break
        raw_correction = llm.complete(
            stage_c_correction_prompt(current_paragraph, verdict.reasons),
            component="stage_c_correction",
        )
        current_paragraph = StageCCorrection(paragraph=raw_correction.strip()).paragraph
        audit_trail.append({"type": "correction", "paragraph": current_paragraph})
    else:
        # for/else: this branch runs only if the loop finished all retry_cap
        # iterations without ever hitting `break` — i.e. the cap was
        # exhausted and the last thing that happened was a correction that
        # was never checked. Audit it now (one call beyond the cap, only in
        # this cap-exhausted case) so stage_b_final below is always a
        # version some audit actually looked at, pass or fail.
        raw_verdict = llm.complete(
            stage_c_audit_prompt(current_paragraph, keyword), component="stage_c_audit"
        )
        verdict = AuditVerdict.model_validate(_parse_json_response(raw_verdict))
        audit_trail.append({"type": "audit", **verdict.model_dump(by_alias=True)})

    result = ChainResult(
        stage_a_intents=session["stage_a_intents"],
        selected_intent=selected_intent,
        stage_b_final=current_paragraph,
        audit_trail=audit_trail,
        final_pass=verdict.passed,
    )
    _save_session(session_id, {**session, "result": asdict(result)})
    return result
