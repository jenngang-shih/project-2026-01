# Architecture Overview

## Relationship between topics

These four topics are related but independently runnable pieces of the same overall "AI for SEO" system:

```
Plan & Author (Topic 1: prompt chaining)
        │
        ▼
Research & Ground (Topic 2: RAG SERP analyzer)
        │
        ▼
Validate — offline/local (Topic 3: local LLM diagnostics)
        │
        ▼
Reconcile multiple perspectives (Topic 4: multi-agent conflict resolution)
```

In practice, a piece of content might flow: draft via Topic 1 → check against SERP/competitor landscape via Topic 2 → run local diagnostics via Topic 3 → resolve any conflicting agent feedback via Topic 4.

## Shared conventions
- Structured data passed between stages as JSON (schemas TBD per topic).
- Human-readable content and reports as Markdown.
- Each topic is runnable standalone for focused development/testing, with an eventual top-level orchestrator (TBD) to chain them.

## Resolved (were "open questions" before topics 1-3 were built)
- Local model choice/runtime for topic 3: Llama-3-8B-Instruct, QLoRA
  fine-tuned, on Colab/T4 — see `topic-3-local-llm-seo-diagnostics/README.md`.
- Topic 4's backend: **Azure OpenAI for both agents**, not the Llama-based
  model this doc originally noted — that note predated topics 1-3 and was
  superseded once Azure OpenAI proved out across topics 1-2; see
  `topic-4-multi-agent-conflict-resolution/docs/problem-statement-categorized.md`'s
  run notes for the explicit decision. LangGraph itself (the graph
  orchestration library) is unaffected by this — still used as named.

## Open questions (to resolve as elaborations arrive)
- Exact JSON schema(s) for inter-topic data exchange
- Whether topics 1/2/4 share one Anthropic API client/config module
- An eventual top-level orchestrator chaining all four topics (still TBD;
  each topic remains independently runnable in the meantime)
