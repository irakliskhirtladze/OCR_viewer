import numpy as np
from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtGui import QImage

from ui.generated.ui_mainwindow import Ui_MainWindow
from ui.models.image_store import ImageStore
from utils.image_convert import qimage_to_cv, cv_to_qimage
from ocr import processor


class FilterManager(QObject):
    """Manages the logic of filters"""

    def __init__(self, ui: Ui_MainWindow, image_store: ImageStore):
        super().__init__()
        self.ui = ui
        self.image_store = image_store
        # self.original_img = self.image_store.get_original_img()
        self.edited_image = self.image_store.get_edited_img()

        self.filters = [
            GreyFilter(self.ui),
            BinaryFilter(self.ui)
        ]

        for filt in self.filters:
            filt.paramsChanged.connect(self.on_params_changed)

    # ===================
    # slots
    # ===================
    @Slot()
    def on_params_changed(self):
        original_img = self.image_store.get_original_img()
        if original_img.isNull():
            return

        cv_image = qimage_to_cv(original_img)
        for filt in self.filters:
            cv_image = filt.apply_filter(cv_image)

        qimg_processed = cv_to_qimage(cv_image)
        self.image_store.set_edited_img(qimg_processed)


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
            return processor.to_gray(img)
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
            return processor.to_binary(img, value, 255)
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
