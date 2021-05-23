"""Provides useful objects."""
import os
import argparse


def get_path_to_data(*args):
    """Returns an absolute path to directory "package_data" which contains package data files."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "package_data", *args)
