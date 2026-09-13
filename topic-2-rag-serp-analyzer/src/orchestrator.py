"""C1 — Orchestrator: deterministic control flow tying together the SERP
Analyzer Skill (C2), the Manual Retriever (C4), and the Proposal Generator
(C5). Source: B3 (umbrella objective), B13 (integrate LLM+RAG+Skill).

Unlike topic 1, there is no human-in-the-loop checkpoint here — see
docs/component-specs.md's run notes for why (B12 requires the build
*process* to be documented, not a runtime human decision inside the
request/response flow). generate_seo_proposal() is a single, fully
automated function, not split around a checkpoint the way topic 1's
start_prompt_chain/resume_prompt_chain are.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .json_utils import parse_json_response
from .llm_client import EmbeddingClient, LLMClient
from .manual_store import retrieve_manual_guidance
from .prompts import proposal_prompt
from .schemas import ProposalOutput, SerpResult
from .skill import analyze_serp


@dataclass
class ProposalResult:
    keyword: str
    serp_analysis: dict[str, Any]
    retrieved_passages: list[dict[str, Any]] = field(default_factory=list)
    proposal: dict[str, Any] = field(default_factory=dict)


def load_serp_data(path: str) -> list[SerpResult]:
    """Source: B4. Raises a clear, wrapped error on a missing/malformed
    file rather than letting a bare FileNotFoundError/JSONDecodeError
    surface — matches component-specs.md's C1 error-handling requirement
    (B21): don't silently proceed with an empty competitive analysis.
    Uses utf-8-sig since data/SERP_Data.json carries a UTF-8 BOM."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not load SERP data from {path}: {exc}") from exc
    return [SerpResult.model_validate(r) for r in raw]


def generate_seo_proposal(
    keyword: str,
    serp_data_path: str,
    llm: LLMClient,
    embedding_client: EmbeddingClient,
    top_k: int = 3,
    persist_dir: str = ".chroma",
) -> ProposalResult:
    """C1's entry point. Source: B3 (umbrella), B13.

    Logic (see docs/component-specs.md's orchestration diagram):
    1. Load SERP data (deterministic, fails loudly on bad input).
    2. Call C2 analyze_serp() — headings + keyword distribution
       (deterministic) + content gaps (dynamic, validated).
    3. Call C4 retrieve_manual_guidance() — vector search against C3's
       pre-populated collection; may legitimately return [].
    4. Call C5 (dynamic) with both bundles together — an empty passages
       list is passed through as-is, not special-cased here: the prompt's
       own Constraints require it to say the manual is silent rather than
       inventing guidance, so the orchestrator doesn't need a second gate
       for that.
    """
    serp_data = load_serp_data(serp_data_path)
    analysis = analyze_serp(serp_data, keyword, llm)
    passages = retrieve_manual_guidance(keyword, embedding_client, top_k=top_k, persist_dir=persist_dir)

    raw_proposal = llm.complete(
        proposal_prompt(
            keyword,
            analysis.model_dump(),
            [p.model_dump() for p in passages],
        ),
        component="proposal_generation",
    )
    proposal = ProposalOutput.model_validate(parse_json_response(raw_proposal))

    return ProposalResult(
        keyword=keyword,
        serp_analysis=analysis.model_dump(),
        retrieved_passages=[p.model_dump() for p in passages],
        proposal=proposal.model_dump(),
    )
