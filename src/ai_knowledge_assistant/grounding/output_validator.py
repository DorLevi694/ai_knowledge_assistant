# src/ai_knowledge_assistant/grounding/output_validator.py
from typing import List
import re
import os

from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.config import CITATION_PATTERN


class OutputValidator:

    def __init__(self, pattern: str = CITATION_PATTERN):
        self._pattern = pattern

    def validate(self, answer: str, contexts: List[Chunk]) -> bool:
        """
        Verifies that every source cited in the answer actually exists
        in the provided context chunks.
        """
        matches = re.findall(self._pattern, answer)
        matches_set: set = set(matches)

        if not matches_set:
            return False

        # Build a set of valid (filename, index) pairs from retrieved contexts
        contexts_set: set = set(
            [
                (os.path.basename(context.source), str(context.index))
                for context in contexts
            ]
        )

        return matches_set.issubset(contexts_set)
