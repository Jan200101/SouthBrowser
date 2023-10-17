# -*- coding: utf-8 -*-
import setuptools
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = None
with open('south_browser/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "south-browser",
    version = version,
    description = "python based",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = [
        "south_browser",
    ],

    python_requires = ">=3.6",

    entry_points = {
        'console_scripts': [
            'south-browser=south_browser.__main__:main',
        ],
    },
)
