from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QScrollArea, QLabel

from models.image_store import ImageItem


class ThumbLabel(QLabel):
    clicked = Signal(ImageItem)

    def __init__(self, img_item: ImageItem, parent=None):
        super().__init__(parent)
        self.img_item = img_item
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: green")
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.img_item)
