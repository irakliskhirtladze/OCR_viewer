from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from ui.widgets.image_viewer import ImageViewerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_widget.setLayout(QHBoxLayout())

        # Add image_viewer to layout
        self.image_viewer = ImageViewerWidget()
        central_widget.layout().addWidget(self.image_viewer, 1)

        # Add right panel to layout
        self.right_widget = QWidget()
        central_widget.layout().addWidget(self.right_widget, 1)


