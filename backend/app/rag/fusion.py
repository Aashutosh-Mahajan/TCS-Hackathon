"""
Reciprocal Rank Fusion (RRF) — merges dense and sparse retrieval rankings.

RRF formula: score(d) = Σ 1 / (k + rank_i(d))
where k is a constant (default 60) and rank_i is the rank from retrieval system i.

This is the ~10-line fusion approach referenced in the PRD.
"""


def reciprocal_rank_fusion(
    dense_rankings: list[tuple[int, float]],
    sparse_rankings: list[tuple[int, float]],
    k: int = 60,
) -> list[tuple[int, float]]:
    """
    Fuse two ranked lists using Reciprocal Rank Fusion.

    Args:
        dense_rankings: List of (doc_index, score) from dense retrieval, sorted by score desc.
        sparse_rankings: List of (doc_index, score) from sparse retrieval, sorted by score desc.
        k: RRF constant (default 60, standard value from the original paper).

    Returns:
        List of (doc_index, fused_score) sorted by fused score descending.
        Scores are normalized to [0, 1].
    """
    fused_scores: dict[int, float] = {}

    for rank, (doc_idx, _score) in enumerate(dense_rankings):
        fused_scores[doc_idx] = fused_scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)

    for rank, (doc_idx, _score) in enumerate(sparse_rankings):
        fused_scores[doc_idx] = fused_scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)

    # Sort by fused score descending
    ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)

    # Normalize scores to [0, 1]
    if ranked:
        max_score = ranked[0][1]
        ranked = [(idx, score / max_score) for idx, score in ranked]

    return ranked
