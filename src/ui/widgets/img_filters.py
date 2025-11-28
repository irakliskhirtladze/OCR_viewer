import numpy as np
from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtGui import QImage

from ui.generated.ui_mainwindow import Ui_MainWindow
from ui.models.image_store import ImageStore
from utils.image_convert import qimage_to_cv


class Filters(QObject):
    """Manages the logic of filters"""

    def __init__(self, ui: Ui_MainWindow, image_store: ImageStore):
        super().__init__()
        self.ui = ui
        self.image_store = image_store

        self.ui.grey_chbx.toggled.connect(self.on_grey_chbx_toggled)

    # ===================
    # slots
    # ===================
    @Slot(bool)
    def on_grey_chbx_toggled(self, checked: bool):
        if checked:
            self.apply_filter(self.image_store.get_edited_img())

    # ===================
    # other methods
    # ===================
    def apply_filter(self, qimage: QImage, filter_type: str):
        cv_image = qimage_to_cv(qimage)

