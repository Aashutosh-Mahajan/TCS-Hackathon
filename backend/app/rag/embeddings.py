"""
Embedding wrapper for intfloat/multilingual-e5-small.

Key design decisions:
- Singleton pattern via module-level instance for performance (model loads once)
- Mandatory 'query: ' / 'passage: ' prefixes per E5 model specification
- 384-dimensional output vectors, normalized for cosine similarity
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import get_settings

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Lazy-load the embedding model (singleton)."""
    global _model
    if _model is None:
        settings = get_settings()
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def encode_query(text: str) -> np.ndarray:
    """
    Encode a search query with the required 'query: ' prefix.
    Returns a 384-dim normalized vector.
    """
    model = _get_model()
    prefixed = f"query: {text}"
    embedding = model.encode([prefixed], normalize_embeddings=True)
    return embedding[0]


def encode_passages(texts: list[str]) -> np.ndarray:
    """
    Encode document passages with the required 'passage: ' prefix.
    Returns array of shape (n, 384) with normalized vectors.
    """
    model = _get_model()
    prefixed = [f"passage: {t}" for t in texts]
    embeddings = model.encode(prefixed, normalize_embeddings=True, show_progress_bar=False)
    return embeddings


def preload_model() -> None:
    """Force model loading at startup (called from FastAPI lifespan)."""
    _get_model()
