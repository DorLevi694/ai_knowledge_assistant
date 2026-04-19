from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from .base import EmbeddedChunk, EmbeddingConfig

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

    from ai_knowledge_assistant.normalize.base import Chunk


def _load_sentence_transformer() -> type[SentenceTransformer]:
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer


class EmbeddingBuilder:
    """
    Handles the transformation of text chunks into vector representations.
    Uses Lazy Loading to avoid unnecessary memory overhead during import.
    """

    def __init__(self, config: EmbeddingConfig):
        self._config = config
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        """
        Lazy loads the transformer model only when first accessed.
        Disables progress bars and reduces logging noise during loading.
        """
        if self._model is None:
            os.environ["TQDM_DISABLE"] = "1"
            logging.getLogger("transformers").setLevel(logging.ERROR)
            sentence_transformer_cls: type[SentenceTransformer] = (
                _load_sentence_transformer()
            )
            self._model = sentence_transformer_cls(self._config.model_name)
        assert self._model is not None
        return self._model

    def build_vectors(self, chunks: list[Chunk]) -> list[EmbeddedChunk]:
        """Encodes multiple text chunks into a list of EmbeddedChunk objects."""
        result_list: list[EmbeddedChunk] = []
        texts = [chunk.text for chunk in chunks]

        # Accessing self.model triggers the lazy loading
        vectors = self.model.encode(texts, show_progress_bar=False)

        for chunk, vector in zip(chunks, vectors, strict=True):
            cur_vector: EmbeddedChunk = EmbeddedChunk(
                source=chunk.source,
                index=chunk.index,
                text=chunk.text,
                vector=vector.tolist(),
            )
            result_list.append(cur_vector)
        return result_list

    def encode_query(self, query: str) -> list[float]:
        """Encodes a single query string for retrieval."""
        return self.model.encode(query, show_progress_bar=False).tolist()
