# src\ai_knowledge_assistant\store\faiss_store.py file
import json
import logging
from dataclasses import asdict

import faiss
import numpy as np

from ai_knowledge_assistant.embedding import EmbeddedChunk
from .base import ScoredChunk

logger = logging.getLogger(__name__)


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # Inner Product (cosine-ready)
        self.items: list[EmbeddedChunk] = []

    def build(self, chunks: list[EmbeddedChunk]) -> None:
        if not chunks:
            logger.warning(
                "build() called with an empty chunk list. Index will remain empty."
            )
            return

        vectors = np.array([c.vector for c in chunks]).astype("float32")
        faiss.normalize_L2(vectors)  # cosine similarity
        self.index.add(vectors)  # type: ignore[call-arg]
        self.items: list[EmbeddedChunk] = chunks

    def search(
        self, query_vector: list[float], k: int = 5, threshold=0.3
    ) -> list[ScoredChunk]:
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
