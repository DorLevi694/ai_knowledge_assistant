# ai_knowledge_assistant\store\base.py
from dataclasses import dataclass


@dataclass(frozen=True)
class ScoredChunk:

    source: str
    index: int
    text: str
    vector: list[float]
    score: float
