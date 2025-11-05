from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel

from utils.image_convert import qimage_to_cv, cv_to_qimage
from core import processor


class EditorContainer(QFrame):
    def __init__(self, image_store):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.image_store = image_store
        self.original_cv_img = None  # OpenCV version of original image

        # To grey editor
        self.to_grey_checkbox = QCheckBox("To grey")
        self.layout().addWidget(self.to_grey_checkbox)

        # to binary editor
        to_binary_cont = QFrame()
        to_binary_cont.setLayout(QHBoxLayout())
        self.to_binary_checkbox = QCheckBox("To binary")
        self.layout().addWidget(self.to_binary_checkbox)

        # inverter widget
        self.invert_checkbox = QCheckBox("Invert")
        self.layout().addWidget(self.invert_checkbox)

        # vertical spacer
        v_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(v_spacer)

        # Connect to original image changes to store the base image
        self.image_store.imageChanged.connect(self.on_original_image_changed)

        # forward any change
        self.to_grey_checkbox.toggled.connect(self.on_params_changed)
        self.to_binary_checkbox.toggled.connect(self.on_params_changed)

    def on_original_image_changed(self, qimg: QImage, path: str):
        """Store the original image when it changes"""
        self.original_cv_img = qimage_to_cv(qimg)
        # Reset checkboxes when new image is loaded
        self.to_grey_checkbox.setChecked(False)
        self.to_binary_checkbox.setChecked(False)
        self.invert_checkbox.setChecked(False)
        # Initialize edited image with original
        self.image_store.set_edited_img(qimg)

    def on_params_changed(self):
        """Handle parameter changes and apply processing"""
        if self.original_cv_img is None:
            return
        
        # Start with a copy of the original image
        processed = self.original_cv_img.copy()
        
        # Apply greyscale if checked
        if self.to_grey_checkbox.isChecked():
            processed = processor.to_gray(processed)
            # Convert back to QImage and set to store
            qimg = cv_to_qimage(processed)
            self.image_store.set_edited_img(qimg)
        
        # Apply binarization if checked (works on current processed state)
        if self.to_binary_checkbox.isChecked():
            # Ensure image is grayscale before binarization
            if len(processed.shape) == 3:
                processed = processor.to_gray(processed)
            # Apply binary threshold
            processed = processor.to_binary(processed, threshold=127, max_value=255)
            # Convert back to QImage and set to store
            qimg = cv_to_qimage(processed)
            self.image_store.set_edited_img(qimg)

        # Apply inverter filter
        if self.invert_checkbox.isChecked():
            processed = processor.invert(processed)
            # Convert back to QImage and set to store
            qimg = cv_to_qimage(processed)
            self.image_store.set_edited_img(qimg)
        
        # If no processing is selected, show original
        if not self.to_grey_checkbox.isChecked() and not self.to_binary_checkbox.isChecked():
            qimg = cv_to_qimage(processed)
            self.image_store.set_edited_img(qimg)


class EditedImageViewer(QFrame):
    def __init__(self, image_store):
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


class ImageEditorContainer(QFrame):
    def __init__(self, image_store):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(EditorContainer(image_store), 1)
        self.layout().addWidget(EditedImageViewer(image_store), 2)
