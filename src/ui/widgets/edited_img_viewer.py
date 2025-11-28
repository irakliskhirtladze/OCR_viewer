from PySide6.QtCore import Qt, QRect, QEvent
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout

from ui.models.image_store import ImageStore
from ui.models.ocr_store import OCRStore
from ui.widgets.base_widgets.image_viewer import ImageViewer


class EditedImageViewer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Image viewer widget (underlying layer)
        self.image_viewer = ImageViewer()
        self.layout().addWidget(self.image_viewer)

        # Bounding box overlay (top layer) - child of image_viewer
        self.bbox_overlay = BoundingBoxOverlay(self.image_viewer, self.image_viewer)
        self.bbox_overlay.setGeometry(self.image_viewer.geometry())
        self.bbox_overlay.show()  # Make overlay visible
        self.bbox_overlay.raise_()  # Bring to front

        # Keep overlay synchronized with image viewer
        self.image_viewer.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Keep overlay synchronized with image viewer transformations."""
        if obj == self.image_viewer:
            if event.type() == QEvent.Resize:
                # Update overlay size and trigger repaint
                self.bbox_overlay.setGeometry(self.image_viewer.geometry())
                self.bbox_overlay.update()
        return super().eventFilter(obj, event)


class BoundingBoxOverlay(QWidget):
    """Transparent overlay for bounding boxes on top of edited image viewer."""

    def __init__(self, image_viewer: ImageViewer, parent=None):
        super().__init__(parent)
        self.image_viewer = image_viewer
        self.boxes = []

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet("background: transparent;")

    def set_boxes(self, boxes: list):
        self.boxes = boxes
        self.update()

    def clear_boxes(self):
        self.boxes = []
        self.update()

    def paintEvent(self, event):
        if not self.boxes or not self.image_viewer.pixmap or not self.image_viewer.original_pixmap:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate image position and scaling
        img_x = (self.image_viewer.width() - self.image_viewer.pixmap.width()) // 2 + self.image_viewer.pan_offset.x()
        img_y = (self.image_viewer.height() - self.image_viewer.pixmap.height()) // 2 + self.image_viewer.pan_offset.y()

        scale_x = self.image_viewer.pixmap.width() / self.image_viewer.original_pixmap.width()
        scale_y = self.image_viewer.pixmap.height() / self.image_viewer.original_pixmap.height()

        # Set up pen for drawing boxes
        pen = QPen(QColor(0, 255, 0), 2)  # Green, 2px
        painter.setPen(pen)

        # Set up font for confidence labels
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)

        for box in self.boxes:
            # Get original coordinates
            left = box['left']
            top = box['top']
            width = box['width']
            height = box['height']
            confidence = box['conf']

            # Scale to displayed size
            scaled_left = int(left * scale_x)
            scaled_top = int(top * scale_y)
            scaled_width = int(width * scale_x)
            scaled_height = int(height * scale_y)

            # Translate to widget position
            box_x = img_x + scaled_left
            box_y = img_y + scaled_top

            # Draw rectangle
            rect = QRect(box_x, box_y, scaled_width, scaled_height)
            painter.drawRect(rect)

            # Draw confidence label
            conf_text = f"{confidence:.0f}%"
            text_rect = painter.fontMetrics().boundingRect(conf_text)

            # Position label above box (or inside if too close to top)
            label_x = box_x
            label_y = box_y - text_rect.height() - 2 if box_y > text_rect.height() + 2 else box_y + 2

            # Draw background for text
            bg_rect = QRect(label_x, label_y, text_rect.width() + 4, text_rect.height() + 2)
            painter.fillRect(bg_rect, QColor(0, 0, 0, 180))

            # Draw text
            painter.setPen(QColor(255, 255, 255))  # White text
            painter.drawText(label_x + 2, label_y + text_rect.height(), conf_text)
            painter.setPen(pen)  # Restore pen for next box