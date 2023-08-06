# -*- coding: utf-8 -*-

"""Snapshot module.

This module implements the functionalities related to the snapshots.
"""

from datetime import datetime, timezone
from json import dumps as serialize, load as deserialize
from pathlib import Path

from treecker import config
from treecker._version import __version_tuple__
from treecker.core.tree import tree_node

def take(directory, hash):
    """Return a snapshot of the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.
    hash : bool
        Add hash value to file signatures.

    Returns
    -------
    dict
        Directory snapshot data.

    """
    file = config.get(__name__, 'snap-file')
    ignore = config.get(__name__, 'ignore-patterns').split()
    ignore.append(file)
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    node = tree_node(directory, ignore, hash)
    snapshot = {
        'version': list(__version_tuple__),
        'date': date,
        'hash': hash,
        'tree': node,
    }
    return snapshot

def save(directory, snapshot):
    """Save the snapshot in the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.
    snapshot : dict
        Directory snapshot to be saved.

    """
    path = Path(directory) / config.get(__name__, 'snap-file')
    with open(path, "w") as file:
        file.write(serialize(snapshot))

def load(directory):
    """Load the last snapshot of the directory.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.

    Returns
    -------
    dict
        Last snapshot of the directory.

    """
    path = Path(directory) / config.get(__name__, 'snap-file')
    with open(path, "r") as file:
        snapshot = deserialize(file)
    return snapshot

def initialized(directory):
    """Check if the directory is tracked.

    Parameters
    ----------
    directory : str
        Path to the directory.

    Returns
    -------
    bool
        True if the directory is tracked.

    """
    path = Path(directory) / config.get(__name__, 'snap-file')
    return path.is_file()
