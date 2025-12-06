from pathlib import Path
import numpy as np
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage
from dataclasses import dataclass

from utils.image_converter import cv_to_qimage


@dataclass
class ImageItem:
    """Wrapper class to store QImage and other metadata attrs"""
    image: np.ndarray
    path: str
    page: int | None = None
    id: str = ""

    def __post_init__(self):
        """Auto-generate ID from path + page"""
        if not self.id and self.path:
            resolved_path = Path(self.path).resolve().as_posix()
            if self.page is not None:
                self.id = f"{resolved_path}#page{self.page}"
            else:
                self.id = resolved_path

    def is_null(self) -> bool:
        """Check if this is an empty/null image item"""
        return not self.path or self.image is None or self.image.size == 0

    def to_qimage(self) -> QImage:
        """Return QImage"""
        return cv_to_qimage(self.image)

    @classmethod
    def empty(cls) -> "ImageItem":
        """Creates an empty/null ImageItem"""
        return cls(image=np.array([]), path="")


@dataclass
class OCRItem:
    """OCR result for a single image"""
    image_id: str
    word_data: list[dict]
    text: str = ""
    engine: str = ""
    languages: tuple[str] = ()


class DataStore(QObject):
    """Central data store for the application"""
    originalImagesChanged = Signal(dict)
    editedImagesChanged = Signal(dict)
    currentImageChanged = Signal(ImageItem)
    ocrResultsChanged = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img_items: dict[str, ImageItem] = {}
        self._current_img_item = ImageItem.empty()
        self._edited_img_items: dict[str, ImageItem] = {}

        self._ocr_items: dict[str, OCRItem] = {}

    # =====================
    # Image methods
    # =====================
    # Dict of original image items where each pair is - id: ImageItem
    def add_img_items(self, img_items: dict[str, ImageItem]):
        self._img_items.update(img_items)
        self.originalImagesChanged.emit(self._img_items)

    def get_img_items(self) -> dict[str, ImageItem]:
        return self._img_items

    def clear_img_items(self):
        self._img_items.clear()
        self.originalImagesChanged.emit(self._img_items)

    # single current image needed for preview
    def set_current_img_item(self, img_item: ImageItem):
        self._current_img_item = img_item
        self.currentImageChanged.emit(self._current_img_item)

    def get_current_img_item(self) -> ImageItem:
        return self._current_img_item

    def clear_current_img_item(self):
        self._current_img_item = ImageItem.empty()
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
        self.originalImagesChanged.emit(self._img_items)

    def clear_all(self):
        self._edited_img_items.clear()
        self._img_items.clear()
        self._current_img_item = ImageItem.empty()
        self._ocr_items.clear()
        self.originalImagesChanged.emit(self._img_items)
        self.currentImageChanged.emit(self._current_img_item)

    # =====================
    # OCR methods
    # =====================
    def set_ocr_items(self, ocr_results: dict[str, OCRItem]):
        """Set OCR word data for a specific edited image"""
        self._ocr_items = ocr_results
        self.ocrResultsChanged.emit(self._ocr_items)

    def get_ocr_items(self) -> dict[str, OCRItem]:
        return self._ocr_items

    def clear_ocr_items(self):
        self._ocr_items.clear()
        self.ocrResultsChanged.emit(self._ocr_items)

