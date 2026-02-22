# ai_knowledge_assistant\store\base.py
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScoredChunk:
    
    source: str
    index: int
    text: str
    vector: List[float]
    score: float
