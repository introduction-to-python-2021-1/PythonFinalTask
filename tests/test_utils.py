# pylint: disable=missing-module-docstring

from __future__ import annotations

from typing import cast
from typing import NamedTuple
from typing import TYPE_CHECKING

from bs4 import Tag  # type: ignore
import pytest  # type: ignore

from ap_rss_reader import utils
from ap_rss_reader.utils import retrieve_title

if TYPE_CHECKING:
    from typing import Any
    from typing import Optional

    from ap_rss_reader.ap_collections import Media
    from ap_rss_reader.ap_typing import Article


class TextTagMock(NamedTuple):
    """Mock of text field of bs4 :obj:`Tag`"""

    string: Optional[str]


class SoupMock(NamedTuple):
    """Mock of bs4 :obj:`Tag`."""

    title: Optional[TextTagMock]
    description: Optional[TextTagMock]


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
            SoupMock(
                title=TextTagMock(string="title"),
                description=TextTagMock(string="description"),
            ),
            "title",
        ),
        (
            SoupMock(title=TextTagMock(string="title"), description=None),
            "title",
        ),
        (
            SoupMock(
                title=None, description=TextTagMock(string="description")
            ),
            "description",
        ),
    ],
    ids=lambda arg: f"{arg}",
)
def test_retrieve_title_valid_data(soup: SoupMock, result: str) -> None:
    assert result == retrieve_title(cast(Tag, soup))
