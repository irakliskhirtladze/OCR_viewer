from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import Qt, QPixmap, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox

from ui.controllers.file_manager import FileManager
from ui.controllers.ocr_manager import OCRManager
from ui.generated.ui_mainwindow import Ui_MainWindow
from models.data_store import DataStore, ImageItem
from ui.controllers.filters import FilterManager
from ui.widgets.common.thumbnail_label import ThumbLabel
from utils.file_utils import open_file_dialog, resource_path, get_project_file, get_cache_dir
from ui.workers.file_loader_thread import FileLoaderThread
from ui.workers.progress_runner import ProgressRunner


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize store
        self.data_store = DataStore()

        # controllers
        self.filter_manager = FilterManager(self.ui, self.data_store)
        self.ocr_manager = OCRManager(self.ui, self.data_store)
        self.file_manager = FileManager(self.ui, self.data_store, self.ocr_manager)

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
            self._save_project()
            event.accept()
        elif reply == QMessageBox.No:
            # Clear the saved flag so startup knows not to resume
            self._clear_saved_state()
            event.accept()
        else:  # Cancel
            event.ignore()

    def _has_unsaved_changes(self) -> bool:
        """Check if there's work worth saving."""
        return bool(self.data_store.get_img_items())

    def _save_project(self):
        project_file = get_project_file()
        cache_dir = get_cache_dir()

        original_img_items = self.data_store.get_img_items()
        original_img_item_ids = original_img_items.keys()

    def _clear_saved_state(self):
        pass





