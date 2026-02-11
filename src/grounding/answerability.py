# src/grounding/answerability.py

from typing import List

from normalize.chunker import Chunk


class AnswerabilityGate:
    MIN_TOTAL_CHARS = 800

    def should_answer(self, context_chunks: List[Chunk]) -> bool:
        if len(context_chunks) < 1:
            return False

        text_length = sum(len(c["text"]) for c in context_chunks)

        total_chars_res = text_length > self.MIN_TOTAL_CHARS
        return total_chars_res
