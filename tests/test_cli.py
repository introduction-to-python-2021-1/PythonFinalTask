# pylint: disable=missing-module-docstring

from __future__ import annotations

from typing import TYPE_CHECKING

from ap_rss_reader.ap_constants import HELLO_WORLD
from ap_rss_reader.cli import main

if TYPE_CHECKING:
    from typing import Any


def test_main(caplog: Any) -> None:
    caplog.clear()
    main()
    assert [HELLO_WORLD] == [record.message for record in caplog.records]
