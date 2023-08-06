# Welcome to Gituptools
Gituptools is a helper for packing Python on Gitlab CICD runners.  It basically
gets as much from the runtime environment as it can to fill in all the packaging
metadata that a typical `setup.py` file needs.

```py
import gituptools

if __name__ == '__main__':
    gituptools.setup()
```
