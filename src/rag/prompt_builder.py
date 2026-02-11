# rag/prompt_builder.py
from typing import List

from retrieve.retriver import ContextChunk


def build_prompt(question: str, contexts: List[ContextChunk]) -> str:

    prompt_list: List[str] = []
    if contexts:
        prompt_list.append("Contexts:")
        for context in contexts:
            context_str = f"source: {context['source']}, score: {context['score']}, text: {context['text']}"
            prompt_list.append(context_str)

    prompt_list.append(f"My Question: {question}")
    return "\n".join(prompt_list)
