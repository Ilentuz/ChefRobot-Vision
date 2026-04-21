"""Utilities for configured project logger creation."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGS_DIRECTORY_NAME: str = "logs"
LOG_FILE_NAME: str = "robot.log"
LOG_MAX_BYTES: int = 1_048_576
LOG_BACKUP_COUNT: int = 5
LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_project_logger(logger_name: str) -> logging.Logger:
    """Return a configured logger that writes to the project logs directory."""
    logger: logging.Logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    logs_path: Path = Path(LOGS_DIRECTORY_NAME)
    logs_path.mkdir(parents=True, exist_ok=True)
    log_file_path: Path = logs_path / LOG_FILE_NAME

    handler: RotatingFileHandler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    formatter: logging.Formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
