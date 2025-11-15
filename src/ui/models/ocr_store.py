from PySide6.QtCore import Signal, QObject, QRect


class OCRStore(QObject):
    text_changed = Signal(str)
    bounding_boxes_changed = Signal(QRect)
    confidence_scores_changed = Signal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = None
        self._bounding_boxes = None

    def get_text(self) -> str | None:
        """returns current text from store instance"""
        return self._text

    def set_text(self, text: str) -> None:
        """Sets current text to store instance"""
        self._text = text
        self.text_changed.emit(text)

    def get_bounding_boxes(self) -> tuple[int, int, int, int]:
        """returns bounding box of current text"""
        return self._bounding_boxes

    def set_bounding_boxes(self, bounding_boxes: tuple[int, int, int, int]) -> None:
        """sets bounding box of current text"""
        self._bounding_boxes = bounding_boxes


