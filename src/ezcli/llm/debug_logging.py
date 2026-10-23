"""Configure local debug logging for LLM requests."""

import logging
from pathlib import Path

LLM_LOGGER_NAME = "ezcli.llm"
DEFAULT_LOG_PATH = Path("logs") / "llm-debug.json"


def configure_llm_logger(log_path: Path | None = None) -> logging.Logger:
    """Return an LLM logger that writes debug records to a local file."""
    logger = logging.getLogger(LLM_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    target_path = (log_path or DEFAULT_LOG_PATH).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            if Path(handler.baseFilename).resolve() == target_path:
                return logger

    handler = logging.FileHandler(target_path, encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger
