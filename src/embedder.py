"""
embedder.py - Sentence-BERT embeddings for semantic similarity scoring
"""

import numpy as np
from typing import List, Union


_model = None


def get_model():
    """Lazy-load the SBERT model (cached after first call)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. Run: pip install sentence-transformers"
            )
        print("Loading Sentence-BERT model (first time may take ~30s)...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
    return _model


def embed_text(text: Union[str, List[str]]) -> np.ndarray:
    """
    Generate SBERT embeddings for a string or list of strings.
    Returns numpy array of shape (n, 384) for list or (384,) for single string.
    """
    model = get_model()
    if isinstance(text, str):
        return model.encode(text, convert_to_numpy=True)
    return model.encode(text, convert_to_numpy=True, show_progress_bar=False)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    vec1 = vec1 / (np.linalg.norm(vec1) + 1e-10)
    vec2 = vec2 / (np.linalg.norm(vec2) + 1e-10)
    return float(np.dot(vec1, vec2))


def batch_similarity(query_embedding: np.ndarray, corpus_embeddings: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between one query and a batch of embeddings.
    Returns array of similarity scores.
    """
    query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-10)
    corpus_norms = corpus_embeddings / (
        np.linalg.norm(corpus_embeddings, axis=1, keepdims=True) + 1e-10
    )
    return corpus_norms @ query_norm
