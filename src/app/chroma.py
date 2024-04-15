from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from chromadb import PersistentClient

if TYPE_CHECKING:
    from chromadb.api import ClientAPI

__all__ = ["get_chroma_client"]


def get_chroma_client() -> ClientAPI:
    client = PersistentClient(path=str(Path("./data").resolve()))

    client.get_or_create_collection("docs")

    return client
