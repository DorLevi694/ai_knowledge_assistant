# file: faiss_store.py

import faiss
import numpy as np
from typing import List, TypedDict
from ai_knowledge_assistant.embedding.builder import EmbeddedChunk
import json
import logging

logger = logging.getLogger(__name__)


class ScoredChunk(TypedDict):
    source: str
    index: int
    text: str
    vector: List[float]
    score: float


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # Inner Product (cosine-ready)
        self.items: List[EmbeddedChunk] = []

    def build(self, chunks: List[EmbeddedChunk]) -> None:
        vectors = np.array([c["vector"] for c in chunks]).astype("float32")
        faiss.normalize_L2(vectors)  # cosine similarity
        self.index.add(vectors)  # type: ignore[call-arg]
        self.items: List[EmbeddedChunk] = chunks

    def search(
        self, query_vector: List[float], k: int = 5, threshold=0.3
    ) -> List[ScoredChunk]:
        results: List[ScoredChunk] = []
        q = np.array([query_vector]).astype("float32")
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, k)  # type: ignore[call-arg]
        for score, indic in zip(scores[0], indices[0]):

            if indic == -1:
                continue
            if score < threshold:
                continue

            results.append(
                {
                    "source": self.items[indic]["source"],
                    "index": self.items[indic]["index"],
                    "text": self.items[indic]["text"],
                    "vector": self.items[indic]["vector"],
                    "score": float(score),
                }
            )

        logger.debug(json.dumps(results, indent=2, ensure_ascii=False))
        return results
