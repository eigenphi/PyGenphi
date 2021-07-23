# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os.path

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

def read(rel_path):
  here = os.path.abspath(os.path.dirname(__file__))
  with codecs.open(os.path.join(here, rel_path), 'r') as fp:
    return fp.read()

def get_version(rel_path):
  print("rel_path: " + rel_path)
  for line in read(rel_path).splitlines():
    if line.startswith('__version__'):
      delim = '"' if '"' in line else "'"
      return line.split(delim)[1]
  raise RuntimeError("Unable to find version string.")

setup(
  name = "PyGenphi",
  version = get_version("PyGenphi/__init__.py"),
  author = "David",
  author_email = "david@eigenphi.com",
  description = "Standard Datasource of Quant Trading",
  long_description_content_type = "text/markdown",
  long_description = long_description,
  license = "MIT",
  url = "https://github.com/eigenphi/PyGenphi",
  packages = ['PyGenphi', 'PyGenphi.enum'],
  install_requires = [
    "aiohttp==3.7.4",
    "wheel==0.36.2",
    "asyncio==3.4.3",
    "requests==2.24.0"
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
