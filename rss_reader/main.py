"""Command Line Interface (CLI) application - RSS reader"""
import sys
import os
import argparse
import logging

from rss_reader.xml_downloader import XmlDownloader
from rss_reader.xml_to_json import XmlJsonConverter
from rss_reader.json_to_json import HtmlJsonToTextJson
from rss_reader.json_io import JsonIO


def main():
    """main() method is parsing command line arguments with argparse module and defines program control flow
    Return:
    -------
    Exit codes:
        0 - Success
        1 - Error
    """
    # Processing command line arguments using module argparse
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    # Adding command line arguments to the application
    # Optional arguments:
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Output verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str, help="Print news from specified date YYYYMMDD")
    # Positional (mandatory) arguments:
    parser.add_argument("source", type=str, nargs="?",  help="RSS URL")
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
        print("Version 1.3", flush=True)
        exit(0)

    logging.info(f"URL: {args.source}")
    if args.source and (255 < len(args.source) < 3):  # Checking [source] URL validity here
        # Waring the user that [source] string is too short or too long
        print("Source is not valid string\nPlease, provide string with length between 3 and 255 symbols", flush=True)
        exit(1)

    if not args.source and not args.date:  # No URL and no date. User must provide URL.
        print("source argument not provided.\n For more information type: rss_reader -h", flush=True)
        exit(1)

    logging.info(f"Limit: {args.limit}")

    if args.limit and (args.limit < 0):   # args.limit parameter limits number of news to print.
        print("Error: [limit] must be positive number", flush=True)
        exit(1)

    # if args.date exists but includes not only digits or has improper length:
    if args.date and (not args.date.isdigit() or not len(args.date) == 8):
        print("DATE must be 8 digits", flush=True)
        exit(1)

    # argparse parameters were checked. Now start processing RSS feed

    storage = JsonIO()  # instance of JSON storage to load or save JSON data

    if args.date:  # --date specified - loading HTML JSON from the storage:
        html_json_list = storage.find_raw_rss(date=args.date, url=args.source, limit=args.limit)
        if not html_json_list:  # data not found in the storage - inform the user and quit
            print(f"No saved news from {args.date} found", flush=True)
            exit(0)
    else:  # Loading RSS feed from Internet
        rss_feed = XmlDownloader(args.source)
        if not rss_feed.xml:  # In case rss_feed.xml empty something is wrong with URL or internet connection
            print("Error: RSS source is not responding", flush=True)
            exit(1)

        # Converting downloaded XML to HTML JSON format usable for storage
        xml_to_json = XmlJsonConverter(rss_feed.xml, args.source)

        if not xml_to_json.html_json_list:  # Can not convert XML - may be non-XML document was downloaded
            print(f"Error: XML could not be parsed", flush=True)
            exit(1)

        html_json_list = xml_to_json.html_json_list

    # Converting HTML JSON format usable for storage to text JSON format usable for printing
    text_json_list = HtmlJsonToTextJson(html_json_list, limit=args.limit)
    if not text_json_list.text_json_list:
        print(f"Error: JSON could not be converted and printed", flush=True)
        exit(1)

    if args.json:  # args.json parameter specified - news are printed to stdout in text JSON format
        logging.info("Print RSS in json")
        text_json_list.dump_json()
    else:  # by default: news are printed to stdout as formatted text
        logging.info("Print RSS in plain text")
        text_json_list.print_json()

    # When we are working with Internet downloaded data must be saved to storage. It may take some time, so it's better
    # to do it in the end, not to disturb the user.
    if not args.date:
        storage.save_raw_rss(html_json_list)
        storage.download_images(html_json_list, args.source)

    # Program finished successfully
    exit(0)


if __name__ == "__main__":
    main()
