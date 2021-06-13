# RSS_READER
## Python FInal Task 2021 EPAM training

RSS reader is a command-line program which receives RSS URL and prints results in console.

## Installation

Clone the repository to your local machine. Walk along the path PythonFinalTask/rss_reader
```sh
git clone https://github.com/UrekMazin0/PythonFinalTask
cd PythonFinalTask
cd rss_reader
```

And use pip install

```sh
pip install .
```
If everything completed successfully, you can use the reader. In case of errors, the logs are located in the folder  tmp/

## USAGE
```sh
usage: RSS_reader [-h] [-ve] [-js] [-vbs] [-li LIMIT] [-d DATE] [-2html] [-2pdf] [source]

---------------------------------------------------------
This script allows you to view RSS feeds in the console.
---------------------------------------------------------

positional arguments:
  source                RSS URL

optional arguments:
  -h, --help            show this help message and exit
  -ve, --version        Info about version
  -js, --json           JSON
  -vbs, --verbose       logs in stdout
  -li LIMIT, --limit LIMIT
                        Limit
  -d DATE, --date DATE  Selection by dates in format: YearMonthDay, as an example: --date 20201201
  -2html, --to_html     convert news into html file
  -2pdf, --to_pdf       convert news into pdf file

```

# Cashing format

```sh
[
    {
        "Channel": "Yahoo News - Latest News & Headlines",
        "Title": "Undervaccinated red states are nowhere near herd immunity as dangerous Delta variant spreads",
        "Date": "2021-06-11T09:00:52Z",
        "Link": "https://news.yahoo.com/undervaccinated-red-states-are-nowhere-near-herd-immunity-as-dangerous-delta-variant-spreads-090052183.html"
    },
    {
        "Channel": "Yahoo News - Latest News & Headlines",
        "Title": "Texas dad rips judge after convicted rapist of his teen daughter gets light sentence: report",
        "Date": "2021-06-11T06:45:04Z",
        "Link": "https://news.yahoo.com/texas-dad-rips-judge-convicted-064504101.html"
    },
    {
        "Channel": "Yahoo News - Latest News & Headlines",
        "Title": "Manchin Says He Will Continue to Support Hyde Amendment",
        "Date": "2021-06-11T02:31:20Z",
        "Link": "https://news.yahoo.com/manchin-says-continue-support-hyde-023120845.html"
    }
]
```
