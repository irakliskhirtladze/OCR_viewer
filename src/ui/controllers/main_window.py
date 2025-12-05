import pymupdf
from PySide6.QtCore import Slot, QThreadPool
from PySide6.QtGui import QImage, Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QHBoxLayout

from ui.controllers.ocr_manager import OCRManager
from ui.generated.ui_mainwindow import Ui_MainWindow
from models.data_store import DataStore, ImageItem
from ui.controllers.filters import FilterManager
from ui.widgets.common.thumbnail_label import ThumbLabel
from utils.file_utils import open_file_dialog
from utils.worker_manager import Worker


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize store
        self.data_store = DataStore()

        # Filter manager
        self.filter_manager = FilterManager(self, self.data_store)

        # ocr manager
        self.ocr_manager = OCRManager(self, self.data_store)

        # Connect signals and slots
        self.choose_files_btn.clicked.connect(self.on_choose_files_clicked)
        self.clear_all_btn.clicked.connect(self.on_clear_all_btn_clicked)

        self.data_store.imagesChanged.connect(self.on_images_changed)
        self.data_store.currentImageChanged.connect(self.on_current_image_changed)
        self.data_store.editedImagesChanged.connect(self.on_edited_images_changed)

        # Thumbnail scroller
        self.thumb_layout = QHBoxLayout()
        self.thumb_scroll_widget.setLayout(self.thumb_layout)

        # Edited thumbnail scroller
        self.edited_thumb_layout = QHBoxLayout()
        self.edited_thumb_scroll_widget.setLayout(self.edited_thumb_layout)

    # ===============================
    #
    # ===============================
    @Slot(bool)
    def on_choose_files_clicked(self):
        """Open file dialog to choose an image."""
        file_paths: list[str] | None = open_file_dialog(
            parent=self,
            caption="Choose Images or PDF",
            filter_str="Files (*.png *.jpg *.jpeg *.pdf)",
            multi=True
        )

        if file_paths:
            # Show loading message
            self.statusbar.showMessage("Loading images...")
            
            # Create worker for background loading
            worker = Worker(self._load_files, file_paths)
            worker.signals.result.connect(self._on_files_loaded)
            worker.signals.error.connect(self._on_load_error)
            
            # Start worker in thread pool
            QThreadPool.globalInstance().start(worker)

    @Slot(list)
    def on_images_changed(self, images: dict[str, ImageItem]):
        """
        Clear thumb scroll widget, and add current items to it as thumbnails.
        Also set first image (if available) from list as single image in store.
        """
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        viewport_h = self.thumb_scroll_area.viewport().height()

        for img_item in images.values():
            label = ThumbLabel(img_item)
            self.thumb_layout.addWidget(label)
            label.setFixedSize(100, viewport_h)

            qimg = img_item.image
            pixmap = QPixmap.fromImage(qimg).scaled(
                label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)

            label.clicked.connect(self.on_image_label_clicked)

        # Whenever images list in store is updated, set the first image to edited image
        if len(images) > 0:
            first_image = next(iter(images.values()))
            self.data_store.set_current_img_item(first_image)
        else:
            self.data_store.clear_img_item()

    @Slot(ImageItem)
    def on_current_image_changed(self, current_img_item: ImageItem):
        """When current image in store is updated, update preview with that image"""
        if current_img_item.image.isNull():
            self.edited_img_viewer.image_viewer.clear()
            self.edited_img_viewer.bbox_overlay.clear_boxes()
            return

        pixmap = QPixmap.fromImage(current_img_item.image)
        self.edited_img_viewer.image_viewer.load_pixmap(pixmap)

    @Slot()
    def on_clear_all_btn_clicked(self):
        """Clears all original images in store."""
        self.data_store.clear_img_items()

    @Slot(ImageItem)
    def on_image_label_clicked(self, img_item: ImageItem):
        self.data_store.set_current_img_item(img_item)

    @Slot(list)
    def on_edited_images_changed(self, img_items: dict[str, ImageItem]):
        """When edited image dict is updated, update the edited thumb scroll area as well"""
        while self.edited_thumb_layout.count():
            item = self.edited_thumb_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        viewport_h = self.edited_thumb_scroll_area.viewport().height()

        for img_item in img_items.values():
            label = ThumbLabel(img_item)
            self.edited_thumb_layout.addWidget(label)
            label.setFixedSize(100, viewport_h)

            qimg = img_item.image
            pixmap = QPixmap.fromImage(qimg).scaled(
                label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)

            label.clicked.connect(self.on_edited_img_label_clicked)

        # Whenever images list in store is updated, set the first image to edited image
        if len(img_items) > 0:
            first_image = next(iter(img_items.values()))
            self.data_store.set_current_img_item(first_image)
        else:
            self.data_store.clear_edited_images()

    @Slot(ImageItem)
    def on_edited_img_label_clicked(self, edited_img_item: ImageItem):
        self.data_store.set_current_img_item(edited_img_item)

    @Slot(list)
    def _on_ocr_changed(self, result: list):
        """Update bounding boxes when OCR results change."""
        self.edited_img_viewer.bbox_overlay.set_boxes(result)

    # ===============================
    # file loading
    # ===============================
    def _load_files(self, file_paths: list) -> dict[str, ImageItem]:
        """Load images files in background thread. Returns dict of ImageItems."""
        image_dict = {}
        for file_path in file_paths:

            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                img_item = ImageItem(QImage(file_path), file_path)
                image_dict[img_item.id] = img_item

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
                        image_dict[img_item.id] = img_item

        return image_dict

    @Slot(object)
    def _on_files_loaded(self, image_dict: dict[str, ImageItem]):
        """Called when file loading completes in background thread."""
        self.data_store.add_img_items(image_dict)
        self.statusbar.showMessage(f"{len(image_dict)} images loaded.", 5000)

    @Slot(tuple)
    def _on_load_error(self, error_info):
        """Called when file loading fails."""
        exctype, value, traceback_str = error_info
        self.statusbar.showMessage(f"Error loading files: {value}", 5000)
        print(f"Error loading files:\n{traceback_str}")


