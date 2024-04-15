from __future__ import annotations

from typing import TYPE_CHECKING

from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.chroma import get_chroma_client
from app.common import Collections, get_embed_model
from app.log import get_logger

if TYPE_CHECKING:
    from llama_index.core.base.response.schema import RESPONSE_TYPE
    from llama_index.core.schema import QueryType

__all__ = ["query"]

logger = get_logger("query")


def query(question: QueryType) -> RESPONSE_TYPE | None:
    logger.info("Starting..")

    client = get_chroma_client()
    collection = client.get_or_create_collection(Collections.Books.value)

    llama = Ollama(
        base_url="http://localhost:11434",
        model="llama2",
        request_timeout=300,
    )

    store = ChromaVectorStore(chroma_collection=collection)

    # TASK: Query the vector database and use llama2 LLM to get an answer to the passed in question.
    # Return: The Response object from the query engine.

    return None
