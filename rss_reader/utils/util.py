"""
    This module contain classes and functions which are make
    work of my_rss_reader easier and more convenient
"""
import os
import re


def create_directory(full_path: str):
    """
    Method create directory for placing file if it is not exist
    :param full_path: full path to file
    :return: created directory
    """

    directory = ""
    if re.search(r'\.\w+$', full_path):
        parts = re.findall(r"^(.+?)(?:[/\\])(\w+\.\w+)\s*$", full_path)
        directory = parts[0][0] if parts else ""
    else:
        directory = full_path

    if directory:
        if not os.path.exists(directory):
            os.makedirs(directory)
    return directory


def log(show_on_console: bool = True, msg: str = "", flag: str = ""):
    """
    :param show_on_console: do we show log on console or not
    :param msg: message to be shown
    :param flag: specified what type message is this. Your may pass INFO, WARNING, ERROR or
    whatever you want to specify your message. Or you may skip in. Empty string by default
    :return: None
    """
    message = "{0}{1}".format(f"[{flag}] " if flag else "", msg)
    if show_on_console:
        print(message)
