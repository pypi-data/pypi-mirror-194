# -*- coding: utf-8 -*-

"""Tree module.

This module implements the functionalities related to the trees.
"""

from fnmatch import fnmatch
from hashlib import new
from multiprocessing import Pool
from os import stat
from pathlib import Path

from treecker import config

def file_hash(path):
    """Return the hash value of the file.

    Parameters
    ----------
    path : Path
        Path to the file.

    Returns
    -------
    str
        File hash value.

    """
    size = config.getint(__name__, 'block-size')
    algo = config.get(__name__, 'hash-algo')
    hashing = new(algo)
    with open(path, 'rb') as f:
        series = f.read(size)
        while len(series) > 0:
            hashing.update(series)
            series = f.read(size)
    hash = hashing.hexdigest()
    return hash

def file_size(path):
    """Return the size of the file in bytes.

    Parameters
    ----------
    path : Path
        Path to the file.

    Returns
    -------
    int
        The size of the file in bytes.

    """
    size = stat(path).st_size
    return size

def subtree_node(path, ignore):
    """Return the node representing the tracked element.

    Parameters
    ----------
    path : Path
        Path to the file of directory.
    ignore : list
        Ignored items patterns.

    Returns
    -------
    dict
        Node corresponding to the path.

    """
    if path.is_file():
        node = [file_size(path)]
    elif path.is_dir():
        node = {}
        for entry in path.iterdir():
            relative = entry.relative_to(path)
            if not any([fnmatch(relative, pattern) for pattern in ignore]):
                node[entry.name] = subtree_node(entry, ignore)
    else:
        raise Exception(f"path '{path}' does not exist")
    return node

def tree_items(node, path=[]):
    """Flatten the tree.

    Parameters
    ----------
    node : dict
        Node to be flattened.
    path : list
        Initial path.

    Returns
    -------
    list
        List of (path, signature) tuples.

    """
    items = []
    if isinstance(node, dict):
        for name, child in node.items():
            items += tree_items(child, path+[name])
    else:
        items.append((path, node))
    return items

def add_hash(directory, tree):
    """Add the hash value to the file signatures.

    Parameters
    ----------
    directory : str
        Path to the tracked directory.
    tree : dict
        Directory node.

    """
    items = tree_items(tree)
    items.sort(key=lambda item: item[1][0], reverse=True)
    paths = [Path(directory, *item[0]) for item in items]
    with Pool() as pool:
        hashs = pool.map(file_hash, paths, chunksize=1)
    for item, hash in zip(items, hashs):
        node = tree
        for entry in item[0]:
            node = node[entry]
        node.append(hash)

def tree_node(directory, ignore, hash):
    """Return the tree corresponding to the directory.

    Parameters
    ----------
    directory : str
        Path to the directory.
    ignore : list
        Ignored patterns.
    hash : bool
        Add hash value to file signatures.

    Returns
    -------
    dict
        Directory node.

    """
    node = subtree_node(Path(directory), ignore)
    if hash:
        add_hash(directory, node)
    return node
