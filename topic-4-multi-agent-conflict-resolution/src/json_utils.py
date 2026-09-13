"""Defensive JSON extraction — same approach as topic 3's notebook (strip
markdown fences, find the first balanced {...} by bracket-counting, never a
bare json.loads). Azure's JSON mode makes this less likely to be needed
than topic 3's un-tuned local model, but the two agents here are also
freer-form than topic 2's tightly-templated prompts, so it's kept rather
than assumed unnecessary.
"""
from __future__ import annotations

import json
import re


def extract_json(raw: str) -> dict:
    """Raises json.JSONDecodeError (via the final json.loads) if no valid
    JSON object can be found at all — callers decide what that means
    (topic 4's nodes treat it as a validation failure, see src/graph.py)."""
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    start = text.find("{")
    if start == -1:
        return json.loads(text)  # will raise, with a clear message

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    return json.loads(text[start:])  # unbalanced -- will raise
