import pytest
from  rss_reader import RssReaderApp

def test_reader():
    app = RssReaderApp()
    entries = app.rss_reader('sample.xml', limit=2)
    assert entries != None
    assert len(entries) == 2
    pass