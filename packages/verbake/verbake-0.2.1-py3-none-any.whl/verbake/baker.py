# hardcode overwrite __version__ in a package's __init__.py with the version attribute from pyproject.toml
# this is done to avoid errors in github actions when setting __version__ dynamically using importlib.metadata and other methods

# import subprocess
import os
import re


def bake() -> None:
    PACKAGE_NAME = input("Package src dir name: ")
    POETRY_TOML = 'pyproject.toml'

    # get version from pyproject.toml
    # ver = subprocess.run(['poetry', 'version', '-s'], capture_output=True, text=True).stdout.rstrip()
    with open(POETRY_TOML, "r") as f:
        text = f.read()
        ver = re.search('version = (.*?)\\n', text).groups()[0] # get version number between 'version = ' and '\n'

    # put version in __init__.py
    PRJ_INIT = os.path.join(PACKAGE_NAME, "__init__.py")
    pattern = '__version__ = (.*?)\n'
    with open(PRJ_INIT, "r") as f:
        text = f.read()
        text_version = re.search(pattern, text)
        if(not text_version):
            return
        text_new = re.sub(pattern, f'__version__ = {ver}\n', text)

    if(text_new):
        with open(PRJ_INIT, "w") as f:
            f.write(text_new)

if(__name__ == "__main__"):
    bake()