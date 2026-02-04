# cli.py file

import sys
import logging
from typing import Dict, List

from embedding.builder import EmbeddedChunk, EmbeddingBuilder
from ingest.reader import read_files
from normalize.chunker import Chunk, get_chunks_from_files
from store.faiss_store import FaissStore
from store.json_store import save_chunks, load_chunks
from store.vector_store import save_chunks_vectors, load_chunks_vectors

from retrieve.naive import naive_search

embeddingBuilder = EmbeddingBuilder()
# from index import indexer
# from ask import asker

# Configure logging for all modules
logging.basicConfig(
    level=logging.INFO, format="%(name)-20s | %(levelname)-8s: %(message)s"
)

logger = logging.getLogger(__name__)


def ask(question: str):
    logger.info(f"Asking question: {question}")


    ''' 
    # naive_search
    chunks: List[Chunk] = load_chunks()
    result: List[Chunk] = naive_search(query=question, chunks=chunks)
    for index, chunk in enumerate(result):
        print(
            f"{index+1}: Source: {chunk['source']} | Index: {chunk['index']}\n{chunk['text']}"
        )
    '''
    vectors_chunks: List[EmbeddedChunk] = load_chunks_vectors()
    faiss_store = FaissStore(dim=384)
    faiss_store.build(vectors_chunks)
    embedding_builder = EmbeddingBuilder()
    question_v = embedding_builder.model.encode(question).tolist()
    
    results = faiss_store.search(question_v,3)
    for res in results:
        print(f'{'*'* 20}\n{res['source']=}, {res['index']=}\n{res['text']=}\n{'*'* 20}')
    return results

def index(paths):
    logger.info(f"Indexing: {paths}")

    text_by_file: Dict[str, str] = read_files(paths)
    chunks: List[Chunk] = get_chunks_from_files(text_by_file)
    save_chunks(chunks)

    # Embedding Vectors
    chunks_vectors: List[EmbeddedChunk] = embeddingBuilder.build_vectors(chunks)
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
