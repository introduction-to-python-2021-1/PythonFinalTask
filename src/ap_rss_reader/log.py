"""Create logger object with predefined handler."""

import logging
import sys

__all__ = ("logger",)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(stream_handler)
