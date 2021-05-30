"""Command Line Interface (CLI) application - RSS reader"""
import sys
import os
import argparse
import logging

import rss_reader.rss_parser as rp


def main():
    """main() method is parsing command line arguments with argparse module and defines program control flow
    Return: Exit codes:
        os.EX_USAGE - misuse of command line arguments
        os.EX_NOHOST - RSS feed url not responding or no internet connection
        os.EX_OK - program finished successfully
    """
    # Processing command line arguments using module argparse
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    # Adding command line arguments to the application
    # Optional arguments:
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Output verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    # Positional (mandatory) arguments:
    parser.add_argument("source", type=str, nargs="?", default=None, help="RSS URL")
    # Parsing arguments
    args = parser.parse_args()

    # [--verbose] mode means that status messages are printed while programming is running
    # logging module is used to print status messages
    if args.verbose:  # Configuring logging to enable status messages
        logging.basicConfig(level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
        logging.info("Verbose mode ON")
    else:  # Configuring logging to disable status messages
        logging.basicConfig(level=logging.CRITICAL, format=" %(asctime)s - %(levelname)s - %(message)s")
        logging.disable(logging.CRITICAL)

    if args.version:  # [--version] argument passed - print version and exit
        print("Version 1.2", flush=True)
        exit(sys.exit(os.EX_OK))

    logging.info(f"URL: {args.source}")
    if 255 < len(args.source) < 3:  # Checking [source] URL validity here
        # Waring the user that [source] string is too short or too long
        print("Source is not valid string\nPlease, provide string with length between 3 and 255 symbols", flush=True)
        exit(sys.exit(os.EX_USAGE))

    logging.info(f"Limit: {args.limit}")

    if args.limit < 0:   # args.limit parameter limits number of news to print.
        print("Error: [limit] must be positive number", flush=True)
        exit(sys.exit(os.EX_USAGE))
    else:
        # RssParser downloading xml from url, parsing and reading rss as list of dictionaries
        # RssParser provides error handling and prints to stdout error messages in case of problems with
        # URL or connection
        rss_feed = rp.RssParser(args.source, args.limit)

    if rss_feed.is_empty:  # In case rss_feed == [] something is wrong with URL or internet connection
        print("RSS source is not responding", flush=True)
        exit(sys.exit(os.EX_NOHOST))

    if args.json:  # args.json parameter specified: news are printed to stdout in json format
        logging.info("Print RSS in json")
        rss_feed.dump_json()
    else:  # by default: news are printed to stdout as formatted text
        logging.info("Print RSS in plain text")
        rss_feed.dump_raw_json()
        rss_feed.print_json()

    # Program finished successfully: exit(0)
    exit(sys.exit(os.EX_OK))


if __name__ == "__main__":
    main()
