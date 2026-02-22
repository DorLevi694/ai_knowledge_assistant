# src\ai_knowledge_assistant\retrieve\retriever.py file

from typing import List, Optional
import logging

from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.embedding.builder import EmbeddedChunk, EmbeddingBuilder
from ai_knowledge_assistant.store.faiss_store import FaissStore, ScoredChunk
from ai_knowledge_assistant.store.vector_store import load_chunks_vectors
from ai_knowledge_assistant.config import DEFAULT_EMBEDDING, DEFAULT_RETRIEVAL_LIMIT

logger = logging.getLogger(__name__)

# Global instances initialized as None to prevent import-time side effects
_embedding_builder: Optional[EmbeddingBuilder] = None
_faiss_store: Optional[FaissStore] = None


def get_embedding_builder() -> EmbeddingBuilder:
    """Singleton-like accessor for the EmbeddingBuilder."""
    global _embedding_builder
    if not _embedding_builder:
        _embedding_builder = EmbeddingBuilder(DEFAULT_EMBEDDING)
    return _embedding_builder


def get_faiss_store() -> FaissStore:
    """Singleton-like accessor for the FaissStore."""
    global _faiss_store
    if not _faiss_store:
        # Data loading and index building happens only when retrieval is requested
        vectors_chunks: List[EmbeddedChunk] = load_chunks_vectors()
        _faiss_store = FaissStore(dim=DEFAULT_EMBEDDING.dimension)
        _faiss_store.build(vectors_chunks)

    return _faiss_store


def retrieve(question: str, limit: int = DEFAULT_RETRIEVAL_LIMIT) -> List[Chunk]:
    """
    Main retrieval logic. Fetches relevant context chunks for the RAG pipeline.
    """
    faiss_store: FaissStore = get_faiss_store()
    embedding_builder: EmbeddingBuilder = get_embedding_builder()

    question_vector = embedding_builder.encode_query(question)

    final_chunks: List[Chunk] = []
    results: List[ScoredChunk] = faiss_store.search(question_vector, limit)

    # Convert ScoredChunk to Chunk while maintaining type safety
    for res in results:
        final_chunks.append(
            Chunk(
                source=res.source,
                index=res.index,
                text=res.text,
            )
        )

    return final_chunks
