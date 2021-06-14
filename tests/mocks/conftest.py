"""Mocks used to test application."""

from typing import NamedTuple
from typing import Optional


class TextTagMock(NamedTuple):
    """Mock of text field of bs4 :obj:`Tag`"""

    string: Optional[str]


class UrlTagsMock(NamedTuple):
    """Mock of url field of bs4 :obj:`Tag`"""

    next: Optional[str]


class MiniSoupMock(NamedTuple):
    """Mock of bs4 :obj:`Tag` with only two fields."""

    title: Optional[TextTagMock]
    description: Optional[TextTagMock]


class SoupMock(NamedTuple):
    """Mock of bs4 :obj:`Tag` with all fields."""

    title: Optional[TextTagMock]
    description: Optional[TextTagMock]
    link: Optional[UrlTagsMock]
    author: Optional[TextTagMock]
    comments: Optional[UrlTagsMock]
    pubdate: Optional[TextTagMock]
    source: Optional[UrlTagsMock]
