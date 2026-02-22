# src/ai_knowledge_assistant/embedding/base.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class EmbeddingConfig:
    model_name: str
    dimension: int
    def validate_with_knowledge(self, supported_models: Dict[str, int]) -> None:
        """Validates the config against the system's global SSOT mapping."""
        if self.model_name not in supported_models:
            raise ValueError(
                f"Unsupported model: '{self.model_name}'. "
                f"Supported models are: {list(supported_models.keys())}"
            )
        
        expected = supported_models[self.model_name]
        if self.dimension != expected:
            raise ValueError(
                f"Dimension mismatch for {self.model_name}: "
                f"expected {expected}, got {self.dimension}"
            )

@dataclass(frozen=True)
class EmbeddedChunk:
    """The outcome of an embedding process."""
    source: str
    index: int
    text: str
    vector: List[float]