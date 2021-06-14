# pylint: disable=missing-module-docstring,redefined-outer-name

from __future__ import annotations

from datetime import datetime
from typing import cast
from typing import TYPE_CHECKING

import pytest  # type: ignore

from ap_rss_reader import ap_constants as const
from ap_rss_reader.ap_collections import Media
from ap_rss_reader.ap_typing import Article

if TYPE_CHECKING:
    from typing import Any


@pytest.fixture(
    params=[
        "http://abc.abc",
        "https://a.a?a=xml",
    ],
    ids=lambda url: f"{url=}",
)
def valid_url(request: Any) -> str:
    return cast(str, request.param)


@pytest.fixture(
    params=["://abc.abc", "https//a.a?a=xml", "http://", 1],
    ids=lambda url: f"{url=}",
)
def invalid_url(request: Any) -> str:
    return cast(str, request.param)


@pytest.fixture()
def date_datetime() -> datetime:
    return datetime(2020, 6, 6, 0, 0, 1)


@pytest.fixture()
def date_str(date_datetime: datetime) -> str:
    return date_datetime.strftime(const.DATETIME_FORMAT)


@pytest.fixture()
def media() -> Media:
    return Media(type="type", url="url", height=None, width=None)


@pytest.fixture()
def valid_article_pubdate(date_datetime: datetime) -> Article:
    return cast(
        Article,
        {
            const.FIELD_PUBDATE: date_datetime,
        },
    )


@pytest.fixture()
def valid_article_category() -> Article:
    return cast(
        Article,
        {
            const.FIELD_CATEGORY: ["category", "category"],
        },
    )


@pytest.fixture()
def valid_article_media(media: Media) -> Article:
    return cast(
        Article,
        {
            const.FIELD_MEDIA: [media],
        },
    )


@pytest.fixture()
def valid_article_title() -> Article:
    return cast(
        Article,
        {
            const.FIELD_TITLE: "title",
        },
    )


@pytest.fixture()
def valid_article(date_datetime: datetime, media: Media) -> Article:
    return cast(
        Article,
        {
            const.FIELD_TITLE: "title",
            const.FIELD_LINK: "link",
            const.FIELD_DESCRIPTION: "description",
            const.FIELD_AUTHOR: "author",
            const.FIELD_CATEGORY: ["category", "category"],
            const.FIELD_COMMENTS: "comments",
            const.FIELD_MEDIA: [media],
            const.FIELD_PUBDATE: date_datetime,
            const.FIELD_SOURCE: "source",
        },
    )
