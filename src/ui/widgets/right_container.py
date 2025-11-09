from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel, QSlider, \
    QSpinBox, QPushButton

import numpy as np

from core.ocr_engine import orc_tesseract
from ui.models.image_store import ImageStore
from ui.models.text_store import TextStore
from utils.image_convert import qimage_to_cv, cv_to_qimage
from core import processor


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


# ============================================================================
# Editor Container (Orchestrator)
# ============================================================================

class EditorContainer(QFrame):
    """Main container that manages all filter widgets"""

    def __init__(self, image_store: ImageStore, text_store: TextStore):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(20)

        self.image_store = image_store
        self.original_cv_img = None  # OpenCV version of original image

        self.text_store = text_store
        self.text_store.text = None

        # List of all filters (order matters - they're applied sequentially)
        self.filters = [
            GrayscaleFilterWidget(),
            BinaryFilterWidget(),
            InvertFilterWidget(),
            GaussianFilterWidget(),
            MedianFilterWidget(),
        ]

        # Add all filters to layout
        for filter_widget in self.filters:
            self.layout().addWidget(filter_widget)
            filter_widget.paramsChanged.connect(self.on_params_changed)

        # Button to run OCR
        self.run_ocr_btn = QPushButton("Run OCR")
        self.layout().addWidget(self.run_ocr_btn)
        self.run_ocr_btn.clicked.connect(self.run_ocr)

        # Vertical spacer to push filters to top
        v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(v_spacer)

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

    @Slot()
    def run_ocr(self):
        """Run the OCR on img"""
        edited_img = self.image_store.edited_img()
        if edited_img is None:
            return

        cv_img = qimage_to_cv(edited_img)
        text = orc_tesseract(cv_img, lang="eng")
        self.text_store.set_text(text)


class EditedImageViewer(QFrame):
    def __init__(self, image_store: ImageStore):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.setStyleSheet("background-color: grey;")
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.image_store = image_store

        # Label for the edited image
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)

        # Store original pixmap for scaling
        self.original_pixmap = None

        # when edited image changes anywhere, show it here as the right panel
        self.image_store.editedImageChanged.connect(self.show_image)

    def show_image(self, qimg: QImage):
        """Set image on the label"""
        if qimg is not None and not qimg.isNull():
            self.original_pixmap = QPixmap.fromImage(qimg)
            self.scale_image()

    def scale_image(self):
        """Scale the pixmap to fit the label while maintaining aspect ratio"""
        if self.original_pixmap is not None and not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Handle widget resize to rescale the image"""
        super().resizeEvent(event)
        self.scale_image()


class RightContainer(QFrame):
    def __init__(self, image_store: ImageStore, text_store: TextStore):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(EditorContainer(image_store, text_store), 1)
        self.layout().addWidget(EditedImageViewer(image_store), 2)
