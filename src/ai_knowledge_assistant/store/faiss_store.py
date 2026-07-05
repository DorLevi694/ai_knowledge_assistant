"""FAISS-backed in-memory vector store for nearest-neighbor similarity search.

This module exposes :class:`FaissStore`, which wraps a FAISS
``IndexFlatIP`` (inner-product / cosine similarity) index and stores the
original :class:`~embedding.EmbeddedChunk` objects alongside the raw
vectors so that results can be returned as rich :class:`~store.base.ScoredChunk`
instances.
"""

# src\ai_knowledge_assistant\store\faiss_store.py file
import json
import logging
from dataclasses import asdict

import faiss
import numpy as np

from ai_knowledge_assistant.config import MIN_SIMILARITY_THRESHOLD
from ai_knowledge_assistant.embedding import EmbeddedChunk

from .base import ScoredChunk

logger = logging.getLogger(__name__)


class FaissStore:
    """In-memory FAISS vector index with cosine-similarity search.

    Vectors are L2-normalized before being added to the index so that
    inner-product scores are equivalent to cosine similarity scores in the
    range [0, 1].
    """

    def __init__(self, dim: int):
        """Initialise an empty index for vectors of the given dimensionality.

        Args:
            dim: The dimensionality of the embedding vectors that will be
                stored (e.g. 384 for ``all-MiniLM-L6-v2``).
        """
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # Inner Product (cosine-ready)
        self.items: list[EmbeddedChunk] = []

    def build(self, chunks: list[EmbeddedChunk]) -> None:
        """Populate the index from a list of embedded chunks.

        All previously indexed vectors are discarded when this method is
        called.  Vectors are L2-normalized in-place before being added to
        the FAISS index.

        Args:
            chunks: The embedded chunks whose vectors should be indexed.  An
                empty list is accepted but results in a warning and leaves
                the index empty.
        """
        if not chunks:
            logger.warning(
                "build() called with an empty chunk list. Index will remain empty."
            )
            return

        vectors = np.array([c.vector for c in chunks]).astype("float32")
        faiss.normalize_L2(vectors)  # cosine similarity
        self.index.add(vectors)  # type: ignore[call-arg]
        self.items = chunks

    def search(
        self,
        query_vector: list[float],
        k: int = 5,
        threshold: float = MIN_SIMILARITY_THRESHOLD,
    ) -> list[ScoredChunk]:
        """Return the top-*k* chunks most similar to the query vector.

        The query vector is L2-normalized before querying so scores are
        cosine-similarity values in [0, 1].  Only results whose score meets
        or exceeds *threshold* are included.

        Args:
            query_vector: The embedding of the query, as a flat list of
                floats.
            k: Maximum number of results to return.  Defaults to 5.
            threshold: Minimum cosine-similarity score a result must have to
                be included in the output.  Defaults to 0.3.

        Returns:
            A list of :class:`~store.base.ScoredChunk` objects sorted by
            descending similarity score (FAISS guarantees this ordering).
        """
        results: list[ScoredChunk] = []
        q = np.array([query_vector]).astype("float32")
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, k)  # type: ignore[call-arg]
        for score, indic in zip(scores[0], indices[0], strict=True):
            if indic == -1:
                continue
            if score < threshold:
                continue

            results.append(
                ScoredChunk(
                    source=self.items[indic].source,
                    index=self.items[indic].index,
                    text=self.items[indic].text,
                    vector=self.items[indic].vector,
                    score=float(score),
                )
            )
        scored_chunks_as_dicts = [asdict(scored_chunk) for scored_chunk in results]
        logger.debug(json.dumps(scored_chunks_as_dicts, indent=2, ensure_ascii=False))
        return results
