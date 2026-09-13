"""Pluggable LLM client used by orchestrator.py.

Implementations:
- AnthropicLLMClient — the real thing; unusable until ANTHROPIC_API_KEY in
  .env holds an actual key (it currently doesn't — see project README).
- AzureOpenAILLMClient — alternative backend for an Azure OpenAI deployment;
  unusable until AZURE_OPENAI_API_KEY/ENDPOINT/API_VERSION/DEPLOYMENT in .env
  hold real values.
- FixtureLLMClient — returns pre-recorded responses instead of calling a
  live model. Used to exercise the deterministic orchestrator logic against
  real (manually authored, not fabricated) dynamic content when no live API
  key is configured. Provenance of any fixtures used lives wherever they're
  constructed (e.g. docs/sample-run.md), not in this module.
"""
from __future__ import annotations

import os
from typing import Any, Protocol

from dotenv import load_dotenv

# Loads the project-root .env (if present) into os.environ. Safe to call
# repeatedly/on import — python-dotenv no-ops if the file is missing and
# never overwrites variables already set in the real environment.
load_dotenv()


class LLMClient(Protocol):
    def complete(self, prompt: str, *, component: str) -> str: ...


class AnthropicLLMClient:
    """Not usable until ANTHROPIC_API_KEY is a real value in .env."""

    def __init__(self) -> None:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key or key == "your-key-here":
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set to a real value in .env — "
                "AnthropicLLMClient cannot make live calls yet."
            )
        self._key = key

    def complete(self, prompt: str, *, component: str) -> str:
        import anthropic  # imported lazily so this module loads without the package installed

        client = anthropic.Anthropic(api_key=self._key)
        msg = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text


class AzureOpenAILLMClient:
    """Not usable until AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION, and AZURE_OPENAI_DEPLOYMENT are all real values
    in .env. AZURE_OPENAI_DEPLOYMENT is the deployment name chosen in Azure
    AI Studio (e.g. 'gpt-5.6-terra'), not a bare model name — Azure's API
    takes it in the `model` field of the chat-completions call.

    For the two components whose contract requires JSON (stage_a → StageAOutput,
    stage_c_audit → AuditVerdict — see schemas.py), this requests Azure/OpenAI's
    JSON mode (response_format={"type": "json_object"}) so a syntactically valid
    JSON response is enforced server-side rather than relying only on the prompt
    instructions the way AnthropicLLMClient currently does — orchestrator.py's
    _parse_json_response is a bare json.loads with no markdown-fence stripping,
    so this matters. JSON mode requires the literal word "json" to appear
    somewhere in the prompt, which prompts.py's stage_a_prompt and
    stage_c_audit_prompt both already do.
    """

    _JSON_COMPONENTS = {"stage_a", "stage_c_audit"}

    def __init__(self) -> None:
        key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "")
        deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
        missing = [
            name
            for name, val in [
                ("AZURE_OPENAI_API_KEY", key),
                ("AZURE_OPENAI_ENDPOINT", endpoint),
                ("AZURE_OPENAI_API_VERSION", api_version),
                ("AZURE_OPENAI_DEPLOYMENT", deployment),
            ]
            if not val or val.startswith("your-") or "<" in val
        ]
        if missing:
            raise RuntimeError(
                "AzureOpenAILLMClient is missing real values in .env for: "
                f"{', '.join(missing)}"
            )
        self._key = key
        self._endpoint = endpoint
        self._api_version = api_version
        self._deployment = deployment

    def complete(self, prompt: str, *, component: str) -> str:
        from openai import AzureOpenAI  # imported lazily so this module loads without the package installed

        client = AzureOpenAI(
            api_key=self._key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
        extra: dict[str, Any] = {}
        if component in self._JSON_COMPONENTS:
            extra["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(
            model=self._deployment,  # Azure takes the deployment name here, not a model name
            messages=[{"role": "user", "content": prompt}],
            # max_completion_tokens, not max_tokens — newer Azure/OpenAI chat
            # deployments (reasoning-tuned and GPT-5-class models included)
            # reject max_tokens outright and require this instead.
            max_completion_tokens=2048,
            **extra,
        )
        return response.choices[0].message.content


class FixtureLLMClient:
    """Returns queued pre-recorded responses per component instead of calling
    a live model. Each `component` key maps to a list of responses consumed
    in order, so repeated calls (e.g. multiple Stage-C audit/correct cycles)
    are each given their own recorded response."""

    def __init__(self, fixtures: dict[str, list[str]]) -> None:
        self._fixtures = {k: list(v) for k, v in fixtures.items()}
        self.calls: list[str] = []

    def complete(self, prompt: str, *, component: str) -> str:
        self.calls.append(component)
        queue = self._fixtures.get(component)
        if not queue:
            raise KeyError(f"No fixture left for component '{component}'")
        return queue.pop(0)
