from datetime import datetime
import sys

import argparse

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class handles command line arguments.
# Stores arguments, checks for correctness
class args_parser:
    def __init__(self):
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
                                 type=str,
                                 help="RSS URL")
        self.parser.add_argument("-ve", "--version",
                                 help="Info about version",
                                 action="version",
                                 version="%(prog)s version 0.1")
        self.parser.add_argument("-js", "--json",
                                 help="JSON",
                                 action="store_true")
        self.parser.add_argument("-vbs", "--verbose",
                                 help="logs",
                                 action="store_true")
        self.parser.add_argument("-li", "--limit",
                                 type=int,
                                 help="Limit")
        self.parser.add_argument("-d", "--date",
                                 type=str,
                                 help="Selection by dates in format: YearMonthDay, as an example: --date 20201201")

    # parses all command line parameters and stores them in class storage
    def __parse_Args(self):
        self.args_Space = self.parser.parse_args()

    def __args_Validation(self):

        # parameter <limit> validation
        if bool(self.args_Space.limit):
            if self.args_Space.limit < 0:
                logger.error("Bad parameter: --limit < 0 .")
                sys.exit()
            else:
                pass
        else:
            if self.args_Space.limit == 0:
                logger.warning("Bad parameter: --limit = 0, you will not see news")
            else:
                logger.info("--limit is void. See all news")

        # parameter <json> validation
        if type(self.args_Space.json) != bool:
            logger.error(
                "Bad parameter: --json. Do not use this parameter with value.")
            sys.exit()

        # parameter <verbose> validation
        if type(self.args_Space.verbose) != bool:
            logger.error(
                "Bad parameter: --verbose. Do not use this parameter with value.")
            sys.exit()
        # verbose check
        if self.args_Space.verbose:
            logger.handlers[1].setLevel("INFO")

        # parameter <date> validation
        if bool(self.args_Space.date):
            try:
                logger.info(datetime.strptime(self.args_Space.date, "%Y%m%d"))
            except ValueError:
                logger.error("Bad parameter : --date. Check --help")
                sys.exit()
