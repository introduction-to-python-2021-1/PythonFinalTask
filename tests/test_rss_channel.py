# pylint: disable=missing-module-docstring

from __future__ import annotations

from ap_rss_reader.rss_channel import RssChannel


def test_rss_channel_init_default() -> None:
    rss_channel = RssChannel()
    assert not rss_channel


def test_rss_channel_init_limit() -> None:
    rss_channel = RssChannel(limit=1)
    assert 1 == rss_channel.limit


def test_rss_channel_limit_setter() -> None:
    rss_channel = RssChannel(limit=1)
    rss_channel.limit = 2
    assert 2 == rss_channel.limit


def test_rss_channel_url(valid_url: str) -> None:
    rss_channel = RssChannel(url=valid_url)
    assert valid_url == rss_channel.url
