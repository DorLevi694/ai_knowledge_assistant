# src\ai_knowledge_assistant\normalize\chunker.py file
import logging
from typing import List, Dict

from ai_knowledge_assistant.normalize.base import Chunk
from ai_knowledge_assistant.config import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


def get_chunks_from_files(text_by_file: Dict[str, str]) -> List[Chunk]:

    results: List[Chunk] = []
    for file_name, text in text_by_file.items():
        one_file_results: List[Chunk] = split_into_chunks(file_name, text)
        results.extend(one_file_results)
    for chunk in results:
        logger.debug("Chunk: %s", chunk)
    return results


def split_into_chunks(file_name: str, text: str) -> List[Chunk]:
    """
    Splits a single string into overlapping segments based on config values.
    Returns a list of Chunk dataclasses.
    """
    chunks: List[Chunk] = []

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
