# src/ai_knowledge_assistant/rag/prompt_builder.py file

import os

from ai_knowledge_assistant.config import PROMPT_SYSTEM_INSTRUCTIONS
from ai_knowledge_assistant.normalize.chunker import Chunk


def build_prompt(question: str, contexts: list[Chunk]) -> str:

    prompt_list: list[str] = []

    if contexts:
        # Instruction Layer
        prompt_list.append(PROMPT_SYSTEM_INSTRUCTIONS)
        prompt_list.append("--- CONTEXT ---\n\n")

        # Context Layer
        for context in contexts:
            filename = os.path.basename(context.source)

            # Ensure the structure here matches the CITATION_PATTERN in config
            context_str = (
                f"[Source: {filename}, chunk {context.index}]\n{context.text}\n\n"
            )
            prompt_list.append(context_str)

    prompt_list.append(f"--- QUESTION ---\n\n{question}")
    prompt_str = "".join(prompt_list)

    return prompt_str
