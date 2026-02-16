# vector_store.py
import os
import json
from typing import List
from embedding.builder import EmbeddedChunk

VECTORS_FILE = os.path.join("data_set", "output", "vectors.json")


def save_chunks_vectors(chunks: List[EmbeddedChunk], path: str = VECTORS_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def load_chunks_vectors(path: str = VECTORS_FILE) -> List[EmbeddedChunk]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
