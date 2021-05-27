import pytest
import os
from rss_reader import RssReaderApp


def test_reader():
    app = RssReaderApp()
    path = os.path.dirname(__file__)
    sample = os.path.join(path, 'sample.xml')
    entries = app.rss_reader(sample, limit=2)
    assert entries is not None
    assert len(entries) == 2
    pass
