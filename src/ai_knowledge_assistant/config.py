"""
Central configuration module for the AI Knowledge Assistant.

Defines application-wide constants covering embedding models, LLM settings,
retrieval/chunking parameters, grounding thresholds, and file-store paths.
All tuneable values should be changed here rather than inline throughout the
codebase.
"""

import os

from ai_knowledge_assistant.embedding import EmbeddingConfig

# --- Embedding ---
# Dictionary of supported models and their dimensions
SUPPORTED_EMBEDDING_MODELS: dict[str, int] = {
    "all-MiniLM-L6-v2": 384,
    "all-mpnet-base-v2": 768,
    # "paraphrase-multilingual-MiniLM-L12-v2": 384,
}


DEFAULT_EMBEDDING = EmbeddingConfig(
    # model_name="paraphrase-multilingual-MiniLM-L12-v2",
    model_name="all-MiniLM-L6-v2",
    dimension=384,
)
DEFAULT_EMBEDDING.validate_with_knowledge(SUPPORTED_EMBEDDING_MODELS)


# --- Grounding & Answerability ---
MIN_TOTAL_CHARS = 800
CITATION_PATTERN = r"\[Source:\s*(.*?),\s*chunk\s*(\d+)\]"


# --- Prompting & Logic ---
INSUFFICIENT_CONTEXT_RESPONSE = "INSUFFICIENT_CONTEXT"

# --- LLM ---
DEFAULT_LLM_MODEL = "gpt-4.1"

# The visual example for the LLM must match CITATION_PATTERN
CITATION_FORMAT_EXAMPLE = "[Source: <filename>, chunk <index>]"

PROMPT_SYSTEM_INSTRUCTIONS = (
    "You are an AI assistant answering questions based strictly on provided "
    "context.\n\n"
    "You must follow these rules:\n"
    "1. Use ONLY the provided context.\n"
    "2. Do NOT use prior knowledge.\n"
    "3. For every factual statement, cite the source in this exact format: "
    f"{CITATION_FORMAT_EXAMPLE}\n"
    "   Use one separate bracket per source. Never combine multiple sources "
    "in a single bracket (e.g. do NOT use semicolons inside brackets).\n"
    "4. If the answer cannot be found in the context, respond exactly: "
    f"{INSUFFICIENT_CONTEXT_RESPONSE}\n\n"
)

# --- Retrieval & Chunking ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MIN_SIMILARITY_THRESHOLD = 0.2

# --- Ingest ---
SUPPORTED_EXTENSIONS = [
    "txt",
    "md",
]

# Store
INDEX_FILE = os.path.join("data_set", "output", "index.json")
VECTORS_FILE = os.path.join("data_set", "output", "vectors.json")
