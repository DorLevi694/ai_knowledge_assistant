# src/grounding/output_validator.py
from typing import List

from normalize.chunker import Chunk
import re
import os


class OutputValidator:

    pattern = r"\[Source:\s*(.*?),\s*chunk\s*(\d+)\]"

    def validate(self, answer: str, contexts: List[Chunk]) -> bool:

        matches = re.findall(self.pattern, answer)
        matches_set: set = set(matches)

        if not matches_set:
            return False

        contexts_set: set = set(
            [
                (os.path.basename(context["source"]), str(context["index"]))
                for context in contexts
            ]
        )

        return matches_set.issubset(contexts_set)

