"""Minimal CLI entry point: runs one full negotiation (Start -> Planning ->
Audit -> Decision, looping per B8) and prints all three B12/B13/B16
deliverables. Requires the AZURE_OPENAI_* vars to be real values in .env.

Defaults to B9/B10's exact forced-conflict fixture (娛樂城推薦 / Casino,
required terms 穩賺不賠 + 保證出金) so `python -m src.cli` with no flags
reproduces the scenario the source explicitly asks for.

Usage:
    python -m src.cli
    python -m src.cli --keyword "房屋二胎利率" --category Mortgage \
        --required-terms "全台最低利" --max-iterations 3
"""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .graph import build_graph, initial_state
from .llm_client import AzureOpenAILLMClient
from .render import render_final_output, render_graph_diagram, render_state_log

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


async def run(args: argparse.Namespace) -> None:
    llm = AzureOpenAILLMClient()  # raises clearly if .env isn't configured
    graph = build_graph(llm)

    compliance_reference = (DATA_DIR / "Manual.txt").read_text(encoding="utf-8-sig")  # BOM, same as topic 2
    state = initial_state(
        keyword=args.keyword,
        category=args.category,
        required_ctr_terms=args.required_terms,
        forbidden_terms=args.forbidden_terms,
        compliance_reference=compliance_reference,
        max_iterations=args.max_iterations,
    )
    final_state = await graph.ainvoke(state)

    print(render_graph_diagram(graph))
    print("\n" + "=" * 72 + "\n")
    print(render_state_log(final_state))
    print("\n" + "=" * 72 + "\n")
    print(render_final_output(final_state))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="娛樂城推薦")
    parser.add_argument("--category", default="Casino")
    parser.add_argument(
        "--required-terms", nargs="+", default=["穩賺不賠", "保證出金"],
        help="Agent A's forced high-CTR terms (B10).",
    )
    parser.add_argument(
        "--forbidden-terms", nargs="+", default=["穩賺不賠", "保證出金"],
        help="Agent B's hard blocklist (B10 — same terms by design: the "
             "whole scenario is that Agent A is configured to require "
             "exactly what Agent B is configured to forbid).",
    )
    parser.add_argument("--max-iterations", type=int, default=5)
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
