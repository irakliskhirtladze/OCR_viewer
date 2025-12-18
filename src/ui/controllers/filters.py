import numpy as np
from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from ui.generated.ui_mainwindow import Ui_MainWindow
from models.data_store import DataStore, ImageItem
from ui.workers.image_processor_thread import ImageProcessorThread
from ui.workers.progress_runner import ProgressRunner
from utils.image_converter import cv_to_qimage
from core import image_processor


class FilterManager(QObject):
    """Manages the logic of filters"""
    def __init__(self, ui: Ui_MainWindow, data_store: DataStore):
        super().__init__()
        self.ui = ui
        self.data_store = data_store
        self.edited_images = self.data_store.get_edited_images()

        self.filters = [
            GreyFilter(self.ui),
            BinaryFilter(self.ui),
            InvertFilter(self.ui),
            MedianBlurFilter(self.ui),
            DilateErodeFilter(self.ui),
        ]

        # Signal to slot binding
        for filt in self.filters:
            filt.paramsChanged.connect(self.apply_filters)

        self.ui.apply_to_all_btn.clicked.connect(self.apply_to_all_images)
        self.ui.reset_all_btn.clicked.connect(self.reset_filters)

        # Progress runner for batch processing
        self._runner = ProgressRunner(self.ui.centralwidget, "Processing", "Applying filters...")

    @Slot()
    def apply_filters(self):
        """
        Apply filters on a single original image and set it to edited image.
        Note that filters must always be applied to original images to avoid double filtering of edited images.
        """
        current_img_item = self.data_store.get_current_img_item()
        if current_img_item.is_null():
            return

        # Get original and apply filters
        original_img_item = self.data_store.get_img_items().get(current_img_item.id)
        cv_img = original_img_item.image
        for filt in self.filters:
            cv_img = filt.apply_filter(cv_img)
        qimg_edited = cv_to_qimage(cv_img)

        # Update viewer directly, don't set to store
        pixmap = QPixmap.fromImage(qimg_edited)
        self.ui.edited_img_viewer.image_viewer.load_pixmap(pixmap)

    @Slot()
    def reset_filters(self):
        reply = QMessageBox.question(
            self.ui.centralwidget,
            "Reset all filters",
            "Are you sure you want to reset all filters for all images?",
        )
        if reply == QMessageBox.Yes:
            for filt in self.filters:
                filt.reset()

            self.data_store.clear_edited_images()
            self.ui.statusbar.showMessage("All filters reset successfully", 5000)

    # ===================
    # apply filters to all images in a separate thread
    # ===================
    @Slot()
    def apply_to_all_images(self):
        thread = ImageProcessorThread(self.data_store.get_img_items(), self.filters)
        thread.finished_processing.connect(self._on_images_processed)
        thread.error.connect(self._on_processing_error)

        self._runner.run(
            thread,
            on_progress=thread.progress,
            on_done=self._on_processing_done
        )

    @Slot(dict)
    def _on_images_processed(self, image_dict: dict[str, ImageItem]):
        """Called when file processing completes."""
        if image_dict:
            self.data_store.add_edited_images(image_dict)
            self.ui.statusbar.showMessage(f"{len(image_dict)} images processed.", 5000)
        else:
            self.ui.statusbar.showMessage("No images processed.", 5000)

    @Slot(str)
    def _on_processing_error(self, error_msg: str):
        """Called when processing fails."""
        self.ui.statusbar.showMessage(f"Error: {error_msg}", 5000)

    def _on_processing_done(self, cancelled: bool):
        """Called when processing completes, errors, or is cancelled."""
        if cancelled:
            self.ui.statusbar.showMessage("Processing cancelled.", 5000)


class BaseFilter(QObject):
    """Abstract base class for all filter widgets"""
    paramsChanged = Signal()

    def __init__(self):
        super().__init__()

    def get_params(self) -> dict:
        """Return current filter parameters"""
        raise NotImplementedError

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        """Apply this filter to the image"""
        raise NotImplementedError

    def reset(self):
        """Reset to default values"""
        raise NotImplementedError


class GreyFilter(BaseFilter):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.ui.grey_chbx.toggled.connect(self.on_checkbox_toggled)

    def get_params(self) -> dict:
        return {
            "enabled": self.ui.grey_chbx.isChecked()
        }

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            return image_processor.to_gray(img)
        return img

    def reset(self):
        self.ui.grey_chbx.setChecked(False)

    @Slot(bool)
    def on_checkbox_toggled(self, checked: bool):
        self.paramsChanged.emit()


class BinaryFilter(BaseFilter):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui

        self.ui.binarize_chbx.toggled.connect(self.on_checkbox_toggled)
        self.ui.binarize_slider.valueChanged.connect(self.on_slider_value_changed)

    def get_params(self) -> dict:
        return {
            "enabled": self.ui.binarize_chbx.isChecked(),
            "threshold": self.ui.binarize_slider.value()
        }

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            value = self.get_params()["threshold"]
            return image_processor.to_binary(img, value, 255)
        return img

    def reset(self):
        self.ui.binarize_chbx.setChecked(False)
        self.ui.binarize_slider.setValue(127)
        self.ui.binarize_slider.setEnabled(False)

    @Slot(bool)
    def on_checkbox_toggled(self, checked: bool):
        self.ui.binarize_slider.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot()
    def on_slider_value_changed(self, value):
        self.ui.binarize_val_lbl.setText(str(value))
        self.paramsChanged.emit()


class InvertFilter(BaseFilter):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui

        self.ui.invert_chbx.toggled.connect(self.on_checkbox_toggled)

    def get_params(self) -> dict:
        return {
            "enabled": self.ui.invert_chbx.isChecked(),
        }

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            return image_processor.invert(img)
        return img

    def reset(self):
        self.ui.invert_chbx.setChecked(False)

    @Slot(bool)
    def on_checkbox_toggled(self, checked: bool):
        self.paramsChanged.emit()


class MedianBlurFilter(BaseFilter):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.ui.median_chbx.toggled.connect(self.on_checkbox_toggled)
        self.ui.median_ksize_spinbox.valueChanged.connect(self.on_ksize_value_changed)

    def get_params(self) -> dict:
        return {
            "enabled": self.ui.median_chbx.isChecked(),
            "k_size": self.ui.median_ksize_spinbox.value(),
        }

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            return image_processor.median_blur(img, self.get_params()["k_size"])
        return img

    def reset(self):
        self.ui.median_chbx.setChecked(False)
        self.ui.median_ksize_spinbox.setValue(3)
        self.ui.median_ksize_spinbox.setEnabled(False)

    @Slot(bool)
    def on_checkbox_toggled(self, checked: bool):
        self.ui.median_ksize_spinbox.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot(int)
    def on_ksize_value_changed(self, value: int):
        self.paramsChanged.emit()


class DilateErodeFilter(BaseFilter):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.ui.dilate_erode_chbx.toggled.connect(self.on_checkbox_toggled)
        self.ui.dilate_radio.clicked.connect(self.on_dilate_radio_clicked)
        self.ui.erode_radio.clicked.connect(self.on_erode_radio_clicked)
        self.ui.dilate_erode_ksize_spinbox.valueChanged.connect(self.on_ksize_value_changed)
        self.ui.dilate_erode_iter_spinbox.valueChanged.connect(self.on_iter_value_changed)

    def get_params(self) -> dict:
        return {
            "enabled": self.ui.dilate_erode_chbx.isChecked(),
            "active_btn": "dilate" if self.ui.dilate_radio.isChecked() else "erode",
            "k_size": (self.ui.dilate_erode_ksize_spinbox.value(), self.ui.dilate_erode_ksize_spinbox.value()),
            "iteration": self.ui.dilate_erode_iter_spinbox.value(),
        }

    def apply_filter(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            if self.get_params()["active_btn"] == "dilate":
                return image_processor.dilate(img, self.get_params()["k_size"], self.get_params()["iteration"])
            elif self.get_params()["active_btn"] == "erode":
                return image_processor.erode(img, self.get_params()["k_size"], self.get_params()["iteration"])
        return img

    def reset(self):
        self.ui.dilate_erode_chbx.setChecked(False)
        self.ui.dilate_radio.setChecked(True)
        self.ui.dilate_radio.setEnabled(False)
        self.ui.erode_radio.setEnabled(False)
        self.ui.dilate_erode_ksize_spinbox.setValue(2)
        self.ui.dilate_erode_ksize_spinbox.setEnabled(False)
        self.ui.dilate_erode_iter_spinbox.setValue(1)
        self.ui.dilate_erode_iter_spinbox.setEnabled(False)

    @Slot(bool)
    def on_checkbox_toggled(self, checked: bool):
        self.ui.dilate_radio.setEnabled(checked)
        self.ui.erode_radio.setEnabled(checked)
        self.ui.dilate_erode_ksize_spinbox.setEnabled(checked)
        self.ui.dilate_erode_iter_spinbox.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot()
    def on_dilate_radio_clicked(self):
        self.paramsChanged.emit()

    @Slot()
    def on_erode_radio_clicked(self):
        self.paramsChanged.emit()

    @Slot()
    def on_ksize_value_changed(self):
        self.paramsChanged.emit()

    @Slot()
    def on_iter_value_changed(self):
        self.paramsChanged.emit()

