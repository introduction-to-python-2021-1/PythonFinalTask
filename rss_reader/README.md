<h1>Python RSS reader.</h1>

<h2> Installation </h2>
<pre>
pip install .
</pre>
<h2> Interface description </h2>
<pre>
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html PATH] [--to-pdf PATH] source

positional arguments:
 url(example: https://news.yahoo.com/rss)

optional arguments:
  -h, --help      Show help message and exit
  --version       Print version and stop
  --json          Output news in json format
  --verbose       Output verbose status messages
  --limit         Limit news topics if provided
  --date DATE     Return news with the specified data (date format: "yyyymmdd")
  --to-pdf PATH   Convert news in pdf format
  --to-html PATH  Convert news in html format
  
</pre>

<h2> JSON structure </h2>
<pre>
{
    'url': 'https://news.yahoo.com/rss/'
    'feed': {
        'name': 'Yahoo News - Latest News & Headlines',
        'items': [
            {
                "title": "Australian police exhume body of 'spy' found dead in 1948 in hope of solving country's most enduring mystery",
                "link": "https://news.yahoo.com/australian-police-exhume-body-spy-143207255.html",
                "date": "21-05-19 14:32",
                "img": [
                    {
                        "src": "https://s.yimg.com/ny/api/res/1.2/mqIND1K4Qx4kNCpDI5W7NQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTcwNTtoPTQ0MC41ODk3NjQwOTQzNjIyNA--/https://s.yimg.com/uu/api/res/1.2/7EFitRizm6pbIMuAg5CRxA--~B/aD0xNTYzO3c9MjUwMTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/the_telegraph_258/728239dfd7d0afd0a70f711ed582055f",
                        "alt": "The Somerton Man has inspired thousands of armchair sleuths"
                    }
                ]
            } 
        ]
    }
}
</pre>