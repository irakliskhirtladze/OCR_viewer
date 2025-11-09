from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStyleOption, QStyle, QFrame

from ui.models.image_store import ImageStore
from ui.models.text_store import TextStore
from ui.widgets.left_container import LeftContainer
from ui.widgets.right_container import RightContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Viewer")
        self.setMinimumSize(QSize(800, 600))
        # self.showMaximized()

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(QHBoxLayout())

        # Image store
        self.image_store = ImageStore()
        self.text_store = TextStore()

        # Add image_viewer to layout
        self.image_viewer_cont = LeftContainer(self.image_store, self.text_store)
        central_widget.layout().addWidget(self.image_viewer_cont, 2)

        # Add right panel to layout
        self.right_cont = RightContainer(self.image_store, self.text_store)
        central_widget.layout().addWidget(self.right_cont, 3)
