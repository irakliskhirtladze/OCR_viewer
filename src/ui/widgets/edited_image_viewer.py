from PySide6.QtCore import Qt, QRect, QEvent
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QLineEdit

from models.data_store import OCRItem, TextRegion
from ui.widgets.common.image_viewer import ImageViewer


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
        self.bbox_overlay.show()
        self.bbox_overlay.raise_()

        # Keep overlay synchronized with image viewer
        self.image_viewer.installEventFilter(self)
        self.image_viewer.transformChanged.connect(self._on_transform_changed)

    def _on_transform_changed(self):
        """Update overlay when image zooms or pans."""
        self.bbox_overlay.update_editors()
        self.bbox_overlay.update()

    def eventFilter(self, obj, event):
        """Keep overlay synchronized with image viewer transformations."""
        if obj == self.image_viewer:
            if event.type() == QEvent.Resize:
                self.bbox_overlay.setGeometry(self.image_viewer.geometry())
                self.bbox_overlay.update_editors()
        return super().eventFilter(obj, event)


class RegionEditor(QLineEdit):
    """Editable text field for a single OCR region."""

    def __init__(self, region: TextRegion, parent=None):
        super().__init__(parent)
        self.region = region
        self.setText(region.text)
        self.setAlignment(Qt.AlignCenter)
        self.setFrame(False)
        self.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 200, 180);
                color: #000;
                border: none;
                padding: 0px;
            }
            QLineEdit:focus {
                background: rgba(255, 255, 150, 220);
            }
        """)
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str):
        self.region.text = text

    def set_font_to_fit(self, width: int, height: int):
        """Adjust font size to fit within given dimensions."""
        if width <= 0 or height <= 0:
            return
        font_size = max(6, height - 4)
        font = QFont("Arial", font_size)
        self.setFont(font)

        fm = QFontMetrics(font)
        text = self.text() or "W"
        while fm.horizontalAdvance(text) > width - 4 and font_size > 6:
            font_size -= 1
            font.setPointSize(font_size)
            fm = QFontMetrics(font)
        self.setFont(font)


class BoundingBoxOverlay(QWidget):
    """Overlay with editable text fields for OCR regions."""

    def __init__(self, image_viewer: ImageViewer, parent=None):
        super().__init__(parent)
        self.image_viewer = image_viewer
        self.regions: list[TextRegion] = []
        self.editors: list[RegionEditor] = []

        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet("background: transparent;")

    def set_regions(self, ocr_item: OCRItem):
        self.clear_regions()
        self.regions = ocr_item.regions
        self._create_editors()
        self.update()

    def clear_regions(self):
        for editor in self.editors:
            editor.deleteLater()
        self.editors.clear()
        self.regions = []
        self.update()

    def _create_editors(self):
        """Create QLineEdit widgets for each region."""
        for region in self.regions:
            editor = RegionEditor(region, self)
            editor.show()
            self.editors.append(editor)
        self.update_editors()

    def update_editors(self):
        """Reposition and resize all editors to match current image transform."""
        if not self.image_viewer.pixmap or not self.image_viewer.original_pixmap:
            return

        img_x = (self.image_viewer.width() - self.image_viewer.pixmap.width()) // 2 + self.image_viewer.pan_offset.x()
        img_y = (self.image_viewer.height() - self.image_viewer.pixmap.height()) // 2 + self.image_viewer.pan_offset.y()
        scale_x = self.image_viewer.pixmap.width() / self.image_viewer.original_pixmap.width()
        scale_y = self.image_viewer.pixmap.height() / self.image_viewer.original_pixmap.height()

        for editor in self.editors:
            region = editor.region
            x = int(img_x + region.bbox[0] * scale_x)
            y = int(img_y + region.bbox[1] * scale_y)
            w = int(region.bbox[2] * scale_x)
            h = int(region.bbox[3] * scale_y)

            editor.setGeometry(x, y, w, h)
            editor.set_font_to_fit(w, h)

    def paintEvent(self, event):
        if not self.regions or not self.image_viewer.pixmap or not self.image_viewer.original_pixmap:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        img_x = (self.image_viewer.width() - self.image_viewer.pixmap.width()) // 2 + self.image_viewer.pan_offset.x()
        img_y = (self.image_viewer.height() - self.image_viewer.pixmap.height()) // 2 + self.image_viewer.pan_offset.y()
        scale_x = self.image_viewer.pixmap.width() / self.image_viewer.original_pixmap.width()
        scale_y = self.image_viewer.pixmap.height() / self.image_viewer.original_pixmap.height()

        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        font = QFont("Arial", 9, QFont.Normal)
        painter.setFont(font)

        for region in self.regions:
            x = int(img_x + region.bbox[0] * scale_x)
            y = int(img_y + region.bbox[1] * scale_y)
            w = int(region.bbox[2] * scale_x)
            h = int(region.bbox[3] * scale_y)

            # Draw bounding box
            rect = QRect(x, y, w, h)
            painter.drawRect(rect)

            # Draw confidence label above box
            conf_text = f"{region.confidence:.2f}"
            text_rect = painter.fontMetrics().boundingRect(conf_text)
            label_x = x
            label_y = y - text_rect.height() - 2

            bg_rect = QRect(label_x, label_y, text_rect.width() + 4, text_rect.height() + 2)
            painter.fillRect(bg_rect, QColor(0, 0, 0, 180))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(label_x + 2, label_y + text_rect.height(), conf_text)
            painter.setPen(pen)

