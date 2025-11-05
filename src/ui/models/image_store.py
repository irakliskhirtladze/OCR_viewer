from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage


class ImageStore(QObject):
    imageChanged = Signal(QImage, str)
    editedImageChanged = Signal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img = QImage()
        self._path = ""
        self._edited_img = QImage()

    # original
    def set_original_img(self, img: QImage, path: str):
        self._img, self._path = img, path
        self.imageChanged.emit(self._img, self._path)

    def original_img(self) -> QImage:
        return self._img

    def path(self) -> str:
        return self._path

    # editor preview
    def set_edited_img(self, img: QImage):
        self._edited_img = img
        self.editedImageChanged.emit(self._edited_img)

    def edited_img(self) -> QImage:
        return self._edited_img
