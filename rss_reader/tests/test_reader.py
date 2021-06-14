import pytest
import os
from rss_reader import RssReaderApp
from rss_reader.args import RssReaderArgs


def test_argparser():
    parser = RssReaderArgs(['--json', '--verbose', '--limit', '10', 'http://tut.by/rss.xml'])
    assert parser.args.json
    assert parser.args.verbose
    assert parser.args.limit == 10
    assert parser.args.source == 'http://tut.by/rss.xml'


def test_reader():
    app = RssReaderApp()
    path = os.path.dirname(__file__)
    sample = os.path.join(path, 'sample.xml')
    entries = app.rss_reader(sample, limit=2)
    assert entries is not None
    assert len(entries) == 2
    pass


def test_reader_print():
    app = RssReaderApp()
    path = os.path.dirname(__file__)
    sample = os.path.join(path, 'sample.xml')
    entries = app.rss_reader(sample, limit=2)
    assert entries is not None
    assert len(entries) == 2
    app.print_entries(entries, json_fmt=False)
    pass


def test_reader_print_json():
    app = RssReaderApp()
    path = os.path.dirname(__file__)
    sample = os.path.join(path, 'sample.xml')
    entries = app.rss_reader(sample, limit=2)
    assert entries is not None
    assert len(entries) == 2
    app.print_entries(entries, json_fmt=True)
    pass
