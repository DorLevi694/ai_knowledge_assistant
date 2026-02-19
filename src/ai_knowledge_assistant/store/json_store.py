# json_store.py file
import os
import json
from typing import List
from ai_knowledge_assistant.normalize.chunker import Chunk

INDEX_FILE = os.path.join("data_set", "output", "index.json")


def save_chunks(chunks: List[Chunk], path: str = INDEX_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def load_chunks(path: str = INDEX_FILE) -> List[Chunk]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
