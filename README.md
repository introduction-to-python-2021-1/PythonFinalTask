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

Title: Nestor heads into Georgia after tornados damage Florida
Date: Sun, 20 Oct 2019 04:21:44 +0300
Link: https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html


Links:
[1]: https://news.yahoo.com/wet-weekend-tropical-storm-warnings-131131925.html (link)
[2]: http://l2.yimg.com/uu/api/res/1.2/Liyq2kH4HqlYHaS5BmZWpw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/ap.org/5ecc06358726cabef94585f99050f4f0 (image)

```

Utility provides the following interface:

```shell
usage: ap_rss_reader [-h] [--limit LIMIT] [--verbose] [--version] [--json] source

AP RSS-reader with CLI.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --limit LIMIT  Limit news topics if this parameter provided
  --verbose      Provides additional details as to what the program is doing
  --version      Shows the version of the program and exits
  --json         Print result as JSON in stdout

```

In case of using `--json` argument utility converts the news into
[JSON](https://en.wikipedia.org/wiki/JSON) format:

```json
{
  "channel_items": [
    {
      "date": "2021-05-30 12:19:27",
      "link": "https://news.yahoo.com/mexico-cartels-hunting-down-police-121927049.html",
      "media_content_url": "https://s.yimg.com/uu/api/res/1.2/laxRlIvAURG7aPTJU6a.Cw--~B/aD0zNjQ4O3c9NTQ3MjthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/cdd01711ada54152f19140789ed6fcb4",
      "source": "Associated Press",
      "source_url": "http://www.ap.org/",
      "title": "In Mexico, cartels are hunting down police at their homes"
    }
  ],
  "title": "Yahoo News - Latest News & Headlines"
}
```

With the argument `--verbose` your program prints all logs in stdout.

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
