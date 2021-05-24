import argparse
import logging
import requests
from bs4 import BeautifulSoup
import json

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = None


def create_logger(verbose):
    """Creates a logger"""
    global logger
    if logger is None:
        logger = logging.getLogger()
    return logger

def command_arguments_parser(args):
    """ Adds positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.0")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    args = parser.parse_args(args)
    return args


