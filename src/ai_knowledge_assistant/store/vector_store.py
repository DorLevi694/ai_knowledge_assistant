# src/ai_knowledge_assistant/store/vector_store.py file
from ai_knowledge_assistant.embedding import EmbeddedChunk

from .base import load_from_json, save_to_json


def save_chunks_vectors(chunks: list[EmbeddedChunk], path: str) -> None:
    """Serializes a list of EmbeddedChunk dataclasses to a JSON file."""
    save_to_json(chunks, path, label="vectors")


def load_chunks_vectors(path: str) -> list[EmbeddedChunk]:
    """Loads vector chunks from JSON and deserializes them into EmbeddedChunk instances."""
    return load_from_json(path, EmbeddedChunk, label="vectors")
