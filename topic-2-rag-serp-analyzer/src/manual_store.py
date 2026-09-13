"""C3 — Manual Ingestion and C4 — Manual Retriever. Source: B9 (+B10), B11.

Both deterministic: chunking, embedding-endpoint calls, and vector
similarity search are all fixed mechanical operations, not generative
judgment — see docs/component-specs.md's classification table for why an
embedding call doesn't count as "dynamic" the way a chat completion does.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from .llm_client import EmbeddingClient
from .schemas import RetrievedPassage

COLLECTION_NAME = "topic2_manual"


def _chunk_manual(text: str) -> list[dict[str, str]]:
    """One chunk per non-empty line. Engineering default (see
    docs/component-specs.md run notes), not a sourced requirement —
    originally planned as paragraph-level (split on blank lines), but the
    actual data/Manual.txt has three distinct compliance rules with *no*
    blank lines between them, which would degenerate paragraph-splitting
    to a single chunk covering the whole file — losing per-rule provenance
    entirely (checked the real file before picking this, not assumed).
    Per-line chunking gives each rule its own retrievable, citable chunk for
    this manual's actual shape. `[needs review]` if a future, longer manual
    has rules that wrap across multiple lines — this would then fragment a
    single rule mid-sentence, and a real paragraph- or sentence-aware
    splitter would be needed instead."""
    chunks: list[dict[str, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            chunks.append({"text": line.strip(), "source_line_range": str(i)})
    return chunks


def get_chroma_client(persist_dir: str = ".chroma"):
    """Lazily imported so this module loads without chromadb installed."""
    import chromadb

    return chromadb.PersistentClient(path=persist_dir)


def ingest_manual(manual_path: str, embedding_client: EmbeddingClient, persist_dir: str = ".chroma") -> None:
    """C3. Source: B9 (+B10). Runs offline/once (or whenever Manual.txt
    changes) — not part of the per-request path; see
    docs/component-specs.md's orchestration diagram.

    Drops and recreates the collection on every call rather than appending,
    so re-running after Manual.txt changes doesn't silently accumulate
    stale chunks alongside the new ones.
    """
    # utf-8-sig, not utf-8 — data/Manual.txt carries a UTF-8 BOM (same as
    # data/SERP_Data.json), which would otherwise land as a stray invisible
    # character prefixing the first chunk.
    text = Path(manual_path).read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError(
            f"{manual_path} is empty — refusing to silently populate an "
            "empty collection that C4 would then query against forever "
            "without anyone noticing (B21)."
        )

    chunks = _chunk_manual(text)
    client = get_chroma_client(persist_dir)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection didn't exist yet — fine, create() below handles it
    # Explicit cosine distance — Chroma's default (squared L2) makes the
    # "score" approximation below uninterpretable (can go negative); cosine
    # is also the standard metric for the kind of normalized text
    # embeddings Azure OpenAI's embedding models produce.
    collection = client.create_collection(COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    vectors = embedding_client.embed([c["text"] for c in chunks])
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=vectors,
        documents=[c["text"] for c in chunks],
        metadatas=[{"source_line_range": c["source_line_range"]} for c in chunks],
    )


def retrieve_manual_guidance(
    keyword: str,
    embedding_client: EmbeddingClient,
    top_k: int = 3,
    persist_dir: str = ".chroma",
) -> List[RetrievedPassage]:
    """C4. Source: B11. `top_k=3` is an engineering default (see
    docs/component-specs.md run notes), not a sourced requirement.

    Raises if the collection doesn't exist (ingest_manual() never ran) —
    this must be distinguishable from "genuinely no relevant guidance for
    this keyword" (a valid, informative empty-list result), not conflated
    with it.
    """
    client = get_chroma_client(persist_dir)
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            "Manual collection not found — call ingest_manual() first "
            "(it hasn't run yet, or persist_dir doesn't match)."
        ) from exc

    [query_vector] = embedding_client.embed([keyword])
    results = collection.query(query_embeddings=[query_vector], n_results=top_k)

    passages: List[RetrievedPassage] = []
    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    dists = results["distances"][0] if results["distances"] else []
    for doc, meta, dist in zip(docs, metas, dists):
        # Chroma's default distance is squared L2 by our (unspecified) index
        # config; treating (1 - dist) as a similarity "score" is a rough
        # approximation good enough for a prototype's provenance display,
        # not a calibrated confidence value.
        passages.append(
            RetrievedPassage(text=doc, score=1 - dist, source_line_range=meta["source_line_range"])
        )
    return passages
