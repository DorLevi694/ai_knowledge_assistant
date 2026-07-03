from ai_knowledge_assistant.config import PROMPT_SYSTEM_INSTRUCTIONS
from ai_knowledge_assistant.normalize.chunker import Chunk
from ai_knowledge_assistant.rag.prompt_builder import build_prompt


def test_build_prompt_with_context():
    question = "How to cook?"
    contexts = [
        Chunk(source="recipe.txt", index=0, text="Boil water."),
        Chunk(source="recipe.txt", index=1, text="Add pasta."),
    ]

    prompt = build_prompt(question, contexts)

    assert "How to cook?" in prompt
    assert "Boil water." in prompt
    assert "Add pasta." in prompt
    assert "[Source: recipe.txt, chunk 0]" in prompt
    assert "[Source: recipe.txt, chunk 1]" in prompt
    assert "--- CONTEXT ---" in prompt
    assert PROMPT_SYSTEM_INSTRUCTIONS in prompt


def test_build_prompt_no_context():
    question = "Who are you?"
    prompt = build_prompt(question, [])

    assert "Who are you?" in prompt
    assert "--- CONTEXT ---" not in prompt
