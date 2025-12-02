import numpy as np
from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtGui import QImage

from ui.generated.ui_mainwindow import Ui_MainWindow
from models.image_store import ImageStore, ImageItem
from utils.image_converter import qimage_to_cv, cv_to_qimage
from core import image_processor


class FilterManager(QObject):
    """Manages the logic of filters"""

    def __init__(self, ui: Ui_MainWindow, image_store: ImageStore):
        super().__init__()
        self.ui = ui
        self.image_store = image_store
        self.edited_image = self.image_store.get_edited_images()

        self.filters = [
            GreyFilter(self.ui),
            BinaryFilter(self.ui),
            InvertFilter(self.ui),
            MedianBlurFilter(self.ui),
        ]

        # Signal to slot binding
        for filt in self.filters:
            filt.paramsChanged.connect(self.apply_filters)

        self.ui.apply_to_all_btn.clicked.connect(self.apply_to_all_images)
        self.ui.reset_all_btn.clicked.connect(self.reset_filters)

    # ===================
    # slots
    # ===================
    @Slot()
    def apply_filters(self):
        """Apply filters on a single image and set it to edited image"""
        # img_item_to_edit = Should be current image item shown on preview

        cv_image = qimage_to_cv(img_item_to_edit.image)
        for filt in self.filters:
            cv_image = filt.apply_filter(cv_image)

        qimg_processed = cv_to_qimage(cv_image)
        qimg_item = ImageItem(qimg_processed, img_item_to_edit.path)
        self.image_store.set_edited_img_item(qimg_item)

    @Slot()
    def apply_to_all_images(self):
        """Apply active filters to all original images in list"""
        original_img_items = self.image_store.get_img_items()
        edited_img_items = []
        for img_item in original_img_items:
            cv_image = qimage_to_cv(img_item.image)
            for filt in self.filters:
                cv_image = filt.apply_filter(cv_image)

            qimg_processed = cv_to_qimage(cv_image)
            edited_img_item = ImageItem(qimg_processed, img_item.path)
            edited_img_items.append(edited_img_item)
        self.image_store.add_edited_images(edited_img_items)

    @Slot()
    def reset_filters(self):
        for filt in self.filters:
            filt.reset()


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
