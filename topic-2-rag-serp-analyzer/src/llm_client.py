"""Pluggable clients for topic 2. Two separate Protocols, not one, because
this topic needs two genuinely different API shapes:
- LLMClient — chat completions for the two dynamic components (gap
  detection, proposal generation): persona/prompt-in, text-out.
- EmbeddingClient — text-in, vector-out. Not a judgment call, so it isn't
  given a Role/Goal/Instructions prompt the way the LLMClient calls are;
  it's closer to a deterministic transformation that happens to be served
  by a hosted model (see docs/component-specs.md's C3/C4 notes).

Implementations:
- AzureOpenAILLMClient / AzureOpenAIEmbeddingClient — the real thing; both
  unusable until the relevant AZURE_OPENAI_* vars in .env hold real values.
- FixtureLLMClient / FixtureEmbeddingClient — deterministic stand-ins for
  exercising the control flow without a live API key or network call.
"""
from __future__ import annotations

import hashlib
import os
from typing import Dict, List, Protocol

from dotenv import load_dotenv

# Loads the project-root .env (if present) into os.environ. Same as topic
# 1's llm_client.py — safe to call repeatedly, no-ops if .env is missing.
load_dotenv()


class LLMClient(Protocol):
    def complete(self, prompt: str, *, component: str) -> str: ...


class EmbeddingClient(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]: ...


def _require_env(names: list[str]) -> Dict[str, str]:
    """Shared validation for both Azure clients below: every named var must
    be present and not an obvious .env.example placeholder ("your-...", or
    containing "<" as in "<your-resource>"). Raises once, naming every
    missing/placeholder var, rather than failing on the first one and
    forcing a fix-one-rerun-fix-the-next cycle."""
    values: Dict[str, str] = {}
    missing = []
    for name in names:
        val = os.environ.get(name, "")
        if not val or val.startswith("your-") or "<" in val:
            missing.append(name)
        else:
            values[name] = val
    if missing:
        raise RuntimeError(
            "Missing real .env values for: " + ", ".join(missing)
        )
    return values


class AzureOpenAILLMClient:
    """Chat-completion backend for the two dynamic components. Requests
    Azure/OpenAI JSON mode for both — unlike topic 1, *every* dynamic
    component here returns structured JSON (neither one is free-text like
    topic 1's Stage B), so there's no free-text exception list."""

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

    def complete(self, prompt: str, *, component: str) -> str:
        from openai import AzureOpenAI  # imported lazily so this module loads without the package installed

        client = AzureOpenAI(
            api_key=self._key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
        response = client.chat.completions.create(
            model=self._deployment,  # Azure takes the deployment name here, not a model name
            messages=[{"role": "user", "content": prompt}],
            # max_completion_tokens, not max_tokens — see topic 1's
            # llm_client.py for why (newer/GPT-5-class deployments reject
            # max_tokens outright).
            max_completion_tokens=2048,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content


class AzureOpenAIEmbeddingClient:
    """Embedding backend for manual ingestion (C3) and retrieval (C4). Uses
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT — a separate deployment from the chat
    model above; Azure serves embeddings and chat completions from
    different deployed models, so this can't reuse AZURE_OPENAI_DEPLOYMENT."""

    def __init__(self) -> None:
        vals = _require_env([
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        ])
        self._key = vals["AZURE_OPENAI_API_KEY"]
        self._endpoint = vals["AZURE_OPENAI_ENDPOINT"]
        self._api_version = vals["AZURE_OPENAI_API_VERSION"]
        self._deployment = vals["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]

    def embed(self, texts: List[str]) -> List[List[float]]:
        from openai import AzureOpenAI  # imported lazily, same reason as above

        client = AzureOpenAI(
            api_key=self._key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
        response = client.embeddings.create(model=self._deployment, input=texts)
        return [item.embedding for item in response.data]


class FixtureLLMClient:
    """Same pattern as topic 1's: queued pre-recorded responses per
    component, consumed in order — so repeated calls to the same component
    each get their own recorded response."""

    def __init__(self, fixtures: Dict[str, list]) -> None:
        self._fixtures = {k: list(v) for k, v in fixtures.items()}
        self.calls: list[str] = []

    def complete(self, prompt: str, *, component: str) -> str:
        self.calls.append(component)
        queue = self._fixtures.get(component)
        if not queue:
            raise KeyError(f"No fixture left for component '{component}'")
        return queue.pop(0)


class FixtureEmbeddingClient:
    """Deterministic fake embeddings — no real API call, no network. Hashes
    each text into a fixed-size float vector so identical text always
    yields an identical vector and different text yields a different one,
    which is enough to exercise Chroma's storage/similarity-search logic in
    tests without a live embedding endpoint. Not a semantically meaningful
    embedding — never use for anything but control-flow testing."""

    DIM = 16

    def embed(self, texts: List[str]) -> List[List[float]]:
        vectors = []
        for t in texts:
            digest = hashlib.sha256(t.encode("utf-8")).digest()
            vectors.append([b / 255.0 for b in digest[: self.DIM]])
        return vectors
