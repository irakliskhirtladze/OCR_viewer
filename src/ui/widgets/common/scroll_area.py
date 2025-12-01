from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QScrollArea, QScrollBar, QWidget


class HorizontalThumbnailScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QWheelEvent):
        """
        Convert vertical wheel movement into horizontal scrolling.
        """
        delta_y = event.angleDelta().y()
        if delta_y != 0:
            bar: QScrollBar = self.horizontalScrollBar()
            # adjust this factor if it feels too fast/slow
            bar.setValue(bar.value() - delta_y)
            event.accept()
        else:
            super().wheelEvent(event)

    def resizeEvent(self, event):
        """
        Keep direct child widgets' height = viewport height (minus scrollbar if needed).
        """
        super().resizeEvent(event)

        viewport_h = self.viewport().height()

        w = self.widget()
        if not w:
            return

        # adjust direct child widget heights (content-agnostic)
        for child in w.findChildren(QWidget, options=Qt.FindDirectChildrenOnly):
            child.setFixedHeight(max(1, viewport_h))