# AI Knowledge Assistant

A command-line tool to index and query documents using AI.

## Features
- Index files and directories
- Query indexed knowledge
- Debug logging with formatted output

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

## Usage

### Index files
```bash
python src/cli.py index <path1> [path2 ...]
python src/cli.py index .\texts\
```

### Ask a question
```bash
python src/cli.py ask "What is this about?"
```

## Project Structure
```
├── src/
│   ├── cli.py           # Main CLI entry point
│   └── ingest/
│       └── reader.py    # File reader module
├── info.md
└── README.md
```

## Logging

Format: `MODULE_NAME | LEVEL | MESSAGE`

Default level: `DEBUG`

## License
MIT
