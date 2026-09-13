"""Fault tolerance for the two dynamic nodes (B19, docs/component-specs.md's
run notes): a real async retry with exponential backoff, scoped specifically
to transient API errors, not a blanket catch-and-retry-anything.

Two genuinely different failure modes are handled differently on purpose:
- Transient (rate limit / timeout / connection): retried here, silently
  recovered if a later attempt succeeds — the caller never sees it.
- Malformed output (bad JSON, failed schema validation): NOT retried by
  this function. A schema failure isn't fixed by resending the identical
  prompt to a model that just failed to follow it; src/graph.py retries
  that case once with the same input (per component-specs.md's G2/G3
  spec), then surfaces it as a real, named failure.
"""
from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

ATTEMPTS = 3
BACKOFF_SECONDS = (1, 2)  # delay before the 2nd and 3rd attempts — see component-specs.md run notes


async def call_with_retry(fn: Callable[[], Awaitable[T]]) -> T:
    """Retries `fn` (a zero-arg async callable — callers wrap their real
    call in a lambda/closure) on transient OpenAI/Azure errors: 3 attempts
    total, waiting 1s then 2s between them. Raises the last transient
    error if every attempt is exhausted; any other exception propagates
    immediately, unretried."""
    from openai import APIConnectionError, APITimeoutError, RateLimitError

    last_exc: Exception | None = None
    for attempt in range(ATTEMPTS):
        if attempt > 0:
            await asyncio.sleep(BACKOFF_SECONDS[attempt - 1])
        try:
            return await fn()
        except (RateLimitError, APITimeoutError, APIConnectionError) as e:
            last_exc = e
            continue
    raise RuntimeError(
        f"LLM call failed after {ATTEMPTS} attempts (transient errors): {last_exc}"
    ) from last_exc
