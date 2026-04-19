"""Base types and shared persistence utilities for the store layer.

Provides:
- :func:`save_to_json` – serialize a list of dataclasses to a JSON file.
- :func:`load_from_json` – deserialize a JSON file back into typed dataclass
  instances.
- :class:`ScoredChunk` – immutable dataclass representing a retrieved chunk
  together with its similarity score.
"""

# ai_knowledge_assistant\store\base.py
import json
import logging
from dataclasses import asdict, dataclass

logger = logging.getLogger(__name__)


def save_to_json[T](items: list[T], path: str, label: str = "items") -> None:
    """Serializes a list of dataclasses to a JSON file."""
    try:
        items_as_dicts = [asdict(item) for item in items]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items_as_dicts, f, ensure_ascii=False, indent=2)
        logger.info("Successfully saved %d %s to %s", len(items), label, path)
    except Exception as e:
        logger.error("Failed to save %s to %s: %s", label, path, e)
        raise


def load_from_json[T](path: str, cls: type[T], label: str = "items") -> list[T]:
    """Loads JSON from a file and deserializes each entry into instances of cls."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return [cls(**item) for item in data]
    except FileNotFoundError:
        logger.warning(
            "%s file not found at %s. Returning empty list.",
            label.capitalize(),
            path,
        )
        return []
    except Exception as e:
        logger.error("Failed to load %s from %s: %s", label, path, e)
        raise


@dataclass(frozen=True)
class ScoredChunk:
    """A document chunk annotated with a retrieval similarity score.

    Attributes:
        source: The file name or path the chunk was extracted from.
        index: Zero-based position of this chunk within its source document.
        text: The raw text content of the chunk.
        score: Cosine-similarity score (0-1) assigned by the vector store.
        vector: Optional embedding vector; may be ``None`` when not needed.
    """

    source: str
    index: int
    text: str
    score: float
    vector: list[float] | None = None
