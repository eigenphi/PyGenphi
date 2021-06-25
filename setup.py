# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name = "PyGenphi",
  version = "0.1.10",
  author = "David",
  author_email = "david@eigenphi.com",
  description = "Standard Datasource of Quant Trading",
  long_description_content_type = "text/markdown",
  long_description = long_description,
  license = "MIT",
  url = "https://github.com/eigenphi/PyGenphi",
  packages = ['PyGenphi'],
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
