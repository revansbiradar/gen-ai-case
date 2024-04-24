from __future__ import annotations

import logging

__all__ = ["get_logger"]


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
    )

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('app.log')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)


    logger.setLevel(logging.DEBUG)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
