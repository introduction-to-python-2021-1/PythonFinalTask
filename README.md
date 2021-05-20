# rss-reader

Python command-line RSS reader.

## Usage

```shell
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [source]

Python command-line RSS reader.

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
        "Title": "Op-Ed: How the world could help end the Israeli-Palestinian conflict \u2014 and prevent future clashes",
        "Publication date": "2021-05-19 21:13:04+00:00",
        "News link": "https://news.yahoo.com/op-ed-world-could-help-211304938.html",
        "Image link": "https://s.yimg.com/uu/api/res/1.2/2YBFKEf5DQGLB7Zpa7Ef8g--~B/aD01NjA7dz04NDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/los_angeles_times_opinion_902/d9a9fe3e28a1063092dbfc42d1f63bbe"
    },
    "1": {
        "Title": "Inquiry into Post Office scandal given powers to compel witnesses",
        "Publication date": "2021-05-19 16:27:22+00:00",
        "News link": "https://news.yahoo.com/inquiry-post-office-scandal-given-162722842.html",
        "Image link": "https://s.yimg.com/uu/api/res/1.2/.RK3lelNYrvZ4n6Ms2WKGA--~B/aD0xNTYzO3c9MjUwMTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/the_telegraph_258/d2dff7a92f196b66cec186b35931f707"
    }
}
</pre>