from ai_knowledge_assistant.normalize.chunker import split_into_chunks


def test_split_into_chunks_basic(monkeypatch):
    # Mock config in the module directly
    monkeypatch.setattr("ai_knowledge_assistant.normalize.chunker.CHUNK_SIZE", 10)
    monkeypatch.setattr("ai_knowledge_assistant.normalize.chunker.CHUNK_OVERLAP", 2)

    text = "0123456789ABCDEF"
    # Step = 10 - 2 = 8
    # Chunk 0: text[0:10] -> "0123456789"
    # Chunk 1: text[8:18] -> "89ABCDEF"

    chunks = split_into_chunks("test.txt", text)

    assert len(chunks) == 2
    assert chunks[0].text == "0123456789"
    assert chunks[1].text == "89ABCDEF"
    assert chunks[0].index == 0
    assert chunks[1].index == 1
    assert chunks[0].source == "test.txt"
    assert chunks[1].source == "test.txt"


def test_split_into_chunks_small_text(monkeypatch):
    monkeypatch.setattr("ai_knowledge_assistant.normalize.chunker.CHUNK_SIZE", 100)
    monkeypatch.setattr("ai_knowledge_assistant.normalize.chunker.CHUNK_OVERLAP", 10)
    text = "small"

    chunks = split_into_chunks("small.txt", text)
    assert len(chunks) == 1
    assert chunks[0].text == "small"
    assert chunks[0].source == "small.txt"
    assert chunks[0].index == 0
