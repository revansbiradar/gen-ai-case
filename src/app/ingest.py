from __future__ import annotations

from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PDFReader
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.chroma import get_chroma_client
from app.common import Collections, get_embed_model
from app.log import get_logger

__all__ = ["ingest"]
logger = get_logger("ingest")


def ingest() -> None:
    logger.info("Starting..")

    client = get_chroma_client()
    collection = client.get_or_create_collection(Collections.Books.value)

    store = ChromaVectorStore(chroma_collection=collection)

    # TASK: Vectorize ./books/frankenstein.pdf into the chromadb collection
    # - create a vector store index from the "store", use get_embed_model() for the embed model
    # - The frankenstein book should be identified by a "book_id" of 1818
    # - Utilize a chunking strategy appropriate for a book
    # - Do not ingest the same book more than once if re-run

    logger.info("Complete.")
