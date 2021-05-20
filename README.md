# rss_reader

RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Usage

An example how it works:

```shell
python3.8 rss_reader/rss_reader.py https://www.theguardian.com/world/rss --limit=1

Feed: World news | The Guardian 

Title: Naturalist Jane Goodall wins 2021 Templeton prize for life’s work
Date: Thu, 20 May 2021 11:00:36 GMT
Link: https://www.theguardian.com/science/2021/may/20/naturalist-jane-goodall-wins-2021-templeton-prize-for-lifes-work
Images: 2
https://i.guim.co.uk/img/media/c2db7d7895051a28277f2a723df23c87d7e69fd3/0_1212_4496_2698/master/4496.jpg?width=140&quality=85&auto=format&fit=max&s=b93d29abb34d76a745c29342f3894a23
https://i.guim.co.uk/img/media/c2db7d7895051a28277f2a723df23c87d7e69fd3/0_1212_4496_2698/master/4496.jpg?width=460&quality=85&auto=format&fit=max&s=3eb92325a31673204b5e397fabedcaeb 
 
Count of news: 1
```
## Interface
RSS reader provides the following interface:

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

### JSON
In case of using `--json` argument RSS reader converts the news into JSON
with the following structure:

```
{
   "Feed": "World news | The Guardian",
   "News": [
      {
         "Title": "Naturalist Jane Goodall wins 2021 Templeton prize for life\u2019s work",
         "Date": "Thu, 20 May 2021 11:00:36 GMT",
         "Link": "https://www.theguardian.com/science/2021/may/20/naturalist-jane-goodall-wins-2021-templeton-prize-for-lifes-work",
         "Images": [
            "https://i.guim.co.uk/img/media/c2db7d7895051a28277f2a723df23c87d7e69fd3/0_1212_4496_2698/master/4496.jpg?width=140&quality=85&auto=format&fit=max&s=b93d29abb34d76a745c29342f3894a23",
            "https://i.guim.co.uk/img/media/c2db7d7895051a28277f2a723df23c87d7e69fd3/0_1212_4496_2698/master/4496.jpg?width=460&quality=85&auto=format&fit=max&s=3eb92325a31673204b5e397fabedcaeb"
         ]
      }
   ]
}
```
