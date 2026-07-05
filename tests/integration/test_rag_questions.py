"""
Integration tests for RAG positive/negative question answering.

Based on the test spec in data_set/inputs/rag_test_questions.txt.

Positive questions  — the answer EXISTS in orlit_company.txt  → expect exit 0
Negative questions  — the answer does NOT exist anywhere       → expect exit 2
"""

import subprocess
import sys

import pytest


@pytest.fixture(scope="module", autouse=True)
def build_index():
    """Index the full inputs directory (including orlit_company.txt) once."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_knowledge_assistant.cli",
            "index",
            "data_set/inputs/",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Indexing failed with exit code {result.returncode}:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Positive tests — answer exists in orlit_company.txt
# ---------------------------------------------------------------------------

POSITIVE_QUESTIONS = [
    ("Who founded Orlit?", "founder"),
    ("What is the accuracy level of the sensor?", "sensor accuracy"),
    ("What is the name of the main product of the company?", "main product"),
    ("In what year was the company founded?", "founding year"),
    ("Who is the CEO of the company?", "CEO"),
]


@pytest.mark.parametrize("question,label", POSITIVE_QUESTIONS)
def test_positive_question_returns_answer(question, label):
    """The RAG pipeline must produce a grounded answer (exit code 0)."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_knowledge_assistant.cli", "ask", question],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"[{label}] Expected a grounded answer for '{question}' "
        f"but got exit code {result.returncode}.\n"
        f"stderr (last 400 chars): {result.stderr[-400:]}"
    )


# ---------------------------------------------------------------------------
# Negative tests — answer does NOT exist in any indexed document
# ---------------------------------------------------------------------------

NEGATIVE_QUESTIONS = [
    ("What is the price of the Solar-Eye sensor?", "sensor price"),
    ("Who are the competitors of Orlit?", "competitors"),
    ("How old is Dana Levi?", "founder age"),
    ("On which stock exchange is the company listed?", "stock exchange"),
    ("How many branches does the company have?", "branches"),
]


@pytest.mark.parametrize("question,label", NEGATIVE_QUESTIONS)
def test_negative_question_returns_insufficient_context(question, label):
    """The RAG pipeline must refuse to answer (exit code 2 = INSUFFICIENT_CONTEXT)."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_knowledge_assistant.cli", "ask", question],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, (
        f"[{label}] Expected INSUFFICIENT_CONTEXT for '{question}' "
        f"but got exit code {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr (last 400 chars): {result.stderr[-400:]}"
    )
