
## Description

RSS reader is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format. 

Utility provides the following interface:
```shell
usage: rss_reader.py  [-h] [--version] [--json] [--verbose]
                      [--limit LIMIT] [--date DATE]
                      [--to-html TO_HTML] [--to-pdf TO_PDF]
                      [source]

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help          Show this help message and exit
  --version           Print version info
  --json              Print result as JSON in stdout
  --verbose           Outputs verbose status messages
  --limit LIMIT       Limit news topics if this parameter provided
  --date DATE         Date for getting news from cache
  --to-html TO_HTML   Save news into html file
  --to-pdf TO_PDF     Save news into pdf file
    

```

## `--json` 
Argument utility converts the news into [JSON](https://en.wikipedia.org/wiki/JSON) format.
## `--verbose`  
Program  print all logs in stdout
## `--limit`
Show limited cont of news. Limit should be positive integer
N.B.: limit affects neither  on a count of loaded news noire on a count of cached news
## `--date`
Use date if you want to load news from cache instead of site.
If argument specified with date, only news which was published on this date will de loaded
If the argument goes without a specific date, all news will be loaded from the cache
N.B. `source` does affect on loading news from the cache. If it is specified, news for this channel will be loaded 
from the cache. Otherwise, news for all channels will be loaded
Pay attention that date should be passed in  %yyyy%mm%dd format. All other variants will be rejected
## `--to-html`
Save news into html file. You should specify file name to writing html or directory, where html should be written. 
In case of specifying directory, file name will be generated automatically
## `--to-pdf`
Save news into pdf file. You should specify file name to writing pdf or directory, where pdf should be written. 
In case of specifying directory, file name will be generated automatically


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
