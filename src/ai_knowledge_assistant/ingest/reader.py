"""File ingestion utilities for reading text documents from disk.

Provides two public helpers:
- ``read_files`` – accepts a list of file/directory paths and returns a
  mapping of absolute file path → raw text content for every supported file
  that was found.
- ``explore_files`` – walks paths recursively and returns the sorted list of
  all discovered absolute file paths.

Only file extensions listed in ``config.SUPPORTED_EXTENSIONS`` are read;
unsupported files are silently skipped.
"""

# reader.py file

import logging
import os
from pathlib import Path

from ai_knowledge_assistant.config import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


def read_files(paths: list[str]) -> dict[str, str]:
    """Read all supported files found under the given paths.

    Args:
        paths: A list of file or directory paths to search. Directories are
            walked recursively.

    Returns:
        A dict mapping each absolute file path to its text content.  Files
        that cannot be read or whose extension is not supported are excluded.
    """
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
    """Resolve a mixed list of files and directories to absolute file paths.

    Each entry in *paths* is resolved to its absolute form.  Missing paths are
    logged as errors and skipped.  Directories are walked recursively; all
    files encountered (regardless of extension) are included in the result.

    Args:
        paths: A list of file or directory paths (relative or absolute).

    Returns:
        A sorted list of unique absolute file paths.
    """

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
    """Read a single file and return its contents as a string.

    Only files whose extension appears in ``config.SUPPORTED_EXTENSIONS`` are
    read.  Any file that does not exist, is not a regular file, or has an
    unsupported extension returns ``None``.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        The file's text content, or ``None`` if the file could not or should
        not be read.
    """

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
