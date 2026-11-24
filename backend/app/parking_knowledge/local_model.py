"""Load one cached CPU model per process, with downloads disabled at runtime."""

import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

from app.parking_knowledge.constants import EMBEDDING_MODEL


def model_cache_dir() -> str:
    default = Path(__file__).resolve().parents[2] / ".cache" / "embeddings"
    return os.getenv("LOCAL_EMBEDDING_CACHE_DIR", str(default))


@lru_cache(maxsize=1)
def load_local_model():
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from fastembed import TextEmbedding
    from tokenizers import Tokenizer

    model = TextEmbedding(
        model_name=EMBEDDING_MODEL,
        cache_dir=model_cache_dir(),
        local_files_only=True,
        threads=2,
        providers=["CPUExecutionProvider"],
    )
    tokenizer = Tokenizer.from_str(model.model.tokenizer.to_str())
    tokenizer.no_truncation()
    tokenizer.no_padding()
    return model, tokenizer
