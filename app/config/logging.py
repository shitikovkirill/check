# mypy: ignore-errors
import logging

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = __name__
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {"format": LOG_FORMAT},
        "access": {"format": LOG_FORMAT},
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": logging.StreamHandler,
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": logging.StreamHandler,
            "stream": "ext://sys.stdout",
        },
    }
    loggers: dict = {
        "uvicorn.error": {"level": "INFO", "handlers": ["default"], "propagate": False},
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["access"],
            "propagate": False,
        },
    }
    root: dict = {"level": LOG_LEVEL, "handlers": ["default"], "propagate": False}
