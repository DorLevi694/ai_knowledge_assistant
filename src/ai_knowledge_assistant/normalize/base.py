# src/ai_knowledge_assistant/normalize/base.py file
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """A segment of text from a source file with its sequence index."""

    source: str
    index: int
    text: str
