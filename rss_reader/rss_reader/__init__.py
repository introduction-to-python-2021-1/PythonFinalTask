import argparse
from .reader import RssReaderApp


def main():
    app = RssReaderApp()
    app.run()
