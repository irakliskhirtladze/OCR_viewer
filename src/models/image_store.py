from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage

from dataclasses import dataclass


@dataclass
class ImageItem:
    """Wrapper class to store QImage and other metadata attrs"""
    image: QImage
    path: str
    page: int | None = None
    id: str = ""

    def __post_init__(self):
        """Auto-generate ID from path + page"""
        if not self.id:
            resolved_path = Path(self.path).resolve().as_posix()
            if self.page is not None:
                self.id = f"{resolved_path}#page{self.page}"
            else:
                self.id = resolved_path


class ImageStore(QObject):
    imagesChanged = Signal(dict)
    currentImageChanged = Signal(ImageItem)
    editedImagesChanged = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img_items: dict[str, ImageItem] = {}
        self._current_img_item = ImageItem(QImage(), "")
        self._edited_img_items: dict[str, ImageItem] = {}

    # Dict of original image items where each pair is - id: ImageItem
    def add_img_items(self, img_items: dict[str, ImageItem]):
        self._img_items.update(img_items)
        self.imagesChanged.emit(self._img_items)

    def get_img_items(self) -> dict[str, ImageItem]:
        return self._img_items

    def clear_img_items(self):
        self._img_items.clear()
        self.imagesChanged.emit(self._img_items)

    # single current image needed for preview
    def set_current_img_item(self, img_item: ImageItem):
        self._current_img_item = img_item
        self.currentImageChanged.emit(self._current_img_item)

    def get_current_img_item(self) -> ImageItem:
        return self._current_img_item

    def clear_img_item(self):
        self._current_img_item = ImageItem(QImage(), "")
        self.currentImageChanged.emit(self._current_img_item)

    # dict of edited images using batch editing
    def add_edited_images(self, img_items: dict[str, ImageItem]):
        self._edited_img_items = img_items
        self.editedImagesChanged.emit(self._edited_img_items)

    def get_edited_images(self) -> dict[str, ImageItem]:
        return self._edited_img_items

    def clear_edited_images(self):
        self._edited_img_items.clear()
        self.editedImagesChanged.emit(self._edited_img_items)
