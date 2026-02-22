# src/ai_knowledge_assistant/store/vector_store.py file
import json
import logging
from dataclasses import asdict
from typing import List

from ai_knowledge_assistant.embedding.base import EmbeddedChunk

logger = logging.getLogger(__name__)


def save_chunks_vectors(chunks: List[EmbeddedChunk], path: str) -> None:
    """
    Serializes a list of EmbeddedChunk dataclasses to a JSON file.
    Converts dataclasses to dictionaries for JSON compatibility.
    """
    try:
        chunks_as_dicts = [asdict(chunk) for chunk in chunks]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunks_as_dicts, f, ensure_ascii=False, indent=2)
        logger.info("Successfully saved %d vectors to %s", len(chunks), path)
    except Exception as e:
        logger.error("Failed to save vectors to %s: %s", path, e)
        raise


def load_chunks_vectors(path: str) -> List[EmbeddedChunk]:
    """
    Loads vector chunks from JSON and deserializes them into EmbeddedChunk instances.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [EmbeddedChunk(**item) for item in data]

    except FileNotFoundError:
        logger.warning("Vectors file not found at %s. Returning empty list.", path)
        return []
    except Exception as e:
        logger.error("Failed to load vectors from %s: %s", path, e)
        return []
