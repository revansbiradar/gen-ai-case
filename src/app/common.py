from __future__ import annotations
import sys
import os
from pathlib import Path
from enum import Enum

from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader, Document
from llama_index.core.storage import StorageContext
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter, SentenceWindowNodeParser, SimpleNodeParser
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
)
from llama_index.core.ingestion import IngestionPipeline
from app.chroma import ChromaClient


__all__ = ["Collections", "get_embed_model"]

FILE_PATH = "/home/admin1/Desktop/AIML/gen-ai/gen-ai-study-v1/gen-ai-study/books/frankenstein.pdf"

class Collections(Enum):
    Books = "books"


def get_llama() -> Ollama:
    llama = Ollama(
        base_url="http://localhost:11434",
        model="llama2",
        request_timeout=300,
    )
    return llama

def get_embed_model():
    return HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")

# def get_embed_model() -> HuggingFaceEmbedding:
#     return HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

def get_chroma_vector_store(collection) -> ChromaVectorStore:
    return ChromaVectorStore(chroma_collection=collection)

def get_storage_context(vector_store) -> StorageContext:
    return StorageContext.from_defaults(vector_store=vector_store, docstore=SimpleDocumentStore(),)

def get_service_context(nodes=[]) -> ServiceContext:
    llm = get_llama()
    if nodes:
        service_context = ServiceContext.from_defaults(
                                                    embed_model=get_embed_model(), 
                                                    llm=llm,
                                                    node_parser=nodes
                                                )
    else:
        service_context = ServiceContext.from_defaults(
                                                    embed_model=get_embed_model(), 
                                                    llm=llm,
                                                )    
    return service_context


def simple_dir_loader():
    return SimpleDirectoryReader('./books/').load_data()


def get_base_nodes():
    sentence_node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text"
    )
    #base_node_parser = SentenceSplitter(llm=llm)
    base_node_parser = SimpleNodeParser()
    #
    documents = simple_dir_loader()
    nodes = sentence_node_parser.get_nodes_from_documents(documents)
    base_nodes = base_node_parser.get_nodes_from_documents(documents)
    # print("nodes, base_nodes", nodes[10])
    return nodes, base_nodes

def load_stored_index():

    client = ChromaClient()
    # get an existing collection
    sentence_collection = client.fetch_collection("sentence_nodes")
    nodes_collection = client.fetch_collection("base_nodes")

    print("sentence_collection", sentence_collection.id)
    print("nodes_collection", nodes_collection.id)

    # fetch exsiting collection store 
    sentence_store = get_chroma_vector_store(sentence_collection)
    base_store = get_chroma_vector_store(nodes_collection)

    service_context = get_service_context()

    # Load index from the storage context
    sentence_index = VectorStoreIndex.from_vector_store(vector_store=sentence_store, service_context=service_context)
    base_index = VectorStoreIndex.from_vector_store(vector_store=base_store, service_context=service_context)

    return sentence_index, base_index


def load_pdf_data():
    document_reader = PDFReader()
    return document_reader.load_data(Path(FILE_PATH))

