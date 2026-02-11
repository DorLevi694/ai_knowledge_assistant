# src/rag/prompt_builder.py
from typing import List

from normalize.chunker import Chunk


def build_prompt(question: str, contexts: List[Chunk]) -> str:

    prompt_list: List[str] = []

    if contexts:
        prompt_prefix = (
            "You are an AI assistant answering questions based strictly on provided context.\n\n"
            "You must follow these rules:\n\n"
            "1. Use ONLY the provided context.\n"
            "2. Do NOT use prior knowledge.\n"
            "3. For every factual statement, cite the source in this format:\n"
            "   [Source: <filename>, chunk <index>]\n"
            "4. If the answer cannot be found in the context, respond exactly:\n"
            "   INSUFFICIENT_CONTEXT\n\n"
        )
        prompt_list.append(prompt_prefix)
        prompt_list.append("--- CONTEXT ---\n\n")

        for context in contexts:
            filename = context["source"].split("\\")[-1]
            context_str = (
                f"[Source: {filename}, chunk {context['index']}]\n{context['text']}\n\n"
            )
            prompt_list.append(context_str)

    prompt_list.append(f"--- QUESTION ---\n\n{question}")
    prompt_str = "".join(prompt_list)

    return prompt_str
