# -*- coding: utf-8 -*-

"""Read feature module.

This module implements the functionality that allows to search and
decode a password.
"""

from getpass import getpass
from os.path import isfile
from pathlib import Path
from sys import stderr

from pashword import config
from pashword.core.book import decode, filter, load
from pashword.core.colors import colorize
from pashword.core.hash import same, save
from pashword.core.sets import combinations

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
    parser.add_argument('--hash',
        help="path to the hash of the key",
        type=str,
    )
    parser.add_argument('--hide',
        action='store_true',
        help="to hide passwords",
        default=False,
    )

def main(book, **kwargs):
    """Decode and display the passwords contained in the book.

    Parameters
    ----------
    book : str
        Path to the password book file.

    Keyword Arguments
    -----------------
    hash : str
        Path to the hash of the key.
    hide : bool
        To hide passwords.

    """
    book = str(book)
    hash = kwargs.get('hash', None)
    hide = kwargs.get('hide', False)
    color_name = config.get(__name__, 'color-name')
    color_show = config.get(__name__, 'color-show')
    color_hide = config.get(__name__, 'color-hide')
    color_warn = config.get(__name__, 'color-warn')
    color_pash = color_hide if hide else color_show
    # load the password book
    data = load(book)
    file = colorize(Path(book).name, color_warn)
    print(f"reading {file} ({len(data)} sections)")
    # filter accounts
    pattern = input("matching pattern: ")
    filtered = filter(data, pattern)
    print(f"{len(filtered)} matching section(s) found")
    if len(filtered) == 0:
        raise SystemExit
    for name in filtered:
        print(f"- {colorize(name, color_name)}")
    # retrieve key
    stop = False
    while not stop:
        if hide:
            key = getpass("secret key: ")
        else:
            key = input("secret key: ")
        if hash:
            if isfile(hash):
                stop = same(key, hash)
            else:
                stop = True
                save(key, hash)
                print(f"key hash saved in {hash}")
        else:
            stop = True
        if not stop:
            error = colorize("incorrect secret key", color_warn)
            print(error, file=stderr)
    # decode
    decoded = decode(filtered, key)
    mode = 'hide' if hide else 'show'
    for name, entries in decoded.items():
        print(f"\n[{colorize(name, color_name)}]")
        for field, value in entries.items():
            if not field in ('password', 'form'):
                print(f"{field} = {value}")
        number = combinations(entries['form'])
        pash = f"{colorize(entries['password'], color_pash)}"
        print(f"pash = {pash} ({number:1.0e})")
    input("\npress enter to exit")
