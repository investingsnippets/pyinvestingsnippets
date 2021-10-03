
[![PyPI version](https://img.shields.io/pypi/v/pyinvestingsnippets.svg)](https://pypi.org/project/pyinvestingsnippets/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/pyinvestingsnippets.svg)
[![Build Status](https://github.com/investingsnippets/pyinvestingsnippets/workflows/CI/badge.svg)](https://github.com/investingsnippets/pyinvestingsnippets/actions?query=workflow%3ACI)
![CodeQL](https://github.com/investingsnippets/pyinvestingsnippets/workflows/CodeQL/badge.svg)



# Python Module for Investing Snippets


## Develop

First install the required venv and tox

```
python3 -m venv .venv
source .venv/bin/activate
pip install tox
```

Run tox test and lint

```
tox
```

Install the package locally

```
pip install .tox/dist/pyinvestingsnippets-<version>.zip
```

## Release
