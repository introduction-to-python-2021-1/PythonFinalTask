"""All constants and literals used in the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict
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
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
DUMP_FILE: Final[str] = "ap-rss-reader-dump.json"

# Error messages
ERROR_CODE: Final[str] = "Error code: [{code}]"
ERROR_FAILED_DECODE: Final[str] = "ERROR: Failed to decode content."
ERROR_INCORRECT_SOURCE_ARG: Final[
    str
] = "'source' argument is incorrect url: %(url)s!"
ERROR_JSON_LOAD: Final[
    str
] = "ERROR: File cannot be read: decoding JSON has failed."
ERROR_NO_ADDRESS: Final[
    str
] = "ERROR: No address associated with host%(host)s."
ERROR_NO_DATA: Final[str] = "Sorry! There's no data that can be parsed."
ERROR_NO_URL: Final[str] = "Data cannot be loaded, because there's no 'url'!"
ERROR_SOMETHING_GOES_WRONG: Final[str] = "ERROR: Sorry! Something goes wrong."
ERROR_TIME_OUT: Final[str] = "ERROR: Read timed out from host%(host)s."
ERROR_OPEN_FILE: Final[
    str
] = "Sorry could not open or write to file (%(filename)s)."
ERROR_TOO_MANY_REDIRECTS: Final[str] = "ERROR: Too many redirects."
REQUEST_ERROR_MESSAGES: Final[Dict[int, str]] = {
    400: "ERROR: Bad request to url: {url}.",
    403: "ERROR: Access to '{url}' is forbidden.",
    404: "ERROR: Page '{url}' not found.",
    500: "ERROR: Server is not available for url: {url}.",
    503: "ERROR: Service unavailable for url: {url}.",
}

INFO_CHANNEL_WAS_CREATED: Final[
    str
] = "Rss channel was created with %(count)i article(s)!"
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
 <meta name="viewport" content="width=device-width, user-scalable=1>
 <meta http-equiv="X-UA-Compatible">
 <title>{title}</title>
</head>
<body>
<h1><a href="{url}">{title}</a></h1>
<p>{description}</p>
<br>
  {body}
</body>
</html>
"""
GREETING: Final[str] = (
    "The software is provided 'as is', without warranty of any kind,"
    " express or implied."
)
APP_TITLE: Final[str] = "AP RSS-reader"
