# reader.py file

import logging
import os
from pathlib import Path

from ai_knowledge_assistant.config import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


def read_files(paths: list[str]) -> dict[str, str]:
    logger.debug(f"read_files({paths})")
    file_paths = explore_files(paths)
    logger.info(f"file_paths: [\n\t{'\n\t'.join(file_paths)}\n\t]")

    files_content = {}
    for file_path in file_paths:
        file_content = read_file(file_path)
        if file_content is not None:
            files_content[file_path] = file_content

    return files_content


def explore_files(paths: list[str]) -> list[str]:

    file_paths: set[str] = set()

    for cur_path in paths:
        abs_path = os.path.abspath(cur_path)
        if not os.path.exists(abs_path):
            logger.error(f"{abs_path:<80}: Not Exist")
            continue

        logger.debug(f"{abs_path:<80}: Exist")
        if os.path.isfile(abs_path):
            file_paths.add(abs_path)

        elif os.path.isdir(abs_path):
            for dirpath, _, filenames in os.walk(abs_path):
                logger.debug(f"{dirpath=}")
                logger.debug(f"{filenames=}")
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    file_paths.add(full_path)

    return sorted(file_paths)


def read_file(file_path: str) -> str | None:

    if not os.path.exists(file_path):
        logger.error(f"File {file_path} - Not exist")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"Path {file_path} - Isn't file")
        return None

    suffix = Path(file_path).suffix.lstrip(".")

    if suffix in SUPPORTED_EXTENSIONS:
        with open(file_path, errors="ignore") as f:
            txt = f.read()
    else:
        return None
    return txt
