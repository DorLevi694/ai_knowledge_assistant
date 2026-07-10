import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

import ai_knowledge_assistant.config as config
from ai_knowledge_assistant.embedding import EmbeddedChunk, EmbeddingBuilder
from ai_knowledge_assistant.normalize import Chunk, get_chunks_from_files
from ai_knowledge_assistant.store import save_chunks, save_chunks_vectors

from .schemas import (
    FileInProcess,
    IngestResponseBase,
    ReadFileReasonFailed,
    ReadFileStatus,
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def health():
    """Liveness probe: no dependencies, returns 200 whenever the process serves HTTP."""
    return {"status": "ok"}


def _read_files(files: list[UploadFile]) -> dict[str, FileInProcess]:
    """Validate and decode uploaded files into per-file ingest results.

    Each file passes three gates: filename present, supported extension,
    UTF-8 decodable. Failures are recorded per file, never raised.
    """
    results: dict[str, FileInProcess] = dict()
    for i, f in enumerate(files):
        try:
            failure_reason: ReadFileReasonFailed | None = None
            filename = f.filename or ""
            text: None | str = None
            if not filename:
                filename = f"file number {i}"
                failure_reason = ReadFileReasonFailed.MISSING_FILENAME

            elif (
                Path(filename).suffix.lstrip(".").lower()
                not in config.SUPPORTED_EXTENSIONS
            ):
                failure_reason = ReadFileReasonFailed.UNSUPPORTED_FILE
            else:
                text = f.file.read().decode("utf-8")
                if text == "":
                    failure_reason = ReadFileReasonFailed.EMPTY_FILE

        except UnicodeDecodeError:
            failure_reason = ReadFileReasonFailed.DECODE_FAILED

        except Exception:
            logger.exception("Unexpected error while reading file %r", f.filename)
            failure_reason = ReadFileReasonFailed.UNKNOWN_ISSUE

        results[filename] = FileInProcess(
            filename=filename,
            status=ReadFileStatus.FAILED if failure_reason else ReadFileStatus.SUCCESS,
            failure_reason=failure_reason,
            text=text,
        )

    return results


@app.post("/ingest", status_code=201)
def ingest_document(files: list[UploadFile]) -> IngestResponseBase:
    """Ingest text documents into the knowledge base.

    Note: the JSON store overwrites on save, so each request replaces the
    entire index (CLI batch semantics). Incremental ingestion arrives with
    the DB-backed store (S2/S3).
    """

    text_by_file_dict: dict[str, FileInProcess] = _read_files(files)

    texts: dict[str, str] = {
        filename: file_in_process.text
        for filename, file_in_process in text_by_file_dict.items()
        if file_in_process.status is ReadFileStatus.SUCCESS
        and file_in_process.text is not None
    }

    if not texts:
        raise HTTPException(
            status_code=400,
            detail=[
                file_in_process.model_dump(mode="json", exclude={"text"})
                for file_in_process in text_by_file_dict.values()
            ],
        )

    chunks: list[Chunk] = get_chunks_from_files(texts)

    os.makedirs(os.path.dirname(config.INDEX_FILE), exist_ok=True)
    save_chunks(chunks, path=config.INDEX_FILE)
    logger.info("Saved %d chunks to index.", len(chunks))

    embedding_builder: EmbeddingBuilder = EmbeddingBuilder(
        config=config.DEFAULT_EMBEDDING
    )
    chunks_vectors: list[EmbeddedChunk] = embedding_builder.build_vectors(chunks)

    save_chunks_vectors(chunks_vectors, path=config.VECTORS_FILE)
    logger.info("Saved %d vectors.", len(chunks_vectors))

    return IngestResponseBase(files=text_by_file_dict)
