"""
BM25 sparse retrieval index.

Uses rank_bm25 for keyword-based matching — complements dense embeddings
by catching exact keyword matches that semantic search might miss.
"""

from rank_bm25 import BM25Okapi
import re


class BM25Index:
    """In-memory BM25 index over a list of passages."""

    def __init__(self):
        self._bm25: BM25Okapi | None = None
        self._passages: list[str] = []

    def build(self, passages: list[str]) -> None:
        """Build the BM25 index from a list of passage texts."""
        self._passages = passages
        # Tokenize: lowercase, split on non-alphanumeric (works for Latin + Devanagari)
        tokenized = [self._tokenize(p) for p in passages]
        self._bm25 = BM25Okapi(tokenized)

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        """
        Search the index for a query.
        Returns list of (passage_index, bm25_score) sorted descending.
        """
        if self._bm25 is None:
            return []

        tokenized_query = self._tokenize(query)
        scores = self._bm25.get_scores(tokenized_query)

        # Get top-k indices sorted by score descending
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [(idx, float(scores[idx])) for idx in ranked_indices if scores[idx] > 0]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Simple whitespace + punctuation tokenizer that works across scripts."""
        text = text.lower()
        tokens = re.findall(r'\w+', text, re.UNICODE)
        return tokens
