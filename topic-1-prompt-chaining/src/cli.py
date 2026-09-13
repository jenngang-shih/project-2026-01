"""CLI entry point running the topic-1 prompt chain end-to-end against a
real model. Requires either ANTHROPIC_API_KEY (--backend anthropic, default)
or the AZURE_OPENAI_* variables (--backend azure) to be real values in .env —
until then this raises clearly rather than silently falling back to fixtures.

For a fixture-backed dry run instead, see docs/sample-run.md.

Usage:
    python -m src.cli --keyword 娛樂城
    python -m src.cli --keyword 娛樂城 --backend azure
"""
from __future__ import annotations

import argparse
import os

from .llm_client import AnthropicLLMClient, AzureOpenAILLMClient
from .orchestrator import resume_prompt_chain, start_prompt_chain


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="娛樂城")
    parser.add_argument("--retry-cap", type=int, default=3)
    parser.add_argument(
        "--backend",
        choices=["anthropic", "azure"],
        default=os.environ.get("LLM_BACKEND", "anthropic"),
        help="Which LLM backend to use (default: anthropic, or $LLM_BACKEND if set)",
    )
    args = parser.parse_args()

    # Each raises clearly if its required .env values aren't configured yet.
    llm = AnthropicLLMClient() if args.backend == "anthropic" else AzureOpenAILLMClient()

    req = start_prompt_chain(args.keyword, llm)
    print(f"Candidate micro-intents for [{args.keyword}]:")
    for i, intent in enumerate(req.stage_a_intents):
        print(f"  [{i}] {intent['intent']}")
    choice = int(input("Pick one by index: "))

    result = resume_prompt_chain(
        req.session_id, req.stage_a_intents[choice], llm, retry_cap=args.retry_cap
    )
    print("\nFinal paragraph:\n", result.stage_b_final)
    print("\nFinal pass:", result.final_pass)
    print(f"Audit/correction cycles: {len(result.audit_trail)}")


if __name__ == "__main__":
    main()
