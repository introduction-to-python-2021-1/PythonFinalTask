from datetime import datetime
import sys

import argparse

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class handles command line arguments.
# Stores arguments, checks for correctness
class args_parser():
    def __init__(self, argv):
        self.command_line_argv = argv
        self.parser = argparse.ArgumentParser(prog="RSS_reader",
                                              formatter_class=argparse.RawDescriptionHelpFormatter,
                                              description="---------------------------------------------------------\n"
                                              "This script allows you to view RSS feeds in the console. \n"
                                              "---------------------------------------------------------\n",
                                              add_help=True)
        self.__parameters_init()
        self.__parse_Args()
        self.__args_Validation()
        logger.info(f"\nRSS Channel positional parameter: {self.args_Space.source}\n"
                    f"--json optional parameter: {self.args_Space.json}\n"
                    f"--verbose optional parameter: {self.args_Space.verbose}\n"
                    f"--limit optional parameter: {self.args_Space.limit}\n")

    # initialization of all arguments
    def __parameters_init(self):
        self.parser.add_argument("source",
                                 nargs='?',
                                 type=str,
                                 help="RSS URL")
        self.parser.add_argument("-ve", "--version",
                                 help="Info about version",
                                 action="version",
                                 version="%(prog)s version 2")
        self.parser.add_argument("-js", "--json",
                                 help="JSON",
                                 action="store_true")
        self.parser.add_argument("-vbs", "--verbose",
                                 help="logs in stdout",
                                 action="store_true")
        self.parser.add_argument("-li", "--limit",
                                 type=int,
                                 help="Limit")
        self.parser.add_argument("-d", "--date",
                                 type=str,
                                 help="Selection by dates in format: YearMonthDay, as an example: --date 20201201")
        self.parser.add_argument("-2html", "--to_html",
                                 help="convert news into html file",
                                 action="store_true")
        self.parser.add_argument("-2pdf", "--to_pdf",
                                 help="convert news into pdf file",
                                 action="store_true")

    # parses all command line parameters and stores them in class storage
    def __parse_Args(self):
        self.args_Space = self.parser.parse_args(self.command_line_argv)

    # arguments validation
    def __args_Validation(self):

        # verbose check
        if self.args_Space.verbose:
            print("govno")
            print(logger.handlers[1])
            logger.handlers[1].setLevel("INFO")
            print(logger.handlers[1])

        # parameter <limit> validation
        if bool(self.args_Space.limit):
            if self.args_Space.limit < 0:
                logger.error("Bad parameter: --limit < 0 .")
                sys.exit()
        else:
            logger.warning("Bad parameter: --limit = 0, you will not see news")
            logger.info("--limit is void. See all news")

        # parameter <date> validation
        if bool(self.args_Space.date):
            try:
                logger.info(datetime.strptime(self.args_Space.date, "%Y%m%d"))
            except ValueError:
                logger.error("Bad parameter : --date. Check --help")
                sys.exit()
