from PySide6.QtCore import Signal, QObject


class TextStore(QObject):
    text_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text = None

    def text(self) -> str | None:
        """returns current text"""
        return self.text

    def set_text(self, text: str) -> None:
        """Sets current text to store instance"""
        self.text = text
        self.text_changed.emit(text)
