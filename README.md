# rss-reader

Pure Python command-line RSS reader.

## Usage

```shell
usage: rss_reader.py [-h] [--version] [--json]
                     [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter
                 provided
```

## JSON structure

<pre>
{
    "title": "TUT.BY: Новости ТУТ - Главные новости",
    "items": {
        "0": {
            "title": "«На 19 мая у него был обратный билет в Норильск». Что известно о докторе, которого задержали в Борисове",
            "url": "https://news.tut.by/society/729590.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
            "description": "[image 0: Фото: sprosivracha.com] В Борисове 3 мая был задержан врач Александр Телего, который работает в России. Сейчас он находится в ИВС, который расположен в здании тюрьмы № 1 в Гродно. В МВД прокомментировали задержание медика и рассказали, что против него возбуждено уголовное дело за оскорбление представителей власти. Мама Александра - Галина и его друзья немного рассказали о докторе и о том, что с ним произошло.",
            "date": "Thu, 06 May 2021 21:43:00",
            "links": {
                "0": {
                    "type": "image",
                    "url": "https://img.tyt.by/thumbnails/n/regiony/05/8/telego_aaleksandr.jpg",
                    "attributes": {
                        "alt": "Фото: sprosivracha.com"
                    }
                }
            }
        }
    }
}
</pre>