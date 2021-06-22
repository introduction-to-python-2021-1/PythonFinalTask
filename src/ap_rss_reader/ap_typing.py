"""All types used in the application."""

from __future__ import annotations

from datetime import datetime
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union

from bs4 import Tag  # type: ignore

from ap_rss_reader.ap_collections import Media

FieldName = Literal[
    "title",
    "link",
    "description",
    "author",
    "category",
    "comments",
    "enclosure",
    "media",
    "media_content",
    "media_thumbnail",
    "pubdate",
    "source",
]
FieldValue = Optional[Union[datetime, str, List[Media], List[str]]]
Article = Dict[FieldName, FieldValue]
FieldHtmlConverter = Callable[[Article, FieldName], str]
FieldParser = Callable[[Tag, FieldName], Tuple[FieldName, FieldValue]]
FieldPrinter = Callable[[Article, FieldName], None]
