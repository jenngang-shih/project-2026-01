"""Pluggable LLM client for topic 4 — same Protocol-plus-Fixture pattern as
topics 1-2's llm_client.py, made async this time. Topic 4 is the first
topic where "asynchronous calls handled correctly" is itself an evaluated
requirement (B19), so this uses the real AsyncAzureOpenAI client rather
than wrapping a sync call in a thread — a genuinely async network call,
not a fake-async shim around blocking I/O.

No EmbeddingClient here: topic 4 doesn't do retrieval (see
docs/component-specs.md's run notes for why Manual.txt is loaded as static
text instead).
"""
from __future__ import annotations

from typing import Dict, Protocol

from dotenv import load_dotenv

load_dotenv()

import os


class LLMClient(Protocol):
    async def complete(self, prompt: str, *, component: str) -> str: ...


def _require_env(names: list[str]) -> Dict[str, str]:
    """Same validation as topics 1-2: every named var must be present and
    not an obvious .env.example placeholder."""
    values: Dict[str, str] = {}
    missing = []
    for name in names:
        val = os.environ.get(name, "")
        if not val or val.startswith("your-") or "<" in val:
            missing.append(name)
        else:
            values[name] = val
    if missing:
        raise RuntimeError("Missing real .env values for: " + ", ".join(missing))
    return values


class AzureOpenAILLMClient:
    """Real backend for both agents (Planner temp 0.7, Auditor temp 0.1 —
    see docs/component-specs.md's run notes for why they differ). One
    client instance is reused across both agents and every round; a fresh
    AsyncAzureOpenAI is constructed per call rather than held open across
    the whole graph run, same trade-off topics 1-2 made (simplicity over
    connection reuse) — not a bottleneck at this call volume."""

    def __init__(self) -> None:
        vals = _require_env([
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT",
        ])
        self._key = vals["AZURE_OPENAI_API_KEY"]
        self._endpoint = vals["AZURE_OPENAI_ENDPOINT"]
        self._api_version = vals["AZURE_OPENAI_API_VERSION"]
        self._deployment = vals["AZURE_OPENAI_DEPLOYMENT"]

    async def complete(self, prompt: str, *, component: str) -> str:
        from openai import AsyncAzureOpenAI  # imported lazily so this module loads without the package installed

        temperature = 0.7 if component == "planner" else 0.1
        client = AsyncAzureOpenAI(
            api_key=self._key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
        response = await client.chat.completions.create(
            model=self._deployment,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=2048,  # not max_tokens — see topic 1's llm_client.py
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content


class FixtureLLMClient:
    """Same queued-response pattern as topics 1-2's fixtures, made async.
    Queued per component ('planner' / 'auditor'), consumed in order — so a
    multi-round fixture run needs one queued response per expected call."""

    def __init__(self, fixtures: Dict[str, list]) -> None:
        self._fixtures = {k: list(v) for k, v in fixtures.items()}
        self.calls: list[str] = []

    async def complete(self, prompt: str, *, component: str) -> str:
        self.calls.append(component)
        queue = self._fixtures.get(component)
        if not queue:
            raise KeyError(f"No fixture left for component '{component}'")
        return queue.pop(0)
