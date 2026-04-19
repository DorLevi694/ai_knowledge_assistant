import os

from ai_knowledge_assistant.ingest.reader import explore_files, read_file


def test_explore_files_single_path(tmp_path):
    # Create temp files
    d = tmp_path / "sub"
    d.mkdir()
    f1 = d / "file1.txt"
    f1.write_text("content1")
    f2 = d / "file2.md"
    f2.write_text("content2")

    # explore_files takes a list of strings
    paths = [str(tmp_path)]
    result = explore_files(paths)

    assert len(result) == 2
    # Convert results to normalized paths for comparison
    normalized_results = [os.path.normpath(r) for r in result]
    assert os.path.normpath(str(f1)) in normalized_results
    assert os.path.normpath(str(f2)) in normalized_results


def test_explore_files_non_existent():
    result = explore_files(["/non/existent/path/at/all"])
    assert result == []


def test_read_file_supported_extension(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("some content")
    assert read_file(str(f)) == "some content"


def test_read_file_no_extension(tmp_path):
    f = tmp_path / "noext"
    f.write_text("data")
    assert read_file(str(f)) is None


def test_read_file_unsupported_extension(tmp_path):
    f = tmp_path / "image.png"
    f.write_bytes(b"\x89PNG")
    assert read_file(str(f)) is None
