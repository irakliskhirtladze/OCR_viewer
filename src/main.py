import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Read the QSS file and apply style globally
    with open("ui/resources/styles.qss", "r") as f:
        _qss = f.read()
    app.setStyleSheet(_qss)

    window = MainWindow()
    window.showMaximized()
    app.exec()
