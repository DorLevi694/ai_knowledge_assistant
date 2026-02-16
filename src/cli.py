# src/cli.py file
"""
AI Knowledge Assistant CLI

A command-line interface for indexing documents and answering questions
using semantic search and RAG (Retrieval-Augmented Generation).

Usage:
    python cli.py index <path1> [path2 ...]
    python cli.py ask "<question>" [--verbose]
    python cli.py --help
    python cli.py --version
"""

import sys
import logging
import os
from typing import Dict, List, Optional

from embedding.builder import EmbeddedChunk, EmbeddingBuilder
from grounding.answerability import AnswerabilityGate
from grounding.output_validator import OutputValidator
from ingest.reader import read_files
from llm.base import LLMConfig
from llm.openai_client import OpenAIClient
from normalize.chunker import Chunk, get_chunks_from_files
from retrieve.retriever import retrieve
from rag.prompt_builder import build_prompt
from store.json_store import save_chunks
from store.vector_store import save_chunks_vectors

__version__ = "0.1.0"

# Exit codes
EXIT_SUCCESS = 0
EXIT_USAGE_ERROR = 1
EXIT_RUNTIME_ERROR = 2
EXIT_NO_ANSWER = 3

# Configure logging for all modules
logging.basicConfig(
    level=logging.INFO, format="%(name)-20s | %(levelname)-8s: %(message)s"
)

logger = logging.getLogger(__name__)

# Global objects (singleton pattern)
_embedding_builder: Optional[EmbeddingBuilder] = None
_llm: Optional[OpenAIClient] = None
_answer_ability_gate: Optional[AnswerabilityGate] = None
_output_validator: Optional[OutputValidator] = None


def _init_globals() -> bool:
    """Initialize global objects safely. Returns True on success."""
    global _embedding_builder, _llm, _answer_ability_gate, _output_validator
    try:
        logger.info("Initializing knowledge assistant...")
        _embedding_builder = EmbeddingBuilder()
        _llm = OpenAIClient()
        _answer_ability_gate = AnswerabilityGate()
        _output_validator = OutputValidator()
        logger.info("✓ Initialization complete")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize: {e}")
        return False


def _get_embedding_builder() -> EmbeddingBuilder:
    """Get or initialize the embedding builder."""
    global _embedding_builder
    if _embedding_builder is None:
        _embedding_builder = EmbeddingBuilder()
    return _embedding_builder


def _get_llm() -> OpenAIClient:
    """Get or initialize the LLM client."""
    global _llm
    if _llm is None:
        _llm = OpenAIClient()
    return _llm


def _get_answer_ability_gate() -> AnswerabilityGate:
    """Get or initialize the answerability gate."""
    global _answer_ability_gate
    if _answer_ability_gate is None:
        _answer_ability_gate = AnswerabilityGate()
    return _answer_ability_gate


def _get_output_validator() -> OutputValidator:
    """Get or initialize the output validator."""
    global _output_validator
    if _output_validator is None:
        _output_validator = OutputValidator()
    return _output_validator


def ask(question: str, verbose: bool = False) -> int:
    """
    Answer a question using the knowledge base.

    Args:
        question: The question to answer
        verbose: If True, print additional context information

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if not question or not question.strip():
        logger.error("Question cannot be empty")
        return EXIT_USAGE_ERROR

    logger.info(f"Processing question: '{question}'")

    try:
        # Retrieve relevant chunks
        logger.debug("Retrieving relevant chunks...")
        results: List[Chunk] = retrieve(question)

        if not results:
            logger.warning("No relevant documents found")
            print("❌ No relevant documents found in knowledge base")
            return EXIT_NO_ANSWER

        if verbose:
            logger.info(f"Retrieved {len(results)} relevant chunks")

        # Check answerability
        answer_gate = _get_answer_ability_gate()
        if not answer_gate.should_answer(results):
            logger.warning("Question deemed unanswerable based on available context")
            print("❌ Insufficient context to answer this question")
            return EXIT_NO_ANSWER

        # Build and generate prompt
        logger.debug("Building prompt...")
        prompt: str = build_prompt(question, results)

        llm_client = _get_llm()
        logger.debug("Generating answer...")
        answer = llm_client.generate(
            prompt,
            config=LLMConfig(
                model="gpt-3.5-turbo",  # "gpt-5.2",
                temperature=0.2,
                max_output_tokens=600,
            ),
        )

        # Validate output
        output_validator = _get_output_validator()
        if not output_validator.validate(answer=answer, contexts=results):
            logger.warning("Generated answer failed validation")
            print("⚠️  Warning: Answer may not be grounded in provided context")
            # TODO: This is what I want? Continue anyway, but warn user

        # Format and display answer
        _print_answer(answer, results, verbose)
        return EXIT_SUCCESS

    except KeyError as e:
        logger.error(f"Missing knowledge base: {e}")
        print("❌ Error: Knowledge base not found. Run 'index' first.")
        return EXIT_RUNTIME_ERROR
    except Exception as e:
        logger.error(f"Unexpected error while answering: {type(e).__name__}: {e}")
        print(f"❌ Error: {e}")
        return EXIT_RUNTIME_ERROR


def _print_answer(answer: str, contexts: List[Chunk], verbose: bool) -> None:
    """Format and print the answer with context."""
    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)

    if verbose and contexts:
        print("\n" + "-" * 60)
        print("SOURCES")
        print("-" * 60)
        for idx, chunk in enumerate(contexts, 1):
            source = chunk.get("source", "Unknown")
            chunk_idx = chunk.get("index", "N/A")
            print(f"{idx}. {source} (chunk #{chunk_idx})")
    print("=" * 60 + "\n")


def index(paths: List[str]) -> int:
    """
    Index documents from given paths.

    Args:
        paths: List of file or directory paths to index

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if not paths:
        logger.error("No paths provided for indexing")
        return EXIT_USAGE_ERROR

    # Validate paths exist
    for path in paths:
        if not os.path.exists(path):
            logger.error(f"Path not found: {path}")
            print(f"❌ Error: Path not found: {path}")
            return EXIT_USAGE_ERROR

    logger.info(f"Indexing {len(paths)} path(s)...")

    try:
        # Read files
        logger.debug(f"Reading files from {paths}...")
        text_by_file: Dict[str, str] = read_files(paths)

        if not text_by_file:
            logger.warning("No text content found in provided paths")
            print("⚠️  Warning: No text content found in provided paths")
            return EXIT_RUNTIME_ERROR

        logger.info(f"Read {len(text_by_file)} file(s)")

        # Chunk text
        logger.debug("Chunking text...")
        chunks: List[Chunk] = get_chunks_from_files(text_by_file)
        logger.info(f"Created {len(chunks)} chunk(s)")

        # Save chunks to JSON
        logger.debug("Saving chunks...")
        save_chunks(chunks)

        # Build and save embeddings
        logger.debug("Building embeddings...")
        embedding_builder = _get_embedding_builder()
        chunks_vectors: List[EmbeddedChunk] = embedding_builder.build_vectors(chunks)
        logger.info(f"Built embeddings for {len(chunks_vectors)} chunk(s)")

        logger.debug("Saving vectors...")
        save_chunks_vectors(chunks_vectors)

        print(
            f"✅ Successfully indexed {len(chunks)} chunks from {len(text_by_file)} file(s)"
        )
        logger.info("Indexing complete")
        return EXIT_SUCCESS

    except PermissionError as e:
        logger.error(f"Permission denied while reading files: {e}")
        print("❌ Error: Permission denied while reading files")
        return EXIT_RUNTIME_ERROR
    except Exception as e:
        logger.error(f"Unexpected error during indexing: {type(e).__name__}: {e}")
        print(f"❌ Error: {e}")
        return EXIT_RUNTIME_ERROR


def print_help() -> None:
    """Print help message."""
    help_text = f"""
{"-" * 70}
AI Knowledge Assistant v{__version__}
{"-" * 70}

A command-line tool for indexing documents and answering questions
using semantic search and Retrieval-Augmented Generation (RAG).

USAGE:
  python cli.py index <path1> [path2 ...]
    Index one or more files/directories into the knowledge base.

  python cli.py ask "<question>" [--verbose]
    Ask a question and get answers from the knowledge base.
    Use --verbose to see source documents.

  python cli.py --help
    Show this help message.

  python cli.py --version
    Show version information.

EXAMPLES:
  # Index a single file
  python cli.py index data/documents.txt

  # Index multiple files
  python cli.py index data/ more_data/

  # Ask a question
  python cli.py ask "What is machine learning?"

  # Ask with verbose output
  python cli.py ask "What is machine learning?" --verbose

ENVIRONMENT:
  API_KEY          OpenAI API key (required for ask command)

EXIT CODES:
  0  Success
  1  Usage error
  2  Runtime error
  3  No answer found

{"-" * 70}
"""
    print(help_text)


def print_version() -> None:
    """Print version information."""
    print(f"AI Knowledge Assistant v{__version__}")


def main() -> int:
    """Main entry point. Returns exit code."""
    args = sys.argv[1:]

    # Handle no arguments
    if not args:
        print_help()
        return EXIT_USAGE_ERROR

    # Handle global flags
    if args[0] in ["--help", "-h", "help"]:
        print_help()
        return EXIT_SUCCESS

    if args[0] in ["--version", "-v", "version"]:
        print_version()
        return EXIT_SUCCESS

    # Validate command
    if args[0] not in ["index", "ask"]:
        print(f"❌ Unknown command: '{args[0]}'")
        print("Run 'python cli.py --help' for usage information")
        return EXIT_USAGE_ERROR

    # Require at least one more argument
    if len(args) < 2:
        print(f"❌ Command '{args[0]}' requires arguments")
        print("Run 'python cli.py --help' for usage information")
        return EXIT_USAGE_ERROR

    command = args[0]

    try:
        if command == "index":
            # index <path1> [path2 ...]
            paths = args[1:]
            return index(paths)

        elif command == "ask":
            # ask <question> [--verbose]
            # Extract question and flags
            question_parts = []
            verbose = False

            if "--verbose" in args[1:] or "-v" in args[1:]:
                verbose = True
                if "--verbose" == args[1]:
                    question_parts = args[2:]
                elif "-v" == args[-1]:
                    question_parts = args[1:-1]

            if not question_parts:
                print("❌ Question cannot be empty")
                return EXIT_USAGE_ERROR

            question = " ".join(question_parts)
            return ask(question, verbose=verbose)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return EXIT_USAGE_ERROR
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        print(f"❌ Unexpected error: {e}")
        return EXIT_RUNTIME_ERROR

    return EXIT_RUNTIME_ERROR


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
