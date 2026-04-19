"""Text chunking utilities for splitting documents into overlapping segments.

This module provides:
- ``get_chunks_from_files`` – batch-splits a dict of file contents into
  :class:`~normalize.base.Chunk` objects.
- ``split_into_chunks`` – splits a single document string into overlapping
  fixed-size chunks using the ``CHUNK_SIZE`` and ``CHUNK_OVERLAP`` settings
  defined in :mod:`config`.
"""

# src\ai_knowledge_assistant\normalize\chunker.py file
import logging

from ai_knowledge_assistant.config import CHUNK_OVERLAP, CHUNK_SIZE

from .base import Chunk

logger = logging.getLogger(__name__)


def get_chunks_from_files(text_by_file: dict[str, str]) -> list[Chunk]:
    """Chunk all files in the provided mapping.

    Iterates over each (filename, text) pair, delegates chunking to
    :func:`split_into_chunks`, and concatenates the results into a single
    flat list.

    Args:
        text_by_file: A dict mapping file names (or paths) to their raw text
            content.

    Returns:
        A flat list of :class:`~normalize.base.Chunk` objects ordered by
        file then by chunk index.
    """

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
