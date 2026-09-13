"""The actual LangGraph wiring (G4, G5 in docs/component-specs.md) plus the
two dynamic nodes (G2, G3). Real langgraph.graph.StateGraph, not a
hand-rolled equivalent — so B12's graph visualization comes from the
compiled graph's own introspection (see render.py), not a hand-drawn
diagram that could silently drift from what this file actually wires.
"""
from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from .json_utils import extract_json
from .llm_client import LLMClient
from .prompts import auditor_prompt, planner_prompt
from .retry import call_with_retry
from .schemas import AuditVerdict, HistoryEntry, NegotiationState, PlannerOutput


def initial_state(
    *,
    keyword: str,
    category: str,
    required_ctr_terms: list[str],
    forbidden_terms: list[str],
    compliance_reference: str,
    max_iterations: int = 5,  # engineering default, see component-specs.md run notes
) -> NegotiationState:
    """`compliance_reference` (Manual.txt's text) is loaded by the caller,
    not resolved internally via a hardcoded path — same reasoning
    topic 2's `ingest_manual(path, ...)` and `load_serp_data(path)` already
    follow: this module stays portable (verbatim-portable into a Colab
    notebook cell, with no `__file__`-relative path to break) and testable
    without touching the real filesystem."""
    return NegotiationState(
        keyword=keyword,
        category=category,
        required_ctr_terms=required_ctr_terms,
        forbidden_terms=forbidden_terms,
        compliance_reference=compliance_reference,
        outline=None,
        audit_verdict=None,
        iteration=0,
        max_iterations=max_iterations,
        history=[],
        status="in_progress",
    )


async def _call_and_validate(llm: LLMClient, prompt: str, component: str, model_cls):
    """Shared logic for both dynamic nodes: call the LLM (with transient-
    error retry), parse defensively, validate against the schema. A
    validation failure (malformed JSON, or JSON that doesn't satisfy the
    schema) is retried exactly once against the same prompt — per
    docs/component-specs.md's G2/G3 spec, this is a different failure mode
    than a transient network error and gets a different, much smaller
    retry budget. If both attempts fail, raise a clear, named error rather
    than let a malformed value silently enter the graph's state."""
    last_error: Exception | None = None
    for validation_attempt in range(2):  # one real attempt + one retry
        raw = await call_with_retry(lambda: llm.complete(prompt, component=component))
        try:
            parsed = extract_json(raw)
            return model_cls.model_validate(parsed)
        except (ValidationError, ValueError) as e:
            last_error = e
            continue
    raise RuntimeError(
        f"{component} produced invalid output after retrying validation once: {last_error}\n"
        f"Last raw response: {raw!r}"
    )


def make_planner_node(llm: LLMClient):
    async def planner_node(state: NegotiationState) -> dict:
        prompt = planner_prompt(state)
        output = await _call_and_validate(llm, prompt, "planner", PlannerOutput)
        return {"outline": output.model_dump()}

    return planner_node


def make_auditor_node(llm: LLMClient):
    async def auditor_node(state: NegotiationState) -> dict:
        prompt = auditor_prompt(state)
        verdict = await _call_and_validate(llm, prompt, "auditor", AuditVerdict)
        return {"audit_verdict": verdict.model_dump()}

    return auditor_node


def decide_node(state: NegotiationState) -> dict:
    """G4's deterministic bookkeeping half: appends this round to history
    (if it's not converging) and sets the terminal status. Kept as its
    own node — separate from the routing function below — because
    updating state and choosing the next node are two different jobs;
    langgraph conditional-edge routing functions should only read state,
    not mutate it."""
    verdict = state["audit_verdict"]
    if verdict["passed"]:
        return {"status": "converged"}

    if state["iteration"] + 1 >= state["max_iterations"]:
        # The outline being returned here is still the one this exact
        # verdict just evaluated and rejected — status says so plainly,
        # no bonus audit call needed (component-specs.md's G4 spec).
        return {"status": "exhausted"}

    entry: HistoryEntry = {
        "iteration": state["iteration"],
        "outline": state["outline"],
        "audit_verdict": verdict,
    }
    return {
        "history": state["history"] + [entry],
        "iteration": state["iteration"] + 1,
        "status": "in_progress",
    }


def route_after_decide(state: NegotiationState) -> Literal["planner", "end"]:
    """The actual conditional-edge routing function — reads the status
    decide_node just set and nothing else."""
    return "end" if state["status"] in ("converged", "exhausted") else "planner"


def build_graph(llm: LLMClient):
    """Wires Start -> Planning -> Audit -> Decision Node exactly as B7
    names it, with the conditional edge B8 describes."""
    graph = StateGraph(NegotiationState)
    graph.add_node("planner", make_planner_node(llm))
    graph.add_node("auditor", make_auditor_node(llm))
    graph.add_node("decide", decide_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "auditor")
    graph.add_edge("auditor", "decide")
    graph.add_conditional_edges("decide", route_after_decide, {"planner": "planner", "end": END})

    return graph.compile()
