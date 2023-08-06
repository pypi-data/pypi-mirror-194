# -*- coding: utf-8 -*-

"""Sort feature module.

This module implements the functionality that allows to sort a
password configuration file.
"""

from pashword.core.book import load, save

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
    parser.add_argument('book',
        help="path to the password book file",
        type=str,
    )

def main(book, **kwargs):
    """Sort a password book.

    Parameters
    ----------
    book : str
        Path to the password book file.

    """
    book = str(book)
    data = load(book)
    ordered = {}
    for name in sorted(data.keys()):
        ordered[name] = data[name]
    save(book, ordered)
