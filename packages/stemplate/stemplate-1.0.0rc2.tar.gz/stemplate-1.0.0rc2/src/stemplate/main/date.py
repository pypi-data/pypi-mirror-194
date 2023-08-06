# -*- coding: utf-8 -*-

"""Date module.

This module implements the functionality that allows to display the
date in different time zones.
"""

from datetime import datetime, timezone

from stemplate import config
from stemplate.core.colors import colorize

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
    parser.add_argument('--color',
        help="name of the color",
        type=str,
    )

def main(**kwargs):
    """Display the date.

    Keyword Arguments
    -----------------
    color : str
        Name of the color.

    """
    color = str(kwargs.get('color', config.get(__name__, 'color')))
    date = datetime.now(timezone.utc)
    zone = date.astimezone().tzinfo
    str1 = date.isoformat(timespec="seconds")
    str2 = date.astimezone(zone).isoformat(timespec="seconds")
    text = f"{str1} (UTC)\n{str2} ({zone})"
    colorized = colorize(text, color)
    print(colorized)
