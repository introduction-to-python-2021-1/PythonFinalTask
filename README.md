# Pure Python command-line RSS reader

## Assumptions
RSS reader for receiving news from link, cashing it, saving to html/pdf and printing to stdout in simple or json format.

## Requirements

Do not need any additional installations for using as a script.

For using as a package please run first `pip install -r requirements.txt`

## Usage

To run the reader it's possible to assign either
`python rss_reader.py "RSS URL" [optional arguments]`

or  `rss_reader "RSS URL" [optional arguments]` (after installation)

```
usage: rss_reader [-h] [--version] [--limit LIMIT] [--json] [--verbose] [--colorize] [--date DATE] 
[--to-pdf TO_PDF] [--to-html TO_HTML] [source]

Pure Python command-line RSS reader

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --limit LIMIT      Limit news topics if this parameter provided
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --colorize         Prints news to the console in colorized mode
  --date DATE        Return news from date yyyymmdd from cash
  --to-pdf TO_PDF    Save news in pdf format in chosen path, eg 'E:\data' or '/home/user/data'
  --to-html TO_HTML  Save news in html format in chosen path, eg 'E:\data' or '/home/user/data'
```

## Output:

Depends on optional arguments (see [Usage](#usage)).

In any case (except `--help` and `--version`) print news to stdout in simple format (see [Examples](#examples)) or
json (if `--json`)

Argument `--date` says reader to look for news not in the Internet, but in the local file. News are written to the local
storage every time user read them from the Internet. User should mention date in format `yyyymmdd` and (optionally) news
site, from which she/he wants to read news. If user tries to ask cashed news before reading any of them from the
Internet, or insert an incorrect date, or no date from this date/source, the reader will print user-friendly message and
stop working.

With arguments `to-pdf` and `to-html` user says to save news in chosen format IN ADDITION to the printing to stdout.
User should mention the absolute path to the folder. File name will be created automatically. Output files include
number of news, limited by user. Each news contains title, published date and link; and summary, description and one
image (if they were in a source). After saving, user-friendly message printing to stdout.

Argument `--colorize` print news to stdout in different colours (or in one on the changed background).

### Examples:

#### --version:

`Version 5.0.0` - and stop running program

#### --json --limit 2:

```
{
 "source": "https://news.yahoo.com/rss/",
 "main_title": "Yahoo News - Latest News & Headlines",
 "news": [
  {
   "Title": "Mom who posed as daughter to sneak into Texas middle school arrested",
   "Published": "2021-06-07T15:52:48Z",
   "Image": "https://s.yimg.com/uu/api/res/1.2/4nHCVnMuD9eXLr4gLMwtjA--~B/aD02MDA7dz02MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/nbc_news_122/d9ccf9ad1b926fc17a064cb0559b80e1",
   "Link": "https://news.yahoo.com/mom-posed-daughter-sneak-texas-155248776.html"
  },
  {
   "Title": "Iran cleric who founded Hezbollah, survived book bomb, dies",
   "Published": "2021-06-07T09:21:01Z",
   "Image": "https://s.yimg.com/uu/api/res/1.2/6ttL5lEjkMPdzympuFBVPA--~B/aD0zNzMwO3c9NjAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/5adde1c4be0b310e385974592680ea44",
   "Link": "https://news.yahoo.com/iran-cleric-founded-hezbollah-survived-092101200.html"
  }
 ]
}
```

#### --verbose --limit 1:

```
2021-06-07 20:44:56,864 - INFO - Starting reading link https://news.yahoo.com/rss/
2021-06-07 20:44:56,867 - INFO - Would read only 1 number of news

Feed: Yahoo News - Latest News & Headlines

Title: Mom who posed as daughter to sneak into Texas middle school arrested
Date: 2021-06-07T15:52:48Z
Link: https://news.yahoo.com/mom-posed-daughter-sneak-texas-155248776.html


Links:
[1]: https://news.yahoo.com/mom-posed-daughter-sneak-texas-155248776.html (link)
[2]: https://s.yimg.com/uu/api/res/1.2/4nHCVnMuD9eXLr4gLMwtjA--~B/aD02MDA7dz02MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/nbc_news_122/d9ccf9ad1b926fc17a064cb0559b80e1 (image)

2021-06-07 20:44:56,869 - INFO - End of reading

```