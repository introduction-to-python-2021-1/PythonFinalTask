# Python command-line RSS reader

This module is a command-line utility which receives [RSS] URL and prints results in human-readable format.

*Utility provides the following interface:*
rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

*Positional arguments:*
  source         RSS URL

*Optional arguments:*
  -h, --help     Show help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

*This utility uses JSON structure:*
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