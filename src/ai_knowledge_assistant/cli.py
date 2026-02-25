# src/ai_knowledge_assistant/cli.py — CLI orchestration layer

import argparse
import logging
import sys

import ai_knowledge_assistant.config as config
from ai_knowledge_assistant.embedding.builder import EmbeddedChunk, EmbeddingBuilder
from ai_knowledge_assistant.grounding.answerability import AnswerabilityGate
from ai_knowledge_assistant.grounding.output_validator import OutputValidator
from ai_knowledge_assistant.ingest.reader import read_files
from ai_knowledge_assistant.llm.base import LLMConfig
from ai_knowledge_assistant.llm.openai_client import OpenAIClient
from ai_knowledge_assistant.normalize.chunker import Chunk, get_chunks_from_files
from ai_knowledge_assistant.rag.prompt_builder import build_prompt
from ai_knowledge_assistant.retrieve.retriever import Retriever
from ai_knowledge_assistant.store.json_store import save_chunks
from ai_knowledge_assistant.store.vector_store import save_chunks_vectors

logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_USAGE_ERROR = 1
EXIT_INSUFFICIENT_CONTEXT = 2
EXIT_WRONG_CONTEXT = 3
EXIT_LLM_ERROR = 4


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(name)-20s | %(levelname)-8s: %(message)s",
    )


def cmd_index(args: argparse.Namespace) -> int:
    logger.info("Indexing: %s", args.paths)

    text_by_file: dict[str, str] = read_files(args.paths)
    if not text_by_file:
        logger.error("No readable files found in the provided paths.")
        return EXIT_USAGE_ERROR

    chunks: list[Chunk] = get_chunks_from_files(text_by_file)
    save_chunks(chunks, path=config.INDEX_FILE)
    logger.info("Saved %d chunks to index.", len(chunks))

    embedding_builder: EmbeddingBuilder = EmbeddingBuilder(
        config=config.DEFAULT_EMBEDDING
    )
    chunks_vectors: list[EmbeddedChunk] = embedding_builder.build_vectors(chunks)
    save_chunks_vectors(chunks_vectors, path=config.VECTORS_FILE)
    logger.info("Saved %d vectors.", len(chunks_vectors))

    return EXIT_OK


def cmd_ask(args: argparse.Namespace) -> int:
    question: str = " ".join(args.question)
    logger.info("Question: %s", question)

    # 1. Retrieve context
    retriever = Retriever(
        embedding_config=config.DEFAULT_EMBEDDING,
        vectors_path=config.VECTORS_FILE,
    )
    results: list[Chunk] = retriever.retrieve(question, limit=args.limit)

    # 2. Answerability gate
    gate = AnswerabilityGate()
    if not gate.should_answer(results):
        logger.warning("Answerability gate rejected the query: INSUFFICIENT_CONTEXT")
        return EXIT_INSUFFICIENT_CONTEXT

    # 3. Generate answer
    prompt: str = build_prompt(question, results)
    llm = OpenAIClient()
    llm_config = LLMConfig(
        model=args.model,
        temperature=args.temperature,
        max_output_tokens=args.max_tokens,
    )

    try:
        answer: str = llm.generate(prompt, config=llm_config)
    except Exception as exc:
        logger.error("LLM call failed: %s", exc)
        return EXIT_LLM_ERROR

    # 4. Output validation
    validator = OutputValidator()
    if not validator.validate(answer=answer, contexts=results):
        logger.warning("Output validation failed: WRONG_CONTEXT")
        return EXIT_WRONG_CONTEXT

    # 5. Print answer
    print("\n=== ANSWER ===\n")
    print(answer)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-knowledge-assistant",
        description="Index text files and ask questions with RAG.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- index ---
    index_parser = subparsers.add_parser("index", help="Index files or directories.")
    index_parser.add_argument(
        "paths", nargs="+", help="One or more file or directory paths to index."
    )
    index_parser.set_defaults(func=cmd_index)

    # --- ask ---
    ask_parser = subparsers.add_parser("ask", help="Ask a question.")
    ask_parser.add_argument("question", nargs="+", help="The question to ask.")
    ask_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max context chunks to retrieve (default: 5).",
    )
    ask_parser.add_argument(
        "--model",
        type=str,
        default=config.DEFAULT_LLM_MODEL,
        help=f"OpenAI model name (default: {config.DEFAULT_LLM_MODEL}).",
    )
    ask_parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2).",
    )
    ask_parser.add_argument(
        "--max-tokens",
        type=int,
        default=600,
        dest="max_tokens",
        help="Max output tokens (default: 600).",
    )
    ask_parser.set_defaults(func=cmd_ask)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    _configure_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
