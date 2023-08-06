# -*- coding: utf-8 -*-

"""Issues feature module.

This module implements the feature that allows to check the file and
directory names.
"""

from os.path import join

from treecker import config
from treecker.core.naming import issues, issues_log
from treecker.core.snapshot import take

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
    """Display incorrectly named files and directories.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.

    """
    directory = str(kwargs.get('dir', '.'))
    # load directory configuration
    config.read(join(directory, config.get('DEFAULT', 'conf-file')))
    # retrieve the tree structure
    snap = take(directory, False)
    tree = snap['tree']
    # display recommendations
    listing = issues(tree)
    log = issues_log(listing)
    print(log)
