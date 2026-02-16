# retrieve/retriever.py
from typing import List, TypedDict
from normalize.chunker import Chunk
from embedding.builder import EmbeddedChunk, EmbeddingBuilder

from store.faiss_store import FaissStore, ScoredChunk
from store.vector_store import load_chunks_vectors
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

embedding_builder = EmbeddingBuilder()
_faiss_store = None


def get_faiss_store() -> FaissStore:
    global _faiss_store
    if not _faiss_store:
        vectors_chunks: List[EmbeddedChunk] = load_chunks_vectors()
        _faiss_store = FaissStore(dim=384)
        _faiss_store.build(vectors_chunks)

    return _faiss_store


def retrieve(question: str, limit: int = 5) -> List[Chunk]:
    """
    Returns context chunks ready for RAG
    """
    faiss_store = get_faiss_store()

    question_v = embedding_builder.model.encode(question, show_progress_bar=False).tolist()
    fin: List[Chunk] = []
    results: List[ScoredChunk] = faiss_store.search(question_v, limit)
    for res in results:
        fin.append(
            {"source": res["source"], "index": res["index"], "text": res["text"]}
        )

        logger.debug(f"{type(results[0])} - {results[0].keys()}")
    return fin
