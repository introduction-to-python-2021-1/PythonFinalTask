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

