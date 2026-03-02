# src/ai_knowledge_assistant/store/json_store.py file
import json
import logging
from dataclasses import asdict

from ai_knowledge_assistant.normalize import Chunk

logger = logging.getLogger(__name__)


def save_chunks(chunks: list[Chunk], path: str) -> None:
    """
    Serializes a list of Chunk dataclasses to a JSON file.
    Converts dataclasses to dictionaries for JSON compatibility.
    """
    try:
        chunks_as_dicts = [asdict(chunk) for chunk in chunks]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunks_as_dicts, f, ensure_ascii=False, indent=2)
        logger.info("Successfully saved %d chunks to %s", len(chunks), path)
    except Exception as e:
        logger.error("Failed to save chunks to %s: %s", path, e)
        raise


def load_chunks(path: str) -> list[Chunk]:
    """
    Loads chunks from a JSON file and converts them back into Chunk dataclass instances.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        # Deserialization: Converting dicts back to Dataclass instances
        return [Chunk(**item) for item in data]

    except FileNotFoundError:
        logger.warning("Index file not found at %s. Returning empty list.", path)
        return []
    except Exception as e:
        logger.error("Failed to load chunks from %s: %s", path, e)
        raise
