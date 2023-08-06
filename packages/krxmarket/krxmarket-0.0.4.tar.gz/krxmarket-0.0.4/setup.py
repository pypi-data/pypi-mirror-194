#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import search

from setuptools import setup


def get_version():
    with open('krxmarket/version.py') as version_file:
        return search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                      version_file.read()).group('version')


setup(
    name="krxmarket",
    version=get_version()
)
