# src/ai_knowledge_assistant/grounding/answerability.py


from ai_knowledge_assistant.config import MIN_TOTAL_CHARS
from ai_knowledge_assistant.normalize.chunker import Chunk


class AnswerabilityGate:

    def __init__(self, min_chars: int = MIN_TOTAL_CHARS):
        self._min_chars = min_chars

    def should_answer(self, context_chunks: list[Chunk]) -> bool:
        """
        Determines if the provided context is substantial enough to
        generate a grounded answer.
        """
        if len(context_chunks) < 1:
            return False

        text_length = sum(len(c.text) for c in context_chunks)

        total_chars_res = text_length > self._min_chars
        return total_chars_res
