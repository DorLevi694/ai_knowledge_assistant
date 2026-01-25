# chunker.py file
import logging
from typing import List, Dict, TypedDict

logger = logging.getLogger(__name__)
chunk_size = 500
overlap_size = 100


class Chunk(TypedDict):
    source: str
    index: int
    text: str


def get_chunks_from_files(text_by_file: Dict[str, str]) -> List[Chunk]:

    results: List[Chunk] = []
    for file_name, text in text_by_file.items():
        one_file_results: List[Chunk] = split_into_chunks(file_name, text)
        results.extend(one_file_results)
    for chunk in results:
        logger.debug("Chunk: %s", chunk)
    return results


def split_into_chunks(file_name: str, text: str) -> List[Chunk]:
    overlap_size
    chunks: List[Chunk] = [
        {
            "source": file_name,
            "index": index,
            "text": text[place : place + chunk_size],
        }
        for index, place in enumerate(range(0, len(text), (chunk_size - overlap_size)))
    ]
    return chunks
