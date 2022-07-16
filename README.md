
[![PyPI version](https://img.shields.io/pypi/v/pyinvestingsnippets.svg)](https://pypi.org/project/pyinvestingsnippets/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/pyinvestingsnippets.svg)
[![Build Status](https://github.com/investingsnippets/pyinvestingsnippets/workflows/CI/badge.svg)](https://github.com/investingsnippets/pyinvestingsnippets/actions?query=workflow%3ACI)
![CodeQL](https://github.com/investingsnippets/pyinvestingsnippets/workflows/CodeQL/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/pyinvestingsnippets/badge/?version=latest)](https://pyinvestingsnippets.readthedocs.io/en/latest/?badge=latest)


# Python Module for Investing Snippets

Pandas extensions and utility classes for stock and investment analysis.


## Installation

```bash
pip install pyinvestingsnippets
```

## Examples and Documentation

Please see detailed examples under the `examples` directory and read the documentation [here](https://pyinvestingsnippets.readthedocs.io/en/latest/)

## Develop

First install the required venv and tox

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install tox
```

> On osx with Big Sur there is an [issue](https://github.com/numpy/numpy/issues/17784) with installing cython! Due to that, you can `docker run --rm -v $(PWD):/app --workdir=/app -it --entrypoint=sh python:3.8`

Run tox test and lint

```bash
tox
```

Install the package locally

```bash
pip install .tox/dist/pyinvestingsnippets-<version>.zip
```

## Run examples

```bash
python3 -m venv .venvtest
source .venvtest/bin/activate
pip install -r requirements.txt
pip install -r examples/requirements.txt
python examples/matplotlib_report.py
```

> If on OSX set env var to `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

## Release

On master change the version in `pyinvestingsnippets/__init__.py`

```bash
git commit -am "v<VERSION>"
git tag -a v0.0.3
git push origin --tags
git push -u
tox -e release
```