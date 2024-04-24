from __future__ import annotations
import os
from pathlib import Path
from typing import TYPE_CHECKING

from chromadb import PersistentClient

if TYPE_CHECKING:
    from chromadb.api import ClientAPI

__all__ = ["get_chroma_client"]


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, "db")

storage_path = Path("./new_data").resolve()

def get_chroma_client() -> ClientAPI:
    client = PersistentClient(path=str(storage_path))

    client.get_or_create_collection("docs")

    return client


class ChromaClient(object):
    """docstring for ChromaClient"""
    def __init__(self, db_path="./new_data"):
        self.db_path = db_path
        self.client = PersistentClient(path=str(Path(self.db_path).resolve()))

    def get_nodes_collection(self, collection):
        return self.client.get_or_create_collection(collection)

    def fetch_collection(self, collection):
        return self.client.get_collection(collection)

    def filter_collection(self, params):
        collection.query(
            query_texts=["doc10", "thus spake zarathustra", ...],
            n_results=10,
            where={"metadata_field": "is_equal_to_this"},
            where_document={"$contains":"search_string"}
        )

    def delete_collection(self, collecton):
        pass