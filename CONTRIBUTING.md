# How to contribute

Thanks for your interest in improving this project! These guidelines attempt to
make the process easier and more enjoyable.

## Working on your first Pull Request?

You can learn how from this **free** series [How to Contribute to an Open
Source Project on GitHub][how to contribute].

## General guidelines

Everyone interacting with this project is expected to follow the [Code of
Conduct][].

Submit questions, bug reports, and feature requests in the [issue tracker][].
Please be as descriptive as you can. For bug reports, please include
information about your local environment, the steps to reproduce the bug, and
any relevant command-line output.

Submit improvements to code and documentation via [pull requests][]. Unless
it's a small/quick fix, pull requests should reference an open issue that's
been discussed. This helps ensure that your contribution is aligned with the
goals of this project.

During development, use the provided tools to check for consistent style,
coding errors, and test coverage. In general, only pull requests with passing
tests and checks will be merged.

## Setting up a development environment

### [Fork and clone][github docs fork-a-repo] this repository

1. Go to `https://github.com/aplatkouski/ap-rss-reader` and click the "fork" to
   create own copy of the project.

2. Using [git][] clone the project to local computer and add the upstream
   repository:

   ```shell
   git clone https://github.com/<your-username>/ap-rss-reader.git
   cd ap-rss-reader
   git remote add upstream https://github.com/aplatkouski/ap-rss-reader.git
   git remote -v
   ```

### Create and activate a [virtual environment][]

**Note**: The minimum supported Python version is 3.8.

To get multiple versions of Python installed on your system use [pyenv][] or
[virtualenv][] tools for that. See short tutorial for details [Pipenv & Virtual
Environments][pipenv & virtual environments].

```shell
cd ap-rss-reader
python3 -m virtualenv -p /usr/bin/python3.8 .venv
source .venv/bin/activate
```

### Check python version

```shell
(.venv) $ python --version
```

### Install this packages

1. Upgrade `pip` and `setuptools`:

   ```shell
   (.venv) $ pip install --no-cache-dir --upgrade pip setuptools
   ```

2. Install package, along with the tools you need to develop and run tests, run
   the following in your virtual environment:

   ```shell
   (.venv) $ pip install -e .[dev,test]
   (.venv) $ pre-commit install --install-hooks
   ```

   This will install:

   - [pre-commit][] to run the formatters and linters on every commit
   - [gitlint][] to check git commit messages
   - [pre-commit hooks][] to run some out-of-the-box hooks for pre-commit
   - [pydocstyle][] to check docstring style
   - [pylint][] to analyze code
   - [isort][] to sort imports alphabetically, and automatically separated into
     sections
   - [black][] to format the code
   - [darglint][] to checks whether a docstring's description matches the
     actual function/method implementation
   - [mypy][] is a static type checker for Python
   - [flake8][] to identify coding errors and check code style
   - [pytest][] and [coverage.py][] to run the tests
   - [tox][] to run common development tasks

**Congratulations!** You're now all set to begin development.

## During development

- Activate your virtual environment

  ```shell
  cd ap-rss-reader
  source .venv/bin/activate
  ```

- If you cloned a while ago, get the latest changes from `upstream`:

  ```shell
  git checkout main
  git pull upstream main
  ```

- Create a new topic branch to contain your feature, change, or fix

  ```shell
  git checkout -b <topic-branch-name>
  ```

- **Your work here ...**

- Run the formatters and linters:

  ```shell
  tox -e check
  ```

  These checks are also run on every commit via [pre-commit hooks][]. Please
  fix any failures before committing.

- Run the tests:

  ```shell
  pytest
  ```

- Run the tests and generate a coverage report:

  ```shell
  tox -e py,coverage
  ```

  Please add or update tests to ensure the coverage doesn't drop.

- Run the tests in all supported Python versions, generate a coverage report,
  and run the checks

  ```shell
  tox
  ```

- Commit your changes in logical chunks

  ```shell
  git commit add .
  git commit -s -m "a brief description of changes"
  ```

## To submit contribution

### Locally rebase the upstream `main` branch into your topic branch

```shell
git pull --rebase upstream main
```

### Push your topic branch up to your fork

```shell
git push origin <topic-branch-name>
```

### Open pull request with a clear title and description

On `https://github.com/aplatkouski/ap-rss-reader` click **Open pull request**.

For details see [GitHub.com Help Documentation][]

**IMPORTANT**: By submitting a patch, you agree to allow the project owners to
license your work under the terms of the [MIT License][].

## Making a release

**Note**: This tutorial is only for contributors who have access to the main
repository.

**Note**: This project adheres to [PEP 440 - Version Identification][pep 440]
and uses [bump2version][].

### Checkout and update `main`

```shell
git checkout main
git pull upstream main
```

### Change a version number and commit the changes

See current version:

```shell
$ python setup.py --version
0.0.1
$ bump2version --dry-run --list --new-version 0.0.2 [major|minor|patch|prerelease|postrelease|devrelease]
```

Run `bump2version` without `--dry-run` upon a correct output.

For example `patch` application:

```shell
version=v`bump2version --dry-run --list --new-version 0.0.2 patch | tail -n 1 | sed -r "s/^.*=//"`
bump2version --new-version 0.0.2 --list patch
```

### Update the [CHANGELOG.md][] and commit the changes

### Push origin

```shell
git push origin main $version
```

### Run the release pipeline to upload to [TestPyPI][]

```shell
tox -e release
```

If it looks good on TestPyPI, run the release pipeline to upload to [PyPI][]

```shell
tox -e release pypi
```

### Create a new GitHub Release

Using the [GitHub CLI][], with the version number as the title, the changelog
as the description, and the distribution packages as assets

```shell
hub release create -m $version -e $(find dist/* -exec echo "-a {}" \;) $version
```

Add the `-p` flag for pre-releases.

[how to contribute]: https://kcd.im/pull-request
[code of conduct]:
  https://github.com/aplatkouski/ap-rss-reader/blob/main/CODE_OF_CONDUCT.md
[issue tracker]: https://github.com/aplatkouski/ap-rss-reader/issues
[pull requests]: https://github.com/aplatkouski/ap-rss-reader/pulls
[github docs fork-a-repo]:
  https://docs.github.com/en/github/getting-started-with-github/fork-a-repo
[git]: https://git-scm.com/
[virtual environment]: https://docs.python.org/3/library/venv.html
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv]: https://virtualenv.pypa.io/en/latest/
[pipenv & virtual environments]: https://docs.python-guide.org/dev/virtualenvs/
[pre-commit]: https://pre-commit.com/
[gitlint]: https://jorisroovers.com/gitlint/
[pre-commit hooks]: https://github.com/pre-commit/pre-commit-hooks
[pydocstyle]: http://www.pydocstyle.org/en/stable/
[pylint]: https://www.pylint.org/
[isort]: https://pycqa.github.io/isort/
[black]: https://black.readthedocs.io/en/stable/
[darglint]: https://github.com/terrencepreilly/darglint
[mypy]: https://mypy.readthedocs.io/en/stable/
[flake8]: https://flake8.pycqa.org/en/latest/
[pytest]: https://docs.pytest.org/en/latest/
[coverage.py]: https://coverage.readthedocs.io/en/latest/
[tox]: https://tox.readthedocs.io/en/latest/
[github.com help documentation]:
  https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests
[mit license]:
  https://github.com/aplatkouski/ap-rss-reader/blob/main/LICENSE.md
[pep 440]: https://www.python.org/dev/peps/pep-0440/
[changelog.md]:
  https://github.com/aplatkouski/ap-rss-reader/blob/main/CHANGELOG.md
[testpypi]: https://test.pypi.org/project/ap-rss-reader/
[pypi]: https://pypi.org/project/ap-rss-reader/
[github cli]: https://hub.github.com/
