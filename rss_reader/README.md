# Python command-line RSS reader

This module is a command-line utility which receives [RSS] URL and prints results in human-readable format.

## Usage

Utility provides the following interface:

    rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

_Positional arguments:_

    source         RSS URL

_Optional arguments:_

    -h, --help     Show help message and exit
    --version      Print version info
    --json         Print result as JSON in stdout
    --verbose      Outputs verbose status messages
    --limit LIMIT  Limit news topics if this parameter provided
    --date DATE    Print news from local storage for specified day

## Local storage
The RSS news are stored to local storage while reading. The format of this storage is JSON file named
`rss_reader_storage.json`. In case of using `--date` argument the utility loads news from it. 

## JSON format
In case of using `--json` or `--date` argument the utility uses the following JSON format:

    [
        {
            "channel_id": <string>,
            "channel_title": <string>,
            "news": [
                {
                    "number": <int>,
                    "title": <string>,
                    "link": <string>,
                    "author": <string>,
                    "date": <string>,
                    "description": <string>
                }
            ]
        }
    ]

## Package structure
    rss_reader/
      |-- setup.py             # installation package
      |-- rss_reader/          
        |-- rss_reader.py      # implementation RSSReader class
      |-- tests                
        |-- test_rss_reader.py # testing RSSReader class
