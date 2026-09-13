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

## Open questions (to resolve as elaborations arrive)
- Exact JSON schema(s) for inter-topic data exchange
- Whether topics 1/2/4 share one Anthropic API client/config module
- Local model choice and runtime for topic 3
- Topic 4 uses LangGraph with a Llama-based model (decided; exact model/runtime TBD)
