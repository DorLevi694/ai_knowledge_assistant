# src/llm/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LLMConfig:
    model: str
    max_output_tokens: int = 600
    temperature: float = 0.2


class LLMClient:
    def generate(self, prompt: str, *, config: Optional[LLMConfig] = None) -> str:
        raise NotImplementedError
