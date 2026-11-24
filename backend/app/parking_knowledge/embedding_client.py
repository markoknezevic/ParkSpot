"""Generate English embeddings locally, without inference API calls."""

import logging
import math
from threading import Lock

from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

from app.parking_knowledge.constants import (
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    MAX_EMBEDDING_INPUT_BYTES,
    MAX_EMBEDDING_TOKENS,
    QUERY_PREFIX,
)
from app.parking_knowledge.local_model import load_local_model

logger = logging.getLogger(__name__)
# Bound CPU/memory use and prevent duplicate model initialization on first use.
_inference_lock = Lock()


class EmbeddingClient:
    model = EMBEDDING_MODEL

    async def embed(self, text: str, *, is_query: bool = False) -> list[float]:
        if not text.strip() or len(text.encode("utf-8")) > MAX_EMBEDDING_INPUT_BYTES:
            raise HTTPException(status_code=422, detail="Embedding input must contain 1 to 8000 UTF-8 bytes")
        return await run_in_threadpool(self._embed, text, is_query)

    def _embed(self, text: str, is_query: bool) -> list[float]:
        model_input = QUERY_PREFIX + text if is_query else text
        with _inference_lock:
            try:
                model, tokenizer = load_local_model()
            except Exception as exc:
                logger.exception("Could not load the local embedding model")
                raise HTTPException(
                    status_code=503,
                    detail="Local embedding model unavailable. Run python -m app.parking_knowledge.download_model during setup.",
                ) from exc

            # Use a separate tokenizer with truncation disabled; never discard document text.
            if len(tokenizer.encode(model_input).ids) > MAX_EMBEDDING_TOKENS:
                raise HTTPException(
                    status_code=422,
                    detail="Text exceeds the local model's 512-token limit. Submit shorter, self-contained rules.",
                )
            try:
                vector = next(model.embed([model_input], batch_size=1)).tolist()
                if len(vector) != EMBEDDING_DIMENSIONS or not all(math.isfinite(value) for value in vector):
                    raise ValueError("Invalid local embedding")
                if not any(value != 0 for value in vector):
                    raise ValueError("Zero vector cannot be used for cosine search")
                return vector
            except Exception as exc:
                logger.exception("Local embedding generation failed")
                raise HTTPException(status_code=503, detail="Local embedding generation failed") from exc
