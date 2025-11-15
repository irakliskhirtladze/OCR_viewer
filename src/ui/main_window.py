from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame

from ui.models.image_store import ImageStore
from ui.models.text_store import TextStore
from ui.widgets.editor_panel import EditorContainer
from ui.widgets.image_viewers import OriginalImageViewer, EditedImageViewer
from ui.widgets.text_viewer import TextViewerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Viewer")
        self.setMinimumSize(QSize(800, 600))

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(QHBoxLayout())

        # Image store
        self.image_store = ImageStore()
        self.text_store = TextStore()

        # ========================================================================
        # Left container
        # ========================================================================
        self.left_container = QFrame()
        central_widget.layout().addWidget(self.left_container, 2)
        self.left_container.setLayout(QVBoxLayout())
        self.left_container.layout().setContentsMargins(0, 0, 0, 0)

        self.original_image_viewer = OriginalImageViewer(self.image_store)
        self.left_container.layout().addWidget(self.original_image_viewer, 2)

        self.text_viewer = TextViewerWidget(self.text_store)
        self.left_container.layout().addWidget(self.text_viewer, 1)

        # ========================================================================
        # right container
        # ========================================================================
        self.right_container = QFrame()
        central_widget.layout().addWidget(self.right_container, 3)
        self.right_container.setLayout(QHBoxLayout())
        self.right_container.layout().setContentsMargins(0, 0, 0, 0)

        self.right_container.layout().addWidget(EditorContainer(self.image_store, self.text_store), 1)
        self.right_container.layout().addWidget(EditedImageViewer(self.image_store), 2)
