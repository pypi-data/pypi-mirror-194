# -*- coding: utf-8 -*-

"""Hash module.

This module provides the hash features for password creation and
secret key validation.
"""

from hashlib import new
from json import dump, load
from uuid import uuid4

from pashword import config
from pashword.core.sets import get

def digest(key, salt):
    """Return the hash value in binary.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.

    Returns
    -------
    bytes
        Digest value.

    """
    algo = config.get(__name__, 'hash-algo')
    hashing = new(algo, usedforsecurity=True)
    hashing.update(key.encode('utf-8'))
    hashing.update(salt.encode('utf-8'))
    return hashing.digest()

def hexdigest(key, salt):
    """Return the hash value in hexadecimal.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.

    Returns
    -------
    str
        Hexadecimal digest value.

    """
    return digest(key, salt).hex()

def password(key, salt, form):
    """Return the account password.

    Parameters
    ----------
    key : str
        Secret key.
    salt : str
        Hash salt.
    form : str
        Password format.

    Returns
    -------
    str
        Password value.

    """
    # get integer hash value
    bytes = digest(key, salt)
    index = int.from_bytes(bytes, byteorder='big', signed=False)
    # get resulting string
    word = []
    for metacharacter in form:
        characters = get(metacharacter)
        size = len(characters)
        word.append(characters[index%size])
        index //= size
    word = ''.join(word)
    return word

def save(key, path):
    """Save a hash of the key in a file.

    Parameters
    ----------
    key : str
        Secret key.
    path : str
        Path of the file containing the hash.

    """
    salt = str(uuid4())
    data = {
        'salt': salt,
        'hash': hexdigest(key, salt),
    }
    with open(path, 'w') as file:
        dump(data, file)

def same(key, path):
    """Return wether the key is the same as the one from the file.

    Parameters
    ----------
    key : str
        Secret key.
    path : str
        Path of the file containing the hash.

    """
    with open(path, 'r') as file:
        data = load(file)
    return data['hash'] == hexdigest(key, data['salt'])
