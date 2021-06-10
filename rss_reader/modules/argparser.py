from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from datetime import datetime
from os.path import exists


class Argparser:
    """ Class for handling command line arguments """

    def __init__(self, logger):
        self.__logger = logger
        self.__parser = ArgumentParser(description='Pure Python command-line RSS reader.')
        self.__create_arguments()

    def __create_arguments(self):
        """Creating a set of arguments for command line input"""
        self.__parser.add_argument('source', type=str, help='RSS URL', nargs='?')
        self.__parser.add_argument('--version', help='Print version info', action='store_true')
        self.__parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
        self.__parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
        self.__parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided',
                                   default=False)
        self.__parser.add_argument('--date', type=str, metavar='YYYYMMDD', help='Print news for the specified date',
                                   default=False)
        self.__parser.add_argument('--to-html', type=str, metavar='PATH', help='Converts news to .html format',
                                   default=False)
        self.__parser.add_argument('--to-pdf', type=str, metavar='PATH', help='Converts news to .pdf format',
                                   default=False)

    def parse_arguments(self, argv):
        """
        Parsing arguments passed to the command line
        :return: argument dictionary
        """
        args = self.__parser.parse_args(argv).__dict__
        self.__validate_arguments(args)
        return args

    def __validate_arguments(self, args):
        """ Checking the correctness of the entered data """
        if (args.get('source') is None or not args.get('source')) \
                and args.get('version') is False \
                and args.get('date') is False:
            raise self.__parser.error('the following arguments are required: source')
        if args.get('date'):
            try:
                date = datetime.strptime(args['date'], "%Y%m%d")
                if date > datetime.now():
                    raise self.__parser.error('date cannot be more than today')
            except ValueError as err:
                raise self.__parser.error(err)
        if args.get('to_html'):
            if not exists(args.get('to_html')):
                raise self.__parser.error('directory "{}" does not exist'.format(args.get('to_html')))
        if args.get('to_pdf'):
            if not exists(args.get('to_pdf')):
                raise self.__parser.error('directory "{}" does not exist'.format(args.get('to_pdf')))

