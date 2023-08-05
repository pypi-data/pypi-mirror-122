#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import re
import os
import sys

# In this way, we are sure we are getting
# the installer's version of the library
# not the system's one
sys.path.insert(0,os.path.dirname(__file__))

from RWFileLock import version as RWFileLock_version

# Populating the long description
with open("README.md", "r") as fh:
	long_description = fh.read()

# Populating the install requirements
requirements = []
if os.path.exists('requirements.txt'):
	with open('requirements.txt') as f:
		egg = re.compile(r"#[^#]*egg=([^=&]+)")
		for line in f.read().splitlines():
			m = egg.search(line)
			requirements.append(line  if m is None  else m.group(1))


setuptools.setup(
	name="RWFileLock",
	version=RWFileLock_version,
	author="José Mª Fernández",
	author_email="jose.m.fernandez@bsc.es",
	description="Readers / writers file lock helper class",
	license="LGPLv2",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/inab/RWFileLock",
	project_urls={
		"Bug Tracker": "https://github.com/inab/RWFileLock/issues"
	},
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.5",
)
