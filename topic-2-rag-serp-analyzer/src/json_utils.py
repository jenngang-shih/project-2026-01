"""Shared deterministic parsing gate for topic 2's dynamic components —
same role as topic 1's orchestrator._parse_json_response, pulled into its
own module here since two different modules (skill.py's gap detection,
orchestrator.py's proposal generation) both need it, not just one.
"""
from __future__ import annotations

import json
from typing import Any


def parse_json_response(raw: str) -> Any:
    """Each dynamic component is instructed to return JSON; this is where
    that contract is enforced rather than trusted blindly (ties to B21 —
    Technical Rigor)."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Component did not return valid JSON: {exc}\nRaw: {raw!r}") from exc
