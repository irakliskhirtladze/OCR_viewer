from PySide6.QtCore import QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QMessageBox

from models.data_store import DataStore
from ui.controllers.file_controller import FileController
from ui.controllers.filter_controller import FilterController
from ui.controllers.ocr_controller import OCRController
from ui.generated.ui_mainwindow import Ui_MainWindow
from utils.session_manager import SessionManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize store
        self.data_store = DataStore()

        # controllers
        self.filter_controller = FilterController(self.ui, self.data_store)
        self.ocr_controller = OCRController(self.ui, self.data_store)
        self.file_controller = FileController(self.ui, self.data_store, self.ocr_controller)

        # Session manager
        self.session_manager = SessionManager()

        # Try restore on startup (after UI is ready)
        QTimer.singleShot(100, self._try_restore_session)

    def closeEvent(self, event: QCloseEvent):
        """Ask user to save before closing."""
        # Check if there's unsaved work
        if not self._has_unsaved_changes():
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "Save Progress",
            "Do you want to save your current progress before closing?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes  # Default button
        )

        if reply == QMessageBox.Yes:
            self.session_manager.clear()
            self.session_manager.save(
                data_store=self.data_store,
                ui=self.ui,
            )
            event.accept()
        elif reply == QMessageBox.No:
            # Clear the saved flag so startup knows not to resume
            self.session_manager.clear()
            event.accept()
        else:  # Cancel
            event.ignore()

    def _has_unsaved_changes(self) -> bool:
        """Check if there's work worth saving."""
        return bool(self.data_store.get_img_items())

    def _try_restore_session(self):
        if not self.session_manager.has_saved_session():
            return

        reply = QMessageBox.question(
            self, "Restore Session",
            "Found a previous session. Restore it?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.session_manager.restore(data_store=self.data_store, ui=self.ui):
                self.ui.statusbar.showMessage("Session restored", 3000)
        else:
            self.session_manager.clear()
