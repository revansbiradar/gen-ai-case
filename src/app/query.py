from __future__ import annotations

from typing import TYPE_CHECKING
from app.common import (
        get_llama,
        load_stored_index
    )
if TYPE_CHECKING:
    from llama_index.core.base.response.schema import RESPONSE_TYPE
    from llama_index.core.schema import QueryType

from app.log import get_logger

__all__ = ["query"]

logger = get_logger("query")


def query(question: QueryType) -> RESPONSE_TYPE | None:
    logger.info("Starting..")
    
    sentence_index, base_index = load_stored_index()
    # # TASK: Query the vector database and use llama2 LLM to get an answer to the passed in question.
    # # Return: The Response object from the query engine.

    sentence_engine = sentence_index.as_query_engine(similarity_top_k=2)
    base_engine = base_index.as_query_engine(similarity_top_k=2)
    response = base_engine.query(question)
    print("response", response)
    return sentence_engine.query(question)
