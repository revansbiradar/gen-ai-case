from __future__ import annotations

from enum import Enum

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

__all__ = ["Collections", "get_embed_model"]


class Collections(Enum):
    Books = "books"


def get_embed_model() -> HuggingFaceEmbedding:
    return HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
