FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    LOCAL_EMBEDDING_CACHE_DIR=/app/.cache/embeddings \
    HF_HUB_DISABLE_TELEMETRY=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Download during setup; runtime inference only reads these local files.
COPY app/parking_knowledge/constants.py app/parking_knowledge/local_model.py app/parking_knowledge/download_model.py ./app/parking_knowledge/
RUN .venv/bin/python -m app.parking_knowledge.download_model

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "8000"]
