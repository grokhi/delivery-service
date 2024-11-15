import sys
from functools import wraps

from loguru import logger as base_logger

from src.core.config import settings


def setup_logging():
    base_logger.remove()
    base_logger.add(
        sys.stdout,
        format="<green>{level}:</green> <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> - <level>{message}</level> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
        level=settings.LOG_LEVEL,
    )
    base_logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG",
        backtrace=True,
        diagnose=True,
    )
    return base_logger


logger = setup_logging()
