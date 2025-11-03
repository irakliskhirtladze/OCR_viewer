from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy

from utils.utils import open_file_dialog


class ImageViewerWidget(QWidget):
    """Widget to display an image. Supports file dialog and image drop to display; Zoom in and out; Pan; Reset view"""

    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: grey")

        # button and text container
        self.btn_cont = QWidget()
        self.btn_cont.setFixedHeight(50)
        self.btn_cont.setLayout(QHBoxLayout())

        self.choose_img_btn = QPushButton("Choose image")
        self.choose_img_btn.setCursor(Qt.PointingHandCursor)
        self.choose_img_btn.clicked.connect(self.on_choose_image)
        self.btn_cont.layout().addWidget(self.choose_img_btn)

        self.text_label = QLabel("Or drag and drop an image file below")
        self.btn_cont.layout().addWidget(self.text_label)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_cont.layout().addItem(spacer)

        self.layout().addWidget(self.btn_cont)

        # image label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap())
        self.layout().addWidget(self.image_label)

    def on_choose_image(self):
        """Open file dialog to choose an image and display it."""
        file_path = open_file_dialog(
            parent=self,
            caption="Choose Image",
            filter_str="Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path is not None:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(False)  # Keep aspect ratio



