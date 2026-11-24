"""Storage and input limits shared by the knowledge module."""

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSIONS = 384
MAX_EMBEDDING_TOKENS = 512
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
# Bound request size before tokenization; the local tokenizer also enforces 512 tokens.
MAX_EMBEDDING_INPUT_BYTES = 8000
