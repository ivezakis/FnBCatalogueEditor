import numpy as np
from PyQt6.QtGui import QUndoCommand

from table.cleanup import remove_mult_spaces
import re


class CommandEditCell(QUndoCommand):
    def __init__(self, model, index, value, description):
        super(CommandEditCell, self).__init__(description)
        self.model = model
        self.index = index
        self.value = value
        self.prev = self.model.items[index.row(), index.column()]

    def redo(self):
        self.model.edit_item(self.index, self.value)

    def undo(self):
        self.model.edit_item(self.index, self.prev)


class CommandInsertRow(QUndoCommand):
    def __init__(self, model, row_index, items, description):
        super(CommandInsertRow, self).__init__(description)
        self.model = model
        self.row_index = row_index
        self.items = items

    def redo(self):
        self.model.insert_row(self.row_index, self.items)

    def undo(self):
        self.model.delete_row(self.row_index)


class CommandDeleteRow(QUndoCommand):
    def __init__(self, model, row_index, description):
        super(CommandDeleteRow, self).__init__(description)
        self.model = model
        self.row_index = row_index
        self.items = self.model.items[row_index, :]

    def redo(self):
        self.model.delete_row(self.row_index)

    def undo(self):
        self.model.insert_row(self.row_index, self.items)


class CommandInsertCol(QUndoCommand):
    def __init__(self, model, col_index, items, description):
        super(CommandInsertCol, self).__init__(description)
        self.model = model
        self.col_index = col_index
        self.items = items

    def redo(self):
        self.model.insert_column(self.col_index, self.items)

    def undo(self):
        self.model.delete_column(self.col_index)


class CommandDeleteCol(QUndoCommand):
    def __init__(self, model, col_index, description):
        super(CommandDeleteCol, self).__init__(description)
        self.model = model
        self.col_index = col_index
        self.items = self.model.items[:, col_index]

    def redo(self):
        self.model.delete_column(self.col_index)

    def undo(self):
        self.model.insert_column(self.col_index, self.items)


class CommandReplaceAll(QUndoCommand):
    def __init__(self, model, find_text, replace_text, description):
        super(CommandReplaceAll, self).__init__(description)
        self.model = model
        self.findText = find_text
        self.replaceText = replace_text
        self.prevItems = self.model.items

    def redo(self):
        self.model.replace(self.findText, self.replaceText)

    def undo(self):
        self.model.items = self.prevItems


class CommandStandardize(QUndoCommand):
    def __init__(self, model, description):
        super(CommandStandardize, self).__init__(description)
        self.model = model
        self.prevItems = self.model.items

    def redo(self):
        vfunc1 = np.vectorize(remove_mult_spaces)
        self.model.items = vfunc1(self.model.items)

        vfunc2 = np.vectorize(titlecase)
        self.model.items = vfunc2(self.model.items)

    def undo(self):
        self.model.items = self.prevItems


def titlecase(s):
    return re.sub(
        r"(?<!\d)\b[A-Za-zΑ-Ωα-ωΆ-Ώά-ώ]+('[A-Za-zΑ-Ωα-ωΆ-Ώά-ώ]+)?",
        lambda word: word.group(0).capitalize(),
        s
    )

