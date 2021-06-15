from argparse import ArgumentParser


def arg_parser() -> ArgumentParser:
    """ Creating argument parser object function. """
    parser = ArgumentParser(description='Simple RSS Reader')
    parser.add_argument('source', type=str, help='RSS URL', nargs='?')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=False,
                        help='Limit news topics if this parameter provided.'
                             ' If limit parameter is invalid, parser will output all news.')
    parser.add_argument('--date', type=str, metavar='YYYYMMDD', help='Print news for the specified date',
                        default=False)
    return parser
