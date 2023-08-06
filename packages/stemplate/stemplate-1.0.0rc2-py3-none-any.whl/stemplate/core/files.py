# -*- coding: utf-8 -*-

"""Files module.

This module implements features for reading files.
"""

from os import stat

import numpy as np

from stemplate import config

def get_beginning(path, lines, **kwargs):
    """Return the first lines of a text file.

    Parameters
    ----------
    path : str
        Path to the file to read.
    lines : int
        Number of lines returned.

    Keyword Arguments
    -----------------
    encoding : str
        Encoding of the file.

    Returns
    -------
    str
        The first lines of the text file.

    """
    lines = int(lines)
    encoding = kwargs.get('encoding', config.get(__name__, 'encoding'))
    head = []
    with open(path, 'r', encoding=encoding) as file:
        for i in range(lines):
            head.append(file.readline())
    return ''.join(head)

def get_size(path):
    """Return the size of the file.

    Parameters
    ----------
    path : str
        Path to the file.

    Returns
    -------
    int
        Size of the file in bytes.

    """
    size = stat(path).st_size
    return np.int64(size)
