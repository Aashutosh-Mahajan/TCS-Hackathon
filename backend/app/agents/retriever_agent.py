"""
Retriever Agent — performs dense + sparse retrieval with RRF fusion.

Combines multilingual-e5-small dense embeddings with BM25 keyword matching,
then fuses rankings with Reciprocal Rank Fusion for robust retrieval.
"""

import time
import re
from app.agents.state import PipelineState
from app.rag.embeddings import encode_query
from app.rag.fusion import reciprocal_rank_fusion
from app.config import get_settings

# These are populated at startup by main.py
_vector_store = None
_bm25_index = None
_passages_data = []

GENERIC_TERMS = {"about", "are", "can", "company", "does", "employee", "for", "how", "information", "is", "of", "on", "policy", "the", "to", "what", "with"}


def _has_specific_term_overlap(query: str, snippets: list[dict]) -> bool:
    """Avoid treating a shared generic word such as 'policy' as evidence."""
    query_terms = {term for term in re.findall(r"[a-z]{3,}", query.lower()) if term not in GENERIC_TERMS}
    if not query_terms:  # Embedding similarity is the cross-language gate.
        return True
    evidence = " ".join(s["text"] for s in snippets).lower()
    return any(term in evidence for term in query_terms)


def init_retriever(vector_store, bm25_index, passages_data: list[dict]):
    """Initialize the retriever with pre-built indices (called at startup)."""
    global _vector_store, _bm25_index, _passages_data
    _vector_store = vector_store
    _bm25_index = bm25_index
    _passages_data = passages_data


def retriever_agent(state: PipelineState) -> dict:
    """Retrieve top-k snippets using dense + sparse + RRF fusion."""
    start = time.perf_counter()
    query = state["query"]
    settings = get_settings()
    top_k = settings.top_k

    # 1. Dense retrieval via embeddings
    query_embedding = encode_query(query)
    dense_results = _vector_store.search(query_embedding, top_k=top_k * 2)
    dense_rankings = [(idx, score) for idx, score, _meta in dense_results]

    # 2. Sparse retrieval via BM25
    sparse_rankings = _bm25_index.search(query, top_k=top_k * 2)

    # 3. Fuse with RRF
    fused_rankings = reciprocal_rank_fusion(dense_rankings, sparse_rankings)

    # 4. Build snippet results (top-k from fused)
    snippets = []
    for doc_idx, fused_score in fused_rankings[:top_k]:
        entry = _passages_data[doc_idx]
        # Also get the raw dense cosine similarity for this doc
        raw_cosine = 0.0
        for didx, score, _meta in dense_results:
            if didx == doc_idx:
                raw_cosine = score
                break

        snippets.append({
            "text": entry["passage"],
            "score": round(raw_cosine, 4),
            "fused_score": round(fused_score, 4),
            "source": entry["metadata"]["source"],
            "language": entry["language"],
            "category": entry["category"],
            "section": entry["metadata"].get("section", ""),
        })

    # Best retrieval score (cosine similarity of top snippet)
    best_score = snippets[0]["score"] if snippets else 0.0
    specific_overlap = _has_specific_term_overlap(query, snippets)
    dataset_match = bool(snippets and best_score >= settings.dataset_match_threshold and specific_overlap)
    # Ranking always returns a nearest neighbour; omit it unless it passes the
    # evidence gate so unrelated questions cannot receive a random answer.
    if not dataset_match:
        snippets = []

    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Retriever Agent",
        "input_summary": f"Query: '{query[:60]}...' | Language: {state.get('detected_language', 'unknown')}",
        "output_summary": f"Dataset match: {dataset_match} | Best score: {best_score:.4f} | Specific overlap: {specific_overlap}",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "retrieved_snippets": snippets,
        "retrieval_score": best_score,
        "dataset_match": dataset_match,
        "dataset_status": "in_dataset" if dataset_match else "not_in_dataset",
        "agent_trace": existing_trace + [trace_entry],
    }
