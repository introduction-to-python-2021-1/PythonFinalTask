# rss-reader

Pure Python command-line RSS reader.

## Usage

```shell 
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf TO_PDF] 
                  [--to-html TO_HTML] [--colorize] [source]

Pure Python command-line RSS reader.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Print cached news for specified date
  --to-pdf TO_PDF    Converts news to PDF format
  --to-html TO_HTML  Converts news to HTML format
  --colorize         Print the result of the utility in colorized mode
```

## Expected arguments values

<pre>
    --limit: Accepts an integer greater than zero (example '--limit=0')
    --date: Accepts a date in the format '%Y%m%d' (example '--date=20210525')
    --to-pdf and --to-html: Accepts an absolute or relative path with or without a filename (example '--to-pdf=folder/filename.pdf' or '--to-html=/home/username/folder').
                            If the file name is not specified, a file is created with the current date and time as filename (example '2021-05-25 12:25:26.850176.pdf')
</pre>

## JSON structure

<pre>
"0": {
    "title": "The 8 Most Architecturally Significant Pavilions of Expo 2020",
    "url": "https://news.yahoo.com/8-most-architecturally-significant-pavilions-145934705.html",
    "description": null,
    "date": "Mon, 24 May 2021 14:59:34",
    "links": {
        "0": {
            "enclosure": false,
            "media": true,
            "type": "image/jpeg",
            "url": "https://s.yimg.com/uu/api/res/1.2/jS4r0oJoL32kMPw21TPBzQ--~B/aD0yMDAwO3c9MzAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/architectural_digest_422/4741bfb27d373037c3e160f60f8d9340",
            "attributes": null
        }
    }
}
</pre>

## Cache file structure

<pre>
{
  "0": {
    "title": "The 8 Most Architecturally Significant Pavilions of Expo 2020",
    "url": "https://news.yahoo.com/8-most-architecturally-significant-pavilions-145934705.html",
    "description": null,
    "date": "Mon, 24 May 2021 14:59:34",
    "links": {
      "0": {
        "enclosure": false,
        "media": true,
        "type": "image/jpeg",
        "url": "https://s.yimg.com/uu/api/res/1.2/jS4r0oJoL32kMPw21TPBzQ--~B/aD0yMDAwO3c9MzAwMDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/architectural_digest_422/4741bfb27d373037c3e160f60f8d9340",
        "attributes": null
      }
    }
  },
  "1": {
    "title": "Последние новости Беларуси и мира | Главные события 2021 - Sputnik",
    "source": "https://sputnik.by/export/rss2/archive/index.xml",
    "items": {
      "0": {
        "title": "Какой сегодня праздник: 26 мая",
        "url": "https://sputnik.by/event/20210526/1035631463/26-maya.html",
        "description": "Сегодня среда, 26 мая. Этот день является 146-м в григорианском календаре. До конца года остается 219 дней.",
        "date": "Wed, 26 May 2021 00:01:00",
        "links": {
          "0": {
            "enclosure": true,
            "media": false,
            "type": "image/jpeg",
            "url": "https://cdn11.img.sputnik.by/images/07e5/05/18/1047701328.jpg",
            "attributes": null
          }
        }
      }
    }
  }
}
</pre>