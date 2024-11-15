from loguru import logger
import sys


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
    logger.add("logs/app.log", rotation="500 MB", retention="10 days", level="DEBUG")

    return logger
