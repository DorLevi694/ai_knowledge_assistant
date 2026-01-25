# reader.py file

import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def read_files(paths: List[str]) -> Dict[str, str]:
    logger.debug(f"read_files({paths})")
    file_paths = explore_files(paths)
    logger.info(f'file_paths: [\n\t{"\n\t".join(file_paths)}\n\t]')

    files_content = {}
    for file_path in file_paths:
        file_content = read_file(file_path)
        if file_content is not None:
            files_content[file_path] = file_content

    # for k, v in files_content.items():
    #     print(f"{k:<60}: {v}")
    return files_content


def explore_files(paths: List[str]) -> List[str]:

    file_paths = []

    for cur_path in paths:
        abs_path = os.path.abspath(cur_path)
        if not os.path.exists(abs_path):
            logger.error(f"{abs_path:<80}: Not Exist")
            continue

        logger.debug(f"{abs_path:<80}: Exist")
        if os.path.isfile(abs_path):
            file_paths.append(abs_path)

        elif os.path.isdir(abs_path):
            files_list = os.listdir(abs_path)
            full_paths = [os.path.join(abs_path, file) for file in files_list]

            logger.debug(f"{abs_path=}")
            logger.debug(f"{files_list=}")
            logger.debug(f"{list(zip(files_list, full_paths))}")

            file_paths.extend(explore_files(full_paths))

    return file_paths


def read_file(file_path: str) -> str:

    if not os.path.exists(file_path):
        logger.error(f"File {file_path} - Not exist")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"Path {file_path} - Isn't file")
        return None

    suffix = file_path.split(".")[-1]

    if suffix in ["txt", "md"]:
        with open(file_path, "r", errors="ignore") as f:
            txt = f.read()
    else:
        return None
    return txt
