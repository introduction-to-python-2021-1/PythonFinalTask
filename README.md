**USAGE**

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
source

Pure Python command-line RSS reader.

positional arguments:
source RSS URL

optional arguments:
-h, --help show this help message and exit --version Print version info --json Print result as JSON in stdout --verbose
Outputs verbose status messages --limit LIMIT Limit news topics if this parameter provided

**JSON STRUCTURE**

python3 rss_reader.py http://feeds.bbci.co.uk/news/world/rss.xml --limit 1 --json

    {
      "new 0": {
        "feed": "BBC News - World",
        "title": "Ethiopia's Tigray crisis: UN aid chief says there is famine",
        "date": "Thu, 10 Jun 2021 21:22:44 GMT",
        "link": "https://www.bbc.co.uk/news/world-africa-57432280",
        "description": "More than 350,000 people are living in \"severe crisis\" after months of conflict in the Tigray region.",
        "links": {
          "link 0": {
            "href": "https://www.bbc.co.uk/news/world-africa-57432280",
            "type": "text/html"
          }
        }
      }
    }
