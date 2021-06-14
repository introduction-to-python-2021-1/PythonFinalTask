# pylint: disable=missing-module-docstring

from __future__ import annotations

from typing import cast
from typing import TYPE_CHECKING

from bs4 import Tag  # type: ignore
import pytest  # type: ignore

from ap_rss_reader import ap_constants as const
from ap_rss_reader import utils
from tests.mocks.conftest import MiniSoupMock
from tests.mocks.conftest import TextTagMock

if TYPE_CHECKING:
    from typing import Any

    from ap_rss_reader.ap_collections import Media
    from ap_rss_reader.ap_typing import Article
    from ap_rss_reader.ap_typing import FieldName


def test_validate_url_valid_data(valid_url: str) -> None:
    assert utils.validate_url(valid_url)


def test_validate_url_invalid_data(invalid_url: str) -> None:
    assert not utils.validate_url(invalid_url)


def test_date_print_valid_data(
    caplog: Any, valid_article_pubdate: Article, date_str: str
) -> None:
    caplog.clear()
    utils.print_article(valid_article_pubdate)
    assert f"Date: {date_str}" == [r.message for r in caplog.records][0]


def test_multiple_print_valid_data(
    caplog: Any, valid_article_category: Article
) -> None:
    caplog.clear()
    utils.print_article(valid_article_category)
    first, second, third, *_ = (r.message for r in caplog.records)
    assert first == "Category:"
    assert second == "\t- category;"
    assert third == "\t- category."


def test_media_print_valid_data(
    caplog: Any, valid_article_media: Article, media: Media
) -> None:
    caplog.clear()
    utils.print_article(valid_article_media)
    first, second, *_ = (r.message for r in caplog.records)
    assert first == "Links:"
    assert second == f"[1]: {media.url} ({media.type})."


def test_text_field_print_valid_data(
    caplog: Any, valid_article_title: Article
) -> None:
    caplog.clear()
    utils.print_article(valid_article_title)
    first, *_ = (r.message for r in caplog.records)
    assert first == "Title: title"


@pytest.mark.parametrize(
    ("soup", "result"),
    [
        (
            MiniSoupMock(
                title=TextTagMock(string="title"),
                description=TextTagMock(string="description"),
            ),
            "title",
        ),
        (
            MiniSoupMock(title=TextTagMock(string="title"), description=None),
            "title",
        ),
        (
            MiniSoupMock(
                title=None, description=TextTagMock(string="description")
            ),
            "description",
        ),
    ],
    ids=lambda arg: f"{arg}",
)
def test_retrieve_title_valid_data(soup: MiniSoupMock, result: str) -> None:
    assert result == utils.retrieve_title(cast(Tag, soup))


@pytest.mark.parametrize(
    "field",
    [
        const.FIELD_TITLE,
        const.FIELD_LINK,
        const.FIELD_DESCRIPTION,
        const.FIELD_AUTHOR,
        const.FIELD_COMMENTS,
        const.FIELD_SOURCE,
    ],
    ids=lambda arg: f"{arg}",
)
def test_parse_article_valid_data(
    field: FieldName, valid_article: Article, valid_soup: MiniSoupMock
) -> None:
    soup = cast(Tag, valid_soup)
    assert valid_article[field] == utils.parse_article(soup)[field]
