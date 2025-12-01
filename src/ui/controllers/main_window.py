import pymupdf
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage, Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QHBoxLayout

from ui.generated.ui_mainwindow import Ui_MainWindow
from models.image_store import ImageStore, ImageItem
from models.ocr_store import OCRStore
from ui.controllers.filters import FilterManager
from ui.widgets.common.thumbnail_label import ThumbLabel
from utils.file_utils import open_file_dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize stores
        self.image_store = ImageStore()
        self.ocr_store = OCRStore()

        # Connect signals and slots
        self.choose_files_btn.clicked.connect(self.on_choose_files_clicked)
        self.clear_all_btn.clicked.connect(self.on_clear_all)
        self.image_store.imagesChanged.connect(self.on_images_changed)
        self.image_store.editedImageChanged.connect(self._on_edited_image_changed)
        self.ocr_store.result_changed.connect(self._on_ocr_changed)

        # Thumbnail scroller
        self.thumb_layout = QHBoxLayout()
        self.thumb_scroll_widget.setLayout(self.thumb_layout)

        # Filters
        self.filters = FilterManager(self, self.image_store)

    # ===============================
    # Slots
    # ===============================
    @Slot(bool)
    def on_choose_files_clicked(self):
        """Open file dialog to choose an image."""
        file_paths = open_file_dialog(
            parent=self,
            caption="Choose Images or PDF",
            filter_str="Files (*.png *.jpg *.jpeg *.pdf)",
            multi=True
        )

        if file_paths:
            self._load_files(file_paths)

    @Slot(list)
    def on_images_changed(self, images: list[ImageItem]):
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        viewport_h = self.thumb_scroll_area.viewport().height()

        for img in images:
            label = ThumbLabel(img)
            self.thumb_layout.addWidget(label)
            label.setFixedSize(100, viewport_h)

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

    @Slot(bool)
    def on_clear_all(self):
        self.image_store.clear_images()

    @Slot(ImageItem)
    def on_image_label_clicked(self, img_item: ImageItem):
        self.image_store.set_original_img(img_item.image)

    @Slot(QImage)
    def _on_edited_image_changed(self, qimg: QImage):
        """Update image viewer when edited image changes."""
        if qimg is not None and not qimg.isNull():
            pixmap = QPixmap.fromImage(qimg)
            self.edited_img_viewer.image_viewer.load_pixmap(pixmap)
            # Trigger overlay repaint
            self.edited_img_viewer.bbox_overlay.update()
            # Clear old bounding boxes since image changed
            self.edited_img_viewer.bbox_overlay.clear_boxes()
        else:
            self.edited_img_viewer.image_viewer.clear()
            self.edited_img_viewer.bbox_overlay.clear_boxes()

    @Slot(list)
    def _on_ocr_changed(self, result: list):
        """Update bounding boxes when OCR results change."""
        self.edited_img_viewer.bbox_overlay.set_boxes(result)

    # ===============================
    # other logic
    # ===============================
    def _load_files(self, file_paths: list):
        """Load images files and set the list of imageItems to store. this does not update ui itself"""
        image_list = []
        for file_path in file_paths:
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                img_item = ImageItem(QImage(file_path), file_path)
                image_list.append(img_item)

            elif file_path.lower().endswith(".pdf"):
                with pymupdf.open(file_path) as doc:
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

        # Set the list of imageItems to store
        self.image_store.add_img_items(image_list)

