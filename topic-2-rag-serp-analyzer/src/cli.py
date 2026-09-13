"""C6 — minimal CLI interface, satisfying B14's literal ask (a user enters
a keyword and sees the generated proposal) without building the Next.js/
React frontend B15 calls a bonus. Requires the AZURE_OPENAI_* vars
(including AZURE_OPENAI_EMBEDDING_DEPLOYMENT) to be real values in .env.

Usage:
    python -m src.cli --keyword "房屋二胎利率"
    python -m src.cli --keyword "房屋二胎利率" --reingest  # re-embed data/Manual.txt first
"""
from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path

from .llm_client import AzureOpenAIEmbeddingClient, AzureOpenAILLMClient
from .manual_store import ingest_manual
from .orchestrator import generate_seo_proposal

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PERSIST_DIR = Path(__file__).resolve().parent.parent / ".chroma"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="房屋二胎利率")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument(
        "--reingest",
        action="store_true",
        help="Re-chunk and re-embed data/Manual.txt before running (run once, or whenever Manual.txt changes).",
    )
    args = parser.parse_args()

    llm = AzureOpenAILLMClient()  # raises clearly if .env isn't configured
    embed = AzureOpenAIEmbeddingClient()

    if args.reingest:
        ingest_manual(str(DATA_DIR / "Manual.txt"), embed, persist_dir=str(PERSIST_DIR))
        print(f"Manual re-ingested into {PERSIST_DIR}.")

    result = generate_seo_proposal(
        args.keyword,
        str(DATA_DIR / "SERP_Data.json"),
        llm,
        embed,
        top_k=args.top_k,
        persist_dir=str(PERSIST_DIR),
    )
    print(json.dumps(dataclasses.asdict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
