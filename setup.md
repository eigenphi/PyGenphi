How to setup a Pypi lib:

1,make dir tree
 |---- PyGenphi
 |       |---- __init__.py
 |       |---- xxx.py
 |---- LICENSE
 |---- pyproject.toml
 |---- README.md
 |---- setup.py

2,complete config files

 - pyproject.toml
```
[build-system]
requires = [
    "aiohttp",
    "wheel",
    "asyncio",
    "requests"
]
build-backend = "setuptools.build_meta"
```

 - setup.py
```
# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
  name = "PyGenphi",
  version = "0.0.5",
  author = "David",
  author_email = "david@eigenphi.com",
  description = "Standard Datasource of Quant Trading",
  long_description = open("README.md").read(),
  license = "MIT",
  url = "https://github.com/eigenphi/PyGenphi",
  packages = ['PyGenphi'],
  install_requires = [
    "aiohttp",
    "wheel",
    "asyncio",
    "requests"
   ],
  classifiers = [
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Text Processing :: Indexing",
    "Topic :: Utilities",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
 ],
)
```

3,Prepare account of Pypi
 - register on Pypi.org
 - edit ~/.pypirc
```
[distutils]
index-servers=pypi

[pypi]
https://upload.pypi.org/legacy/
username = hitdavid
password = ***
```
Then run command：
``` 
chmod 600 ~/.pypirc
python setup.py register -r pypi
```

3,build and publish

``` 
python3 setup.py sdist
python3 setup.py install
twine upload dist/*
```

