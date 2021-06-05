import rss_reader.app_logger as app_logger
import rss_reader.feed_container as feed_container

import os
from pathlib import Path

logger = app_logger.get_logger(__name__)


class local_storage:
    def __init__(self, url):
        self.feed = feed_container.FeedContainer(url)
        self.tmp_path = Path("../tmp")
