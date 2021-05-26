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
  --date DATE        Return news topics which were published in specific date
  --to-html TO_HTML  Save news in .html format by provided path
  --to-pdf TO_PDF    Save news in .pdf format by provided path

```

In case of using `--json` argument utility converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format and prints it to stdout. The JSON structure is shown below.

```json
[
    {
        "Feed": "Yahoo News - Latest News & Headlines",
        "Title": "Republican anger with Dr. Fauci reaches new heights",
        "Date": "2021-05-10T20:17:40Z",
        "Link": "https://news.yahoo.com/republican-anger-with-dr-fauci-reaches-new-heights-201740818.html",
        "image_url": "https://news.yahoo.com/republican-anger-with-dr-fauci-reaches-new-heights-201740818.jpg"
    }
]
```

With the argument `--verbose` program prints all logs in stdout.

## Distribution

Utility is wrapped into distribution package with `setuptools`. This package exports CLI utility named `rss-reader`.

### Usage

Application works both with and without installation of CLI utility, meaning that it can work:

    $ python rss_reader.py ...

as well as this:

    $ rss_reader ...

## News caching

The RSS news is stored in a local storage while reading. Local storage is located in the directory **data** as **localstorage.json**. The format of this storage is shown down below:

```json
{
    "https://news.yahoo.com/rss/": [
        {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Republican anger with Dr. Fauci reaches new heights",
            "Date": "2021-05-10T20:17:40Z",
            "Link": "https://news.yahoo.com/republican-anger-with-dr-fauci-reaches-new-heights-201740818.html",
            "image_url": "https://news.yahoo.com/republican-anger-with-dr-fauci-reaches-new-heights-201740818.jpg"
        }
    ]
}
```