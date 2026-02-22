# src/ai_knowledge_assistant/llm/openai_client.py file

from typing import Optional

from openai import OpenAI

from ai_knowledge_assistant.llm.base import LLMClient, LLMConfig


class OpenAIClient(LLMClient):

    def __init__(self, api_key: Optional[str] = None, default_model: str = "gpt-5.2"):

        self._client = OpenAI(api_key=api_key)
        self._default_model: str = default_model

    def generate(self, prompt: str, *, config: Optional[LLMConfig]) -> str:

        cfg = config or LLMConfig(model=self._default_model)

        if not cfg.model:
            raise ValueError("model must be provided")

        if not (0.0 <= cfg.temperature <= 2.0):
            raise ValueError("temperature must be between 0.0 and 2.0")

        if cfg.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be > 0")

        response = self._client.responses.create(
            model=cfg.model,
            input=prompt,
            temperature=cfg.temperature,
            max_output_tokens=cfg.max_output_tokens,
        )

        text = (response.output_text or "").strip()
        if not text:
            raise RuntimeError("Empty response from OpenAI")

        return text
