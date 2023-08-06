# -*- coding: utf-8 -*-

"""Comparison module.

This module implements the comparison between two trees.
"""

from pathlib import Path

from treecker import config
from treecker.core.colors import colorize

def differences(old, new, hash, path=[]):
    """Return a list of the differences between two tree objects.

    Parameters
    ----------
    old : dict
        Old directory node.
    new : dict
        New directory node.
    hash : bool
        Compare file hash values.
    path : list
        Initial path.

    Returns
    -------
    list
        Differences betwen the two nodes.

    """
    listing = []
    if isinstance(old, dict) and isinstance(new, dict):
        for n in old:
            if n in new:
                listing += differences(old[n], new[n], hash, path+[n])
            else:
                listing.append({'type': 'removed', 'path': path+[n]})
        for n in new:
            if not n in old:
                listing.append({'type': 'added', 'path': path+[n]})
    elif isinstance(old, dict) or isinstance(new, dict):
        listing.append({'type': 'removed', 'path': path})
        listing.append({'type': 'added', 'path': path})
    elif (old[0] != new[0]) or hash and (old[1] != new[1]):
        listing.append({'type': 'edited', 'path': path})
    return listing

def differences_log(differences):
    """Return a printable log of the differences.

    Parameters
    ----------
    differences : list
        List of differences.

    Returns
    -------
    str
        Differences log.

    """
    color, symbol = {}, {}
    for name, value in config[__name__].items():
        if name.startswith('color-'):
            color[name[6:]] = eval(f"'{value}'")
        elif name.startswith('symbol-'):
            symbol[name[7:]] = value
    lines = []
    for diff in differences:
        type = diff['type']
        path = Path(*diff['path'])
        line = colorize(f"{symbol[type]} {path}", color[type])
        lines.append(line)
    if len(differences) == 0:
        lines.append(f"no change found")
    log = "\n".join(lines)
    return log
