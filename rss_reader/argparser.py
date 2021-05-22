import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Python RSS-reader',
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
                        help='Outputs verbose status messages',
                        )

    parser.add_argument('--json',
                        action='store_true',
                        help='Outputs news in json format',
                        )

    parser.add_argument('--version',
                        action='version',
                        version='Rss reader 1.0.',
                        help='Prints version and stop',
                        )

    args = parser.parse_args()
    return args
