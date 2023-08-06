# -*- coding: utf-8 -*-

"""Colors module.

This module implements features related to text colorization.
"""

from pashword import config

def get_code(name):
    """Return the color code.

    Parameters
    ----------
    name : str
        Name of the color code in the configuration file.

    Returns
    -------
    str
        Color code.

    """
    color = config.get(__name__, name)
    return eval(f"'{color}'")

def colorize(string, color):
    """Return the colorized string.

    Parameters
    ----------
    string : str
        The text to colorize.
    color : str
        The name of the color.

    Returns
    -------
    str
        Colorized text.

    """
    start = get_code(color)
    end = get_code('end')
    return start + string + end
