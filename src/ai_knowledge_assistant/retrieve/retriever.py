# src/ai_knowledge_assistant/retrieve/retriever.py file

import logging

from ai_knowledge_assistant.embedding.base import EmbeddingConfig
from ai_knowledge_assistant.embedding.builder import EmbeddedChunk, EmbeddingBuilder
from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.store.faiss_store import FaissStore, ScoredChunk
from ai_knowledge_assistant.store.vector_store import load_chunks_vectors

logger = logging.getLogger(__name__)


class Retriever:
    """
    Encapsulates the retrieval pipeline: loads vectors, builds a FAISS index,
    and provides semantic search over embedded chunks.

    All dependencies (config, paths) are injected via the constructor.
    """

    def __init__(self, embedding_config: EmbeddingConfig, vectors_path: str) -> None:
        self._embedding_builder = EmbeddingBuilder(config=embedding_config)

        vectors_chunks: list[EmbeddedChunk] = load_chunks_vectors(path=vectors_path)
        if not vectors_chunks:
            raise FileNotFoundError(
                f"No vectors found at '{vectors_path}'. Run the 'index' command first."
            )

        self._faiss_store = FaissStore(dim=embedding_config.dimension)
        self._faiss_store.build(vectors_chunks)

    def retrieve(self, question: str, limit: int = 5) -> list[Chunk]:
        """
        Returns the most relevant context chunks for the given question.
        """
        question_vector = self._embedding_builder.encode_query(question)
        results: list[ScoredChunk] = self._faiss_store.search(question_vector, limit)

        return [
            Chunk(source=res.source, index=res.index, text=res.text) for res in results
        ]
