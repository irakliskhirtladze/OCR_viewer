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
    editedImageChanged = Signal(ImageItem)
    editedImagesChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img_items: list[ImageItem] = []
        self._keys: set[tuple[str, int | None]] = set()

        self._img_item = ImageItem(QImage(), "")

        self._edited_img_item = ImageItem(QImage(), "")

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

    def get_img_items(self) -> list[ImageItem]:
        return self._img_items

    def clear_img_items(self):
        self._img_items.clear()
        self._keys.clear()
        self.imagesChanged.emit(self._img_items)

    # single original image needed for preview
    def set_img_item(self, img_item: ImageItem):
        self._img_item = img_item
        self.imageChanged.emit(self._img_item)

    def get_img_item(self) -> ImageItem:
        return self._img_item

    def clear_img_item(self):
        self._img_item = ImageItem(QImage(), "")
        self.imageChanged.emit(self._img_item)

    # single edited image for preview
    def set_edited_img_item(self, img_item: ImageItem):
        self._edited_img_item = img_item
        self.editedImageChanged.emit(self._edited_img_item)

    def get_edited_img_item(self) -> ImageItem:
        return self._edited_img_item

    def clear_edited_img_item(self):
        self._edited_img_item = ImageItem(QImage(), "")

    # list of edited images using batch editing
    def add_edited_images(self, img_items: list[ImageItem]):
        self._edited_img_items = img_items
        self.editedImagesChanged.emit(self._edited_img_items)

    def get_edited_images(self) -> list[ImageItem]:
        return self._edited_img_items

    def clear_edited_images(self):
        self._edited_img_items.clear()
        self.editedImagesChanged.emit(self._edited_img_items)
