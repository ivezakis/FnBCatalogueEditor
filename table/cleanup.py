import re


def remove_mult_spaces(string):
    """Remove multiple spaces from a string.

    Parameters
    ----------
    string : str
        The string to remove the spaces from.

    Returns
    -------
    str
        The transformed string.

    """
    return re.sub(' +', ' ', string.strip())
