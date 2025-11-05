from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame

from ui.widgets.image_editor import ImageEditorContainer


class TextViewerWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet("background-color: grey;")
        self.setMinimumSize(100, 100)


class RightContainer(QFrame):
    def __init__(self, image_store):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Add child widgets so the container has a non-zero size hint
        self.img_editor_widget = ImageEditorContainer(image_store)
        self.layout().addWidget(self.img_editor_widget, 2)

        self.txt_viewer_widget = TextViewerWidget()
        self.layout().addWidget(self.txt_viewer_widget, 1)
