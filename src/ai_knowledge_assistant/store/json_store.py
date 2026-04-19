# src/ai_knowledge_assistant/store/json_store.py file
from ai_knowledge_assistant.normalize import Chunk

from .base import load_from_json, save_to_json


def save_chunks(chunks: list[Chunk], path: str) -> None:
    """Serializes a list of Chunk dataclasses to a JSON file."""
    save_to_json(chunks, path, label="chunks")


def load_chunks(path: str) -> list[Chunk]:
    """Loads chunks from a JSON file and converts them back into Chunk dataclass
    instances."""
    return load_from_json(path, Chunk, label="chunks")
