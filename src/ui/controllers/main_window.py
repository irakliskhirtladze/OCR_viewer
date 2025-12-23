from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import Qt, QPixmap, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox

from ui.controllers.file_controller import FileController
from ui.controllers.ocr_controller import OCRController
from ui.generated.ui_mainwindow import Ui_MainWindow
from models.data_store import DataStore, ImageItem
from ui.controllers.filter_controller import FilterController
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
        self.filter_controller = FilterController(self.ui, self.data_store)
        self.ocr_controller = OCRController(self.ui, self.data_store)
        self.file_controller = FileController(self.ui, self.data_store, self.ocr_controller)







