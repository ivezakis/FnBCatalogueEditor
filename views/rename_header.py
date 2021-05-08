from PyQt6.QtWidgets import QDialog

from views import rename_header_ui as rh


class RenameHeaderDialog(QDialog, rh.Ui_Rename_header_dialog):
    def __init__(self, index, parent=None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.index = index
        self.connect_signals_slots()
        if parent:
            self.lineEdit.setText(
                str(self.parent.model.header[self.index.column()]))

    def connect_signals_slots(self):
        self.buttonBox.accepted.connect(self.accept)

    def accept(self):
        value = self.lineEdit.text()
        self.parent.model.rename_header(self.index, value)
        self.close()
