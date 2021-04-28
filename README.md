# One-shot command-line RSS reader.

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.

The textbox below provides an example of this utility usage:

```shell
$ rss_reader.py "https://news.yahoo.com/rss/" --limit 1
Feed: Yahoo News - Latest News & Headlines

Title: Biden envoy: Afghan government won't collapse
Date: 2021-04-28T17:52:59Z
Link: https://news.yahoo.com/biden-envoy-afghan-government-wont-collapse-175259465.html

```

Utility provides the following interface:

```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

```

In case of using `--json` argument utility converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format. The JSON structure is shown below.

```json
{
    "Title": "Yahoo News - Latest News & Headlines",
    "Items": [
        {
            "Title": "AP sources: Feds search Rudy Giuliani's NYC home, office",
            "Date": "2021-04-28T16:26:16Z",
            "Link": "https://news.yahoo.com/ap-source-feds-execute-warrant-162616009.html"
        }
    ]
}
```

With the argument `--verbose` program prints all logs in stdout.

## Tests

For running all tests write down:

    $ python3 -m unittest discover

For running some specific tests you can do this as following (Ex: process_response):

    $ python3 -m unittest tests.test_process_response