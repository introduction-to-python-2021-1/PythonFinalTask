from parser import ParserError

import feedparser
import pytest
import requests

from rss_reader.main import db_obj, cache_news, get_news_from_cache, format_news_to_print, parse_feed
from rss_reader.parser import parse_args
from rss_reader.converter import Converter, FPDF, Image, Template


def test_parse_args():
    args = parse_args(
        ["https://news.yahoo.com/rss/", "--date",  "20210613", "--to-html", "--json", "--verbose", "--limit", "2"]
    )
    assert args.source == "https://news.yahoo.com/rss/"
    assert args.date == "20210613"
    assert args.convert_type == "html"
    assert args.json is True
    assert args.verbose is True
    assert args.limit == 2


def test_parse_feed1(mocker):
    mocker.patch.object(feedparser, "parse", return_value=mocker.Mock(entries=["feed"]))
    mocker.patch.object(requests, "get", return_value=True)
    feed = parse_feed("https://example.com")
    assert feed is not None


def test_parse_feed(mocker):
    mocker.patch.object(feedparser, "parse", return_value=mocker.Mock(entries=[]))
    with pytest.raises(SystemExit):
        parse_feed("https://example.com")


def test_format_news_to_print1():
    content = format_news_to_print(
        [
            {
                "source": "source",
                "pubdate": "20210101",
                "title": "title",
                "image": "image",
                "link": "link"
            }
        ]
    )
    assert content == [{"source": "source", "pubdate": "20210101", "title": "title", "image": "image", "link": "link"}]


def test_format_news_to_print():
    content = format_news_to_print(
        [{"source": "source", "pubdate": "20210101", "title": "title", "image": None, "link": "link"}]
    )
    assert content == [{"source": "source", "pubdate": "20210101", "title": "title", "link": "link"}]


def test_cache_news1(mocker):
    mocker.patch.object(db_obj, "add_news", return_value=None)
    assert cache_news(
        [{"source": "source", "pubdate": "20210101", "title": "title", "image": "image", "link": "link"}]
    ) is None


def test_get_news_from_cache1(mocker):
    mocker.patch.object(
        db_obj,
        "select_news_from_cache",
        return_value=[
            {"date": "20210101", "title": "title", "image": "image", "link": "link"}
        ]
    )
    assert get_news_from_cache("20210101", None) == [
        {"date": "20210101", "title": "title", "image": "image", "link": "link"}
    ]


def test_get_news_from_cache2(mocker):
    mocker.patch.object(db_obj, "select_news_from_cache", return_value=None)
    with pytest.raises(SystemExit):
        get_news_from_cache("20210101", None)


def test_get_news_from_cache3(mocker):
    mocker.patch.object(db_obj, "select_news_from_cache", side_effect=ParserError)
    with pytest.raises(SystemExit):
        get_news_from_cache("20210", None)


def test_converter_pdf(mocker):
    mocker.patch.object(FPDF, "__init__", return_value=None)
    mocker.patch.object(FPDF, "add_page", return_value=None)
    mocker.patch.object(FPDF, "set_font", return_value=None)
    mocker.patch.object(FPDF, "cell", return_value=None)
    mocker.patch.object(FPDF, "image", return_value=None)
    mocker.patch.object(Image, "open", return_value=None)
    mocker.patch.object(FPDF, "output", return_value=None)

    content = [{"pubdate": "20210101", "title": "title", "image": "image", "image_path": "image_path", "link": "link"}]
    converter = Converter("pdf", "/some/path")
    converter.execute(content)

    FPDF.add_page.assert_called()
    FPDF.set_font.assert_called()
    FPDF.cell.assert_called()
    FPDF.image.assert_called()
    FPDF.output.assert_called()
