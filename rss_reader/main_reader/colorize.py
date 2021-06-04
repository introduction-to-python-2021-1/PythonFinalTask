""" Create colorized print functions. """
from termcolor import cprint


def print_roses(text):
    """ Colorize text to magento(rose) color. """
    return cprint(text, "magenta")


def print_red_bold(text):
    """ Colorize text to red color and make it bold. """
    return cprint(text, "red", attrs=["bold"])


def print_blue(text):
    """ Colorize text to blue color. """
    return cprint(text, "blue")


def print_yellow_on_green(text):
    """ Colorize text to yellow color on green back. """
    return cprint(text, "yellow", "on_green")
