# src/ai_knowledge_assistant/grounding/output_validator.py
import os
import re

from ai_knowledge_assistant.config import CITATION_PATTERN
from ai_knowledge_assistant.normalize.chunker import Chunk


class OutputValidator:
    def __init__(self, pattern: str = CITATION_PATTERN):
        self._pattern = pattern
        self._citation_fragment_pattern = r"Source:\s*([^,\];]+),\s*chunk\s*(\d+)"

    def validate(self, answer: str, contexts: list[Chunk]) -> bool:
        """
        Verifies that every source cited in the answer actually exists
        in the provided context chunks.
        """
        matches = re.findall(self._citation_fragment_pattern, answer)
        matches_set: set[tuple[str, str]] = set(matches)

        if not matches_set:
            return False

        # Build a set of valid (filename, index) pairs from retrieved contexts
        contexts_set: set[tuple[str, str]] = set(
            [
                (os.path.basename(context.source), str(context.index))
                for context in contexts
            ]
        )

        return matches_set.issubset(contexts_set)
