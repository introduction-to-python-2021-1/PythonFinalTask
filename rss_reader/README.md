
## Description

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format. 

Utility provides the following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

```

In case of using `--json` argument utility converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format.
With the argument `--verbose` your program should print all logs in stdout.


## Example of output

```
Yahoo News - Latest News & Headlines [link: https://www.yahoo.com/news]
(The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.)

Title: 'The long-term implications for our country are profound': Government looks to disrupt ransomware business
Date: 2021-05-13T19:03:13Z
Link: https://news.yahoo.com/the-long-term-implications-for-our-country-are-profound-government-looks-to-disrupt-ransomware-business-190313224.html
Media: ['https://s.yimg.com/os/creatr-uploaded-images/2021-05/11e8c600-b416-11eb-bb7f-8b4d11dfb6de']

...
```

##Example of JSON
```
{
   "Link":"https://www.yahoo.com/news",
   "Description":"The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
   "Title":"Yahoo News - Latest News & Headlines",
   "News":[
      {
         "Title":"Will anything break the GOP\u2019s embrace of election lies?",
         "Date":"2021-05-13T15:52:55Z",
         "Link":"https://news.yahoo.com/will-anything-break-the-go-ps-embrace-of-election-lies-155255077.html",
         "Media":[
            "https://s.yimg.com/os/creatr-uploaded-images/2021-05/99cb0c00-b401-11eb-bf77-8537f9da4152"
         ]
      }
   ]
}
```
