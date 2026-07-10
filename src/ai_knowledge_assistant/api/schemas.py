from enum import StrEnum, auto

from pydantic import BaseModel


class ReadFileStatus(StrEnum):
    SUCCESS = auto()
    FAILED = auto()


class ReadFileReasonFailed(StrEnum):
    UNSUPPORTED_FILE = auto()
    MISSING_FILENAME = auto()
    FAIL_TO_SAVE = auto()
    UNKNOWN_ISSUE = auto()
    EMPTY_FILE = auto()
    DECODE_FAILED = auto()


class FileResponseBase(BaseModel):
    filename: str
    status: ReadFileStatus
    failure_reason: None | ReadFileReasonFailed = None


class IngestResponseBase(BaseModel):
    files: dict[str, FileResponseBase]


# internal - not part of the API response
class FileInProcess(FileResponseBase):  # all base fields + text
    text: str | None = None
