import numpy as np
import pandas as pd


def insert_row(table, index, data=None):
    """Insert a row to a table.

    Parameters
    ----------
    table : np.ndarray
        The table to insert the row to.
    index : int
        The index of the row to be inserted.
    data : np.ndarray
        Optionally provide a row with data to insert.

    Returns
    -------
    np.ndarray
        The table with the row inserted.
    """
    return np.insert(table, index, data, axis=0)


def insert_column(table, index, header=None, data=None):
    """ Insert a column to a table.

    Parameters
    ----------
    table : np.ndarray
        The table to insert the column to.
    index : int
        The index of the column to be inserted.
    header : np.ndarray
        An optional array containing the headers of the table, if they
         exist.
    data : np.ndarray
        Optionally provide data to insert to the new column.

    Returns
    -------
    np.ndarray
        The table with the column inserted.
    np.ndarray or None
        The table's headers, with the new one inserted. None if
        no headers were given.
    """
    if data is None:
        new_header = np.empty(1, dtype=str)
        data = np.empty((1, table.shape[0]), dtype=str)
    else:
        new_header = data[0]

    table = np.insert(table, index, data, axis=1)
    if header is not None:
        new_header = np.insert(header, index, new_header)
    else:
        new_header = None

    return table, new_header


def delete_row(table, index):
    """Delete a row from a table.

    Parameters
    ----------
    table : np.ndarray
        The table to delete the row from.
    index : int
        The index of the row to delete.

    Returns
    -------
    np.ndarray
        The table with the row deleted.
    """
    return np.delete(table, index, axis=0)


def delete_column(table, index, header=None):
    """Delete a column from a table.

    Parameters
    ----------
    table : np.ndarray
        The table to delete the column from.
    index : int
        The index of the column to delete.
    header : np.ndarray
        Optionally provide the row with headers, if it exists.

    Returns
    -------
    np.ndarray
        The table with the deleted column.
    np.ndarray or None
        The headers with the respective index deleted. None if no
        headers were given.
    """
    table = np.delete(table, index, axis=1)
    if header is not None:
        header = np.delete(header, index)
    return table, header


def edit_item(table, value, row, col):
    """Edit a cell in a table.

    Parameters
    ----------
    table : np.ndarray
        The table whose cell is to be edited.
    value : str
    The value to add to the cell.
    row : int
        The cell's row index.
    col : int
        The cell's column index.

    Returns
    -------
    np.ndarray
        The updated table.
    """
    table[row, col] = value
    return table


def replace_all(table, expression, value, header=None):
    """Replace all occurences in the table using regular expression.

    Parameters
    ----------
    table : np.ndarray
        The table where the respective values will be replaced.
    expression : str
        A regular expression to find matches.
    value : str
        The string to replace the matches with.
    header : np.ndarry
        An optional array with the header names, if they are defined.

    Returns
    -------
    np.ndarray
        The table with the replaced values.
    """
    df = pd.DataFrame(table, columns=header)
    df.replace(str(expression), str(value), regex=True, inplace=True)
    table = df.to_numpy(dtype=str)
    return table


def find(table, value, header=None):
    """Perform a search using a regular expression.

    Parameters
    ----------
    table : The table to search in.
    value : A regular expression to search.
    header : Optionally provide the table's headers, if they exist.

    Returns
    -------
    np.ndarray
        An nx2 array containing the indexes of the results.

    """
    df = pd.DataFrame(table, columns=header)
    return df.apply(lambda x: x.str.contains(value)).values.nonzero()

