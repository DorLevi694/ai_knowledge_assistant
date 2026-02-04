# file: faiss_store.py

import faiss
import numpy as np
from typing import List
from embedding.builder import EmbeddedChunk


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # Inner Product (cosine-ready)
        self.items: List[EmbeddedChunk] = []

    def build(self, chunks: List[EmbeddedChunk]) -> None:
        vectors = np.array([c["vector"] for c in chunks]).astype("float32")
        faiss.normalize_L2(vectors)  # cosine similarity
        self.index.add(vectors)
        self.items = chunks

    def search(self, query_vector: List[float], k: int = 5) -> List[EmbeddedChunk]:
        q = np.array([query_vector]).astype("float32")
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, k)
        return [self.items[i] for i in indices[0] if i != -1]
