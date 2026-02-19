# AI Knowledge Assistant

A CLI-first Retrieval-Augmented Generation (RAG) pipeline for indexing local text files and answering questions with grounded, source-cited responses.

## How It Works

```text
Files → Text → Chunks → Embeddings → Vector Store → Retrieval → Answer + Source
```

| Stage             | Module                      | Description                                       |
| ----------------- | --------------------------- | ------------------------------------------------- |
| **Ingestion**     | `ingest/reader.py`      | Reads `.txt` and `.md` files recursively          |
| **Normalization** | `normalize/chunker.py`  | Splits text into overlapping chunks               |
| **Embedding**     | `embedding/builder.py`  | Generates vectors via `sentence-transformers`     |
| **Storage**       | `store/`                | Persists chunks (JSON) and vectors (JSON + FAISS) |
| **Retrieval**     | `retrieve/retriever.py` | Semantic search over FAISS index                  |
| **Reasoning**     | `rag/prompt_builder.py` | Builds a grounded prompt with context             |
| **LLM**           | `llm/openai_client.py`  | Calls OpenAI to generate an answer                |
| **Grounding**     | `grounding/`            | Gates on context quality and validates citations  |

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

Set your OpenAI API key before running any `index` and `ask` command:

```powershell
# PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

```bash
# Bash / macOS
export OPENAI_API_KEY="sk-..."
```

## Quick Start

**1. Index your documents:**

```bash
python -m ai_knowledge_assistant.cli index data_set/inputs
```

**2. Ask a question:**

```bash
python -m ai_knowledge_assistant.cli ask "What are the main topics in the indexed files?"
```

## CLI Reference

### `index`

Scans files and directories, builds chunks + embeddings, and writes:

- `data_set/output/index.json` — chunk metadata
- `data_set/output/vectors.json` — embedding vectors

```bash
python -m ai_knowledge_assistant.cli index <path1> [path2 ...]
```

### `ask`

Queries the indexed knowledge and returns a grounded answer with source citations.

```bash
python -m ai_knowledge_assistant.cli ask "<question>" [options]
```

| Option          | Default   | Description                    |
| --------------- | --------- | ------------------------------ |
| `--limit`       | `5`       | Max context chunks to retrieve |
| `--model`       | `gpt-4.1` | OpenAI model name              |
| `--temperature` | `0.2`     | Sampling temperature (0.0–2.0) |
| `--max-tokens`  | `600`     | Max output tokens              |
| `-v, --verbose` | off       | Enable debug logging           |

### Global Flags

| Flag            | Description                                           |
| --------------- | ----------------------------------------------------- |
| `-v, --verbose` | Print debug-level logs (`MODULE \| LEVEL \| MESSAGE`) |

## Project Structure

```text
src/
└── ai_knowledge_assistant/     # Main Python package
    ├── __init__.py
    ├── cli.py                  # Entry point & argument parsing
    ├── ingest/
    │   ├── __init__.py
    │   └── reader.py           # Recursive file reading
    ├── normalize/
    │   ├── __init__.py
    │   └── chunker.py          # Text → overlapping chunks
    ├── embedding/
    │   ├── __init__.py
    │   └── builder.py          # Chunks → vector embeddings
    ├── store/
    │   ├── __init__.py
    │   ├── json_store.py       # JSON persistence for chunks
    │   ├── vector_store.py     # JSON persistence for vectors
    │   └── faiss_store.py      # FAISS index & cosine search
    ├── retrieve/
    │   ├── __init__.py
    │   ├── retriever.py        # Semantic retrieval pipeline
    │   └── naive.py            # Keyword-based fallback search
    ├── rag/
    │   ├── __init__.py
    │   └── prompt_builder.py   # Context → grounded prompt
    ├── llm/
    │   ├── __init__.py
    │   ├── base.py             # LLM client interface
    │   └── openai_client.py    # OpenAI implementation
    └── grounding/
        ├── __init__.py
        ├── answerability.py    # Pre-answer context gate
        └── output_validator.py # Post-answer citation check
data_set/
├── inputs/                     # Source documents (.txt, .md)
└── output/                     # Generated index & vectors
pyproject.toml
requirements.txt
```

## Exit Codes

| Code | Meaning                                                         |
| ---- | --------------------------------------------------------------- |
| `0`  | Success                                                         |
| `1`  | Usage error (no readable files, bad arguments)                  |
| `2`  | `INSUFFICIENT_CONTEXT` — not enough relevant context found      |
| `3`  | `WRONG_CONTEXT` — answer citations don't match retrieved chunks |
| `4`  | LLM error (API failure, empty response)                         |

## Troubleshooting

| Problem                    | Solution                                                    |
| -------------------------- | ----------------------------------------------------------- |
| `INSUFFICIENT_CONTEXT`     | Index more documents or increase `--limit`                  |
| `WRONG_CONTEXT`            | The LLM hallucinated sources — try lowering `--temperature` |
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

## Limitations

- Ingestion supports only `.txt` and `.md` files (no PDF).
- `data_set/output/` must exist before indexing.
- All commands must be run from the project root directory.

## License

MIT
