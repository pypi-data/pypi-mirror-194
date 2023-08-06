#!/usr/bin/env python

# hardcode overwrite __version__ in a package's __init__.py with the version attribute from pyproject.toml
# this is done to avoid errors in github actions when setting __version__ dynamically using importlib.metadata and other methods

# import subprocess
import os
import re
import sys
from packaging import version as pv


def bake() -> None:

    POETRY_TOML = 'pyproject.toml'

    # get version from pyproject.toml
    # ver = subprocess.run(['poetry', 'version', '-s'], capture_output=True, text=True).stdout.rstrip()
    with open(POETRY_TOML, "r") as f:
        text = f.read()
        new_ver = re.search('version = "(.*?)"\\n', text).groups()[0] # get version number between 'version = ' and '\n'
        PACKAGE_NAME = re.search('name = "(.*?)"\\n', text).groups()[0] # get package name between 'name = ' and '\n'

    # put version in __init__.py
    PRJ_INIT = os.path.join(PACKAGE_NAME, "__init__.py")
    
    pattern = '__version__ = "(.*?)"'
    with open(PRJ_INIT, "r") as f:
        text = f.read()
        old_ver = re.search(pattern, text)
        if(not old_ver):
            return
        old_ver = old_ver.groups()[0]
        text_new = re.sub(pattern, f'__version__ = "{new_ver}"', text)

    if(text_new and pv.parse(new_ver) > pv.parse(old_ver)):
        with open(PRJ_INIT, "w") as f:
            f.write(text_new)
        print(f'Updated __version__ in "{PRJ_INIT}" to match {POETRY_TOML}')
        print(f'Old: __version__ = {old_ver}')
        print(f'New: __version__ = {new_ver}')

    sys.exit(0)


if(__name__ == "__main__"):
    bake()
