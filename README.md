# rss-reader

Pure Python command-line RSS reader.

## Usage

```shell
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [source]

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Print cached news for specified date
```

## JSON structure

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
        "title": "TUT.BY: Новости ТУТ - Главные новости",
        "source": "https://news.tut.by/rss/index.rss",
        "items": {
            "0": {
                "title": "Налоговая в суде выясняет с Тихановским, должен ли он заплатить налог с тех самых найденных за диваном 900 тысяч долларов",
                "url": "https://finance.tut.by/news730254.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
                "description": "[image 0: Фото: Сергей Комков, TUT.BY] По решению налоговой, Тихановский должен уплатить в бюджет 257 тысяч 992 рубля и 72 копейки - исходя из суммы превышения доходов над расходами.",
                "date": "Thu, 13 May 2021 17:20:00",
                "links": {
                    "0": {
                        "type": "image",
                        "url": "https://img.tyt.by/thumbnails/n/regiony/08/9/tikhanovskiy_studiya.jpg",
                        "attributes": {
                            "alt": "Фото: Сергей Комков, TUT.BY"
                        }
                    }
                }
            }
        }
    }
}
</pre>