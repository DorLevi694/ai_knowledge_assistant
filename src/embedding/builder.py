# embedding\builder.py
import logging
import os
from typing import List, TypedDict

os.environ["TQDM_DISABLE"] = "1"  # Suppress tqdm progress bars

from normalize.chunker import Chunk
from sentence_transformers import SentenceTransformer


class EmbeddedChunk(TypedDict):
    source: str
    index: int
    text: str
    vector: List[float]


class EmbeddingBuilder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logging.getLogger("transformers").setLevel(logging.ERROR)
        self.model = SentenceTransformer(model_name)

    def build_vectors(self, chunks: List[Chunk]) -> List[EmbeddedChunk]:
        result_list: List[EmbeddedChunk] = []

        texts = [chunk["text"] for chunk in chunks]
        vectors = self.model.encode(texts, show_progress_bar=False)

        for chunk, vector in zip(chunks, vectors):
            cur_vector: EmbeddedChunk = {
                "source": chunk["source"],
                "index": chunk["index"],
                "text": chunk["text"],
                "vector": vector.tolist(),
            }
            result_list.append(cur_vector)
        return result_list
