# RSS reader for Yahoo news feed
RSS reader receives URL and prints results in human-readable format: to stdout and (optionally) converts news items into pdf and/or html format.

## Interface
The tility has the following interface:
```
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf TO_PDF] [--to-html TO_HTML] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Publishing date
  --to-pdf TO_PDF    Converts output to PDF format. Enter path
  --to-html TO_HTML  Converts output to HTML format. Enter path
```
## Source
The program works with Yahoo News RSS feed, located at https://news.yahoo.com/rss/. Please, use this URL only.
If you omit this argument but specify a date, the program will retrieve the necessary news items from local cache.

## Limit
To limit the number of news items printed in stdout, type `--limit`, next argument should be a positive number. If your number is larger than the actual number of news, the program will print all available news to stdout.

## JSON
To print the news items in JSON format in stdout, use this argument `--json`. If you don't, the output will be in text format.

### Structure of output in JSON
```
{'Feed': 'Yahoo News - Latest News & Headlines',
 'Items': [{'Date': '2021-06-15',
            'Image': {'Path': '/home/rmaladziashyn/PycharmProjects/PythonFinalTask/rss_reader/local_storage/images/01.png',
                      'URL': 'https://s.yimg.com/uu/api/res/1.2/CC5KS4D.HMYqe2GYDTcQTQ--~B/aD01NDk7dz05NzY7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/bbc_us_articles_995/e3dce8532651370e84652829e92e3f12'},
            'Link': 'https://news.yahoo.com/delhi-riots-india-court-grants-084707250.html',
            'Source': 'BBC',
            'Time': '08:47:07',
            'Title': 'Delhi riots: India court grants bail to activists held '
                     'over citizenship law protests'}],
 'Items count': 1}
```

### Structure of output in text format
```
Feed: Yahoo News - Latest News & Headlines
Items count: 2

Title: Delhi riots: India court grants bail to activists held over citizenship law protests
Date: 2021-06-15
Time: 08:47:07
Link: https://news.yahoo.com/delhi-riots-india-court-grants-084707250.html
Source: BBC
Image:
        URL: https://s.yimg.com/uu/api/res/1.2/CC5KS4D.HMYqe2GYDTcQTQ--~B/aD01NDk7dz05NzY7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/bbc_us_articles_995/e3dce8532651370e84652829e92e3f12
        Path: /home/rmaladziashyn/PycharmProjects/PythonFinalTask/rss_reader/local_storage/images/01.png
```

## Date
To print news for a specific date, type `--date` and specify the date in this format: YYYYMMDD.
If there are no news items for the specified date, the program will return an error message.

## Caching
If you specify the correct URL, the program will first store the news items and respective images in the local folder. This data can later be used to retrieve news for specific dates without specifying the source as an argument.

## Conversion
The program converts news output into 2 formats: pdf and/or html.
To convert to pdf, type `--to-pdf` next type the file name, e.g. `my_rss.pdf`.
To convert to html, type `--to-html`, next type the file name, e.g. `my_rss.html`.

## Verbose
To print all logs in stdout, use `--verbose` argument.