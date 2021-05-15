"""Command Line Interface (CLI) application - RSS reader


"""

import argparse
from rss_reader.disp import display
import logging
import rss_reader.rss_parser as rp

import feedparser as fp

def main():
    # To process command line arguments using module argparse
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
    if args.verbose:
        # Configuring logging to enable status messages
        logging.basicConfig(level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
        logging.info("rss_reader starting...")
        logging.info("Verbose mode ON")
    else:
        # Configuring logging to disable status messages
        logging.basicConfig(level=logging.CRITICAL, format=" %(asctime)s - %(levelname)s - %(message)s")
        logging.disable(logging.CRITICAL)

    # [--version] argument passed - print version and exit
    if args.version:
        print("Version 1.1", flush=True)
        exit(0)




    logging.info(f"URL: {args.source}")
    # Checking [source] URL validity here
    if 255 < len(args.source) < 3:
        # Messaging the user that the [source] string does not comply with URL standard
        print("Source is not valid string", flush=True)
        exit(0)

    logging.info(f"Limit: {args.limit}")

    '''
        if args.json:
            display_json()
        else:
            display()
    '''

    # Handling url, parsing and reading rss as list of dictionaries
    print(f"Source: {args.source}", flush=True)

    rss_feed = rp.RssParser(args.source, args.limit)

    # rss_feed.print_raw_rss_feed()
    # print(rss_feed.get_rss_limited_feed(), end="  ")

    if rss_feed.not_empty():
        rss_feed.print_raw_rss()
    else:
        print("RSS source is empty", flush=True)
        exit(0)


    print("Hi", flush=True)
    display()

if __name__ == "__main__":
    main()


