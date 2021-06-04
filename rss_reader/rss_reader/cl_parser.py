import sys

import argparse

import rss_reader.app_logger as app_logger

logger = app_logger.get_logger(__name__)


# This class handles command line arguments.
# Stores arguments, checks for correctness
class args_Parser:
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
            logger.warning("Bad parameter: --limit = 0, you will not see news")

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
