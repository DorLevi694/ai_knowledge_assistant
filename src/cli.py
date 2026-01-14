import sys
import logging
from ingest.reader import read_files

# from index import indexer
# from ask import asker

# Configure logging for all modules
logging.basicConfig(
    level=logging.INFO, format="%(name)-20s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)


def ask(question: str):
    logger.info(f"Asking question: {question}")


def index(paths):
    logger.info(f"Indexing: {paths}")
    # read_files(paths)


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
