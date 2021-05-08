import re

import pandas as pd
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import numpy as np
from ast import literal_eval
from datetime import datetime

import table.table_operations as tap
from undoCommands import CommandEditCell


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, items, parent):
        super(TableModel, self).__init__()
        self.parent = parent
        self._items = items.to_numpy(dtype=str)
        self.header = np.array(items.columns)

        items = pd.DataFrame(self._items, columns=self.header)
        items.replace('^nan', '', regex=True, inplace=True)
        items.replace('^<NA>', '', regex=True, inplace=True)
        self._items = items.to_numpy(dtype=str)

    def headerData(self, section, orientation, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientations.Horizontal:
                return str(self.header[section]).strip()
            if orientation == Qt.Orientations.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return self._items.shape[0]

    def columnCount(self, index):
        return self._items.shape[1]

    def data(self, index, role=None):
        if index.isValid():
            row = index.row()
            col = index.column()

            if role == Qt.ItemDataRole.DisplayRole:
                cell = self._items[row, col]
                try:
                    cell = literal_eval(cell)
                    if isinstance(cell, datetime):
                        return cell.strftime("%Y-%m-%d")
                    if isinstance(cell, float):
                        return "%.2f" % cell
                    if isinstance(cell, int):
                        return "%.0f" % cell
                except Exception:
                    return str(cell).strip()

            if role == Qt.ItemDataRole.EditRole:
                cell = self._items[row, col]
                return str(cell)

            if role == Qt.ItemDataRole.TextAlignmentRole:
                cell = self._items[row, col]
                try:
                    if not isinstance(literal_eval(cell), str):
                        return Qt.Alignment.AlignRight | Qt.Alignment.AlignCenter
                except Exception:
                    pass

        return None

    def setData(self, index, value, role=None):
        if role == Qt.ItemDataRole.EditRole:
            if self._items[index.row(), index.column()] != str(value):
                try:
                    command = CommandEditCell(self, index, value, "Edit cell")
                    self.parent.undo_stack.push(command)
                except Exception as e:
                    raise e
                return True
            return False

    def flags(self, index):
        return Qt.ItemFlags.ItemIsSelectable | Qt.ItemFlags.ItemIsEnabled | Qt.ItemFlags.ItemIsEditable

    def insert_row(self, row_index, items=None):
        self._items = tap.insert_row(self._items, row_index, items)
        self.layoutChanged.emit()

    def insert_column(self, col_index, items=None):
        self._items, self.header = tap.insert_column(self._items, col_index,
                                                     self.header, items)
        self.layoutChanged.emit()

    def delete_row(self, row_index):
        self._items = tap.delete_row(self._items, row_index)
        self.layoutChanged.emit()

    def delete_column(self, col_index):
        self._items, self.header = tap.delete_column(self._items, col_index,
                                                     self.header)
        self.layoutChanged.emit()

    def edit_item(self, index, value):
        self._items = tap.edit_item(self._items, str(value), index.row(),
                                    index.column())
        self.dataChanged.emit(index, index)

    def replace(self, to_replace, value):
        self._items = tap.replace_all(self._items, to_replace, value,
                                      self.header)
        self.layoutChanged.emit()

    def find(self, value):
        return tap.find(self._items, value, self.header)

    def rename_header(self, index, value):
        self.header = tap.edit_item(self.header, str(value), None,
                                    index.column())
        self.layoutChanged.emit()

    @property
    def items(self):
        return np.copy(self._items)

    @items.setter
    def items(self, values):
        self._items = values
        self.layoutChanged.emit()


class TableModel2(TableModel):
    def __init__(self, items, parent, parent_table):
        super(TableModel, self).__init__()
        self.parent_table = parent_table
        self.parent = parent
        self._items = items.to_numpy(dtype=str)
        self.header = np.array(items.columns)

        items = pd.DataFrame(self._items, columns=self.header)
        items.replace('^nan', '', regex=True, inplace=True)
        items.replace('^<NA>', '', regex=True, inplace=True)
        self._items = items.to_numpy(dtype=str)

    def setData(self, index, value, role=None):
        if role == Qt.ItemDataRole.EditRole:
            if self._items[index.row(), index.column()] != str(value):
                try:
                    self.parent_table.replace(
                        '^' + re.escape(self._items[
                            index.row(), index.column()]) + '$', value)
                    command = CommandEditCell(self, index, value, "Edit cell")
                    self.parent.undo_stack.push(command)
                except Exception as e:
                    raise e
                return True
            return False
