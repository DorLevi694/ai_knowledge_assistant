import subprocess
import sys

import pytest


def test_full_workflow():
    """
    Test the full workflow:
    1. Index the data_set/inputs/ directory.
    2. Ask a question about Python.
    """

    # Step 1: Indexing
    print("\nRunning Step 1: Indexing...")
    index_cmd = [
        sys.executable,
        "-m",
        "ai_knowledge_assistant.cli",
        "index",
        "data_set/inputs/",
    ]
    index_result = subprocess.run(index_cmd, capture_output=True, text=True)

    print("Index Output:", index_result.stdout)
    print("Index Error:", index_result.stderr)

    assert index_result.returncode == 0, (
        f"Indexing failed with exit code {index_result.returncode}"
    )
    assert "Saved" in index_result.stderr or "Saved" in index_result.stdout

    # Step 2: Asking
    print("\nRunning Step 2: Asking...")
    ask_cmd = [
        sys.executable,
        "-m",
        "ai_knowledge_assistant.cli",
        "ask",
        "Explain",
        "something",
        "about",
        "python",
        "systems",
    ]
    ask_result = subprocess.run(ask_cmd, capture_output=True, text=True)

    print("Ask Output:", ask_result.stdout)
    print("Ask Error:", ask_result.stderr)

    # We accept 0 (Success) or 2 (Insufficient Context) as valid results
    # for a smoke test since we don't know if the LLM will find the answer
    # or if the API key is set.
    assert ask_result.returncode in [
        0,
        2,
    ], f"Ask command crashed with exit code {ask_result.returncode}"


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
