# src\ai_knowledge_assistant\normalize\chunker.py file
import logging

from ai_knowledge_assistant.config import CHUNK_OVERLAP, CHUNK_SIZE
from ai_knowledge_assistant.normalize.base import Chunk

logger = logging.getLogger(__name__)


def get_chunks_from_files(text_by_file: dict[str, str]) -> list[Chunk]:

    results: list[Chunk] = []
    for file_name, text in text_by_file.items():
        one_file_results: list[Chunk] = split_into_chunks(file_name, text)
        results.extend(one_file_results)
    for chunk in results:
        logger.debug("Chunk: %s", chunk)
    return results


def split_into_chunks(file_name: str, text: str) -> list[Chunk]:
    """
    Splits a single string into overlapping segments based on config values.
    Returns a list of Chunk dataclasses.
    """
    chunks: list[Chunk] = []

    # Calculate step size to ensure overlap
    step = CHUNK_SIZE - CHUNK_OVERLAP

    chunks = [
        Chunk(
            source=file_name,
            index=index,
            text=text[place : place + CHUNK_SIZE],
        )
        for index, place in enumerate(range(0, len(text), step))
    ]
    return chunks
