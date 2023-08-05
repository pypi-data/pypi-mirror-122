#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise ValueError("Requires Python 3.6+")

from metriql2metabase import __version__

with open("requirements.txt", "r") as f:
    requires = [x.strip() for x in f if x.strip()]

with open("requirements-test.txt", "r") as f:
    test_requires = [x.strip() for x in f if x.strip()]

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="metriql-metabase",
    version=__version__,
    description="Metriql Metabase integration",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Burak Emre Kabakci",
    author_email="emre@rakam.io",
    url="https://github.com/metriql/metriql-metabase",
    license="MIT License",
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
    scripts=["metriql2metabase/bin/metriql-metabase"],
    tests_require=test_requires,
    install_requires=requires,
    extras_require={"test": test_requires},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)