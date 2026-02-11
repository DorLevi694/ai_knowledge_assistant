# cli.py file

import sys
import logging
from typing import Dict, List

from embedding.builder import EmbeddedChunk, EmbeddingBuilder
from grounding.answerability import AnswerabilityGate
from ingest.reader import read_files
from llm.base import LLMConfig
from llm.openai_client import OpenAIClient
from normalize.chunker import Chunk, get_chunks_from_files
from retrieve.retriver import ContextChunk, retrieve
from rag.prompt_builder import build_prompt
from store.json_store import save_chunks, load_chunks
from store.vector_store import save_chunks_vectors

from retrieve.naive import naive_search

embedding_builder = EmbeddingBuilder()
# from index import indexer
# from ask import asker

# Configure logging for all modules
logging.basicConfig(
    level=logging.INFO, format="%(name)-20s | %(levelname)-8s: %(message)s"
)

logger = logging.getLogger(__name__)


# From cli.py
def ask(question: str):
    logger.info(f"Asking question: {question}")

    """ 
    # naive_search
    chunks: List[Chunk] = load_chunks()
    result: List[Chunk] = naive_search(query=question, chunks=chunks)
    for index, chunk in enumerate(result):
        print(
            f"{index+1}: Source: {chunk['source']} | Index: {chunk['index']}\n{chunk['text']}"
        )
    """
    llm = OpenAIClient()
    answer_ability_gate = AnswerabilityGate()
    results: List[ContextChunk] = retrieve(question)
    if not answer_ability_gate.should_answer(results):
        print("Insufficient_context")
        return

    prompt: str = build_prompt(question, results)
    try:
        answer = llm.generate(
            prompt,
            config=LLMConfig(
                model="gpt-5.2",
                temperature=0.2,
                max_output_tokens=600,
            ),
        )

        # 4️⃣ Output
        print("\n=== ANSWER ===\n")
        print(answer)
    except Exception as e:
        print(f"Something went wrong: {e}")


def index(paths):
    logger.info(f"Indexing: {paths}")

    text_by_file: Dict[str, str] = read_files(paths)
    chunks: List[Chunk] = get_chunks_from_files(text_by_file)
    save_chunks(chunks)

    # Embedding Vectors
    chunks_vectors: List[EmbeddedChunk] = embedding_builder.build_vectors(chunks)
    save_chunks_vectors(chunks_vectors)


def usage():
    logger.info("Usage:")
    logger.info("  python cli.py index <path1> [path2 ...]")
    logger.info('  python cli.py ask "<question>"')


def main():
    args = sys.argv[1:]

    if len(args) < 2 or args[0] not in ["index", "ask"]:
        usage()
        return

    method = args[0]

    if method == "index":
        paths = args[1:]
        index(paths)
    elif method == "ask":
        question = " ".join(args[1:])
        ask(question)


if __name__ == "__main__":
    main()
