"""G6 — Output Renderer: turns a finished graph run into the three
deliverables B12/B13/B16 actually ask for. Pure formatting over an
already-final NegotiationState; no new judgment happens here.
"""
from __future__ import annotations

from .schemas import NegotiationState


def render_graph_diagram(compiled_graph) -> str:
    """B12 — captured directly from the compiled LangGraph object's own
    introspection, not hand-drawn, so it can't drift from what the code
    actually wires."""
    return compiled_graph.get_graph().draw_mermaid()


def render_state_log(state: NegotiationState) -> str:
    """B13 — a full per-round transcript: every prior round from
    `history`, plus the final round (whichever ended the run)."""
    lines: list[str] = ["# State Log — full negotiation transcript", ""]

    rounds = list(state["history"])
    final_round_num = state["history"][-1]["iteration"] + 1 if state["history"] else 0
    rounds.append({
        "iteration": final_round_num,
        "outline": state["outline"],
        "audit_verdict": state["audit_verdict"],
    })

    for r in rounds:
        outline = r["outline"]
        verdict = r["audit_verdict"]
        lines.append(f"## Round {r['iteration']}")
        lines.append("")
        lines.append(f"**Planner (Agent A) outline** — keywords used: {', '.join(outline['keywords_used'])}")
        for item in outline["outline"]:
            lines.append(f"- {item}")
        lines.append(f"\n*Rationale:* {outline['rationale']}")
        lines.append("")
        verdict_word = "PASSED" if verdict["passed"] else "REJECTED"
        lines.append(f"**Auditor (Agent B) verdict: {verdict_word}**")
        if verdict["issues"]:
            lines.append("Issues:")
            for issue in verdict["issues"]:
                lines.append(f"- {issue}")
        if verdict["revision_suggestions"]:
            lines.append("Revision suggestions:")
            for s in verdict["revision_suggestions"]:
                lines.append(f"- {s}")
        lines.append("")

    return "\n".join(lines)


def render_final_output(state: NegotiationState) -> str:
    """B16 — the final outline plus a plain-language summary of the
    negotiation's key turning points. `status` is reported as-is
    ("converged" or "exhausted") — never smoothed into an implied success."""
    outline = state["outline"]
    lines = ["# Final Output", ""]
    lines.append(f"**Status: {state['status']}** (after {state['iteration'] + 1} round(s))")
    lines.append("")
    lines.append("## Final article outline")
    for item in outline["outline"]:
        lines.append(f"- {item}")
    lines.append(f"\n**Keywords used:** {', '.join(outline['keywords_used'])}")
    lines.append(f"\n**Rationale:** {outline['rationale']}")
    lines.append("")

    lines.append("## Negotiation summary")
    if not state["history"] and state["status"] == "converged":
        lines.append("Converged on round 0 — the first draft passed audit with no revision needed.")
    else:
        rejected_rounds = list(state["history"])
        if state["status"] == "exhausted":
            # The round that triggered "exhausted" was never appended to
            # history (see graph.py's decide_node) — include it here so
            # the summary doesn't silently omit the final rejection.
            rejected_rounds = rejected_rounds + [{
                "iteration": state["iteration"],
                "audit_verdict": state["audit_verdict"],
            }]
        lines.append(f"Took {len(rejected_rounds)} rejected round(s) before {state['status']}:")
        for entry in rejected_rounds:
            v = entry["audit_verdict"]
            lines.append(
                f"- Round {entry['iteration']}: rejected for "
                f"{'; '.join(v['issues'])} → asked to {'; '.join(v['revision_suggestions'])}"
            )
        if state["status"] == "exhausted":
            lines.append(
                f"\n**Did not converge within {state['max_iterations']} rounds** — the "
                "outline above is the last-audited version, still carrying the "
                "Auditor's final unresolved issues, not a passed result."
            )

    return "\n".join(lines)
