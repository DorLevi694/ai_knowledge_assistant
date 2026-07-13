FROM python:3.14-slim

# uv is a static binary; copy it from the official image (pinned to the
# same version used locally).
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

WORKDIR /code

# Dependencies only — this layer stays cached until pyproject/uv.lock change.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY src/ai_knowledge_assistant ./ai_knowledge_assistant

# Make the venv's executables (uvicorn) the default ones.
ENV PATH="/code/.venv/bin:$PATH"

CMD ["uvicorn", "ai_knowledge_assistant.api.main:app", "--host", "0.0.0.0", "--port", "80"]
