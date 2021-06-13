"""All constants and literals used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final
    from typing import List
    from typing import Literal

    from ap_rss_reader.ap_typing import FieldName


FIELD_TITLE: Literal["title"] = "title"
FIELD_LINK: Literal["link"] = "link"
FIELD_PUBDATE: Literal["pubdate"] = "pubdate"
FIELD_AUTHOR: Literal["author"] = "author"
FIELD_SOURCE: Literal["source"] = "source"
FIELD_DESCRIPTION: Literal["description"] = "description"
FIELD_CATEGORY: Literal["category"] = "category"
FIELD_COMMENTS: Literal["comments"] = "comments"
FIELD_MEDIA: Literal["media"] = "media"
FIELD_MEDIA_CONTENT: Literal["media_content"] = "media_content"
FIELD_MEDIA_THUMBNAIL: Literal["media_thumbnail"] = "media_thumbnail"
FIELD_ENCLOSURE: Literal["enclosure"] = "enclosure"
# This variable determine in what order the fields will be printed.
SUPPORTED_FIELDS: List[FieldName] = [
    FIELD_TITLE,
    FIELD_LINK,
    FIELD_PUBDATE,
    FIELD_AUTHOR,
    FIELD_SOURCE,
    FIELD_DESCRIPTION,
    FIELD_CATEGORY,
    FIELD_COMMENTS,
    FIELD_MEDIA,
    FIELD_MEDIA_CONTENT,
    FIELD_MEDIA_THUMBNAIL,
    FIELD_ENCLOSURE,
]
DATE_OR_SOURCE_IS_REQUIRED: Final[
    str
] = "At least one of the 'date' or 'source' arguments must be specified!\n"
DUMP_FILE: Final[str] = "ap-rss-reader-dump.json"

# Error messages
ERROR_CODE = "Error code: [{code}]"
ERROR_FAILED_DECODE = "ERROR: Failed to decode content."
ERROR_INCORRECT_SOURCE_ARG = "'source' argument is incorrect url: %(url)s!"
ERROR_JSON_LOAD = "ERROR: File cannot be read: decoding JSON has failed."
ERROR_NO_ADDRESS = "ERROR: No address associated with host%(host)s."
ERROR_NO_DATA = "Sorry! There's no data that can be parsed."
ERROR_NO_URL = "Data cannot be loaded, because there's no 'url'!"
ERROR_SOMETHING_GOES_WRONG = "ERROR: Sorry! Something goes wrong."
ERROR_TIME_OUT = "ERROR: Read timed out from host%(host)s."
ERROR_TOO_MANY_REDIRECTS = "ERROR: Too many redirects."
REQUEST_ERROR_MESSAGES = {
    400: "ERROR: Bad request to url: {url}.",
    403: "ERROR: Access to '{url}' is forbidden.",
    404: "ERROR: Page '{url}' not found.",
    500: "ERROR: Server is not available for url: {url}.",
    503: "ERROR: Service unavailable for url: {url}.",
}

INFO_CHANNEL_WAS_CREATED = "Rss channel was created with %(count)i article(s)!"

GREETING: Final[str] = (
    "The software is provided 'as is', without warranty of any kind,"
    " express or implied."
)
APP_TITLE: Final[str] = "AP RSS-reader"
