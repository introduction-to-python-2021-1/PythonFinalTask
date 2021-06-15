import argparse

from rss_reader.constants import VERSION


def parse_args(args):
    """Parse console arguments"""
    parser = argparse.ArgumentParser(description="Pure Python RSS reader")

    parser.add_argument("source", nargs="?", type=str, default=None, help="RSS URL")
    parser.add_argument("--version", action="version", version=f"Version of RSS reader: {VERSION}",
                        help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=0, help="Limit news topics if this parameter provided "
                                                             "(If limit more or less then length of feed "
                                                             "it is set by default = length feed).")
    parser.add_argument("--date", type=str, default=None, help="Outputs news by date from cache"
                                                               "(It should take a date in YYYYMMDD format.).")
    parser.add_argument("--to-html", action="store_const", const="html", dest="convert_type", default=None)
    parser.add_argument("--to-pdf", action="store_const", const="pdf", dest="convert_type", default=None)
    return parser.parse_args(args)
