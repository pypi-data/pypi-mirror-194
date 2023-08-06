# -*- coding: utf-8 -*-

"""Init feature module.

This module implements the feature that allows to initialize a tree
tracker in a directory.
"""

from os.path import join

from treecker import config
from treecker.core.snapshot import initialized, save, take

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
        help="add hash value to file signatures",
    )

def main(**kwargs):
    """Create the first snapshot of a directory.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.
    hash : bool
        Add hash value to file signatures.

    """
    directory = str(kwargs.get('dir', '.'))
    hash = bool(kwargs.get('hash', False))
    # load directory configuration
    config.read(join(directory, config.get('DEFAULT', 'conf-file')))
    # check that the directory is not already tracked
    if initialized(directory):
        raise Exception(f"treecker already initialized in {directory}")
    # initialize the tracker in the directory
    snap = take(directory, hash)
    save(directory, snap)
    print(f"treecker initialized in {directory}")
