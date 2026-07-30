"""
In-memory vector store using numpy cosine similarity.

No external vector DB dependency — optimized for hackathon speed
with a small dataset (20 entries). The embedding model already
returns normalized vectors, so cosine similarity = dot product.
"""

import numpy as np


class VectorStore:
    """Simple in-memory vector store with cosine similarity search."""

    def __init__(self):
        self._embeddings: np.ndarray | None = None
        self._metadata: list[dict] = []

    def add(self, embeddings: np.ndarray, metadata: list[dict]) -> None:
        """
        Add vectors and their associated metadata to the store.

        Args:
            embeddings: Array of shape (n, dim) — must be L2-normalized.
            metadata: List of dicts with at least 'text', 'source', 'language' keys.
        """
        if self._embeddings is None:
            self._embeddings = embeddings
        else:
            self._embeddings = np.vstack([self._embeddings, embeddings])
        self._metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[tuple[int, float, dict]]:
        """
        Search for the most similar vectors.

        Args:
            query_embedding: 1-D array of shape (dim,) — must be L2-normalized.
            top_k: Number of results to return.

        Returns:
            List of (index, cosine_similarity, metadata) sorted descending.
        """
        if self._embeddings is None or len(self._metadata) == 0:
            return []

        # Cosine similarity via dot product (vectors are pre-normalized)
        similarities = np.dot(self._embeddings, query_embedding)

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            (int(idx), float(similarities[idx]), self._metadata[idx])
            for idx in top_indices
        ]

    @property
    def size(self) -> int:
        return len(self._metadata)
