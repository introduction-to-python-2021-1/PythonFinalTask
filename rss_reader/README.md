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

## JSON format
In case of using `--json` argument the utility uses the following json format:

    {
        "channel": <string>,
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

## Package structure
    rss_reader/
      |-- setup.py           # installation package
      |-- rss_reader.py      # implementation RSSReader class
      |-- test_rss_reader.py # testing RSSReader class
