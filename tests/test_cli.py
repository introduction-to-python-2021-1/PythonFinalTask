# pylint: disable=missing-module-docstring

from __future__ import annotations

from argparse import ArgumentParser
from typing import TYPE_CHECKING

from ap_rss_reader.ap_constants import GREETING
from ap_rss_reader.cli import create_parser
from ap_rss_reader.cli import main

if TYPE_CHECKING:
    from typing import Any


def test_create_parser() -> None:
    parser: ArgumentParser = create_parser()
    assert isinstance(parser, ArgumentParser)


def test_main(caplog: Any) -> None:
    caplog.clear()
    main()
    assert GREETING == [record.message for record in caplog.records][0]


def test_arg_version_exist() -> None:
    args = create_parser().parse_args(["https://a.b", "--verbose"])
    assert hasattr(args, "source")
    assert hasattr(args, "verbose")
