# verbake

A simple script that copies the value of `version` from `pyproject.toml` and uses it to overwrite the value of `__version__` in a package's main `__init__.py`.

This is for getting around the problem of needing to remember to manually version bump both `pyproject.toml` and `__init__.py` (for those packages that need the version in both places) every time you update your project.

This also helps avoid an error that occurs when testing your package in remote environments like GitHub Actions which is caused by dynamically setting `__version__` using `importlib.metadata` and other methods.

## Install ([PyPI](https://pypi.org/project/verbake/))
```
pip install verbake
```

## Usage
```
from verbake.baker import bake
bake()
```
