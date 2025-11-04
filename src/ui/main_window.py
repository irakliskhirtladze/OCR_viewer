from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStyleOption, QStyle, QFrame

from ui.widgets.image_viewer import ImageViewerWidget
from ui.widgets.right_container import RightContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Viewer")
        self.setMinimumSize(QSize(800, 600))

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(QHBoxLayout())

        # Add image_viewer to layout
        self.image_viewer_cont = ImageViewerWidget()
        central_widget.layout().addWidget(self.image_viewer_cont, 1)

        # Add right panel to layout
        self.right_cont = RightContainer()
        central_widget.layout().addWidget(self.right_cont, 1)


