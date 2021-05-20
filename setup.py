# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name = "PyGenphi",
  version = "0.1.0",
  author = "David",
  author_email = "hitdavid@eigenphi.com",
  description = "Standard Datasource of Quant Trading",
  long_description_content_type = "text/markdown",
  long_description = long_description,
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
