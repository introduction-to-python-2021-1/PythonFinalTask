# AP RSS-reader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MyPy](https://img.shields.io/badge/MyPy-passing-success.svg)](https://mypy.readthedocs.io/en/stable/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/aplatkouski/ap-rss-reader/main.svg)](https://results.pre-commit.ci/latest/github/aplatkouski/ap-rss-reader/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Run tests](https://github.com/aplatkouski/ap-rss-reader/workflows/Run%20tests/badge.svg)](https://github.com/aplatkouski/ap-rss-reader/actions?query=workflow%3A%22Run+tests%22+branch%3Amaster)
[![codecov](https://codecov.io/gh/aplatkouski/ap-rss-reader/branch/main/graph/badge.svg?token=FHs5Yrro0x)](https://codecov.io/gh/aplatkouski/ap-rss-reader)
[![Requirements Status](https://requires.io/github/aplatkouski/ap-rss-reader/requirements.svg?branch=main)](https://requires.io/github/aplatkouski/ap-rss-reader/requirements/?branch=main)

## Installation

The project has been tested only with [python 3.8][python] on Ubuntu Linux and
Windows 10. If you have python 3.8 and above installed in your machine, just
install the AP Games from [PyPI][pypi ap-rss-reader]:

```shell
python --version
pip install ap-rss-reader
```

You can find source code of this package on [github][]. See
[aplatkouski/ap-rss-reader][] repository.

## How to use it

Run module:

```shell
python -m ap_rss_reader
```

Or open the python console and type:

```python
# Python version 3.8+
from ap_rss_reader import cli
cli.main()
```

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
