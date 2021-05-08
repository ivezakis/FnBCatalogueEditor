import sys
from PyQt6.QtWidgets import (QApplication)
from views.main_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
