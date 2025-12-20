from PySide6.QtCore import Slot
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox

from ui.controllers.ocr_manager import OCRManager
from ui.generated.ui_mainwindow import Ui_MainWindow
from models.data_store import DataStore, ImageItem
from ui.controllers.filters import FilterManager
from ui.widgets.common.thumbnail_label import ThumbLabel
from utils.file_utils import open_file_dialog
from ui.workers.file_loader_thread import FileLoaderThread
from ui.workers.progress_runner import ProgressRunner


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
        self.choose_files_btn.clicked.connect(self.choose_files_btn_clicked)
        self.clear_all_btn.clicked.connect(self.clear_all_btn_clicked)

        self.data_store.originalImagesChanged.connect(self.on_original_images_changed)
        self.data_store.editedImagesChanged.connect(self.on_edited_images_changed)
        self.data_store.currentImageChanged.connect(self.on_current_image_changed)

        self.bboxes_chbox.toggled.connect(self.ocr_manager.on_show_bboxes_toggled)

        # Thumbnail scroller
        self.thumb_layout = QHBoxLayout()
        self.thumb_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_layout.setSpacing(5)
        self.thumb_scroll_widget.setLayout(self.thumb_layout)

        # Progress runner for file loading
        self._runner = ProgressRunner(self, "Loading", "Loading images...")

    # ===============================
    # file loading
    # ===============================
    @Slot(bool)
    def choose_files_btn_clicked(self):
        """Open file dialog to choose an image."""
        file_paths: list[str] | None = open_file_dialog(
            parent=self,
            caption="Choose Images or PDF",
            filter_str="Files (*.png *.jpg *.jpeg *.pdf)",
            multi=True
        )

        if file_paths:
            self._start_file_loading(file_paths)

    def _start_file_loading(self, file_paths: list[str]):
        """Start background file loading with progress dialog."""
        thread = FileLoaderThread(file_paths, self)
        thread.finished_loading.connect(self._on_files_loaded)
        thread.error.connect(self._on_load_error)

        self._runner.run(
            thread,
            on_progress=thread.progress,
            on_done=self._on_loading_done
        )

    @Slot(dict)
    def _on_files_loaded(self, image_dict: dict[str, ImageItem]):
        """Called when file loading completes."""
        if image_dict:
            self.data_store.add_img_items(image_dict)
            self.statusbar.showMessage(f"{len(image_dict)} images loaded.", 5000)
        else:
            self.statusbar.showMessage("No images loaded.", 5000)

    @Slot(str)
    def _on_load_error(self, error_msg: str):
        """Called when file loading fails."""
        self.statusbar.showMessage(f"Error: {error_msg}", 5000)

    def _on_loading_done(self, cancelled: bool):
        """Called when loading completes, errors, or is cancelled."""
        if cancelled:
            self.statusbar.showMessage("Loading cancelled.", 5000)

    # ===============================
    # Other logic
    # ===============================
    @Slot(dict)
    def on_original_images_changed(self, img_items: dict[str, ImageItem]):
        """Handle original images loaded or cleared - rebuild thumbnails with originals."""
        self._rebuild_thumbnails(img_items)

        # Set current image from originals
        current = self.data_store.get_current_img_item()
        if not current.is_null() and current.id in img_items:
            self.data_store.set_current_img_item(img_items[current.id])
        elif img_items:
            self.data_store.set_current_img_item(next(iter(img_items.values())))

    @Slot(dict)
    def on_edited_images_changed(self, img_items: dict[str, ImageItem]):
        """Handle edited images applied - rebuild thumbnails with edited versions."""
        if not img_items:
            return

        self._rebuild_thumbnails(img_items)
        self.run_ocr_btn.setEnabled(True)

        # Set current image from edited set
        current = self.data_store.get_current_img_item()
        if not current.is_null() and current.id in img_items:
            self.data_store.set_current_img_item(img_items[current.id])
        elif img_items:
            self.data_store.set_current_img_item(next(iter(img_items.values())))

    def _rebuild_thumbnails(self, img_items: dict[str, ImageItem]):
        """Clear and rebuild thumbnail widgets from given image items."""
        # Clear existing thumbnails
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            if w := item.widget():
                w.deleteLater()

        # Build new thumbnails
        viewport_h = self.thumb_scroll_area.viewport().height()
        # scrollbar_h = 17  # 12px scrollbar + 5px margin
        for img_item in img_items.values():
            label = ThumbLabel(img_item)
            self.thumb_layout.addWidget(label)
            label.setFixedSize(150, viewport_h)

            qimg = img_item.to_qimage()
            pixmap = QPixmap.fromImage(qimg).scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.clicked.connect(self.image_label_clicked)

    @Slot(ImageItem)
    def on_current_image_changed(self, current_img_item: ImageItem):
        """When current image in store is updated, update preview with that image"""
        if current_img_item.is_null():
            self.edited_img_viewer.image_viewer.clear()
            self.edited_img_viewer.bbox_overlay.clear_regions()
            self.bboxes_chbox.setEnabled(False)
            return

        pixmap = QPixmap.fromImage(current_img_item.to_qimage())
        self.edited_img_viewer.image_viewer.load_pixmap(pixmap)
        if self.data_store.get_ocr_items().get(current_img_item.id) is not None:
            self.bboxes_chbox.setEnabled(True)
            self.ocr_manager.on_show_bboxes_toggled(self.bboxes_chbox.isChecked())
        else:
            self.bboxes_chbox.setEnabled(False)
            self.edited_img_viewer.bbox_overlay.clear_regions()

    @Slot()
    def clear_all_btn_clicked(self):
        """Clears all images in store."""
        reply = QMessageBox.question(
            self,
            "Clear all images",
            "Are you sure you want to clear all images?",
        )

        if reply == QMessageBox.Yes:
            self.data_store.clear_all()
            self.statusbar.showMessage("All images cleared.")

    @Slot(ImageItem)
    def image_label_clicked(self, img_item: ImageItem):
        self.data_store.set_current_img_item(img_item)





