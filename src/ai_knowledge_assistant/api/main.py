import logging
import os

from fastapi import FastAPI, UploadFile

import ai_knowledge_assistant.config as config
from ai_knowledge_assistant.embedding import EmbeddedChunk, EmbeddingBuilder
from ai_knowledge_assistant.normalize import Chunk, get_chunks_from_files
from ai_knowledge_assistant.store import save_chunks, save_chunks_vectors

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest_document(files: list[UploadFile]):

    text_by_file: dict[str, str] = {
        f.filename: f.file.read().decode("utf-8") for f in files if f.filename
    }
    chunks: list[Chunk] = get_chunks_from_files(text_by_file)

    os.makedirs(os.path.dirname(config.INDEX_FILE), exist_ok=True)
    save_chunks(chunks, path=config.INDEX_FILE)
    logger.info("Saved %d chunks to index.", len(chunks))

    embedding_builder: EmbeddingBuilder = EmbeddingBuilder(
        config=config.DEFAULT_EMBEDDING
    )
    chunks_vectors: list[EmbeddedChunk] = embedding_builder.build_vectors(chunks)

    save_chunks_vectors(chunks_vectors, path=config.VECTORS_FILE)
    logger.info("Saved %d vectors.", len(chunks_vectors))

    return "Good"
