from __future__ import annotations
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, ServiceContext

from app.chroma import ChromaClient
from app.common import (
    Collections,
    get_llama,
    get_embed_model,
    simple_dir_loader,
    get_base_nodes,
    get_chroma_vector_store,
    get_storage_context,
    get_service_context
)
from app.log import get_logger

__all__ = ["ingest"]
logger = get_logger("ingest")



def vector_storages():
    sentence_collection = ChromaClient().get_nodes_collection("sentence_nodes")
    base_collection = ChromaClient().get_nodes_collection("base_nodes")

    sentence_store = get_chroma_vector_store(sentence_collection)
    base_store = get_chroma_vector_store(base_collection)

    sentence_storage = get_storage_context(sentence_store)
    base_storage = get_storage_context(base_store)

    return sentence_storage, base_storage


def ingest() -> None:
    logger.info("Starting..")
    # print(sentence_storage, base_storage)

    # if not bool(sentence_storage):
    llm = get_llama()
    embed_model = get_embed_model()
    nodes, base_nodes = get_base_nodes()
    sentence_storage, base_storage = vector_storages()
    sentence_storage.docstore.add_documents(nodes)
    ctx_sentence = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=nodes
    )
    sentence_index = VectorStoreIndex(nodes, storage_context=sentence_storage, service_context=ctx_sentence)
    sentence_path = str(Path("./new_data/sentence_nodes").resolve())
    sentence_index.storage_context.persist(sentence_path)

    base_storage.docstore.add_documents(base_nodes)
    ctx_base = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=base_nodes
    )
    base_index = VectorStoreIndex(base_nodes, storage_context=base_storage, service_context=ctx_base)
    base_path = str(Path("./new_data/base_nodes").resolve())
    base_index.storage_context.persist(base_path)

    # TASK: Vectorize ./books/frankenstein.pdf into the chromadb collection
    # - create a vector store index from the "store", use get_embed_model() for the embed model
    # - The frankenstein book should be identified by a "book_id" of 1818
    # - Utilize a chunking strategy appropriate for a book
    # - Do not ingest the same book more than once if re-run
    # query_engine = index.as_query_engine(similarity_top_k=2)
    # response = query_engine.query("Succinctly summarize what disturbes Victor's sleep?")
    # print("response ========", response)
    logger.info("Complete.")
