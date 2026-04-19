# AI Knowledge Assistant

A CLI-first Retrieval-Augmented Generation (RAG) pipeline for indexing local text files and answering questions with grounded, source-cited responses.

## Architecture Overview

The system is a single pipeline that transforms raw files into grounded, source-cited answers:

```text
Files → Text → Chunks → Embeddings → Vector Store → Retrieval → Answer + Source
```

| Stage             | Module                 | Description                                          |
| ----------------- | ---------------------- | ---------------------------------------------------- |
| **Ingestion**     | `ingest/reader.py`     | Reads `.txt` and `.md` files recursively             |
| **Normalization** | `normalize/chunker.py` | Splits text into overlapping fixed-size chunks       |
| **Embedding**     | `embedding/builder.py` | Generates vectors via `sentence-transformers`        |
| **Storage**       | `store/`               | Persists chunks (JSON) and vectors (JSON + FAISS)    |
| **Retrieval**     | `retrieve/retriever.py`| Semantic search over FAISS index (cosine similarity) |
| **Reasoning**     | `rag/prompt_builder.py`| Builds a grounded prompt with context and citations  |
| **LLM**           | `llm/openai_client.py` | Calls OpenAI to generate an answer                   |
| **Grounding**     | `grounding/`           | Gates on context quality and validates citations     |

## Prerequisites

- Python 3.14+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Installation

```bash
git clone https://github.com/DorLevi694/ai_knowledge_assistant.git
cd ai_knowledge_assistant
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Set your OpenAI API key before running any `index` or `ask` command:

```powershell
# PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

```bash
# Bash / macOS
export OPENAI_API_KEY="sk-..."
```

## Usage

### 1. Index your documents

Scan files and directories, build chunks and embeddings, and write the index:

```bash
python -m ai_knowledge_assistant.cli index data_set/inputs
```

This produces two output files:

- `data_set/output/index.json` -- chunk metadata
- `data_set/output/vectors.json` -- embedding vectors

You can pass multiple paths:

```bash
python -m ai_knowledge_assistant.cli index path/to/docs path/to/notes
```

### 2. Ask a question

Query the indexed knowledge and receive a grounded answer with source citations:

```bash
python -m ai_knowledge_assistant.cli ask "What are the main topics in the indexed files?"
```

Customize the query with options:

```bash
python -m ai_knowledge_assistant.cli ask "Explain how FAISS indexing works" \
  --limit 10 --model gpt-4.1 --temperature 0.1 --max-tokens 800
```

## CLI Reference

### `index`

```bash
python -m ai_knowledge_assistant.cli index <path1> [path2 ...]
```

Recursively reads supported files (`.txt`, `.md`), splits them into chunks, generates embeddings, and persists everything to `data_set/output/`.

### `ask`

```bash
python -m ai_knowledge_assistant.cli ask "<question>" [options]
```

| Option          | Default    | Description                    |
| --------------- | ---------- | ------------------------------ |
| `--limit`       | `5`        | Max context chunks to retrieve |
| `--model`       | `gpt-4.1`  | OpenAI model name              |
| `--temperature` | `0.2`      | Sampling temperature (0.0-2.0) |
| `--max-tokens`  | `600`      | Max output tokens              |
| `-v, --verbose` | off        | Enable debug logging           |

### Global Flags

| Flag            | Description                                             |
| --------------- | ------------------------------------------------------- |
| `-v, --verbose` | Print debug-level logs (`MODULE \| LEVEL \| MESSAGE`)   |

## How Grounding Works

The grounding layer prevents hallucinated or unsupported answers through two checks:

**1. Answerability gate (pre-answer)**

Before calling the LLM, the `AnswerabilityGate` checks whether the retrieved context chunks contain enough content to form a meaningful answer. If the total text length falls below a minimum threshold (800 characters by default), the pipeline returns `INSUFFICIENT_CONTEXT` and exits with code 2.

**2. Citation validation (post-answer)**

After the LLM generates a response, the `OutputValidator` extracts all `[Source: <filename>, chunk <index>]` citations from the answer and verifies that every cited source exists in the retrieved context. If any citation references a chunk that was not retrieved -- or if the answer contains no citations at all -- the pipeline returns `WRONG_CONTEXT` and exits with code 3.

## Project Structure

```text
src/
└── ai_knowledge_assistant/
    ├── __init__.py
    ├── cli.py                  # Entry point and argument parsing
    ├── config.py               # Centralized constants and defaults
    ├── ingest/
    │   └── reader.py           # Recursive file reading (.txt, .md)
    ├── normalize/
    │   └── chunker.py          # Text → overlapping fixed-size chunks
    ├── embedding/
    │   └── builder.py          # Chunks → vector embeddings (sentence-transformers)
    ├── store/
    │   ├── base.py             # Shared persistence utilities
    │   ├── json_store.py       # JSON persistence for chunks
    │   ├── vector_store.py     # JSON persistence for vectors
    │   └── faiss_store.py      # FAISS index with cosine similarity search
    ├── retrieve/
    │   └── retriever.py        # Semantic retrieval pipeline
    ├── rag/
    │   └── prompt_builder.py   # Context → grounded prompt with citations
    ├── llm/
    │   ├── base.py             # Abstract LLM client interface
    │   └── openai_client.py    # OpenAI implementation
    └── grounding/
        ├── answerability.py    # Pre-answer context gate
        └── output_validator.py # Post-answer citation check
tests/
├── unit/                       # Unit tests
└── integration/                # Integration tests
data_set/
├── inputs/                     # Source documents
└── output/                     # Generated index and vectors
```

## Running Tests

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/unit/test_chunker.py
```

## Exit Codes

| Code | Meaning                                                         |
| ---- | --------------------------------------------------------------- |
| `0`  | Success                                                         |
| `1`  | Usage error (no readable files, bad arguments)                  |
| `2`  | `INSUFFICIENT_CONTEXT` -- not enough relevant context found     |
| `3`  | `WRONG_CONTEXT` -- answer citations don't match retrieved chunks|
| `4`  | LLM error (API failure, empty response)                         |

## Troubleshooting

| Problem                    | Solution                                                    |
| -------------------------- | ----------------------------------------------------------- |
| `INSUFFICIENT_CONTEXT`     | Index more documents or increase `--limit`                  |
| `WRONG_CONTEXT`            | The LLM hallucinated sources -- try lowering `--temperature`|
| Empty OpenAI response      | Verify `OPENAI_API_KEY` is set and the model name is valid  |
| `FileNotFoundError` on ask | Run `index` first to generate the vector store              |
| `ModuleNotFoundError`      | Run from the project root directory                         |

## Dependencies

| Package                 | Purpose                          |
| ----------------------- | -------------------------------- |
| `openai`                | LLM API calls                    |
| `sentence-transformers` | Local embedding model            |
| `faiss-cpu`             | Vector similarity search         |
| `numpy`                 | Numerical operations for vectors |

## License

MIT
