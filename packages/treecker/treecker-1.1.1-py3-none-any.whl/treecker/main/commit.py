# -*- coding: utf-8 -*-

"""Commit feature module.

This module implements the feature that allows to save in a new
snapshot the changes that have occurred in the directory.
"""

from datetime import datetime, timezone
from os.path import join

from treecker import config
from treecker.core.comparison import differences, differences_log
from treecker.core.snapshot import initialized, load, save, take

def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    parser.set_defaults(
        func=main,
    )
    parser.add_argument('--dir',
        help="path to the tracked directory",
        type=str,
    )

def main(**kwargs):
    """Save the changes in a new snapshot.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.

    """
    directory = str(kwargs.get('dir', '.'))
    # load directory configuration
    config.read(join(directory, config.get('DEFAULT', 'conf-file')))
    # check that the directory is tracked before loading latest snapshot
    if not initialized(directory):
        raise Exception(f"treecker not initialized in {directory}")
    snap1 = load(directory)
    # inform user
    date = datetime.fromisoformat(snap1['date'])
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    date = date.astimezone(zone).isoformat(timespec="seconds")
    print(f"comparing with snapshot from {date} ({zone})")
    # hash or no hash
    hash1 = snap1['hash']
    hash2 = hash1
    if not hash2:
        print("comparison of files based on their size only")
    # display differences
    snap2 = take(directory, hash2)
    listing = differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)
    # write new snapshot
    if len(listing) > 0:
        if input("save modifications? (y|n) ") == "y":
            save(directory, snap2)
            print(f"changes commited in {directory}")
