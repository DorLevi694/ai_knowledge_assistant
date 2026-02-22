# src/ai_knowledge_assistant/store/json_store.py file
import os
import json
import logging
from typing import List
from dataclasses import asdict
from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.config import INDEX_FILE  

logger = logging.getLogger(__name__)

def save_chunks(chunks: List[Chunk], path: str = INDEX_FILE) -> None:
    """
    Serializes a list of Chunk dataclasses to a JSON file.
    Converts dataclasses to dictionaries for JSON compatibility.
    """
    try:
        chunks_as_dicts = [asdict(chunk) for chunk in chunks]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunks_as_dicts, f, ensure_ascii=False, indent=2)
        logger.info("Successfully saved %d chunks to %s", len(chunks), path)
    except Exception as e:
        logger.error("Failed to save chunks to %s: %s", path, e)
        raise

def load_chunks(path: str = INDEX_FILE) -> List[Chunk]:
    """
    Loads chunks from a JSON file and converts them back into Chunk dataclass instances.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Deserialization: Converting dicts back to Dataclass instances
        return [Chunk(**item) for item in data]
    
    except FileNotFoundError:
        logger.warning("Index file not found at %s. Returning empty list.", path)
        return []
    except Exception as e:
        logger.error("Failed to load chunks from %s: %s", path, e)
        return []
