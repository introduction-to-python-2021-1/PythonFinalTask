"""Provides useful objects."""
import os
import argparse
from pathvalidate.argparse import validate_filepath_arg

VERSION = "4.0"


def create_argument_parser(argv):
    """
    Creates argument parser using argparse module.

    Parameters:
        argv (list): Command line arguments

    Returns:
        (argparse.ArgumentParser): Argument parser
    """
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", nargs="?" if "--date" in argv else None, type=str, help="RSS URL")
    parser.add_argument("--version", action="version", version=f'"Version {VERSION}"', help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str, help="Return news topics which were published in specific date")
    parser.add_argument("--to-html", type=validate_filepath_arg, help="Save news in .html format by provided path")
    parser.add_argument("--to-pdf", type=validate_filepath_arg, help="Save news in .pdf format by provided path")

    return parser


def get_path_to_data(*args):
    """Returns an absolute path to directory "package_data" which contains package data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "package_data", *args)
