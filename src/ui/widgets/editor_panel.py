import numpy as np
from PySide6.QtCore import Qt, Signal, Slot, QThreadPool, QRunnable
from PySide6.QtGui import QImage
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel, QSlider,
                               QSpinBox, QPushButton, QErrorMessage, QApplication, QRadioButton, QButtonGroup)

from backend import processor
from backend.ocr_engine import orc_tesseract
from backend.processor import dilate, erode
from ui.models.image_store import ImageStore
from ui.models.ocr_store import OCRStore
from utils.image_convert import qimage_to_cv, cv_to_qimage
from utils.worker_manager import Worker


# ============================================================================
# Base Filter Widget
# ============================================================================
class BaseFilterWidget(QFrame):
    """Abstract base class for all filter widgets"""
    paramsChanged = Signal()

    def __init__(self):
        super().__init__()

    def get_params(self) -> dict:
        """Return current filter parameters"""
        raise NotImplementedError

    def reset(self):
        """Reset to default values"""
        raise NotImplementedError

    def apply(self, img: np.ndarray) -> np.ndarray:
        """Apply this filter to the image"""
        raise NotImplementedError


# ============================================================================
# Individual Filter Widgets
# ============================================================================
class GrayscaleFilterWidget(BaseFilterWidget):
    """Converts image to grayscale"""

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("To Grey")
        self.layout().addWidget(self.checkbox)

        self.checkbox.toggled.connect(self._on_toggled)

    @Slot(bool)
    def _on_toggled(self):
        self.paramsChanged.emit()

    def get_params(self) -> dict:
        return {"enabled": self.checkbox.isChecked()}

    def reset(self):
        self.checkbox.setChecked(False)

    def apply(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            return processor.to_gray(img)
        return img


class BinaryFilterWidget(BaseFilterWidget):
    """Converts image to binary with adjustable threshold"""

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("Binary")
        self.layout().addWidget(self.checkbox)

        # Threshold slider container
        slider_cont = QFrame()
        slider_cont.setLayout(QHBoxLayout())
        slider_cont.layout().setContentsMargins(10, 0, 0, 0)  # Indent

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimumWidth(50)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(127)
        self.slider.setEnabled(False)

        self.threshold_label = QLabel("127")
        self.threshold_label.setMinimumWidth(30)

        slider_cont.layout().addWidget(QLabel("Threshold:"))
        slider_cont.layout().addWidget(self.slider)
        slider_cont.layout().addWidget(self.threshold_label)

        self.layout().addWidget(slider_cont)

        # Connect signals
        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        self.slider.valueChanged.connect(self._on_slider_changed)

    @Slot(bool)
    def _on_checkbox_toggled(self, checked: bool):
        self.slider.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot(int)
    def _on_slider_changed(self, value: int):
        self.threshold_label.setText(str(value))
        if self.checkbox.isChecked():
            self.paramsChanged.emit()

    def get_params(self) -> dict:
        return {
            "enabled": self.checkbox.isChecked(),
            "threshold": self.slider.value()
        }

    def reset(self):
        self.checkbox.setChecked(False)
        self.slider.setValue(127)

    def apply(self, img: np.ndarray) -> np.ndarray:
        params = self.get_params()
        if params["enabled"]:
            # Ensure image is grayscale before binarization
            if len(img.shape) == 3:
                img = processor.to_gray(img)
            return processor.to_binary(img, params["threshold"], 255)
        return img


class InvertFilterWidget(BaseFilterWidget):
    """Inverts image colors"""

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("Invert")
        self.layout().addWidget(self.checkbox)

        self.checkbox.toggled.connect(self._on_toggled)

    @Slot(bool)
    def _on_toggled(self):
        self.paramsChanged.emit()

    def get_params(self) -> dict:
        return {"enabled": self.checkbox.isChecked()}

    def reset(self):
        self.checkbox.setChecked(False)

    def apply(self, img: np.ndarray) -> np.ndarray:
        if self.get_params()["enabled"]:
            return processor.invert(img)
        return img


class GaussianFilterWidget(BaseFilterWidget):
    """Apply gaussian filter to the image"""

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("Gaussian blur")
        self.layout().addWidget(self.checkbox)

        self.ksize_cont = QFrame()
        self.ksize_cont.setLayout(QHBoxLayout())
        self.ksize_cont.layout().setContentsMargins(10, 0, 0, 0)
        self.layout().addWidget(self.ksize_cont)

        self.ksize_label = QLabel("Ksize:")
        self.ksize_cont.layout().addWidget(self.ksize_label)

        self.ksize_spinbox_1 = QSpinBox()
        self.ksize_spinbox_1.setMinimum(1)
        self.ksize_spinbox_1.setMaximum(39)
        self.ksize_spinbox_1.setValue(3)
        self.ksize_spinbox_1.setSingleStep(2)
        self.ksize_spinbox_1.setEnabled(False)
        self.ksize_cont.layout().addWidget(self.ksize_spinbox_1)

        self.ksize_spinbox_2 = QSpinBox()
        self.ksize_spinbox_2.setMinimum(1)
        self.ksize_spinbox_2.setMaximum(39)
        self.ksize_spinbox_2.setValue(3)
        self.ksize_spinbox_2.setSingleStep(2)
        self.ksize_spinbox_2.setEnabled(False)
        self.ksize_cont.layout().addWidget(self.ksize_spinbox_2)

        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        self.ksize_spinbox_1.valueChanged.connect(self._on_ksize_changed)
        self.ksize_spinbox_2.valueChanged.connect(self._on_ksize_changed)

    @Slot(bool)
    def _on_checkbox_toggled(self, checked: bool):
        self.ksize_spinbox_1.setEnabled(checked)
        self.ksize_spinbox_2.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot()
    def _on_ksize_changed(self):
        if self.checkbox.isChecked():
            self.paramsChanged.emit()

    def get_params(self) -> dict:
        return {"enabled": self.checkbox.isChecked(),
                "k_tuple": (self.ksize_spinbox_1.value(), self.ksize_spinbox_2.value())}

    def reset(self):
        self.checkbox.setChecked(False)
        self.ksize_spinbox_1.setValue(3)
        self.ksize_spinbox_2.setValue(3)

    def apply(self, img: np.ndarray) -> np.ndarray:
        params = self.get_params()
        if params["enabled"]:
            return processor.gaussian_blur(img, params["k_tuple"])
        return img


class MedianFilterWidget(BaseFilterWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("Median blur")
        self.layout().addWidget(self.checkbox)

        self.ksize_cont = QFrame()
        self.ksize_cont.setLayout(QHBoxLayout())
        self.ksize_cont.layout().setContentsMargins(10, 0, 0, 0)
        self.layout().addWidget(self.ksize_cont)

        self.ksize_label = QLabel("Ksize:")
        self.ksize_cont.layout().addWidget(self.ksize_label)

        self.ksize_spinbox = QSpinBox()
        self.ksize_spinbox.setMinimum(1)
        self.ksize_spinbox.setMaximum(39)
        self.ksize_spinbox.setValue(3)
        self.ksize_spinbox.setSingleStep(2)
        self.ksize_spinbox.setEnabled(False)
        self.ksize_cont.layout().addWidget(self.ksize_spinbox)

        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        self.ksize_spinbox.valueChanged.connect(self._on_ksize_changed)

    @Slot(bool)
    def _on_checkbox_toggled(self, checked: bool):
        self.ksize_spinbox.setEnabled(checked)
        self.paramsChanged.emit()

    @Slot()
    def _on_ksize_changed(self):
        self.paramsChanged.emit()

    def get_params(self) -> dict:
        return {"enabled": self.checkbox.isChecked(),
                "ksize": self.ksize_spinbox.value()}

    def reset(self):
        self.checkbox.setChecked(False)
        self.ksize_spinbox.setValue(3)

    def apply(self, img: np.ndarray) -> np.ndarray:
        params = self.get_params()
        if params["enabled"]:
            return processor.median_blur(img, params["ksize"])
        return img


class DilationErosionFilterWidget(BaseFilterWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox("Erode/dilate")
        self.layout().addWidget(self.checkbox)

        self.filter_cont = QFrame()
        self.filter_cont.setLayout(QHBoxLayout())
        self.filter_cont.layout().setContentsMargins(10, 0, 0, 0)
        self.layout().addWidget(self.filter_cont)

        self.radio_btn_cont = QFrame()
        self.radio_btn_cont.setLayout(QVBoxLayout())
        self.radio_btn_cont.layout().setContentsMargins(0, 0, 0, 0)
        self.btn_group = QButtonGroup()
        self.dilate_radio = QRadioButton("Dilate")
        self.dilate_radio.setChecked(True)
        self.dilate_radio.setEnabled(False)
        self.btn_group.addButton(self.dilate_radio, 1)
        self.radio_btn_cont.layout().addWidget(self.dilate_radio)
        self.erode_radio = QRadioButton("Erode")
        self.erode_radio.setEnabled(False)
        self.btn_group.addButton(self.erode_radio, 2)
        self.filter_cont.layout().addWidget(self.radio_btn_cont)
        self.radio_btn_cont.layout().addWidget(self.erode_radio)

        self.ksize_cont = QFrame()
        self.ksize_cont.setLayout(QVBoxLayout())
        self.ksize_cont.layout().setContentsMargins(0, 0, 0, 0)
        self.ksize_label = QLabel("Ksize")
        self.ksize_cont.layout().addWidget(self.ksize_label)
        self.ksize_spinbox = QSpinBox()
        self.ksize_spinbox.setEnabled(False)
        self.ksize_spinbox.setMinimum(1)
        self.ksize_spinbox.setMaximum(40)
        self.ksize_spinbox.setValue(2)
        self.ksize_cont.layout().addWidget(self.ksize_spinbox)
        self.filter_cont.layout().addWidget(self.ksize_cont)

        self.iter_cont = QFrame()
        self.iter_cont.setLayout(QVBoxLayout())
        self.iter_cont.layout().setContentsMargins(0, 0, 0, 0)
        self.iter_label = QLabel("Iteration")
        self.iter_cont.layout().addWidget(self.iter_label)
        self.iter_spinbox = QSpinBox()
        self.iter_spinbox.setEnabled(False)
        self.iter_spinbox.setMinimum(1)
        self.iter_spinbox.setMaximum(40)
        self.iter_spinbox.setValue(1)
        self.iter_cont.layout().addWidget(self.iter_spinbox)
        self.filter_cont.layout().addWidget(self.iter_cont)

        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        self.btn_group.buttonClicked.connect(self._on_radio_btn_clicked)
        self.ksize_spinbox.valueChanged.connect(self._on_ksize_changed)
        self.iter_spinbox.valueChanged.connect(self._on_iter_changed)

    @Slot(bool)
    def _on_checkbox_toggled(self, checked: bool):
        self.dilate_radio.setEnabled(checked)
        self.erode_radio.setEnabled(checked)
        self.ksize_spinbox.setEnabled(checked)
        self.iter_spinbox.setEnabled(checked)

        self.paramsChanged.emit()

    @Slot()
    def _on_radio_btn_clicked(self):
        self.paramsChanged.emit()

    @Slot()
    def _on_ksize_changed(self):
        self.paramsChanged.emit()

    @Slot()
    def _on_iter_changed(self):
        self.paramsChanged.emit()

    def get_checked_radio_btn_id(self) -> int:
        """Returns the checked and enabled radio button id."""
        checked_btn = self.btn_group.checkedButton()
        if checked_btn is not None and checked_btn.isEnabled():
            return self.btn_group.id(checked_btn)
        return -1

    def get_params(self) -> dict:
        return {
            "enabled": self.dilate_radio.isEnabled() and self.erode_radio.isEnabled(),
            "checked_btn": self.get_checked_radio_btn_id(),
            "k_tuple": (self.ksize_spinbox.value(), self.ksize_spinbox.value()),
            "iter": self.iter_spinbox.value()
        }

    def apply(self, img: np.ndarray) -> np.ndarray:
        params = self.get_params()
        if params["enabled"]:
            if params["checked_btn"] == 1:
                return dilate(img, params["k_tuple"], params["iter"])
            elif params["checked_btn"] == 2:
                return erode(img, params["k_tuple"], params["iter"])
        return img

    def reset(self):
        self.dilate_radio.setEnabled(False)
        self.erode_radio.setEnabled(False)
        self.ksize_spinbox.setEnabled(False)
        self.ksize_spinbox.setValue(2)
        self.iter_spinbox.setEnabled(False)
        self.iter_spinbox.setValue(1)


# ============================================================================
# Editor Container (Orchestrator)
# ============================================================================
class EditorContainer(QFrame):
    """Main container that manages all filter widgets"""

    def __init__(self, image_store: ImageStore, ocr_store: OCRStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(20)

        self.image_store = image_store
        self.original_cv_img = None  # OpenCV version of original image

        self.ocr_store = ocr_store
        self.ocr_store.text = None

        # List of all filters (order matters - they're applied sequentially)
        self.filters = [
            GrayscaleFilterWidget(),
            BinaryFilterWidget(),
            InvertFilterWidget(),
            GaussianFilterWidget(),
            MedianFilterWidget(),
            DilationErosionFilterWidget()
        ]

        # Add all filters to layout
        for filter_widget in self.filters:
            self.layout().addWidget(filter_widget)
            filter_widget.paramsChanged.connect(self.on_params_changed)

        # Button to run OCR
        self.run_ocr_btn = QPushButton("Run OCR")
        self.layout().addWidget(self.run_ocr_btn)
        self.run_ocr_btn.clicked.connect(self._ocr_worker)

        # Vertical spacer to push filters to top
        v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(v_spacer)

        # set up threadpool to run ocr in separate thread
        self.threadpool = QThreadPool()

        # Connect to original image changes
        self.image_store.imageChanged.connect(self.on_original_image_changed)

    def on_original_image_changed(self, qimg: QImage, path: str):
        """Store the original image when it changes"""
        self.original_cv_img = qimage_to_cv(qimg)
        # Reset all filters
        self.reset_all_filters()
        # Initialize edited image with original
        self.image_store.set_edited_img(qimg)

    @Slot()
    def on_params_changed(self):
        """Handle parameter changes and apply all filters in sequence"""
        if self.original_cv_img is None:
            return

        # Start with a copy of the original image
        processed = self.original_cv_img.copy()

        # Apply all filters in sequence
        for filter_widget in self.filters:
            processed = filter_widget.apply(processed)

        # Convert back to QImage and update store once at the end
        qimg = cv_to_qimage(processed)
        self.image_store.set_edited_img(qimg)

    def reset_all_filters(self):
        """Reset all filters to default values"""
        for filter_widget in self.filters:
            filter_widget.reset()

    # ============================================================================
    # OCR worker
    # ============================================================================
    @Slot()
    def _ocr_worker(self):
        """worker method to call and run ocr process in another thread"""
        # Set wait cursor on main thread
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        worker = Worker(self.run_ocr)
        worker.signals.result.connect(self._on_ocr_successful)
        worker.signals.error.connect(self._on_ocr_error)
        worker.signals.completed.connect(self._on_ocr_completed)
        self.threadpool.start(worker)

    def run_ocr(self) -> str | None:
        """Run the OCR on img"""
        edited_img = self.image_store.get_edited_img()
        cv_img = qimage_to_cv(edited_img)
        text = orc_tesseract(cv_img, lang="eng")
        return text

    @Slot()
    def _on_ocr_successful(self, text: str):
        """Set the result text to textarea if ocr is completed"""
        self.ocr_store.set_text(text)

    @Slot()
    def _on_ocr_error(self, error: tuple):
        """Show error dialog"""
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(str(error[1]))

    @Slot()
    def _on_ocr_completed(self):
        """Restore cursor when OCR completes (called on main thread)"""
        QApplication.restoreOverrideCursor()
