# -*- coding: utf-8 -*-

"""Status feature module.

This module implements the feature that allows to display the changes
that have occurred in the tracked directory.
"""

from datetime import datetime, timezone
from os.path import join

from treecker import config
from treecker.core.comparison import differences, differences_log
from treecker.core.snapshot import initialized, load, take

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
    parser.add_argument('--hash',
        action='store_true',
        help="compare file hash values",
    )

def main(**kwargs):
    """Display the changes since last snapshot.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.
    hash : bool
        Compare file hash values.

    """
    directory = str(kwargs.get('dir', '.'))
    hash = bool(kwargs.get('hash', False))
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
    if hash and not hash1:
        raise Exception("previous hash values not known")
    hash2 = hash
    if not hash2:
        print("comparison of files based on their size only")
    # display differences
    snap2 = take(directory, hash2)
    listing = differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)
