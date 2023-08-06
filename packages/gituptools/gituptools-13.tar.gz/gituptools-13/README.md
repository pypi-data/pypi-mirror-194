# Welcome to Gituptools

[![Build](https://gitlab.com/sol-courtney/python-packages/gituptools/badges/main/pipeline.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools)
[![Tests](https://gitlab.com/sol-courtney/python-packages/gituptools/badges/main/coverage.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools)

Gituptools is a helper for packing Python on Gitlab CICD runners.  It basically gets as much from the runtime environment as it can to fill in all the packaging metadata that a typical `setup.py` file needs.

Gituptools is 100% standard library.  No 3rd party dependencies.

## Installation

From [PyPI](https://pypi.org/project/gituptools/) directly:

```
pip install gituptools
```

## Examples

```py
import gituptools

if __name__ == '__main__':
    gituptools.setup()
```
