# src\ai_knowledge_assistant\retrieve\naive.py file
from typing import List
from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.config import DEFAULT_RETRIEVAL_LIMIT


def naive_search(
    query: str, chunks: List[Chunk], limit: int = DEFAULT_RETRIEVAL_LIMIT
) -> List[Chunk]:
    query_lower = query.lower()
    results: List[Chunk] = []

    for chunk in chunks:
        if query_lower in chunk.text.lower():
            results.append(chunk)
            if len(results) >= limit:
                break

    return results
