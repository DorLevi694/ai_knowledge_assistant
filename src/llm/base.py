# src/llm/base.py
from dataclasses import dataclass
from typing import Optional


class LLMClient:
    def generate(self, prompt: str, *, config: Optional[LLMConfig]) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class LLMConfig:
    model: str
    max_output_tokens: int = 600
    temperature: float = 0.2
