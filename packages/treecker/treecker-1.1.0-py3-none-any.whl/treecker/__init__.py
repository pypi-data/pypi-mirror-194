# -*- coding: utf-8 -*-

"""Treecker package.

This Python package is for inspecting and tracking the organization of
files in a directory.
"""

__author__ = 'Dunstan Becht'

from configparser import ConfigParser
from pkgutil import get_data

config = ConfigParser()
config.read_string(get_data(__package__, 'default.conf').decode())
