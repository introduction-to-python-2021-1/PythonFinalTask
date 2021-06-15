# AP RSS-reader

[![PyPI](https://img.shields.io/pypi/v/ap-rss-reader)][pypi ap-rss-reader]
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MyPy](https://img.shields.io/badge/MyPy-passing-success.svg)](https://mypy.readthedocs.io/en/stable/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/aplatkouski/ap-rss-reader/develop.svg)](https://results.pre-commit.ci/latest/github/aplatkouski/ap-rss-reader/develop)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Run tests](https://github.com/aplatkouski/ap-rss-reader/workflows/Run%20tests/badge.svg)](https://github.com/aplatkouski/ap-rss-reader/actions?query=workflow%3A%22Run+tests%22+branch%3Amaster)
[![codecov](https://codecov.io/gh/aplatkouski/ap-rss-reader/branch/develop/graph/badge.svg?token=FHs5Yrro0x)](https://codecov.io/gh/aplatkouski/ap-rss-reader)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/96a2cb6578804c48852068a0788b3574)](https://www.codacy.com/gh/aplatkouski/ap-rss-reader/dashboard?utm_source=github.com&utm_medium=referral&utm_content=aplatkouski/ap-rss-reader&utm_campaign=Badge_Grade)
[![Requirements Status](https://requires.io/github/aplatkouski/ap-rss-reader/requirements.svg?branch=develop)](https://requires.io/github/aplatkouski/ap-rss-reader/requirements/?branch=develop)
[![Build Status](https://www.travis-ci.com/aplatkouski/ap-rss-reader.svg?branch=develop)](https://www.travis-ci.com/aplatkouski/ap-rss-reader)

## Installation

The project has been tested only with [python 3.8][python] on Ubuntu Linux and
Windows 10. If you have python 3.8 and above installed in your machine, just
install the AP RSS-reader from [PyPI][pypi ap-rss-reader]:

```shell
python --version
pip install ap-rss-reader
```

You can find source code of this package on [github][]. See
[aplatkouski/ap-rss-reader][] repository.

## How to use it

```shell
$ ap_rss_reader "https://news.yahoo.com/rss/" --limit 1
Feed: Yahoo News - Latest News & Headlines
Url: https://news.yahoo.com/rss/
Description: The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.

Title: California finally lifts its last big COVID restrictions. Did the state play it too safe?
Link: https://news.yahoo.com/california-finally-lifts-its-last-big-covid-restrictions-did-the-state-play-it-too-safe-133838908.html
Date: 2021-06-15 13:38:38
Source: Yahoo News
Links:
[1]: https://s.yimg.com/os/creatr-uploaded-images/2021-06/28ddb610-cddc-11eb-8e72-e3afb144a08a (content).

```

Utility provides the following interface:

```shell
usage: ap_rss_reader [-h] [--date DATE] [--limit LIMIT] [--verbose] [--version] [--json] [--to-html TO_HTML] [--to-pdf TO_PDF] [source]

AP RSS-reader with CLI.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --date DATE        Limit news topics by publishing date: YYYYMMDD
  --limit LIMIT      Limit news topics if this parameter provided
  --verbose          Provides additional details as to what the program is doing
  --version          Shows the version of the program and exits
  --json             Print result as JSON in stdout
  --to-html TO_HTML  Save rss channel as html file with given path: 'C:\rss.html' or '/home/user/rss.html'.
  --to-pdf TO_PDF    Save rss channel as pdf file with given path: 'C:\rss.html' or '/home/user/rss.html'.

```

In case of using `--json` argument utility converts the news into
[JSON](https://en.wikipedia.org/wiki/JSON) format:

```json
{
  "articles": [
    {
      "link": "https://news.yahoo.com/california-finally-lifts-its-last-big-covid-restrictions-did-the-state-play-it-too-safe-133838908.html",
      "media": [
        [
          "content",
          "https://s.yimg.com/os/creatr-uploaded-images/2021-06/28ddb610-cddc-11eb-8e72-e3afb144a08a",
          "86",
          "130"
        ]
      ],
      "pubdate": "2021-06-15 13:38:38",
      "source": "Yahoo News",
      "title": "California finally lifts its last big COVID restrictions. Did the state play it too safe?"
    }
  ],
  "description": "The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
  "title": "Yahoo News - Latest News & Headlines",
  "url": "https://news.yahoo.com/rss/"
}
```

With the argument `--verbose` program prints all logs in stdout.

## Development & Contributing

Development of this happens on GitHub, patches including tests, documentation
are very welcome, as well as bug reports!

This project has a [code of conduct][]. By interacting with this repository,
organization, or community you agree to abide by its terms.

See also our [CONTRIBUTING.md][].

## Copyright

Copyright (c) 2021 Artsiom Platkouski. `ap-rss-reader` is licensed under the
MIT License - see the [LICENSE.txt][] file for details.

[python]: https://www.python.org/
[pypi ap-rss-reader]: https://pypi.org/project/ap-rss-reader/
[github]: https://github.com
[aplatkouski/ap-rss-reader]: https://github.com/aplatkouski/ap-rss-reader
[code of conduct]:
  https://github.com/aplatkouski/ap-rss-reader/blob/master/CODE_OF_CONDUCT.md
[contributing.md]:
  https://github.com/aplatkouski/ap-rss-reader/blob/master/CONTRIBUTING.md
[license.txt]:
  https://github.com/aplatkouski/ap-rss-reader/blob/master/LICENSE.txt
