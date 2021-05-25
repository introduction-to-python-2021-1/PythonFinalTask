# rss-reader

Pure Python command-line RSS reader.

## Usage

```shell 
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf TO_PDF] 
                  [--to-html TO_HTML] [source]

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
        "title": "Yahoo News - Latest News & Headlines",
        "source": "https://news.yahoo.com/rss/",
        "items": {
            "0": {
                "title": "Tennessee leads with anti-transgender laws",
                "url": "https://news.yahoo.com/tennessee-leads-anti-transgender-laws-203549108.html",
                "description": null,
                "date": "Sun, 23 May 2021 20:35:49",
                "links": null
            }
        }
    }
</pre>

## Cache file structure

<pre>
{
    "0": {
        "title": "Yahoo News - Latest News & Headlines",
        "source": "https://news.yahoo.com/rss",
        "items": {
            "0": {
                "title": "Israel military draws up plan for ground invasion of Gaza",
                "url": "https://news.yahoo.com/israel-military-draws-plan-ground-064023988.html",
                "description": null,
                "date": "Thu, 13 May 2021 06:40:23",
                "links": null
            }
        }
    },
    "1": {
        "title": "Последние новости Беларуси и мира | Главные события 2021 - Sputnik",
        "source": "https://sputnik.by/export/rss2/archive/index.xml",
        "items": {
            "0": {
                "title": "Транспортная перезагрузка: что от нее ждут Беларусь и Россия?",
                "url": "https://sputnik.by/press_center/20210520/1047678494/Transportnaya-perezagruzka-chto-ot-nee-zhdut-Belarus-i-Rossiya.html",
                "description": "Минск планирует построить в России собственные перевалочные терминалы для экспорта продукции по морю.",
                "date": "Thu, 20 May 2021 18:35:16",
                "links": {
                    "0": {
                        "enclosure": true,
                        "type": "image/jpeg",
                        "url": "https://cdn11.img.sputnik.by/images/07e5/01/1b/1046753762.jpg",
                        "attributes": null
                    }
                }
            }
        }
    }
}
</pre>