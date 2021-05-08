from PyQt6.QtCore import QItemSelectionModel
from PyQt6.QtWidgets import QWidget

import undoCommands
from views import find_and_replace_ui as far


class FindReplaceWidget(QWidget, far.Ui_FindAndReplace):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.findNextBtn.clicked.connect(self.find)
        self.replaceAllBtn.clicked.connect(self.replace)

    def find(self):
        matches = self.parent.model.find(self.findText.text())
        selection_model = self.parent.tableView.selectionModel()
        selection_model.select(self.parent.model.index(0, 0),
                               QItemSelectionModel.SelectionFlags.Clear)
        self.replaceBtn.setEnabled(False)
        self.replaceAllBtn.setEnabled(True)
        for i in range(len(matches[0])):
            selection_model.select(
                self.parent.model.index(matches[0][i], matches[1][i]),
                QItemSelectionModel.SelectionFlags.Select)

    def replace(self):
        command = undoCommands.CommandReplaceAll(
            self.parent.model,
            self.findText.text(),
            self.replaceText.text(),
            "Replace %s with %s".format(self.findText.text(),
                                        self.replaceText.text())
        )
        self.parent.undo_stack.push(command)
