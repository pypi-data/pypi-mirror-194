# -*- coding: utf-8 -*-

"""Book module.

This module implements functionalities to manipulate password books.
"""

from configparser import ConfigParser
from fnmatch import fnmatch

from pashword import config
from pashword.core.hash import password

def load(path):
    """Return the data contained in the file.

    Parameters
    ----------
    path : str
        Path to the password book.

    Returns
    -------
    dict
        Password book data.

    """
    config = ConfigParser()
    with open(path, 'r') as file:
        config.read_file(file)
    book = {}
    for name in config.sections():
        book[name] = dict(config[name])
    return book

def save(path, book):
    """Save the book into a file.

    Parameters
    ----------
    path : str
        Path of the password book to be saved.
    book : dict
        Password book data to be saved.

    """
    config = ConfigParser()
    config.read_dict(book)
    with open(path, 'w') as file:
        config.write(file)

def filter(book, pattern):
    """Return the accounts whose name matches the pattern.

    Parameters
    ----------
    book : dict
        Password book.
    pattern : str
        Filtering pattern.

    Returns
    -------
    dict
        Filtered password book.

    """
    filtered = {}
    for name, account in book.items():
        if fnmatch(name, pattern):
            filtered[name] = account
    return filtered

def decode(book, key):
    """Return the book augmented with passwords.

    Parameters
    ----------
    book : dict
        Password book.
    key : str
        Secret key.

    Returns
    -------
    dict
        Decoded password book.

    """
    decoded = {}
    for name, account in book.items():
        data = account.copy()
        form = data.pop('form')
        salt = ''.join(sorted(data.values())) + name
        word = password(key, salt, form)
        data = dict(**account, password=word)
        decoded[name] = data
    return decoded
