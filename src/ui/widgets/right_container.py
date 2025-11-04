from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame


class ImageEditorWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.setStyleSheet("background-color: orange;")
        self.setMinimumSize(100, 100)


class TextViewerWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet("background-color: green;")
        self.setMinimumSize(100, 100)


class RightContainer(QFrame):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet("background-color: red;")
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Add child widgets so the container has a non-zero size hint
        self.img_editor_widget = ImageEditorWidget()
        self.layout().addWidget(self.img_editor_widget, 2)

        self.txt_viewer_widget = TextViewerWidget()
        self.layout().addWidget(self.txt_viewer_widget, 1)
