from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QFont, QWheelEvent
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, \
    QScrollBar, QScrollArea, QErrorMessage
from PySide6.QtCore import QEvent, Slot, Qt, QRect, Signal

import fitz

from ui.models.image_store import ImageStore
from ui.models.ocr_store import OCRStore
from ui.widgets.custom_image_viewer import ImageViewer
from utils.file_utils import open_file_dialog

from ui.models.image_store import ImageItem


class HorizontalThumbnailScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
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
        Keep thumbnail labels' height = viewport height minus scrollbar height.
        """
        super().resizeEvent(event)

        viewport_h = self.viewport().height()

        w = self.widget()
        if not w:
            return

        # adjust direct child QLabel thumbnail heights
        for child in w.findChildren(QLabel, options=Qt.FindDirectChildrenOnly):
            child.setFixedHeight(max(1, viewport_h))


class ThumbLabel(QLabel):
    clicked = Signal(ImageItem)

    def __init__(self, img_item):
        super().__init__()
        self.img_item = img_item
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.img_item)


class OriginalImageViewer(QFrame):
    def __init__(self, image_store: ImageStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.image_store = image_store

        # Listen to image store changes
        self.image_store.imagesChanged.connect(self.on_images_changed)

        # Top button bar
        self._create_button_bar()

        # Horizontal scroll area for thumbnails
        self.thumb_scroll = HorizontalThumbnailScrollArea()
        self.thumb_scroll.setStyleSheet("background-color: grey")
        self.thumb_scroll.setFixedHeight(100)
        self.layout().addWidget(self.thumb_scroll)

        self.thumb_container = QWidget()
        self.thumb_layout = QHBoxLayout(self.thumb_container)
        self.thumb_layout.setContentsMargins(0, 0, 0, 0)
        # self.thumb_layout.setSpacing(4)

        self.thumb_scroll.setWidget(self.thumb_container)

    def _create_button_bar(self):
        """Create the top button bar with file chooser."""
        btn_cont = QFrame()
        btn_cont.setStyleSheet("background-color: grey")
        btn_cont.setFixedHeight(50)
        btn_cont.setLayout(QHBoxLayout())

        # Choose image button
        choose_btn = QPushButton("Choose files")
        btn_cont.layout().addWidget(choose_btn)
        choose_btn.setCursor(Qt.PointingHandCursor)
        choose_btn.clicked.connect(self.on_choose_files)

        # Spacer
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btn_cont.layout().addItem(spacer)

        # clear all button
        clear_all_btn = QPushButton("Clear all")
        btn_cont.layout().addWidget(clear_all_btn)
        clear_all_btn.setCursor(Qt.PointingHandCursor)
        clear_all_btn.clicked.connect(self.on_clear_all)

        self.layout().addWidget(btn_cont)

    # ========================================================================
    # File Loading
    # ========================================================================
    @Slot()
    def on_choose_files(self):
        """Open file dialog to choose an image."""
        file_paths = open_file_dialog(
            parent=self,
            caption="Choose Images or PDF",
            filter_str="Files (*.png *.jpg *.jpeg *.pdf)",
            multi=True
        )

        if file_paths:
            self._load_files(file_paths)

    def _load_files(self, file_paths: list):
        """Load images and add to scroll area."""
        image_list = []
        for file_path in file_paths:
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                img_item = ImageItem(QImage(file_path), file_path)
                image_list.append(img_item)

            elif file_path.lower().endswith(".pdf"):
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(alpha=False)
                    qimage = QImage(
                        pix.samples,
                        pix.width,
                        pix.height,
                        pix.stride,
                        QImage.Format.Format_RGB888
                    ).copy()
                    img_item = ImageItem(qimage, file_path, page_num)
                    image_list.append(img_item)

        self.image_store.add_img_items(image_list)

    @Slot(list)
    def on_images_changed(self, images: list[ImageItem]):
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        viewport_h = self.thumb_scroll.viewport().height()

        for img in images:
            label = ThumbLabel(img)
            self.thumb_layout.addWidget(label)
            label.setFixedSize(100, viewport_h)
            label.setStyleSheet("background-color: red")
            label.setAlignment(Qt.AlignCenter)

            qimg = img.image
            pixmap = QPixmap.fromImage(qimg)
            pixmap = pixmap.scaled(
                label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)

            label.clicked.connect(self.on_image_label_clicked)

        # Whenever images list in store is updated, set the first image to edited image
        if len(images) > 0:
            self.image_store.set_original_img(images[0].image)
        else:
            self.image_store.clear_original_img()

    @Slot()
    def on_clear_all(self):
        self.image_store.clear_images()

    @Slot(ImageItem)
    def on_image_label_clicked(self, img_item: ImageItem):
        self.image_store.set_original_img(img_item.image)


class EditedImageViewer(QFrame):
    def __init__(self, image_store: ImageStore, ocr_store: OCRStore):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.image_store = image_store
        self.ocr_store = ocr_store

        # Image viewer widget (underlying layer)
        self.image_viewer = ImageViewer()
        self.layout().addWidget(self.image_viewer)

        # Bounding box overlay (top layer) - child of image_viewer
        self.bbox_overlay = BoundingBoxOverlay(self.image_viewer, self.image_viewer)
        self.bbox_overlay.setGeometry(self.image_viewer.geometry())
        self.bbox_overlay.show()  # Make overlay visible
        self.bbox_overlay.raise_()  # Bring to front

        # Connect signals
        self.image_store.editedImageChanged.connect(self._on_edited_image_changed)
        self.ocr_store.result_changed.connect(self._on_ocr_changed)

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

    @Slot(QImage)
    def _on_edited_image_changed(self, qimg: QImage):
        """Update image viewer when edited image changes."""
        if qimg is not None and not qimg.isNull():
            pixmap = QPixmap.fromImage(qimg)
            self.image_viewer.load_pixmap(pixmap)
            # Trigger overlay repaint
            self.bbox_overlay.update()
            # Clear old bounding boxes since image changed
            self.bbox_overlay.clear_boxes()
        else:
            self.image_viewer.clear()
            self.bbox_overlay.clear_boxes()

    @Slot(list)
    def _on_ocr_changed(self, result: list):
        """Update bounding boxes when OCR results change."""
        self.bbox_overlay.set_boxes(result)


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
