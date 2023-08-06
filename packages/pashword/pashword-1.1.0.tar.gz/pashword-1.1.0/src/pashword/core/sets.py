# -*- coding: utf-8 -*-

"""Character sets module.

This module provides the character sets used for the construction of
passwords.
"""

from pashword import config

def get(metacharacter):
    """Return the set of characters associated to the metacharacter.

    Parameters
    ----------
    metacharacter : str
        Character associated with a set of characters.

    Returns
    -------
    str
        The set of characters associated to the metacharacter.

    """
    return config.get(__name__, metacharacter, fallback=metacharacter)

def combinations(form):
    """Return the number of possible combinations for the given format.

    Parameters
    ----------
    form : str
        Metacharacters defining the password format.

    Returns
    -------
    int
        The number of possible combinations for the given format.

    """
    number = 1
    for metacharacter in form:
        number *= len(get(metacharacter))
    return number
