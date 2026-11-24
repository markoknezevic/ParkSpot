"""One-time model download: python -m app.parking_knowledge.download_model."""

from app.parking_knowledge.constants import EMBEDDING_MODEL
from app.parking_knowledge.local_model import model_cache_dir


def main() -> None:
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from fastembed import TextEmbedding

    TextEmbedding(
        model_name=EMBEDDING_MODEL,
        cache_dir=model_cache_dir(),
        threads=2,
        providers=["CPUExecutionProvider"],
    )
    print(f"Local embedding model ready: {EMBEDDING_MODEL}")


if __name__ == "__main__":
    main()
