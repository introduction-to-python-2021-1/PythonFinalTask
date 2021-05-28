import argparse


class argsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="RSS_reader",
                                              formatter_class=argparse.RawDescriptionHelpFormatter,
                                              description="---------------------------------------------------------\n"
                                                          "This script allows you to view RSS feeds in the console. \n"
                                                          "---------------------------------------------------------\n",
                                              add_help=True)
        self.__parametrsInit()
        self.__parseArgs()

    def __parametrsInit(self):
        self.parser.add_argument("source",
                                 type=str,
                                 help="RSS URL")
        self.parser.add_argument("-v", "--version",
                                 help="Info about version",
                                 action="version",
                                 version="%(prog)s version 0.1")
        self.parser.add_argument("-j", "--json",
                                 help="JSON",
                                 action="store_true")
        self.parser.add_argument("-vbs", "--verbose",
                                 help="logs",
                                 action="store_true")
        self.parser.add_argument("-li", "--limit",
                                 type=int,
                                 help="Limit")

    def __parseArgs(self):
        self.args_Space = self.parser.parse_args()