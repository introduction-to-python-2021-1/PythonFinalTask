"""All utils used in the application."""

from __future__ import annotations

from datetime import datetime
from typing import cast
from typing import List
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import urlparse

from bs4 import Tag  # type: ignore
from dateutil import parser

from ap_rss_reader import ap_constants as const
from ap_rss_reader.ap_collections import Media
from ap_rss_reader.ap_constants import SUPPORTED_FIELDS
from ap_rss_reader.log import logger

if TYPE_CHECKING:
    from typing import Dict
    from typing import Tuple

    from ap_rss_reader.ap_typing import Article
    from ap_rss_reader.ap_typing import FieldName
    from ap_rss_reader.ap_typing import FieldParser
    from ap_rss_reader.ap_typing import FieldPrinter
    from ap_rss_reader.ap_typing import FieldValue

__all__ = ("parse_article", "print_article", "retrieve_title", "validate_url")


def validate_url(url: str) -> bool:
    """Check if 'url' string valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except (AttributeError, ValueError):
        return False


def _url_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve url from given field name.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and retrieved url.

    """
    field = getattr(soup, field_name)
    return (field_name, field.next if field else None)


def _date_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve date from given field name.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and retrieved date.

    """
    field = getattr(soup, field_name)
    return (field_name, parser.parse(field.string) if field else None)


def _multiple_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve data from fields with given name.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and list of
            retrieved values.

    """
    return (
        field_name,
        [
            value.string
            for value in soup.select(field_name)
            if value and value.string
        ],
    )


def _media_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve media data from given field.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and list with
            retrieved media.

    """
    field = getattr(soup, field_name)
    if field:
        return (
            const.FIELD_MEDIA,
            [
                Media(
                    type=(
                        field_name[len("media_") :]
                        if field_name.startswith("media_")
                        else cast(str, field_name)
                    ),
                    url=field["url"],
                    height=field["height"],
                    width=field["width"],
                )
            ],
        )
    return (const.FIELD_MEDIA, cast(List[Media], []))


def _enclosure_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve data from 'enclosure' field.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and retrieved field value.

    """
    return (
        const.FIELD_MEDIA,
        [
            Media(
                type=enclosure["type"],
                url=enclosure["url"],
                height=None,
                width=None,
            )
            for enclosure in soup.select(field_name)
            if enclosure and enclosure["type"] and enclosure["url"]
        ],
    )


def _text_field_parse(
    soup: Tag, field_name: FieldName
) -> Tuple[FieldName, FieldValue]:
    """Retrieve text from text field.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'
        field_name: field to be retrieved.

    Returns:
        Tuple with two elements: the new field name and retrieved field value.

    """
    field = getattr(soup, field_name)
    return (field_name, field.string if field else None)


PARSER_MAP: Dict[Tuple[FieldName, ...], FieldParser] = {
    (const.FIELD_LINK, const.FIELD_COMMENTS, const.FIELD_SOURCE): _url_parse,
    (const.FIELD_PUBDATE,): _date_parse,
    (const.FIELD_CATEGORY,): _multiple_parse,
    (const.FIELD_MEDIA_CONTENT, const.FIELD_MEDIA_THUMBNAIL): _media_parse,
    (const.FIELD_ENCLOSURE,): _enclosure_parse,
    (const.FIELD_DESCRIPTION, const.FIELD_AUTHOR): _text_field_parse,
}


def parse_article(soup: Tag) -> Article:
    """Parse item from rss channel.

    Args:
        soup: xml element 'rss' -> 'channel' -> 'item'

    Returns:
        Rss article as dict.

    """
    result: Article = {}

    title = retrieve_title(soup)
    if not title:
        return result

    result[const.FIELD_TITLE] = title
    for field_names in PARSER_MAP:
        for field_name in field_names:
            if getattr(soup, field_name):
                field_parser = PARSER_MAP[field_names]
                key, value = field_parser(soup, field_name)
                if (
                    key in result
                    and isinstance(result[key], list)
                    and isinstance(value, list)
                    and (values := cast(List[Union[Media, str]], result[key]))
                ):
                    values.extend(value)
                else:
                    result[key] = value
    return result


def _date_print(article: Article, key: FieldName) -> None:
    if key in article and isinstance(article[key], datetime):
        date = cast(datetime, article[key])
        logger.info(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}")


def _multiple_print(article: Article, key: FieldName) -> None:
    if key in article and isinstance(article[key], list) and article[key]:
        values = cast(List[Union[Media, str]], article[key])
        logger.info(f"{key.capitalize()}:")
        for count, value in enumerate(values, start=1):
            logger.info(f"\t- {value}{';' if count != len(values) else '.'}")


def _media_print(article: Article, key: FieldName) -> None:
    if key in article and isinstance(article[key], list) and article[key]:
        logger.info("Links:")
        medias = cast(List[Media], article[key])
        for count, media in enumerate(medias, start=1):
            logger.info(
                f"[{count}]: {media.url} ({media.type})"
                f"{';' if count != len(medias) else '.'}"
            )
        logger.info("\n")


def _text_field_print(article: Article, key: FieldName) -> None:
    if key in article and article[key]:
        logger.info(f"{key.capitalize()}: {article[key]}")


PRINTER_MAP: Dict[Tuple[FieldName, ...], FieldPrinter] = {
    (const.FIELD_PUBDATE,): _date_print,
    (const.FIELD_CATEGORY,): _multiple_print,
    (const.FIELD_MEDIA,): _media_print,
    (
        const.FIELD_TITLE,
        const.FIELD_DESCRIPTION,
        const.FIELD_AUTHOR,
        const.FIELD_LINK,
        const.FIELD_COMMENTS,
        const.FIELD_SOURCE,
    ): _text_field_print,
}


def print_article(article: Article) -> None:
    """Print rss channel article.

    Args:
        article: rss channel article.

    """
    for field_name in SUPPORTED_FIELDS:
        for printable_fields in PRINTER_MAP:
            if field_name in printable_fields:
                field_printer = PRINTER_MAP[printable_fields]
                field_printer(article, field_name)


def retrieve_title(soup: Tag) -> str:
    """Retrieve 'title' or 'description' field from soup.

    At least one of 'title' and 'description' field must exist.

    Args:
        soup: tag that'll be processed.

    Returns:
        String with 'title' or 'None'.

    """
    if (title := getattr(soup, const.FIELD_TITLE)) and title.string:
        return cast(str, title.string)
    if (
        description := getattr(soup, const.FIELD_DESCRIPTION)
    ) and description.string:
        return cast(str, description.string)
    return ""
