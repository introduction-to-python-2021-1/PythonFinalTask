"""
This module provides tools for parsing arguments
"""


import argparse


def get_args():
    """
    Parses arguments
    """
    parser = argparse.ArgumentParser(description='Python rss_reader',
                                     prog='rss_parser',
                                     )

    parser.add_argument('url',
                        type=str,
                        help='URL to parse.',
                        )

    parser.add_argument('--limit',
                        type=int,
                        default=None,
                        help='Limit news topics if provided',
                        )

    parser.add_argument('--verbose',
                        action='store_true',
                        help='Output verbose status messages',
                        )

    parser.add_argument('--json',
                        action='store_true',
                        help='Output news in json format',
                        )

    parser.add_argument('--version',
                        action='version',
                        version='Rss rss_reader 1.0.',
                        help='Print version and stop',
                        )

    parser.add_argument('--date',
                        type=str,
                        help='Return news with the specified data',
                        default='',
                        )

    parser.add_argument('--to-pdf',
                        type=str,
                        help='Convert news in pdf format',
                        default=None,
                        metavar='PATH',
                        )

    parser.add_argument('--to-html',
                        type=str,
                        help='Convert news in html format',
                        default=None,
                        metavar='PATH',
                        )

    args = parser.parse_args()
    return args
