from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage

from dataclasses import dataclass


@dataclass
class ImageItem:
    image: QImage
    path: str
    page: int | None = None


class ImageStore(QObject):
    imagesChanged = Signal(list)
    imageChanged = Signal(ImageItem)
    editedImagesChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img_items: list[ImageItem] = []
        self._keys: set[tuple[str, int | None]] = set()

        self._img_item = ImageItem(QImage(), "")

        self._edited_img_items: list[ImageItem] = []

    # list of loaded images where each item is an instance of ImageItem
    def _key(self, item: ImageItem):
        return Path(item.path).resolve().as_posix(), item.page

    def add_img_items(self, img_items: list[ImageItem]):
        changed = False
        for item in img_items:
            key = self._key(item)
            if key not in self._keys:
                self._keys.add(key)
                self._img_items.append(item)
                changed = True
        if changed:
            self.imagesChanged.emit(self._img_items)

    def get_images(self) -> list[ImageItem]:
        return self._img_items

    def clear_images(self):
        self._img_items.clear()
        self._keys.clear()
        self.imagesChanged.emit(self._img_items)

    # original image. needed to set unprocessed image
    def set_img_item(self, img_item: ImageItem):
        self._img_item = img_item
        self.imageChanged.emit(self._original_img)

    def get_img_item(self) -> ImageItem:
        return self._img_item

    def clear_img_item(self):
        self._original_img = QImage()
        self.originalImageChanged.emit(self._original_img)

    # list of edited images using batch editing
    def set_edited_images(self, img: QImage):
        self._edited_img = img
        self.editedImageChanged.emit(self._edited_img)

    def get_edited_img(self) -> QImage:
        return self._edited_img

    def clear_edited_img(self):
        self._edited_img = QImage()
        self.editedImageChanged.emit(self._edited_img)
