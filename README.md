# Pure Python command-line RSS reader

## Assumptions
RSS reader for printing news from link to stdout in simple or json format

## Requirements 
Do not need any installations for using as a package.

For using as a script please run `pip install -r requirements.txt`

## Usage
To run the package it's possible to assign either 
`rss_reader "RSS URL" [optional arguments]` 

or `python rss_reader.py "RSS URL" [optional arguments]` (after installation)

```
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

## Output:
Depends from optional arguments

### Examples:

#### -h, --help:
See Usage section

#### --version:
`Version 2.0.1` - and stop running program

#### --json --limit 1:
```
{
 "news": [
  {
   "Title": "On-duty police officer sexually assaulted by gas station manager, Georgia cops say",
   "Published": "2021-05-18T01:06:34Z",
   "Media_content": [
    {
     "height": "86",
     "url": "https://s.yimg.com/uu/api/res/1.2/A3riyROEGQuSpO0M838c0g--~B/aD02NDE7dz0xMTQwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/lexington_herald_leader_mcclatchy_articles_314/d453d37647ec075638a8bc71a3e80ce0",
     "width": "130"
    }
   ],
   "Link": "https://news.yahoo.com/duty-police-officer-sexually-assaulted-010634049.html"
  }
 ]
}
```

#### --verbose --limit 1:
```
2021-05-19 18:22:24,287 - INFO - Starting reading link https://news.yahoo.com/rss/
2021-05-19 18:22:24,288 - INFO - Would read only 1 number of news

Yahoo News - Latest News & Headlines

Title: 11-year-old girl fights back, escapes attempted abduction at Florida bus stop
Published: 2021-05-19T05:09:32Z
Media_content: [{'height': '86', 'url': 'https://s.yimg.com/uu/api/res/1.2/9vsC7EHL3unEzuVkXlaTlQ--~B/aD0xMDgwO3c9MTkyMTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/nbc_news_122/08d
bcabc6f633292d0747757d09a129a', 'width': '130'}]
Link: https://news.yahoo.com/11-old-girl-fights-back-050932837.html


2021-05-19 18:22:24,290 - INFO - End of reading
```