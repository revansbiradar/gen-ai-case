from __future__ import annotations

from app.evaluate import evaluate
from app.ingest import ingest
from app.log import get_logger
from app.query import query

__all__ = ["main"]

logger = get_logger("main")


def main() -> None:
    logger.info("Started.")

    # ingest()

    response = query("Succinctly summarize what disturbes Victor's sleep?")

    if not response or not response:
        logger.info("No query response! Aborting...")
        return

    logger.info("Query response: %s", str(response))

    eval_response = evaluate(response)

    if not eval_response:
        logger.info("No eval response! Aborting...")
        return

    logger.info("Evaluated: %s", eval_response)

    logger.info("Complete.")
