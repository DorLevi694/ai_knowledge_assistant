# retrieve/naive.py
from typing import List
from normalize.chunker import Chunk

def naive_search(query: str, chunks: List[Chunk], limit: int = 5) -> List[Chunk]:
    query_lower = query.lower()
    results: List[Chunk] = []

    for chunk in chunks:
        if query_lower in chunk["text"].lower():
            results.append(chunk)
            if len(results) >= limit:
                break

    return results
