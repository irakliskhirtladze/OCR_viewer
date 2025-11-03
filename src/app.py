"""
Main application setup.
Handles QApplication, creates and shows the main window.
Scalable: Add themes, plugins, or error handling here.
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


class OCRViewer(QApplication):
    def __init__(self):
        super().__init__([])
        self.setApplicationName("OCR Viewer")

        # Create and show main window
        self.main_window = MainWindow()
        self.main_window.show()
        self.main_window.setMinimumSize(800, 600)

    def exec(self):
        return super().exec()
