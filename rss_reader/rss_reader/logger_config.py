"""Creates a unique logger."""
import logging

logging.basicConfig(level=logging.WARNING, format="%(message)s")

logger = None


def get_logger():
    """Returns the same logger for each call."""
    global logger

    if logger is None:
        logger = logging.getLogger()

    return logger
